# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caserec/recommenders/rating_prediction/user_attribute_knn.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 6702 bytes
""""
    User Based Collaborative Filtering Recommender with Attributes (User Attribute KNN)
    [Rating Prediction]

    User-Attribute-kNN predicts a user’s rating according to how similar users rated the same item. The algorithm
    matches similar users based on the similarity of their attributes scores. However, instead of traditional UserKNN,
    this approach uses a pre-computed similarity matrix based on metadata.

"""
import numpy as np
from caserec.recommenders.rating_prediction.userknn import UserKNN
from caserec.utils.process_data import ReadFile
__author__ = 'Arthur Fortes <fortes.arthur@gmail.com>'

class UserAttributeKNN(UserKNN):

    def __init__(self, train_file=None, test_file=None, output_file=None, metadata_file=None, similarity_file=None, k_neighbors=30, as_similar_first=True, metadata_as_binary=False, metadata_similarity_sep='\t', similarity_metric='cosine', sep='\t', output_sep='\t'):
        """
        User Attribute KNN for Rating Prediction

        This algorithm predicts a rating for each pair (user, item) based on the similar items that his neighbors
        (similar users) consumed, using a metadata or similarity pre-computed file

        Usage::

            >> UserAttributeKNN(train, test, similarity_file=sim_matrix, as_similar_first=True).compute()
            >> UserAttributeKNN(train, test, metadata_file=metadata, as_similar_first=True).compute()

        :param train_file: File which contains the train set. This file needs to have at least 3 columns
        (user item feedback_value).
        :type train_file: str

        :param test_file: File which contains the test set. This file needs to have at least 3 columns
        (user item feedback_value).
        :type test_file: str, default None

        :param output_file: File with dir to write the final predictions
        :type output_file: str, default None

        :param metadata_file: File which contains the metadata set. This file needs to have at least 2 columns
        (user metadata).
        :type metadata_file: str, default None

        :param similarity_file: File which contains the similarity set. This file needs to have at least 3 columns
        (user user similarity).
        :type similarity_file: str, default None

        :param k_neighbors: Number of neighbors to use. If None, k_neighbor = int(sqrt(n_users))
        :type k_neighbors: int, default None

        :param as_similar_first: If True, for each unknown item, which will be predicted, we first look for its k
        most similar users and then take the intersection with the users that
        seen that item.
        :type as_similar_first: bool, default True

        :param metadata_as_binary: f True, the explicit value will be transform to binary
        :type metadata_as_binary: bool, default False

        :param metadata_similarity_sep: Delimiter for similarity or metadata file
        :type metadata_similarity_sep: str, default '   '

        :param similarity_metric:
        :type similarity_metric: str, default cosine

        :param sep: Delimiter for input files file
        :type sep: str, default '       '

        :param output_sep: Delimiter for output file
        :type output_sep: str, default '        '
        """
        super(UserAttributeKNN, self).__init__(train_file=train_file, test_file=test_file, output_file=output_file, k_neighbors=k_neighbors,
          as_similar_first=as_similar_first,
          similarity_metric=similarity_metric,
          sep=sep,
          output_sep=output_sep)
        self.recommender_name = 'User Attribute KNN Algorithm'
        self.metadata_file = metadata_file
        self.similarity_file = similarity_file
        self.metadata_as_binary = metadata_as_binary
        self.metadata_similarity_sep = metadata_similarity_sep

    def init_model(self):
        """
        Method to fit the model. Create and calculate a similarity matrix by metadata file or a pre-computed similarity
        matrix

        """
        self.users_id_viewed_item = {}
        if self.k_neighbors is None:
            self.k_neighbors = int(np.sqrt(len(self.users)))
        else:
            for item in self.items:
                for user in self.train_set['users_viewed_item'].get(item, []):
                    self.users_id_viewed_item.setdefault(item, []).append(self.user_to_user_id[user])

            if self.metadata_file is not None:
                metadata = ReadFile((self.metadata_file), sep=(self.metadata_similarity_sep), as_binary=(self.metadata_as_binary)).read_metadata_or_similarity()
                self.matrix = np.zeros((len(self.users), len(metadata['col_2'])))
                meta_to_meta_id = {}
                for m, data in enumerate(metadata['col_2']):
                    meta_to_meta_id[data] = m

                for user_m in metadata['col_1']:
                    for m1 in metadata['dict'][user_m]:
                        try:
                            self.matrix[(self.user_to_user_id[user_m], meta_to_meta_id[m1])] = metadata['dict'][user_m][m1]
                        except KeyError:
                            pass

                sparsity = (1 - metadata['number_interactions'] / (len(metadata['col_1']) * len(metadata['col_2']))) * 100
                self.extra_info_header = '>> metadata:: %d users and %d metadata (%d interactions) | sparsity:: %.2f%%' % (
                 len(metadata['col_1']), len(metadata['col_2']), metadata['number_interactions'],
                 sparsity)
                self.su_matrix = self.compute_similarity(transpose=False)
            else:
                if self.similarity_file is not None:
                    similarity = ReadFile((self.similarity_file), sep=(self.metadata_similarity_sep), as_binary=False).read_metadata_or_similarity()
                    self.su_matrix = np.zeros((len(self.users), len(self.users)))
                    for u in similarity['col_1']:
                        for u_j in similarity['dict'][u]:
                            self.su_matrix[(self.user_to_user_id[u], self.user_to_user_id[int(u_j)])] = similarity['dict'][u][u_j]

                    self.su_matrix[np.isnan(self.su_matrix)] = 0.0
                else:
                    raise ValueError('This algorithm needs a similarity matrix or a metadata file!')
        self.create_matrix()