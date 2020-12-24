# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/label_flipping_test.py
# Compiled at: 2018-07-20 16:31:15
# Size of source mod 2**32: 4230 bytes
from adlib.adversaries.label_flipping import LabelFlipping
from adlib.learners import SimpleLearner
from adlib.utils.common import calculate_correct_percentages
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from copy import deepcopy
from sklearn import svm
import numpy as np, time

def test_label_flipping():
    print()
    print('###################################################################')
    print('START label flipping attack.\n')
    begin = time.time()
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    training_data, predict_data = dataset.split({'train':25,  'test':75})
    training_data = load_dataset(training_data)
    predict_data = load_dataset(predict_data)
    print('Training sample size: ', (len(training_data)), '/400\n', sep='')
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, training_data)
    learner.train()
    orig_learner = deepcopy(learner)
    cost = list(np.random.binomial(2, 0.5, len(training_data)))
    total_cost = 0.3 * len(training_data)
    attacker = LabelFlipping(learner, cost, total_cost, verbose=True)
    attack_data = attacker.attack(training_data)
    flip_vector = []
    for i in range(len(attack_data)):
        if attack_data[i].get_label() != training_data[i].get_label():
            flip_vector.append(0)
        else:
            flip_vector.append(1)

    print('Flip vector with 0 -> flipped and 1 -> not flipped: \n', np.array(flip_vector), '\n')
    original_pred_labels = learner.predict(training_data)
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, attack_data)
    learner.train()
    attack_pred_labels = learner.predict(training_data)
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
    end = time.time()
    print('\nTotal time: ', (round(end - begin, 2)), 's', '\n', sep='')
    print('\nEND label flipping attack.')
    print('###################################################################')
    print()


if __name__ == '__main__':
    test_label_flipping()