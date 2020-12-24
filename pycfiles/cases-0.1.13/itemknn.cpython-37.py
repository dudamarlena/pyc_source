# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caserec/recommenders/rating_prediction/itemknn.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 10045 bytes
__doc__ = '\n    ItemKNN based on Collaborative Filtering Recommender\n    [Rating Prediction]\n\n    Literature:\n        KAggarwal, Charu C.:\n        Chapter 2: Neighborhood-Based Collaborative Filtering\n        Recommender Systems: The Textbook. 2016\n        https://www.springer.com/br/book/9783319296579\n\n'
from collections import defaultdict
import numpy as np
from caserec.utils.extra_functions import timed
from caserec.recommenders.rating_prediction.base_knn import BaseKNN
__author__ = 'Arthur Fortes <fortes.arthur@gmail.com>'

class ItemKNN(BaseKNN):

    def __init__(self, train_file=None, test_file=None, output_file=None, similarity_metric='cosine', k_neighbors=None, as_similar_first=False, sep='\t', output_sep='\t'):
        """
        ItemKNN for rating prediction

        Its philosophy is as follows: in order to determine the rating of User u on item m, we can find other items
        that are similar to item m, and based on User u’s ratings on those similar items we infer his rating on
        item m.

        Usage::

            >> ItemKNN(train, test).compute()
            >> ItemKNN(train, test, ranking_file, as_similar_first=True).compute()

        :param train_file: File which contains the train set. This file needs to have at least 3 columns
        (user item feedback_value).
        :type train_file: str

        :param test_file: File which contains the test set. This file needs to have at least 3 columns
        (user item feedback_value).
        :type test_file: str, default None

        :param output_file: File with dir to write the final predictions
        :type output_file: str, default None

        :param similarity_metric: Pairwise metric to compute the similarity between the items. Reference about
        distances: http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.pdist.html
        :type similarity_metric: str, default cosine

        :param k_neighbors: Number of neighbors to use. If None, k_neighbor = int(sqrt(n_users))
        :type k_neighbors: int, default None

        :param as_similar_first: If True, for each unknown item, which will be predicted, we first look for its k
        most similar users and then take the intersection with the users that
        seen that item.
        :type as_similar_first: bool, default False

        :param sep: Delimiter for input files
        :type sep: str, default '       '

        :param output_sep: Delimiter for output file
        :type output_sep: str, default '        '

        """
        super(ItemKNN, self).__init__(train_file=train_file, test_file=test_file, output_file=output_file, sep=sep, output_sep=output_sep,
          similarity_metric=similarity_metric)
        self.recommender_name = 'ItemKNN Algorithm'
        self.as_similar_first = as_similar_first
        self.k_neighbors = k_neighbors
        self.si_matrix = None
        self.similar_items = None

    def init_model(self):
        super(ItemKNN, self).init_model()
        self.similar_items = defaultdict(list)
        if self.k_neighbors is None:
            self.k_neighbors = int(np.sqrt(len(self.items)))
        self.si_matrix = self.compute_similarity(transpose=True)
        for i_id, item in enumerate(self.items):
            self.similar_items[i_id] = sorted((range(len(self.si_matrix[i_id]))), key=(lambda k: -self.si_matrix[i_id][k]))[1:self.k_neighbors + 1]

    def predict(self):
        """
        Method to predict ratings for all known users in the train set.

        """
        for user in self.users:
            if len(self.train_set['feedback'].get(user, [])) != 0:
                if self.test_file is not None:
                    if self.as_similar_first:
                        self.predictions += self.predict_similar_first_scores(user, self.test_set['items_seen_by_user'].get(user, []))
                    else:
                        self.predictions += self.predict_scores(user, self.test_set['items_seen_by_user'].get(user, []))
                else:
                    items_seen_by_user = []
                    u_list = list(np.flatnonzero(self.matrix[self.user_to_user_id[user]] == 0))
                    for item_id in u_list:
                        items_seen_by_user.append(self.item_id_to_item[item_id])

                    if self.as_similar_first:
                        self.predictions += self.predict_similar_first_scores(user, items_seen_by_user)
                    else:
                        self.predictions += self.predict_scores(user, items_seen_by_user)
                        continue

    def predict_scores(self, user, unpredicted_items):
        predictions = []
        for item_j in unpredicted_items:
            item_j_id = self.item_to_item_id[item_j]
            rui = 0
            sim_sum = 0
            neighbors_list = []
            for item in self.train_set['items_seen_by_user'][user]:
                neighbors_list.append((item, self.si_matrix[(item_j_id, self.item_to_item_id[item])],
                 self.train_set['feedback'][user][item]))

            neighbors_list = sorted(neighbors_list, key=(lambda x: -x[1]))[::self.k_neighbors]
            if neighbors_list:
                for triple in neighbors_list:
                    rui += (triple[2] - self.bui[user][triple[0]]) * triple[1] if triple[1] != 0 else 0.001
                    sim_sum += triple[1] if triple[1] != 0 else 0.001

                rui = self.bui[user][item_j] + rui / sim_sum
            else:
                rui = self.bui[user][item_j]
            if rui > self.train_set['max_value']:
                rui = self.train_set['max_value']
            if rui < self.train_set['min_value']:
                rui = self.train_set['min_value']
            predictions.append((user, item_j, rui))

        return sorted(predictions, key=(lambda x: x[1]))

    def predict_similar_first_scores(self, user, unpredicted_items):
        """
        In this implementation, for each unknown item, which will be
        predicted, we first look for its k most similar items and then take the intersection with the seen items of
        the user. Finally, the score of the unknown item will be the sum of the  similarities of k's most similar
        to it, taking into account only the items that each user seen.

        """
        predictions = []
        user_id = self.user_to_user_id[user]
        seen_items_id = np.flatnonzero(self.matrix[user_id])
        for item_j in unpredicted_items:
            item_j_id = self.item_to_item_id[item_j]
            rui = 0
            sim_sum = 0
            neighbors_list_id = list(set(self.similar_items[item_j_id]).intersection(seen_items_id))
            if neighbors_list_id:
                for item_id in neighbors_list_id:
                    item = self.item_id_to_item[item_id]
                    similarity = self.si_matrix[(item_j_id, item_id)]
                    rui += (self.train_set['feedback'][user][item] - self.bui[user][item]) * similarity if similarity != 0 else 0.001
                    sim_sum += similarity if similarity != 0 else 0.001

                rui = self.bui[user][item_j] + rui / sim_sum
            else:
                rui = self.bui[user][item_j]
            if rui > self.train_set['max_value']:
                rui = self.train_set['max_value']
            if rui < self.train_set['min_value']:
                rui = self.train_set['min_value']
            predictions.append((user, item_j, rui))

        return sorted(predictions, key=(lambda x: x[1]))

    def compute(self, verbose=True, metrics=None, verbose_evaluation=True, as_table=False, table_sep='\t'):
        """
        Extends compute method from BaseItemRecommendation. Method to run recommender algorithm

        :param verbose: Print recommender and database information
        :type verbose: bool, default True

        :param metrics: List of evaluation metrics
        :type metrics: list, default None

        :param verbose_evaluation: Print the evaluation results
        :type verbose_evaluation: bool, default True

        :param as_table: Print the evaluation results as table
        :type as_table: bool, default False

        :param table_sep: Delimiter for print results (only work with verbose=True and as_table=True)
        :type table_sep: str, default ' '

        """
        super(ItemKNN, self).compute(verbose=verbose)
        if verbose:
            self.init_model()
            print('training_time:: %4f sec' % timed(self.train_baselines))
            if self.extra_info_header is not None:
                print(self.extra_info_header)
            print('prediction_time:: %4f sec' % timed(self.predict))
        else:
            self.extra_info_header = None
            self.init_model()
            self.train_baselines()
            self.predict()
        self.write_predictions()
        if self.test_file is not None:
            self.evaluate(metrics, verbose_evaluation, as_table=as_table, table_sep=table_sep)