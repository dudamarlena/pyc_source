# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_rating_based_algorithm.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 1328 bytes
__doc__ = '\n    Running Precision and Recall metrics on rating-based algorithms\n\n'
from caserec.recommenders.rating_prediction.matrixfactorization import MatrixFactorization
from caserec.recommenders.rating_prediction.nnmf import NNMF
from caserec.utils.process_data import ReadFile
from caserec.evaluation.rating_prediction import RatingPredictionEvaluation
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
predictions_output_filepath = './predictions_output.dat'
model = NNMF(tr, te, output_file=predictions_output_filepath)
model.compute(verbose=False)
reader = ReadFile(input_file=predictions_output_filepath)
predictions = reader.read()
evaluator = RatingPredictionEvaluation(sep='\t', n_rank=[10], as_rank=True, metrics=['PREC'])
item_rec_metrics = evaluator.evaluate(predictions['feedback'], model.test_set)
print('\nItem Recommendation Metrics:\n', item_rec_metrics)
model.predict()
print('\nOriginal Rating Prediction Metrics:\n', model.evaluation_results)