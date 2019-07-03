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

def calcFBeta(tp, fp, fn, beta):
    beta2 = float(beta)**2
    bottom = float((1 + beta2)*tp + beta2*fn + fp)
    return (1 + beta2) * tp / bottom if bottom != 0.0 else 1

def calcF1(tp, fp, fn):
    bottom = float(2*tp + fp + fn)
    return 2.0*tp / bottom if bottom != 0.0 else 1

def calcF05(tp, fp, fn):
    return calcFBeta(tp, fp, fn, 0.5)


class MedlineEvaluator:

    def __init__(self, medline_dir_old, medline_dir_new, old_unannotated_fname, eval_articles_fname):
        self._medline_dir_old = medline_dir_old
        self._medline_dir_new = medline_dir_new
        self._old_unannotated_fname = old_unannotated_fname
        self._eval_articles_fname = eval_articles_fname
        self._max_workers = 12

    def extractCandidates(self, only_major):
        # first find the articles that are not annotated in the old dataset
        articles_old = self._readMedline(self._medline_dir_old, only_major)

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
        articles_new = self._readMedline(self._medline_dir_new, only_major)
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

    def appendMeshHeadings(self, articles, mesh, only_major=False):
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

    def evalExactMatches(self, articles, wgt_cutoff=0.0):
        print 'evaluating exact matches'

        n_articles = len(articles)

        f1_dataset = 0
        f05_dataset = 0

        classified_uis_mean = 0
        real_uis_mean = 0

        f1_mean = 0
        f05_mean = 0
        precision_mean = 0
        recall_mean = 0

        n_bins = 101
        f1_dist = [0 for _ in range(n_bins)]
        f05_dist = [0 for _ in range(n_bins)]
        precision_dist = [0 for _ in range(n_bins)]
        recall_dist = [0 for _ in range(n_bins)]

        for articleN, article in enumerate(articles):
            if articleN % 10000 == 0:
                print 'processing article ' + str(articleN+1)
            classified_uis = Set([heading['descriptorUi'] for heading in article['classifiedMeshHeadings'] if heading['weight'] >= wgt_cutoff])
            real_uis = Set(article['meshHeadings'])

            tp = len(classified_uis.intersection(real_uis))
            fp = len(classified_uis.difference(real_uis))
            fn = len(real_uis.difference(classified_uis))

            f1_article = calcF1(tp, fp, fn)
            f05_article = calcF05(tp, fp, fn)
            precision = calcPrecision(tp, fp, fn)
            recall = calcRecall(tp, fp, fn)

            f1_mean += f1_article
            f05_mean += f05_article
            precision_mean += precision
            recall_mean += recall

            f1_binN = int(100*f1_article)
            f1_dist[f1_binN] += 1

            f05_binN = int(100*f05_article)
            f05_dist[f05_binN] += 1

            precision_binN = int(100*precision)
            precision_dist[precision_binN] += 1

            recall_binN = int(100*recall)
            recall_dist[recall_binN] += 1

            f1_dataset += f1_article
            f05_dataset += f05_article

            classified_uis_mean += len(classified_uis)
            real_uis_mean += len(real_uis)

            f1_dataset += f1_article

        classified_uis_mean /= float(len(articles))
        real_uis_mean /= float(len(articles))

        f1_dataset /= len(articles)
        f05_dataset /= len(articles)

        f1_mean /= float(n_articles)
        f05_mean /= float(n_articles)
        precision_mean /= float(n_articles)
        recall_mean /= float(n_articles)

        def median(dist):
            prob_sum = 0
            for valN, val in enumerate(dist):
                prob_sum += val
                if prob_sum >= 0.5:
                    return 0.005*(valN + valN+1)
            return 1


        f1_dist = [float(val) / n_articles for val in f1_dist]
        f05_dist = [float(val) / n_articles for val in f05_dist]
        precision_dist = [float(val) / n_articles for val in precision_dist]
        recall_dist = [float(val) / n_articles for val in recall_dist]

        f1_median = median(f1_dist)
        f05_median = median(f05_dist)
        precision_median = median(precision_dist)
        recall_median = median(recall_dist)

        return {
            'avgHeadings': real_uis_mean,
            'avgClassifiedHeadings': classified_uis_mean,
            # 'precision': precision,
            # 'recall': recall,
            'f1_dataset': f1_dataset,
            'f05_dataset': f05_dataset,
            'f1_mean': f1_mean,
            'f05_mean': f05_mean,
            'precision_mean': precision_mean,
            'recall_mean': recall_mean,
            'f1_median': f1_median,
            'f05_median': f05_median,
            'precision_median': precision_median,
            'recall_median': recall_median,
            'f1_dist': f1_dist,
            'f05_dist': f05_dist,
            'precision_dist': precision_dist,
            'recall_dist': recall_dist
        }

    def evalToDepth(self, articles, depth, wgt_cutoff=0.0):
        f1_dataset = 0
        f05_dataset = 0

        classified_uis_mean = 0
        real_uis_mean = 0

        f1_mean = 0
        f05_mean = 0
        precision_mean = 0
        recall_mean = 0

        n_bins = 101
        f1_dist = [0 for _ in range(n_bins)]
        f05_dist = [0 for _ in range(n_bins)]
        precision_dist = [0 for _ in range(n_bins)]
        recall_dist = [0 for _ in range(n_bins)]

        n_articles = 0
        for articleN, article in enumerate(articles):
            if articleN % 10000 == 1:
                print 'processing article ' + str(articleN) + ', depth ' + str(depth) + ', wgt cutoff ' + str(wgt_cutoff)

            classified_headings = article['classifiedMeshHeadings']
            real_headings = article['annotatedMeshHeadings']

            classified_headings = [heading for heading in classified_headings if heading['weight'] >= wgt_cutoff]

            tp = 0
            fp = 0
            fn = 0

            classified_undupl = TreeNumberHelper.removeDuplicates(classified_headings, depth)
            real_undupl = TreeNumberHelper.removeDuplicates(real_headings, depth)

            if len(real_undupl) == 0:
                continue

            # print '\n\n\n\nclassified: ' + str(classified_headings) + '\nundupl: ' + str(classified_undupl)
            # print '\n\n\n\nreal: ' + str(real_headings) + '\nundupl: ' + str(real_undupl)

            # true positives and false positives
            for classified_tree_numbers in classified_undupl:
                # classified_tree_numbers = classified_heading['treeNumbers']

                # check if the heading appears in the real headings
                is_tp = False
                for real_tree_numbers in real_undupl:
                    # real_tree_numbers = real_heading['treeNumbers']

                    match = TreeNumberHelper.anyMatchesToDepth(
                        classified_tree_numbers,
                        real_tree_numbers,
                        depth
                    )

                    # print 'matches: ' + str(match) + '\nclassified: ' + str(classified_tree_numbers) + '\nreal: ' + str(real_tree_numbers)
                    if match:
                        is_tp = True
                        break

                tp += 1 if is_tp else 0
                fp += 1 if not is_tp else 0

            # false negatives
            for real_tree_numbers in real_undupl:
                # real_tree_numbers = real_heading['treeNumbers']

                if len(real_tree_numbers) == 0:
                    continue

                # check that the heading does not appear in the classified headings
                is_fn = True
                for classified_tree_numbers in classified_undupl:
                    # classified_tree_numbers = classified_heading['treeNumbers']
                    match = TreeNumberHelper.anyMatchesToDepth(
                        classified_tree_numbers,
                        real_tree_numbers,
                        depth
                    )
                    if match:
                        is_fn = False
                        break

                fn += 1 if is_fn else 0

            # if articleN >= 10:
            #     print 'exiting'
            #     exit(0)

            f1_article = calcF1(tp, fp, fn)
            f05_article = calcF05(tp, fp, fn)
            precision = calcPrecision(tp, fp, fn)
            recall = calcRecall(tp, fp, fn)

            f1_mean += f1_article
            f05_mean += f05_article
            precision_mean += precision
            recall_mean += recall

            f1_binN = int(100*f1_article)
            f1_dist[f1_binN] += 1

            f05_binN = int(100*f05_article)
            f05_dist[f05_binN] += 1

            precision_binN = int(100*precision)
            precision_dist[precision_binN] += 1

            recall_binN = int(100*recall)
            recall_dist[recall_binN] += 1

            f1_dataset += f1_article
            f05_dataset += f05_article

            classified_uis_mean += len(classified_undupl)
            real_uis_mean += len(real_undupl)

            n_articles += 1

        classified_uis_mean /= float(len(articles))
        real_uis_mean /= float(len(articles))

        f1_dataset /= len(articles)
        f05_dataset /= len(articles)

        f1_mean /= float(n_articles)
        f05_mean /= float(n_articles)
        precision_mean /= float(n_articles)
        recall_mean /= float(n_articles)

        def median(dist):
            prob_sum = 0
            for valN, val in enumerate(dist):
                prob_sum += val
                if prob_sum >= 0.5:
                    return 0.005*(valN + valN+1)
            return 1


        f1_dist = [float(val) / n_articles for val in f1_dist]
        f05_dist = [float(val) / n_articles for val in f05_dist]
        precision_dist = [float(val) / n_articles for val in precision_dist]
        recall_dist = [float(val) / n_articles for val in recall_dist]

        f1_median = median(f1_dist)
        f05_median = median(f05_dist)
        precision_median = median(precision_dist)
        recall_median = median(recall_dist)

        return {
            'avgHeadings': real_uis_mean,
            'avgClassifiedHeadings': classified_uis_mean,
            'f1_dataset': f1_dataset,
            'f05_dataset': f05_dataset,
            'f1_mean': f1_mean,
            'f05_mean': f05_mean,
            'precision_mean': precision_mean,
            'recall_mean': recall_mean,
            'f1_median': f1_median,
            'f05_median': f05_median,
            'precision_median': precision_median,
            'recall_median': recall_median,
            'f1_dist': f1_dist,
            'f05_dist': f05_dist,
            'precision_dist': precision_dist,
            'recall_dist': recall_dist
        }



    def evalPartialMatches(self, articles):
        print 'evaluating partial matches'

        for article in articles:
            classified_headings = article['classifiedMeshHeadings']
            real_headings = article['annotatedMeshHeadings']

    def _readMedline(self, medline_dir, only_major):
        medline_articles = []

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            # read the directory structure
            dirs = os.listdir(medline_dir)
            for dirN, dirname in enumerate(dirs):
                print 'processing directory ' + dirname + ' [' + str(dirN + 1) + ' of ' + str(len(dirs)) + ']'
                # go through all the files in the directory
                medline_files = os.listdir(os.path.join(medline_dir, dirname))
                all_args = [
                   (os.path.join(medline_dir, dirname, medline_fname), only_major)
                    for medline_fname in medline_files
                ]

                start_msecs = time.time()*1000.0

                article_batches = executor.map(self._readMedlineFiles, all_args)

                for batch in article_batches:
                    medline_articles += batch

                dur_msecs = time.time()*1000.0 - start_msecs
                print 'processed folder ' + dirname + ' in ' + str(dur_msecs*0.001) + ' seconds'

        return medline_articles

    def _readMedlineFiles(self, args):
        file_name = args[0]
        only_major = args[1]
        parser = MedlineFileParser(only_major, True)
        parser.parse(file_name)
        articles = parser.getArticles()
        return articles


class TreeNumberHelper:

    @staticmethod
    def removeDuplicates(headings, depth):
        # filter the classified tree numbers
        headings_undupl = []
        for heading in headings:
            heading_tree_numbers = heading['treeNumbers']

            # filter the tree numbers
            filtered_tree_numbers = []
            taken_numbers = Set()
            for tree_number in heading_tree_numbers:
                tn_cut = TreeNumberHelper.cutTreeNumber(tree_number, depth)
                if tn_cut not in taken_numbers:
                    taken_numbers.add(tn_cut)
                    filtered_tree_numbers.append(tn_cut)

            # check if the filtered tree numbers are already in the headings
            filtered_tree_numbers.sort()

            one_tn_matches = False
            for present_numbers in headings_undupl:
                # we have a match if all the tree numbers are the same
                if len(present_numbers) != len(filtered_tree_numbers):
                    continue
                all_match = True
                for tnN, tn in enumerate(present_numbers):
                    if tn != filtered_tree_numbers[tnN]:
                        all_match = False
                        break

                if all_match:
                    one_tn_matches = True
                    break

            if not one_tn_matches:
                headings_undupl.append(filtered_tree_numbers)

        return headings_undupl

    @staticmethod
    def cutTreeNumber(tree_number, depth):
        if depth == 1:
            return tree_number[0]
        else:
            return '.'.join(tree_number.split('.')[0:depth-1])

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
