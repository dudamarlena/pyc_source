# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/dp_learner_test.py
# Compiled at: 2018-07-20 18:23:49
# Size of source mod 2**32: 11735 bytes
from adlib.learners import SimpleLearner
from adlib.learners import TRIMLearner
from adlib.learners import AlternatingTRIMLearner
from adlib.learners import IterativeRetrainingLearner
from adlib.learners import OutlierRemovalLearner
from adlib.adversaries.label_flipping import LabelFlipping
from adlib.adversaries.k_insertion import KInsertion
from adlib.adversaries.datamodification.data_modification import DataModification
from adlib.tests.adversaries.data_modification_test import calculate_target_theta
from adlib.utils.common import report
from copy import deepcopy
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from sklearn import svm
from typing import Dict, List
import numpy as np, sys, time

class TestDataPoisoningLearner:

    def __init__(self, learner_names: List[str] or str, attacker_name: str, dataset: EmailDataset, params: Dict=None, verbose=True):
        """
        Test setup.
        :param learner_names: List of learner names or one string either 'trim', 'atrim', 'irl',
                              or 'outlier-removal'
        :param attacker_name: Either 'label-flipping', 'k-insertion', 'data-modification', or
                              'dummy'
        :param dataset: the dataset
        :param params: the params to pass to the learner - if None, defaults will be used
        :param verbose: if True, will print START and STOP and set learners and attackers to
                        verbose mode
        """
        if isinstance(learner_names, str):
            learner_names = [
             learner_names]
        learner_names = list(map(lambda x: x.lower(), learner_names))
        if set(learner_names) > {'trim', 'atrim', 'irl', 'outlier-removal'}:
            raise ValueError('Learner name not trim, atrim, nor irl.')
        if attacker_name.lower() not in ('label-flipping', 'k-insertion', 'data-modification',
                                         'dummy'):
            raise ValueError('Attacker name not label-flipping, k-insertion, data-modification, nor dummy.')
        self.learner_names = learner_names

        def update_lnr_names(x):
            if x == 'trim':
                x = 'TRIM Learner'
            else:
                if x == 'atrim':
                    x = 'Alternating TRIM Learner'
                else:
                    if x == 'irl':
                        x = 'Iterative Retraining Learner'
                    else:
                        x = 'Outlier Removal Learner'
            return x

        self.learner_names = list(map(update_lnr_names, self.learner_names))
        self.attacker_name = attacker_name.lower()
        self.params = params
        self.verbose = verbose
        training_data, testing_data = dataset.split({'train':50,  'test':50})
        self.training_instances = load_dataset(training_data)
        self.testing_instances = load_dataset(testing_data)
        self.learner = None
        self.attack_learner = None
        self.dp_learner = None
        self.attacker = None
        self.attack_instances = None
        self.training_pred_labels = None
        self.testing_pred_labels = None
        self.attack_training_pred_labels = None
        self.attack_testing_pred_labels = None
        self.dp_learner_training_pred_labels = None
        self.dp_learner_testing_pred_labels = None
        self.labels = []
        for inst in self.training_instances + self.testing_instances:
            self.labels.append(inst.get_label())

        self.results = []

    def test(self):
        if self.verbose:
            print('\n###################################################################')
            print('START', self.learner_names[0] if len(self.learner_names) == 1 else 'learner', 'test.\n')
        self._setup()
        self._attack()
        self._retrain()
        for name in self.learner_names:
            begin = time.time()
            self._run_learner(name)
            end = time.time()
            result = (
             list(self.labels),
             list(self.training_pred_labels) + list(self.testing_pred_labels),
             list(self.attack_training_pred_labels) + list(self.attack_testing_pred_labels),
             list(self.dp_learner_training_pred_labels) + list(self.dp_learner_testing_pred_labels),
             end - begin)
            self.results.append(result)

        if self.verbose:
            print('\nEND', self.learner_names[0] if len(self.learner_names) == 1 else 'learner', 'test.')
            print('###################################################################\n')
        if len(self.results) == 1:
            return self.results[0]
        return self.results

    def _setup(self):
        if self.verbose:
            print('Training sample size: ', (len(self.training_instances)), '/400\n', sep='')
        learning_model = svm.SVC(probability=True, kernel='linear')
        self.learner = SimpleLearner(learning_model, self.training_instances)
        self.learner.train()
        self.training_pred_labels = self.learner.predict(self.training_instances)
        self.testing_pred_labels = self.learner.predict(self.testing_instances)

    def _attack(self):
        if self.attacker_name == 'label-flipping':
            cost = list(np.random.binomial(2, 0.5, len(self.training_instances)))
            total_cost = 40
            if self.params:
                self.attacker = LabelFlipping((deepcopy(self.learner)), **self.params)
            else:
                self.attacker = LabelFlipping((deepcopy(self.learner)), cost, total_cost, verbose=(self.verbose))
        elif self.attacker_name == 'k-insertion':
            self.attacker = KInsertion((deepcopy(self.learner)), (self.training_instances[0]),
              number_to_add=50,
              verbose=(self.verbose))
        else:
            if self.attacker_name == 'data-modification':
                target_theta = calculate_target_theta(deepcopy(self.learner), deepcopy(self.training_instances), deepcopy(self.testing_instances))
                self.attacker = DataModification((deepcopy(self.learner)), target_theta, verbose=(self.verbose))
            else:
                num_instances = len(self.training_instances)

                class DummyAttacker:

                    def attack(self, instances):
                        attack_instances = deepcopy(instances)
                        tmp = np.random.binomial(1, 0.2, num_instances)
                        for i, val in enumerate(tmp):
                            if val == 1:
                                attack_instances[i].set_label(attack_instances[i].get_label() * -1)

                        print('Poisoned instances: ', (sum(tmp)), '/', num_instances, sep='')
                        print('Unpoisoned instances: ', (num_instances - sum(tmp)), '/', num_instances, sep='')
                        return attack_instances

                self.attacker = DummyAttacker()
        if self.verbose:
            print('\n###################################################################')
            print('START', self.attacker_name, 'attack.\n')
        elif self.attacker_name == 'data-modification':
            self.attack_instances = self.attacker.attack(deepcopy(self.training_instances[:40]))
            self.attack_instances += deepcopy(self.training_instances[:-160])
        else:
            self.attack_instances = self.attacker.attack(deepcopy(self.training_instances))
        if self.verbose:
            print('\nEND', self.attacker_name, 'attack.')
            print('###################################################################\n')

    def _retrain(self):
        learning_model = svm.SVC(probability=True, kernel='linear')
        self.attack_learner = SimpleLearner(learning_model, self.attack_instances)
        self.attack_learner.train()
        self.attack_training_pred_labels = self.attack_learner.predict(self.training_instances)
        self.attack_testing_pred_labels = self.attack_learner.predict(self.testing_instances)

    def _run_learner(self, name):
        if self.verbose:
            print('\n###################################################################')
            print('START ', name, '.\n', sep='')
        elif name == 'TRIM Learner':
            self.dp_learner = TRIMLearner((deepcopy(self.attack_instances)), (int(len(self.attack_instances) * 0.8)),
              verbose=(self.verbose))
        else:
            if name == 'Alternating TRIM Learner':
                self.dp_learner = AlternatingTRIMLearner((deepcopy(self.attack_instances)), verbose=(self.verbose))
            else:
                if name == 'Iterative Retraining Learner':
                    self.dp_learner = IterativeRetrainingLearner((deepcopy(self.attack_instances)), verbose=(self.verbose))
                else:
                    self.dp_learner = OutlierRemovalLearner((deepcopy(self.attack_instances)), verbose=(self.verbose))
        self.dp_learner.train()
        if self.verbose:
            print('\nEND ', name, '.', sep='')
            print('###################################################################\n')
        self.dp_learner_training_pred_labels = self.dp_learner.predict(self.training_instances)
        self.dp_learner_testing_pred_labels = self.dp_learner.predict(self.testing_instances)


def test_dp_learners():
    if len(sys.argv) == 2 and sys.argv[1] in ('label-flipping', 'k-insertion', 'data-modification',
                                              'dummy'):
        attacker_name = sys.argv[1]
    else:
        attacker_name = 'dummy'
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    learners = [
     'trim', 'atrim', 'irl', 'outlier-removal']
    tester = TestDataPoisoningLearner(learners, attacker_name, dataset)
    results = tester.test()
    for i, tup in enumerate(results):
        report(tup, learners[i].upper())


if __name__ == '__main__':
    test_dp_learners()