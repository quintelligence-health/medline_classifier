from eval.eval import MedlineEvaluator

from util.arguments import settings

import requests
import json

class MeshClassifier:

    def __init__(self, endpoint_url, n_categories):
        self._endpoint_url = endpoint_url
        self._n_categories = n_categories

    def classify(self, text):
        body_json = {
            'text': text,
            'maxCategories': self._n_categories
        }

        res_text = None

        try:
            headers = {'Content-Type': 'application/json'}

            res = requests.post(url=self._endpoint_url, data=json.dumps(body_json), headers=headers)

            status = res.status_code
            if 200 <= status and status < 300:
                res_text = res.text
                categories_json = json.loads(res_text)
                return categories_json
            else:
                print 'invalid status code: ' + str(status)
                return None
        except:
            print 'failed to parse text with options:\n' + str(body_json)
            return None

if __name__ == '__main__':
    medline_path_new = settings['medline_path']
    medline_path_old = settings['medline_path_old']
    unannotated_path = '/home/midas/data/eval/old-unannotated.json'
    eval_candidate_path = '/home/midas/data/eval/new-annotated-major.json'
    classified_path = '/home/midas/data/eval/new-classified-major.json'

    endpoint_url = 'http://qmidas.quintelligence.com/classify-mesh-major/api/classify'
    n_categories = 250

    print 'articles path: ' + medline_path_new
    print 'classified path: ' + medline_path_new

    classifier = MeshClassifier(endpoint_url, n_categories)

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    evaluator.classify(classifier, classified_path)
