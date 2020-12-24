# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/coordinate_greedy.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 12443 bytes
from adlib.adversaries.adversary import Adversary
from data_reader.binary_input import Instance
from data_reader.real_input import RealFeatureVector
from typing import List, Dict
from adlib.learners.simple_learner import SimpleLearner
from sklearn.svm import SVC
from random import shuffle
import numpy as np
import adlib.learners as learners
from copy import deepcopy
from random import *
from sklearn.metrics import pairwise
DEBUG = False

class CoordinateGreedy(Adversary):

    def __init__(self, learn_model=None, max_iteration=1000, lambda_val=0.01, epsilon=1e-09, step_size=1, cost_function='quadratic', random_start=3, convergence_time=100):
        """
        :param learner: Learner(from learners)
        :param max_iteration: max times allowed to change the feature
        :param lambda_val: weight in quodratic distances calculation
        :param epsilon: the limit of difference between transform costs of ,xij+1, xij, and
                        orginal x
        :param step_size: weight for coordinate descent
        :param cost_function: decide whether to use exponential cost or quadratic cost
        """
        Adversary.__init__(self)
        self.lambda_val = lambda_val
        self.epsilon = epsilon
        self.step_size = step_size
        self.num_features = 0
        self.bias = 0
        self.learn_model = learn_model
        self.max_iteration = max_iteration
        self.cost_function = cost_function
        self.random_start = random_start
        self.convergence_time = convergence_time

    def get_available_params(self) -> Dict:
        return {'max_iteration':self.max_iteration, 
         'lambda_val':self.lambda_val, 
         'epsilon':self.epsilon, 
         'step_size':self.step_size, 
         'random_start':self.random_start, 
         'cost_function':self.cost_function, 
         'convergence_time':self.convergence_time}

    def set_params(self, params: Dict):
        if 'max_iteration' in params.keys():
            self.max_iteration = params['max_iteration']
        if 'lambda_val' in params.keys():
            self.lambda_val = params['lambda_val']
        if 'epsilon' in params.keys():
            self.f_attepsilonack = params['epsilon']
        if 'step_size' in params.keys():
            self.step_size = params['step_size']
        if 'random_start' in params.keys():
            self.random_start = params['random_start']
        if 'cost_function' in params.keys():
            self.cost_function = params['cost_function']
        if 'convergence_time' in params.keys():
            self.convergence_time = params['convergence_time']

    def set_adversarial_params(self, learner, train_instances: List[Instance]):
        self.learn_model = learner
        self.num_features = train_instances[0].get_feature_count()

    def attack(self, Instances) -> List[Instance]:
        if self.num_features == 0:
            self.num_features = Instances[0].get_feature_count()
        transformed_instances = []
        for instance in Instances:
            if instance.label > 0:
                transformed_instances.append(self.random_start_coordinate_greedy(instance))
            else:
                transformed_instances.append(instance)

        return transformed_instances

    def coordinate_greedy(self, instance: Instance):
        """
         Greedily update the feature to incrementally improve the attackers utility.
         run CS from L random starting points in the feature space. We repeat the
         alternation until differences of instances are small or max_change is
         reached.

         no_improve_count: number of points
         Q: transofrm cost（we use quodratic distance）
         GreedyImprove: using the coordinate descent algorithm.
        :param instance:
        :return: if the result is still classified as +1, we return origin instance
                 else we return the improved.
        """
        instance_len = instance.get_feature_count()
        if DEBUG:
            iteration_list = []
            Q_value_list = []
        x = xk = instance.get_csr_matrix().toarray()[0]
        converge = 0
        for iteration_time in range(self.max_iteration):
            i = randint(0, instance_len - 1)
            xkplus1 = self.minimize_transform(xk, x, i)
            old_q = self.transform_cost(xk, x)
            new_q = self.transform_cost(xkplus1, x)
            if new_q - old_q <= 0:
                xk = xkplus1
                step_change = old_q - new_q
                if step_change <= self.epsilon:
                    converge += 1
                    if converge >= self.convergence_time:
                        break

        mat_indices = [x for x in range(0, self.num_features) if xk[x] != 0]
        mat_data = [xk[x] for x in range(0, self.num_features) if xk[x] != 0]
        new_instance = Instance(-1, RealFeatureVector(self.num_features, mat_indices, mat_data))
        return new_instance

    def random_start_coordinate_greedy(self, instance: Instance):
        """
        implement the n random start algorithm by performing CG for n times.
        The minimized Q and x is used as new attack instance.
        :param instance:
        :return:
        """
        instance_lst = []
        q_value_lst = []
        old_x = instance.get_csr_matrix().toarray()[0]
        for i in range(self.random_start):
            new_attacked_instance = self.coordinate_greedy(instance)
            x = new_attacked_instance.get_csr_matrix().toarray()[0]
            q = self.transform_cost(x, old_x)
            instance_lst.append(new_attacked_instance)
            q_value_lst.append(q)

        return min((zip(instance_lst, q_value_lst)), key=(lambda x: x[1]))[0]

    def learner_predict(self, attack_instance):
        if type(self.learn_model == SimpleLearner) and type(self.learn_model.model.learner) == SVC:
            param_map = self.learn_model.get_params()
            attribute_map = self.learn_model.get_attributes()
            if param_map['kernel'] == 'rbf':
                return self.learn_model.model.learner.decision_function(attack_instance.reshape(1, -1))
            if param_map['kernel'] == 'linear':
                return attribute_map['coef_'][0].dot(attack_instance) + attribute_map['intercept_']
        else:
            return self.learn_model.get_weight().dot(attack_instance) + self.learn_model.get_constant()

    def compute_gradient(self, attack_instance, index):
        if type(self.learn_model == SimpleLearner) and type(self.learn_model.model.learner) == SVC:
            param_map = self.learn_model.get_params()
            attribute_map = self.learn_model.get_attributes()
            if param_map['kernel'] == 'rbf':
                grad = []
                dual_coef = attribute_map['dual_coef_']
                support = attribute_map['support_vectors_']
                gamma = param_map['gamma']
                kernel = pairwise.rbf_kernel(support, attack_instance.reshape(1, -1), gamma)
                for element in range(0, len(support)):
                    if grad == []:
                        grad = dual_coef[0][element] * kernel[0][element] * 2 * gamma * (support[element] - attack_instance)
                    else:
                        grad += dual_coef[0][element] * kernel[element][0] * 2 * gamma * (support[element] - attack_instance)

                return (-grad)[index]
            if param_map['kernel'] == 'linear':
                return attribute_map['coef_'][0][index]
        else:
            try:
                grad = self.learn_model.get_weight()[index]
                return grad
            except:
                print('Did not find the gradient for this classifier.')

    def minimize_transform(self, xi: np.array, x: np.array, i):
        xk = np.copy(xi)
        val = 0
        if self.cost_function == 'quadratic':
            val = self.step_size * (self.compute_gradient(xk, i) + self.lambda_val * (xk[i] - x[i]))
        elif self.cost_function == 'exponential':
            val = self.step_size * (self.compute_gradient(xk, i) + self.lambda_val * self.exponential_cost(x, xi) * (1 / np.sqrt(np.sum((x - xi) ** 2) + 1)) * (xk[i] - x[i]))
        if xk[i] - val >= 0:
            xk[i] -= val
        return xk

    def transform_cost(self, x: np.array, xi: np.array):
        if self.cost_function == 'quadratic':
            return self.learner_predict(x) + self.quadratic_cost(x, xi)
        if self.cost_function == 'exponential':
            return self.learner_predict(x) + self.exponential_cost(x, xi)

    def quadratic_cost(self, x: np.array, xi: np.array):
        return self.lambda_val / 2 * sum((x - xi) ** 2)

    def exponential_cost(self, x: np.array, xi: np.array):
        return np.exp(self.lambda_val * np.sqrt(np.sum((x - xi) ** 2) + 1))