# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caserec/evaluation/rating_prediction.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 5017 bytes
__doc__ = '"\n    This class is responsible for evaluate rating prediction algorithms.\n\n    This file contains rating prediction evaluation metrics:\n        - Mean Absolute Error - MAE\n        - Root Mean Squared Error - RMSE\n\n    Types of evaluation:\n        - Simple: Evaluation with traditional strategy\n        - All-but-one Protocol: Considers only one pair (u, i) from the test set to evaluate the predictions\n\n'
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np, random
from caserec.evaluation.item_recommendation import ItemRecommendationEvaluation
from caserec.evaluation.base_evaluation import BaseEvaluation
__author__ = 'Arthur Fortes <fortes.arthur@gmail.com>'

class RatingPredictionEvaluation(BaseEvaluation):

    def __init__(self, sep='\t', metrics=list(['MAE', 'RMSE']), all_but_one_eval=False, verbose=True, as_table=False, table_sep='\t', as_rank=False, n_rank=(5, 10)):
        """
        Class to evaluate predictions in a rating prediction scenario

        :param sep: Delimiter for input files
        :type sep: str, default '       '

        :param metrics: List of evaluation metrics
        :type metrics: list, default ('MAE', 'RMSE')

        :param all_but_one_eval: If True, considers only one pair (u, i) from the test set to evaluate the ranking
        :type all_but_one_eval: bool, default False

        :param verbose: Print the evaluation results
        :type verbose: bool, default True

        :param as_table: Print the evaluation results as table (only work with verbose=True)
        :type as_table: bool, default False

        :param table_sep: Delimiter for print results (only work with verbose=True and as_table=True)
        :type table_sep: str, default ' '
        
        :param as_rank: If True, evaluate as rank.
        :type as_rank: bool, default False

        """
        super(RatingPredictionEvaluation, self).__init__(sep=sep, metrics=metrics, all_but_one_eval=all_but_one_eval, verbose=verbose,
          as_table=as_table,
          table_sep=table_sep)
        self.as_rank = as_rank
        self.n_rank = n_rank

    def evaluate(self, predictions, test_set):
        """
        Method to calculate all the metrics for item recommendation scenario using dictionaries of ranking
        and test set. Use read() in ReadFile to transform your prediction and test files in a dict

        :param predictions: Dict of predictions
        :type predictions: dict

        :param test_set: Dictionary with test set information.
        :type test_set: dict

        :return: Dictionary with all evaluation metrics and results
        :rtype: dict

        """
        eval_results = {}
        predictions_list = []
        test_list = []
        if not self.as_rank:
            if self.all_but_one_eval:
                for user in test_set['users']:
                    item = random.choice(test_set['feedback'][user])
                    test_set['feedback'][user] = {item: test_set['feedback'][user][item]}

            for user in predictions:
                for item in predictions[user]:
                    rui_predict = predictions[user][item]
                    rui_test = test_set['feedback'].get(user, {}).get(item, np.nan)
                    if not np.isnan(rui_test):
                        predictions_list.append(rui_predict)
                        test_list.append(float(rui_test))

            eval_results.update({'MAE':round(mean_absolute_error(test_list, predictions_list), 6), 
             'RMSE':round(np.sqrt(mean_squared_error(test_list, predictions_list)), 6)})
            if self.verbose:
                self.print_results(eval_results)
        else:
            new_predict_set = []
            new_test_set = {}
            for user in predictions:
                partial_predictions = []
                for item in predictions[user]:
                    if predictions[user][item] > 3:
                        partial_predictions.append([user, item, predictions[user][item]])
                    if test_set['feedback'].get(user, {}).get(item, 0) > 3:
                        new_test_set.setdefault(user, []).append(item)

                partial_predictions = sorted(partial_predictions, key=(lambda x: -x[2]))
                new_predict_set += partial_predictions

            new_test_set['items_seen_by_user'] = new_test_set
            new_test_set['users'] = test_set['users']
            eval_results = ItemRecommendationEvaluation(n_ranks=(self.n_rank), all_but_one_eval=(self.all_but_one_eval),
              metrics=(self.metrics)).evaluate_recommender(new_predict_set, new_test_set)
        return eval_results