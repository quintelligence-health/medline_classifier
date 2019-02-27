from eval.eval import MedlineEvaluator

from util.arguments import settings

import requests
import json

class MeshClassifier:

    def __init__(self, endpoint_url):
        self._endpoint_url = endpoint_url

    def classify(self, text):
        body_json = {
            'text': text,
            'maxCategories': 50
        }
        headers = {'Content-Type': 'application/json'}

        res = requests.post(url=self._endpoint_url, data=json.dumps(body_json), headers=headers)
        categories_json = res.json()

        return categories_json

if __name__ == '__main__':
    medline_path_new = settings['medline_path']
    medline_path_old = settings['medline_path_old']
    unannotated_path = '/home/midas/data/eval/old-unannotated.json'
    eval_candidate_path = '/home/midas/data/eval/new-annotated.json'
    classified_path = '/home/midas/data/eval/new-classified.json'

    endpoint_url = 'http://qmidas.quintelligence.com/classify-mesh/api/classify'

    print 'articles path: ' + medline_path_new
    print 'classified path: ' + medline_path_new

    classifier = MeshClassifier(endpoint_url)

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    evaluator.classify(classifier, classified_path)
