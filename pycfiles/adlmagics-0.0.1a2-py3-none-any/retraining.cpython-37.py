# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/learners/retraining.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 4486 bytes
from adlib.learners.learner import Learner
from typing import Dict, List
from data_reader.dataset import EmailDataset
from data_reader.binary_input import Instance
from adlib.learners.models.sklearner import Model
import numpy as np
from data_reader.operations import fv_equals

class Retraining(Learner):

    def __init__(self, base_model=None, training_instances=None, attack_alg=None):
        Learner.__init__(self)
        self.model = Model(base_model)
        self.attack_alg = attack_alg
        self.adv_params = None
        self.attacker = None
        self.set_training_instances(training_instances)
        self.iterations = 5

    def set_params(self, params: Dict):
        if 'attack_alg' in params.keys():
            self.attack_alg = params['attack_alg']
        else:
            if 'attacker' in params.keys():
                self.attacker = params['attacker']
            if params['adv_params'] is not None:
                self.adv_params = params['adv_params']
            if 'iterations' in params.keys() and 'iterations' is not None:
                self.iterations = params['iterations']

    def get_available_params(self) -> Dict:
        params = {'attacker':self.attacker,  'adv_params':self.adv_params, 
         'iterations':self.iterations}
        return params

    def train(self):
        """
        This is implemented according to Algorithm 1 in Central Rettraining Framework
        for Scalable Adversarial Classification. This will iterate between computing
        a classifier and adding the adversarial instances to the training data that evade
        the previously computed classifier.
        :return: None
        """
        self.model.train(self.training_instances)
        iteration = self.iterations
        self.attacker = self.attack_alg()
        self.attacker.set_params(self.adv_params)
        self.attacker.set_adversarial_params(self.model, self.training_instances)
        malicious_instances = [x for x in self.training_instances if self.model.predict(x) == 1]
        augmented_instances = self.training_instances
        while iteration != 0:
            print('iteration: {}'.format(iteration))
            new = []
            transformed_instances = self.attacker.attack(malicious_instances)
            for instance in transformed_instances:
                in_list = False
                for idx, old_instance in enumerate(augmented_instances):
                    if fv_equals(old_instance.get_feature_vector(), instance.get_feature_vector()):
                        in_list = True

                if not in_list:
                    new.append(instance)
                augmented_instances.append(Instance(label=1, feature_vector=(instance.get_feature_vector())))

            self.model.train(augmented_instances)
            malicious_instances = [x for x in augmented_instances if self.model.predict(x) == 1]
            iteration -= 1
            if new is None:
                break

    def decision_function(self, instances):
        return self.model.decision_function_(instances)

    def predict(self, instances):
        """

        :param instances: matrix of instances shape (num_instances, num_feautres_per_instance)
        :return: list of labels (int)
        """
        return self.model.predict(instances)

    def predict_proba(self, instances):
        return self.model.predict_proba(instances)

    def get_weight(self):
        print('weight shape in retraining: {}'.format(self.model.learner.coef_[0].T.shape))
        return self.model.learner.coef_[0].T

    def get_constant(self):
        return self.model.learner.intercept_