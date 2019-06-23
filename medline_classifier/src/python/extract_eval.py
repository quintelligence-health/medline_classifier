from eval.eval import MedlineEvaluator

from util.arguments import settings

if __name__ == '__main__':
    medline_path_new = settings['medline_path']
    medline_path_old = settings['medline_path_old']
    unannotated_path = '/home/midas/data/eval/old-unannotated-major.json'
    eval_candidate_path = '/home/midas/data/eval/new-annotated-major.json'
    only_major = True

    print 'old: ' + medline_path_old
    print 'new: ' + medline_path_new

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    evaluator.extractCandidates(only_major)

    print 'done!'
