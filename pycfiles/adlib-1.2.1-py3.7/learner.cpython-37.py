# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/learners/learner.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 2382 bytes
from typing import Dict, List
from data_reader.binary_input import Instance

class Learner(object):
    __doc__ = 'Base class for initial learning methods.\n\n    Defines the bare-minimum functionality for initial learning\n    strategies. Specified learning algorithms can create wrappers\n    around the underlying methods.\n\n    '
    positive_classification = 1
    negative_classification = -1

    def __init__(self):
        """New generic initial learner with no specified learning model.

        """
        self.num_features = 0
        self.training_instances = None

    def set_training_instances(self, training_data):
        """

        :param training_data: an dataset object , which when calling numpy() will return
                X: feature matrix. shape (num_instances, num_feautres_per_instance)
                y: label array. shape (num_instances, )
        """
        if isinstance(training_data, List):
            self.training_instances = training_data
            self.num_features = self.training_instances[0].get_feature_vector().get_feature_count()
        else:
            self.training_instances = training_data
            self.num_features = training_data.features.shape[1]

    def train(self):
        """Train on the set of training instances.

        """
        raise NotImplementedError

    def predict(self, instances):
        """Predict classification labels for the set of instances.

        Args:
            :param instances: matrix of instances shape (num_instances, num_feautres_per_instance)

        Returns:
            label classifications (List(int))

        """
        raise NotImplementedError

    def set_params(self, params: Dict):
        """Set params for the initial learner.

        Defines default behavior, setting only BaseModel params

        Args:
            params (Dict): set of available params with updated values.

        """
        raise NotImplementedError

    def predict_proba(self, X):
        """
        outputs a list of log probability of prediction
        :param X: matrix of instances shape (num_instances, num_feautres_per_instance)
        :return: list of log probability
        """
        raise NotImplementedError

    def decision_function(self, X):
        raise NotImplementedError