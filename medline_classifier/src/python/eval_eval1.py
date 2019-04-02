from eval.eval import MedlineEvaluator
from parsers.mesh_xml import MeshTree

from util.arguments import settings

import os
import requests
import json
import pickle

if __name__ == '__main__':
    mesh_path = settings['mesh_path']
    classified_path = '/home/midas/data/eval/new-classified.json'

    mesh_serialize_path = '/home/midas/storage/data/eval/temp/mesh.pkl'

    # required for MedlineEvaluator
    medline_path_new = settings['medline_path']
    medline_path_old = settings['medline_path_old']
    unannotated_path = '/home/midas/data/eval/old-unannotated.json'
    eval_candidate_path = '/home/midas/data/eval/new-annotated.json'

    articles_json = None

    print 'reading articles'
    with open(classified_path, 'r') as f:
        articles_json = json.load(f)

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    scores = evaluator.evalExactMatches(articles_json)

    print 'score: ' + str(scores)
    print 'done'
