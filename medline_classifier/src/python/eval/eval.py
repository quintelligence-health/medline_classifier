import os
import json

from sets import Set

import time

from concurrent.futures import ThreadPoolExecutor

from parsers.medline_xml import MedlineFileParser

def calcPrecision(tp, fp, fn):
    al = float(tp + fp)
    return float(tp) / al if al != 0.0 else 1

def calcRecall(tp, fp, fn):
    al = float(tp + fn)
    return float(tp) / al if al != 0.0 else 1

def calcF1(tp, fp, fn):
    bottom = float(2*tp + fp + fn)
    return 2.0*tp / bottom if bottom != 0.0 else 1

class MedlineEvaluator:

    def __init__(self, medline_dir_old, medline_dir_new, old_unannotated_fname, eval_articles_fname):
        self._medline_dir_old = medline_dir_old
        self._medline_dir_new = medline_dir_new
        self._old_unannotated_fname = old_unannotated_fname
        self._eval_articles_fname = eval_articles_fname
        self._max_workers = 12

    def extractCandidates(self):
        # first find the articles that are not annotated in the old dataset
        articles_old = self._readMedline(self._medline_dir_old)

        unannotated_json = []
        old_article_map = {}

        for articleN, article in enumerate(articles_old):
            if articleN % 10000 == 0:
                print 'processing article ' + str(articleN+1)

            if not article.hasMeshHeadings():
                article_id = article.pmid
                old_article_map[article_id] = article
                unannotated_json.append(article.asDict())
                if len(old_article_map) % 10000 == 1:
                    print 'found ' + str(len(old_article_map)) + ' unannotated articles'

        print 'found ' + str(len(old_article_map)) + ' unannotated articles'

        # dump the articles that are not annotated to a file
        print 'dumping unannotated articles'
        with open(self._old_unannotated_fname, 'w') as f:
            json.dump(unannotated_json, f, indent=4, sort_keys=True)

        # release memory
        del unannotated_json
        del articles_old

        eval_candidates = []

        # read the new articles
        articles_new = self._readMedline(self._medline_dir_new)
        for articleN, article in enumerate(articles_new):
            if articleN % 10000 == 0:
                print 'processing article ' + str(articleN+1)

            article_id = article.pmid
            if article_id in old_article_map and article.hasMeshHeadings():
                eval_candidates.append(article.asDict())
                if len(eval_candidates) % 10000 == 1:
                    print 'found ' + str(len(eval_candidates)) + ' candidates for evaluation'

        # dump the evaluation candidates to a file
        print 'dumping evaluation candidates'
        with open(self._eval_articles_fname, 'w') as f:
            json.dump(eval_candidates, f, indent=4, sort_keys=True)

    def classify(self, classifier, classified_path):
        '''
        Classifying the articles
        '''
        annotated_path = self._eval_articles_fname
        articles_json = None

        print 'reading articles'
        with open(annotated_path, 'r') as f:
            articles_json = json.load(f)

        start_secs = time.time()

        failed_count = 0
        for articleN, article_json in enumerate(articles_json):
            if articleN % 1000 == 0:
                print 'processing article ' + str(articleN+1)
            abstract = article_json['abstract']
            classified_headings = classifier.classify(abstract)

            if classified_headings is not None:
                article_json['classifiedMeshHeadings'] = classified_headings
            else:
                failed_count += 1
                print 'failed classifications: ' + str(failed_count)

        end_secs = time.time()
        dur_secs = end_secs - start_secs

        print 'writing json'
        with open(classified_path, 'w') as f:
            json.dump(articles_json, f, indent=4, sort_keys=True)

        print 'classified ' + str(len(articles_json)) + ' articles in ' + str(dur_secs) + ' seconds'
        print 'total failed classifications: ' + str(failed_count)

    def appendMeshHeadings(self, articles, mesh):
        descriptor_set = Set()

        missing_descriptors = 0
        total_descriptors = 0

        for articleN, article in enumerate(articles):
            if articleN % 10000 == 1:
                print 'processing article ' + str(articleN)

            descriptor_set.clear()
            classified_descriptors = []
            annotated_headings = []

            categories = article['classifiedMeshHeadings']
            meshHeadings = article['meshHeadings']

            total_descriptors += len(categories)

            for category in categories:
                descriptor_ui = None
                category_wgt = category['weight']

                if 'descriptorUi' in category:
                    descriptor_ui = category['descriptorUi']
                else:
                    category_name = category['category']


                    descriptor_ui = mesh.getCategoryDescriptor(category_name)
                    if descriptor_ui is None:
                        missing_descriptors += 1
                        continue

                    if articleN % 10000 == 1:
                        print 'category `' + str(category_name) + '` translated to `' + str(descriptor_ui) + '`'

                tree_numbers = mesh.getTreeNumbers(descriptor_ui)

                if not descriptor_ui in descriptor_set:
                    descriptor_set.add(descriptor_ui)
                    classified_descriptors.append({
                        'descriptorUi': descriptor_ui,
                        'treeNumbers': tree_numbers,
                        'weight': category_wgt
                    })

            for headingN in xrange(len(meshHeadings)):
                descriptor_ui = meshHeadings[headingN]
                tree_numbers = mesh.getTreeNumbers(descriptor_ui)
                annotated_headings.append({
                    'descriptorUi': descriptor_ui,
                    'treeNumbers': tree_numbers
                })

            article['classifiedMeshHeadings'] = classified_descriptors
            article['annotatedMeshHeadings'] = annotated_headings

        print 'missing descriptors ' + str(missing_descriptors) + ' of ' + str(total_descriptors)
        print 'done!'

    def evalExactMatches(self, articles):
        print 'evaluating exact matches'
        total_tp = 0
        total_fp = 0
        total_fn = 0

        f1_dataset = 0

        classified_uis_mean = 0
        real_uis_mean = 0

        for article in articles:
            classified_uis = Set([heading['descriptorUi'] for heading in article['classifiedMeshHeadings']])
            real_uis = Set(article['meshHeadings'])

            tp = len(classified_uis.intersection(real_uis))
            fp = len(classified_uis.difference(real_uis))
            fn = len(real_uis.difference(classified_uis))

            f1_article = 2.0*float(tp) / float(2*tp + fn + fp)

            classified_uis_mean += len(classified_uis)
            real_uis_mean += len(real_uis)

            total_tp += tp
            total_fp += fp
            total_fn += fn

            f1_dataset += f1_article

        classified_uis_mean /= float(len(articles))
        real_uis_mean /= float(len(articles))

        precision = float(total_tp) / float(total_tp + total_fp)
        recall = float(total_tp) / float(total_tp + total_fn)

        f1_global = 2*precision*recall / (precision + recall)
        f1_dataset /= len(articles)

        return {
            'tp': total_tp,
            'fp': total_fp,
            'fn': total_fn,
            'avgHeadings': real_uis_mean,
            'avgClassifiedHeadings': classified_uis_mean,
            'precision': precision,
            'recall': recall,
            'f1_global': f1_global,
            'f1_dataset': f1_dataset
        }

    def evalToDepth(self, articles, depth, wgt_cutoff=0.0):
        total_tp = 0
        total_fp = 0
        total_fn = 0

        f1_dataset = 0

        classified_uis_mean = 0
        real_uis_mean = 0

        for articleN, article in enumerate(articles):
            if articleN % 10000 == 1:
                precision = calcPrecision(total_tp, total_fp, total_fn)
                recall = calcRecall(total_tp, total_fp, total_fn)
                # print '==========================='
                print 'processing article ' + str(articleN) + ', depth ' + str(depth) + ', wgt cutoff ' + str(wgt_cutoff) + ', precision: ' + str(precision) + ', recall: ' + str(recall)
                # print 'tp: ' + str(total_tp)
                # print 'fp: ' + str(total_fp)
                # print 'fn: ' + str(total_fn)
                # print 'precision: ' + str(precision)
                # print 'recall: ' + str(recall)
                # print '==========================='

            classified_headings = article['classifiedMeshHeadings']
            real_headings = article['annotatedMeshHeadings']

            classified_headings = [heading for heading in classified_headings if heading['weight'] >= wgt_cutoff]

            # print 'comparing classified: ' + str(classified_headings) + ' to ' + str(real_headings)

            tp = 0
            fp = 0
            fn = 0

            # true positives and false positives
            for classified_heading in classified_headings:
                classified_tree_numbers = classified_heading['treeNumbers']

                # print 'classified DescriptorUI: ' + classified_heading['descriptorUi']
                # check if the heading appears in the real headings
                is_tp = False
                for real_heading in real_headings:
                    real_tree_numbers = real_heading['treeNumbers']
                    # print 'real DescriptorUI: ' + real_heading['descriptorUi']
                    match = TreeNumberHelper.anyMatchesToDepth(
                        classified_tree_numbers,
                        real_tree_numbers,
                        depth
                    )
                    if match:
                        is_tp = True
                        break

                # print 'is TP: ' + str(is_tp)

                tp += 1 if is_tp else 0
                fp += 1 if not is_tp else 0

            # false negatives
            for real_heading in real_headings:
                real_tree_numbers = real_heading['treeNumbers']

                if len(real_tree_numbers) == 0:
                    continue

                # check that the heading does not appear in the classified headings
                is_fn = True
                for classified_heading in classified_headings:
                    classified_tree_numbers = classified_heading['treeNumbers']
                    match = TreeNumberHelper.anyMatchesToDepth(
                        classified_tree_numbers,
                        real_tree_numbers,
                        depth
                    )
                    if match:
                        is_fn = False
                        break

                # print 'is FN: ' + str(is_fn)

                fn += 1 if is_fn else 0

            total_tp += tp
            total_fp += fp
            total_fn += fn

            f1_article = calcF1(tp, fp, fn)

            classified_uis_mean += len(classified_headings)
            real_uis_mean += len(real_headings)

            f1_dataset += f1_article

        classified_uis_mean /= float(len(articles))
        real_uis_mean /= float(len(articles))

        precision = calcPrecision(total_tp, total_fp, total_fn)
        recall = calcRecall(total_tp, total_fp, total_fn)
        # precision = float(total_tp) / float(total_tp + total_fp)
        # recall = float(total_tp) / float(total_tp + total_fn)

        f1_global = calcF1(total_tp, total_fp, total_fn)
        f1_dataset /= len(articles)

        return {
            'tp': total_tp,
            'fp': total_fp,
            'fn': total_fn,
            'avgHeadings': real_uis_mean,
            'avgClassifiedHeadings': classified_uis_mean,
            'precision': precision,
            'recall': recall,
            'f1_global': f1_global,
            'f1_dataset': f1_dataset
        }



    def evalPartialMatches(self, articles):
        print 'evaluating partial matches'

        for article in articles:
            classified_headings = article['classifiedMeshHeadings']
            real_headings = article['annotatedMeshHeadings']

    def _readMedline(self, medline_dir):
        medline_articles = []

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            # read the directory structure
            dirs = os.listdir(medline_dir)
            for dirN, dirname in enumerate(dirs):
                print 'processing directory ' + dirname + ' [' + str(dirN + 1) + ' of ' + str(len(dirs)) + ']'
                # go through all the files in the directory
                medline_files = os.listdir(os.path.join(medline_dir, dirname))
                file_names = [os.path.join(medline_dir, dirname, medline_fname) for medline_fname in medline_files]

                start_msecs = time.time()*1000.0

                article_batches = executor.map(self._readMedlineFiles, file_names)

                for batch in article_batches:
                    medline_articles += batch

                dur_msecs = time.time()*1000.0 - start_msecs
                print 'processed folder ' + dirname + ' in ' + str(dur_msecs*0.001) + ' seconds'

        return medline_articles

    def _readMedlineFiles(self, file_name):
        parser = MedlineFileParser(False, True)
        parser.parse(file_name)
        articles = parser.getArticles()
        return articles


class TreeNumberHelper:

    @staticmethod
    def anyMatchesToDepth(tree_numbers1, tree_numbers2, depth):
        for tree_number1 in tree_numbers1:
            spl1 = tree_number1.split('.')[0:depth-1]
            for tree_number2 in tree_numbers2:
                if depth == 1:
                    if tree_number1[0] == tree_number1[0]:
                        return True
                else:
                    spl2 = tree_number2.split('.')[0:depth-1]
                    if spl1 == spl2:
                        return True
        return False
