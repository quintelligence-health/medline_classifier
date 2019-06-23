from eval.eval import MedlineEvaluator
from parsers.mesh_xml import MeshTree

from util.arguments import settings

import os
import requests
import json
import pickle

def serialize(object, fname):
    with open(fname, 'w') as f:
        pickle.dump(object, f)

def deserialize(fname):
    with open(fname, 'r') as f:
        return pickle.load(f)

if __name__ == '__main__':
    mesh_path = settings['mesh_path']

    classified_path = '/home/midas/data/eval/new-classified-major.json'
    is_only_major = True

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

    mesh = None
    if not os.path.isfile(mesh_serialize_path):
        print 'parsing the MeSH structure'
        mesh = MeshTree()
        mesh.parse(mesh_path)
        print 'serializing mesh'
        serialize(mesh, mesh_serialize_path)
    else:
        mesh = deserialize(mesh_serialize_path)

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    evaluator.appendMeshHeadings(articles_json, mesh, only_major=is_only_major)

    print 'writing articles'
    with open(classified_path, 'w') as f:
        json.dump(articles_json, f, indent=4, sort_keys=True)

    print 'done'
