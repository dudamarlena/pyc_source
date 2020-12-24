# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/binary_greedy.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 5910 bytes
from adlib.adversaries.adversary import Adversary
from data_reader.binary_input import Instance, BinaryFeatureVector
from typing import List, Dict
from random import shuffle
import numpy as np

class BinaryGreedy(Adversary):

    def __init__(self, learner=None, max_change=200, lambda_val=0.05, epsilon=0.0002, step_size=0.05):
        """
        :param learner: Learner(from adlib.learners)
        :param max_change: max times allowed to change the feature
        :param lambda_val: weight in quodratic distances calculation
        :param epsilon: the limit of difference between transform costs of
                        xij+1, xij, and orginal x
        :param step_size: weight for coordinate descent
        """
        Adversary.__init__(self)
        self.lambda_val = lambda_val
        self.epsilon = epsilon
        self.step_size = step_size
        self.num_features = 0
        self.learn_model = learner
        self.max_change = max_change
        if self.learn_model is not None:
            self.weight_vector = self.learn_model.get_weight()
        else:
            self.weight_vector = None

    def get_available_params(self) -> Dict:
        raise NotImplementedError

    def set_params(self, params: Dict):
        raise NotImplementedError

    def set_adversarial_params(self, learner, train_instances: List[Instance]):
        self.learn_model = learner
        self.num_features = train_instances[0].get_feature_count()

    def attack(self, Instances) -> List[Instance]:
        if self.weight_vector is None:
            if self.learn_model is not None:
                self.weight_vector = self.learn_model.get_weight()
        if self.num_features == 0:
            self.num_features = Instances[0].get_feature_count()
        if self.weight_vector is None:
            raise ValueError('Must set learner_model and weight_vector before attack.')
        transformed_instances = []
        for instance in Instances:
            if instance.label > 0:
                transformed_instances.append(self.coordinate_greedy(instance))
            else:
                transformed_instances.append(instance)

        return transformed_instances

    def coordinate_greedy(self, instance: Instance) -> Instance:
        indices = [i for i in range(0, self.num_features)]
        x = xk = instance.get_csr_matrix().toarray()[0]
        no_improve_count = 0
        shuffle(indices)
        for i in indices:
            xkplus1 = self.minimize_transform(xk, i)
            oldQ = self.transform_cost(xk, x)
            newQ = self.transform_cost(xkplus1, x)
            step_change = newQ - oldQ
            if step_change >= 0:
                no_improve_count += 1
                if no_improve_count >= self.max_change:
                    break
            else:
                xk = xkplus1

        mat_indices = [x for x in range(0, self.num_features) if xk[x] != 0]
        new_instance = Instance(-1, BinaryFeatureVector(self.num_features, mat_indices))
        if self.learn_model.predict(new_instance) == self.learn_model.positive_classification:
            return instance
        return new_instance

    def minimize_transform(self, xi: np.array, i):
        xk = np.copy(xi)
        xk[i] = 1 - xi[i]
        return xk

    def transform_cost(self, x: np.array, xi: np.array):
        return self.weight_vector.dot(x) + self.quadratic_cost(x, xi)

    def quadratic_cost(self, x: np.array, xi: np.array):
        return self.lambda_val / 2 * sum((x - xi) ** 2)