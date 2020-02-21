from eval.eval import MedlineEvaluator
from parsers.mesh_xml import MeshTree

from util.arguments import settings

import os
import requests
import json
import pickle

if __name__ == '__main__':
    dataset = 'all'

    mesh_path = settings['mesh_path']
    classified_path = '../../data/classified.json'

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

    print 'n_articles: ' + str(len(articles_json))

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)

    scores = []
    for iterN in range(15, 51):
        wgt_cutoff = 0.01*float(iterN)

        print 'evaluating for cutoff: ' + str(wgt_cutoff)
        score = evaluator.evalExactMatches(articles_json, wgt_cutoff=wgt_cutoff)
        scores.append((wgt_cutoff, score))

    print 'score: ' + str(scores)

    with open('../../data/results-eval1.json', 'w') as f:
        json.dump(scores, f, indent=4)

    print 'done'
