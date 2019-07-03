from eval.eval import MedlineEvaluator
from parsers.mesh_xml import MeshTree

from concurrent.futures import ThreadPoolExecutor

from util.arguments import settings

import os
import requests
import json
import pickle
import random

def evalToDepth((wgt_cutoff, depth)):
    print 'processing <wgt_cutoff, depth>: <' + str(wgt_cutoff) + ', ' + str(depth) + '>'
    score = evaluator.evalToDepth(articles_json, depth, wgt_cutoff)
    return score

if __name__ == '__main__':
    dataset = settings['dataset']#'250'
    sample_size = int(settings['sample']) if 'sample' in settings is not None and int(settings['sample']) > 0 else None

    if dataset == '':
        print 'please specify parameter `dataset` (either `major` or `250`)'
        exit(1)

    print 'using dataset: ' + dataset

    if sample_size is not None:
        print 'evaluating on a sample of size: ' + str(sample_size)

    mesh_path = settings['mesh_path']
    classified_path = '/home/midas/data/eval/new-classified-' + dataset + '.json'

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
        if sample_size is not None:
            articles_json = random.sample(articles_json, sample_size)

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)

    score_map = {}
    with ThreadPoolExecutor(max_workers=1) as executor:
        wgt_depth_tuples = []
        for iterN in range(15, 51):
            wgt_cutoff = 0.01*float(iterN)
            for depth in range(1, 10):
            # for depth in range(5, 10):
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

    fname_out = 'eval2-' + dataset + ('-' + str(sample_size) if sample_size is not None else '') + '.json'
    with open('../../../scripts/data/' + fname_out, 'w') as f:
        json.dump(score_map, f, indent=4)

    print 'done'
