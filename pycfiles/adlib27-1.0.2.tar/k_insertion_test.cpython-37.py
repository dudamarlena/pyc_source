# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/k_insertion_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 5257 bytes
from adlib.adversaries.k_insertion import KInsertion
from adlib.learners import SimpleLearner
from adlib.utils.common import calculate_correct_percentages
from copy import deepcopy
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from sklearn import svm
import sys, time

def test_k_insertion():
    """
    Use as follows:
    python3 adlib/tests/adversaries/k_insertion_test.py NUMBER-TO-ADD
    """
    print()
    print('###################################################################')
    print('START k-insertion attack.\n')
    begin = time.time()
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    training_data, predict_data = dataset.split({'train':20,  'test':80})
    training_data = load_dataset(training_data)
    predict_data = load_dataset(predict_data)
    print('Training sample size: ', (len(training_data)), '/400\n', sep='')
    if len(sys.argv) > 2:
        number_to_add = int(sys.argv[1])
    else:
        number_to_add = int(0.25 * len(training_data))
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, training_data)
    learner.train()
    original_pred_labels = learner.predict(training_data)
    before_attack_label = original_pred_labels[0]
    orig_learner = deepcopy(learner)
    attacker = KInsertion(learner, (training_data[0]),
      number_to_add=number_to_add,
      verbose=True)
    attack_data = attacker.attack(training_data)
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, attack_data)
    learner.train()
    print('Number of added instances: ', len(attack_data) - len(training_data))
    attack_pred_labels = learner.predict(training_data)
    after_attack_label = attack_pred_labels[0]
    orig_precent_correct, attack_precent_correct, difference = calculate_correct_percentages(original_pred_labels, attack_pred_labels, training_data)
    print('###################################################################')
    print('Predictions with training dataset:')
    print('Original correct percentage: ', orig_precent_correct, '%')
    print('Attack correct percentage: ', attack_precent_correct, '%')
    print('Difference: ', difference, '%')
    original_pred_labels = orig_learner.predict(predict_data)
    attack_pred_labels = learner.predict(predict_data)
    orig_precent_correct, attack_precent_correct, difference = calculate_correct_percentages(original_pred_labels, attack_pred_labels, predict_data)
    print('###################################################################')
    print('Predictions with other half of dataset:')
    print('Original correct percentage: ', orig_precent_correct, '%')
    print('Attack correct percentage: ', attack_precent_correct, '%')
    print('Difference: ', difference, '%')
    print('###################################################################')
    print('Selected instance true label: ', training_data[0].get_label())
    print('Selected instance predicted label BEFORE attack: ', before_attack_label)
    print('Selected instance predicted label AFTER attack: ', after_attack_label)
    print('###################################################################')
    print('poison_instance loss before attack: ', round(attacker.poison_loss_before, 4))
    print('poison_instance loss after attack: ', round(attacker.poison_loss_after, 4))
    print('poison_instance loss difference: ', round(attacker.poison_loss_after - attacker.poison_loss_before, 4))
    end = time.time()
    print('\nTotal time: ', (round(end - begin, 2)), 's', '\n', sep='')
    print('\nEND k-insertion attack.')
    print('###################################################################')
    print()


if __name__ == '__main__':
    test_k_insertion()