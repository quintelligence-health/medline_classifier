from eval.eval import MedlineEvaluator
from parsers.mesh_xml import MeshTree
from concurrent.futures import ThreadPoolExecutor

from util.arguments import settings

import os
import requests
import json
import pickle

def evalToDepth((wgt_cutoff, depth)):
    print 'processing <wgt_cutoff, depth>: <' + str(wgt_cutoff) + ', ' + str(depth) + '>'
    score = evaluator.evalToDepth(articles_json, depth, wgt_cutoff)
    return score

if __name__ == '__main__':
    mesh_path = settings['mesh_path']
    classified_path = '/home/midas/data/eval/new-classified-major.json'

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

    score_map = {}
    with ThreadPoolExecutor(max_workers=1) as executor:
        wgt_depth_tuples = []
        for iterN in range(15, 51):
            wgt_cutoff = 0.01*float(iterN)
            for depth in range(1, 10):
                wgt_depth_tuples.append((wgt_cutoff, depth))

        print 'computing'
        scores = executor.map(evalToDepth, wgt_depth_tuples)
        scores = [score for score in scores]

        print 'results computed, organizing'
        for resultN in range(len(wgt_depth_tuples)):
            score = scores[resultN]
            wgt_depth_tup = wgt_depth_tuples[resultN]
            score_map[str(wgt_depth_tup[0]) + '-' + str(wgt_depth_tup[1])] = score

    print 'score: ' + str(score_map)

    with open('eval2-major.json', 'w') as f:
        json.dump(score_map, f, indent=4)

    print 'done'
