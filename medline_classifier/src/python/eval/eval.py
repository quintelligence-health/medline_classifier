import os
import json

import time

from concurrent.futures import ThreadPoolExecutor

from parsers.medline_xml import MedlineFileParser

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

        for articleN, article_json in enumerate(articles_json):
            if articleN % 1000 == 0:
                print 'processing article ' + str(articleN+1)
            abstract = article_json['abstract']
            classified_headings = classifier.classify(abstract)
            article_json['classifiedMeshHeadings'] = classified_headings

        print 'writing json'
        with open(classified_path) as f:
            json.dump(articles_json, f, indent=4, sort_keys=True)

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
