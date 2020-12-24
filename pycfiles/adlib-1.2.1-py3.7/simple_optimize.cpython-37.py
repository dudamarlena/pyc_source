# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/simple_optimize.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 2695 bytes
from adlib.adversaries.adversary import Adversary
from typing import List, Dict
from data_reader.binary_input import Instance
from adlib.learners.learner import Learner
from copy import deepcopy
from math import exp

class SimpleOptimize(Adversary):

    def __init__(self, lambda_val=-100, max_change=1000, learn_model=None):
        Adversary.__init__(self)
        self.lambda_val = lambda_val
        self.max_change = max_change
        self.num_features = None
        self.learn_model = learn_model

    def attack(self, instances: List[Instance]) -> List[Instance]:
        transformed_instances = []
        for instance in instances:
            transformed_instance = deepcopy(instance)
            if instance.get_label() == Learner.positive_classification:
                transformed_instances.append(self.optimize(transformed_instance))
            else:
                transformed_instances.append(transformed_instance)

        return transformed_instances

    def set_params(self, params: Dict):
        if 'lambda_val' in params.keys():
            self.lambda_val = params['lambda_val']
        if 'max_change' in params.keys():
            self.max_change = params['max_change']

    def get_available_params(self) -> Dict:
        params = {'lambda_val':self.lambda_val,  'max_change':self.max_change}
        return params

    def set_adversarial_params(self, learner, training_data):
        self.learn_model = learner
        self.num_features = training_data[0].get_feature_vector().get_feature_count()

    def optimize(self, instance: Instance):
        """Flip features that lower the prob. of being classified adversarial.
        Args:
            instance: (scipy.sparse.csr_matrix) feature vector

        """
        change = 0
        for i in range(0, self.num_features):
            orig_prob = self.learn_model.predict_proba([instance])[0]
            new_instance = deepcopy(instance)
            new_instance.get_feature_vector().flip_bit(i)
            new_prob = self.learn_model.predict_proba([new_instance])[0]
            if new_prob < orig_prob - exp(self.lambda_val):
                instance.get_feature_vector().flip_bit(i)
                change += 1
            if change > self.max_change:
                break

        return instance