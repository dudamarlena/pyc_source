# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/adversaries/gradient_descent.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 18788 bytes
from adlib.adversaries.adversary import Adversary
from data_reader.binary_input import Instance
from data_reader.real_input import RealFeatureVector
from adlib.learners.simple_learner import SimpleLearner
from typing import List, Dict
from random import shuffle
import numpy as np
import adlib.learners as learners
from copy import deepcopy
from sklearn.svm import SVC
from sklearn.metrics import pairwise
from collections import deque
from data_reader.operations import sparsify
import operator

class GradientDescent(Adversary):

    def __init__(self, learn_model=None, step_size=0.01, trade_off=10, stp_constant=1e-09, mimicry='euclidean', max_iter=1000, mimicry_params={}, bound=0.1, binary=False):
        """
        :param learner: Learner(from learners)
        :param max_change: max times allowed to change the feature
        :param lambda_val: weight in quodratic distances calculation
        :param epsilon: the limit of difference between transform costs of ,xij+1, xij, and
                        orginal x
        :param step_size: weight for coordinate descent
        :param max_boundaries: maximum number of gradient descent iterations to be performed
                               set it to a large number by default.
        :param mimicry_params: hyperparameter for mimicry params.
        :param bound: limit how far one instance can move from its root instance.
                      this is d(x,x_prime) in the algortihm.
        """
        Adversary.__init__(self)
        self.step_size = step_size
        self.lambda_val = trade_off
        self.num_features = 0
        self.learn_model = learn_model
        self.epsilon = stp_constant
        self.mimicry = mimicry
        self.max_iter = max_iter
        self.mimicry_params = mimicry_params
        self.bound = bound
        self.binary = binary

    def get_available_params(self) -> Dict:
        return {'step_size':self.step_size, 
         'trade_off':self.lambda_val, 
         'learn_model':self.learn_model, 
         'stp_constant':self.epsilon, 
         'mimicry':self.minicry, 
         'max_iteration':self.max_iteration, 
         'mimicry_params':self.mimicry_params, 
         'bound':self.bound, 
         'binary':self.binary}

    def set_params(self, params: Dict):
        if 'step_size' in params.keys():
            self.step_size = params['step_size']
        if 'trade_off' in params.keys():
            self.lambda_val = params['trade_off']
        if 'stp_constant' in params.keys():
            self.epsilon = params['stp_constant']
        if 'learn_model' in params.keys():
            self.learn_model = params['learn_model']
        if 'self.minicry' in params.keys():
            self.minicry = params['minicry']
        if 'max_iteration' in params.keys():
            self.max_iteration = params['max_iteration']
        if 'mimicry_params' in params.keys():
            self.mimicry_params = params['mimicry_params']
        if 'bound' in params.keys():
            self.bound = params['bound']
        if 'binary' in params.keys():
            self.binary = params['binary']

    def set_adversarial_params(self, learner, train_instances: List[Instance]):
        self.learn_model = learner
        self.num_features = train_instances[0].get_feature_count()
        self.train_instances = train_instances

    def attack(self, Instances) -> List[Instance]:
        if self.num_features == 0:
            self.num_features = Instances[0].get_feature_count()
        benign_instances = []
        malicious_instances = []
        for instance in Instances:
            if instance.label < 0:
                benign_instances.append(instance)

        y_list, X_list = sparsify(benign_instances)
        num_instances = len(y_list)
        y, X = np.array(y_list).reshape((num_instances, 1)), X_list.toarray().reshape((
         num_instances, self.num_features))
        transformed_instances = []
        for instance in Instances:
            if instance.label < 0:
                transformed_instances.append(instance)
            else:
                transformed_instances.append(self.gradient_descent(instance, X))

        return transformed_instances

    def gradient_descent(self, instance: Instance, neg_instances):
        attack_instance = instance.get_csr_matrix().toarray()
        root_instance = attack_instance
        obj_function_value_list = []
        candidate_attack_instances = [
         attack_instance]
        attacker_score = self.get_score(attack_instance)
        closer_neg_instances, dist, grad_update = self.compute_gradient(attack_instance, neg_instances)
        obj_func_value = attacker_score + self.lambda_val * dist
        obj_function_value_list.append(obj_func_value)
        for iter in range(self.max_iter):
            past_instance = candidate_attack_instances[(-1)]
            new_instance = self.update_within_boundary(past_instance, root_instance, grad_update)
            closer_neg_instances, dist, new_grad_update = self.compute_gradient(new_instance, closer_neg_instances)
            new_attacker_score = self.get_score(new_instance)
            obj_func_value = new_attacker_score + self.lambda_val * dist
            if self.check_convergence_info(obj_func_value, obj_function_value_list):
                mat_indices = [x for x in range(0, self.num_features) if new_instance[0][x] != 0]
                mat_data = [new_instance[0][x] for x in range(0, self.num_features) if new_instance[0][x] != 0]
                return Instance(-1, RealFeatureVector(self.num_features, mat_indices, mat_data))
            if obj_func_value < obj_function_value_list[(-1)]:
                obj_function_value_list.append(obj_func_value)
            if not (new_instance == candidate_attack_instances[(-1)]).all():
                candidate_attack_instances.append(new_instance)
            attacker_score = new_attacker_score
            grad_update = new_grad_update

        mat_indices = [x for x in range(0, self.num_features) if candidate_attack_instances[(-1)][0][x] != 0]
        mat_data = [candidate_attack_instances[(-1)][0][x] for x in range(0, self.num_features) if candidate_attack_instances[(-1)][0][x] != 0]
        return Instance(-1, RealFeatureVector(self.num_features, mat_indices, mat_data))

    def check_convergence_info(self, obj_func_value, obj_function_value_list):
        if len(obj_function_value_list) >= 5:
            val = obj_function_value_list[(-5)] - obj_func_value
            if val <= self.epsilon:
                return True
        return False

    def compute_gradient(self, attack_instance, neg_instances):
        """
        compute gradient with the trade off of density estimation, return a unit vector
        :param attack_instance:
        :param neg_instances:
        :param lambda_value:
        :param mimicry_params:
        :return: 1.the set of closest legitimate samples 2.the distance value wrt to the closest
                   sample
                 3.the updated gradient by lambda_val * KDE
        """
        grad = self.gradient(attack_instance)
        if self.lambda_val > 0:
            closer_neg_instances, grad_mimicry, dist = self.gradient_mimicry(attack_instance, neg_instances, self.mimicry_params)
            grad_update = grad + self.lambda_val * grad_mimicry
        else:
            print('The trade_off parameter is 0!')
            closer_neg_instances = neg_instances
            grad_update = grad
            dist = 0
        if np.linalg.norm(grad_update) != 0:
            grad_update = grad_update / np.linalg.norm(grad_update)
        return (closer_neg_instances, dist, grad_update)

    def update_within_boundary(self, attack_instance, root_instance, grad_update):
        new_instance = np.array(attack_instance - self.step_size * grad_update)
        for i in range(len(new_instance[0])):
            if new_instance[0][i] - root_instance[0][i] > self.bound:
                new_instance[0][i] = root_instance[0][i] + self.bound

        return new_instance

    def gradient(self, attack_instance):
        """
        Compute gradient in the case of different classifiers
        if kernel is rbf, the gradient is updated as exp{-2rexp||x-xi||^2}
        if kernel is linear, it should be the weight vector
        support sklearn.svc rbr/linear and robust learner classes
        :return:
        """
        if type(self.learn_model) == SimpleLearner and type(self.learn_model.model.learner) == SVC:
            param_map = self.learn_model.get_params()
            attribute_map = self.learn_model.get_attributes()
            if param_map['kernel'] == 'rbf':
                grad = []
                dual_coef = attribute_map['dual_coef_']
                support = attribute_map['support_vectors_']
                gamma = param_map['gamma']
                kernel = pairwise.rbf_kernel(support, attack_instance, gamma)
                for element in range(0, len(support)):
                    if grad == []:
                        grad = dual_coef[0][element] * kernel[0][element] * 2 * gamma * (support[element] - attack_instance)
                    else:
                        grad += dual_coef[0][element] * kernel[element][0] * 2 * gamma * (support[element] - attack_instance)

                return -grad
            if param_map['kernel'] == 'linear':
                return attribute_map['coef_'][0]
        else:
            try:
                grad = self.learn_model.get_weight()
                return grad
            except:
                print('Did not find the gradient for this classifier.')

    def gradient_mimicry(self, attack_instance, negative_instances, params):
        max_neg_instance = 10
        weight = 1
        gamma = 0.1
        if 'max_neg_instance' in params.keys():
            max_neg_instance = params['max_neg_instance']
        if 'weight' in params.keys():
            weight = params['weight']
        if 'gamma' in params.keys():
            gamma = params['gamma']
        if self.mimicry == 'euclidean':
            return self.gradient_euclidean(attack_instance, negative_instances, max_neg_instance, weight)
        if self.mimicry == 'kde_euclidean':
            return self.gradient_kde_euclidean(attack_instance, negative_instances, max_neg_instance, gamma, weight)
        if self.mimicry == 'kde_hamming':
            return self.gradient_kde_hamming(attack_instance, negative_instances, max_neg_instance, gamma, weight)
        print('Gradient Descent Attack: unsupported mimicry distance %s.' % self.mimicry)
        return

    def gradient_euclidean(self, attack_instance, negative_instances, max_neg_instance=10, weights=1):
        dist = [(negative_instance, self.euclidean_dist(attack_instance, negative_instance, weights)) for negative_instance in negative_instances]
        dist.sort(key=(operator.itemgetter(1)))
        if max_neg_instance < len(dist):
            dist = dist[:max_neg_instance]
        neg_instances = [instances[0] for instances in dist]
        return (
         neg_instances, 2 * (attack_instance - neg_instances[0]), dist[0][1])

    def gradient_kde_euclidean(self, attack_instance, negative_instances, max_neg_instance=10, gamma=0.1, weights=1):
        kernel = [(negative_instance, np.exp(-gamma * self.euclidean_dist_power2(attack_instance, negative_instance, weights))) for negative_instance in negative_instances]
        kernel.sort(key=(operator.itemgetter(1)), reverse=True)
        if max_neg_instance < len(kernel):
            kernel = kernel[:max_neg_instance]
        neg_instances = [instances[0] for instances in kernel]
        kde = 0.0
        gradient_kde = 0.0
        for i, k in enumerate(kernel):
            kde += k[1]
            gradient_kde += -gamma * 2 * (attack_instance - neg_instances[i]) * k[1]

        kde = kde / len(kernel)
        gradient_kde = gamma * gradient_kde / len(kernel)
        return (
         neg_instances, -gradient_kde, -kde)

    def gradient_kde_hamming(self, attack_instance, negative_instances, max_neg_instance=10, gamma=0.1, weights=1):
        kernel = [(negative_instance, np.exp(-gamma * self.hamming_dist(attack_instance, negative_instance, weights))) for negative_instance in negative_instances]
        kernel.sort(key=(operator.itemgetter(1)), reverse=True)
        if max_neg_instance < len(kernel):
            kernel = kernel[:max_neg_instance]
        neg_instances = [instances[0] for instances in kernel]
        kde = 0.0
        gradient_kde = 0.0
        for i, k in enumerate(kernel):
            kde += k[1]
            gradient_kde += -(attack_instance - neg_instances[i]) * k[1]

        kde = kde / len(kernel)
        return (
         neg_instances, -gradient_kde, -kde)

    def hamming_dist(self, a, b, norm_weights):
        return np.sum(np.absolute(a - b) * norm_weights)

    def euclidean_dist_power2(self, a, b, norm_weights):
        return np.sum(((a - b) * norm_weights) ** 2)

    def euclidean_dist(self, a, b, norm_weights):
        return np.linalg.norm((a - b) * norm_weights)

    def get_score(self, pattern):
        score = self.learn_model.decision_function(pattern)
        return score[0]