from eval.eval import MedlineEvaluator

from util.arguments import settings

if __name__ == '__main__':
    medline_path_new = settings['medline_path']
    medline_path_old = settings['medline_path_old']
    unannotated_path = '/home/midas/data/eval/old-unannotated.json'
    eval_candidate_path = '/home/midas/data/eval/new-annotated.json'

    print 'old: ' + medline_path_old
    print 'new: ' + medline_path_new

    evaluator = MedlineEvaluator(medline_path_old, medline_path_new, unannotated_path, eval_candidate_path)
    evaluator.extractCandidates()

    print 'done!'
