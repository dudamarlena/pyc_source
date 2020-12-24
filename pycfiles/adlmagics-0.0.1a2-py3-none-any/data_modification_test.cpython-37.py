# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/data_modification_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 6330 bytes
from adlib.learners import SimpleLearner
from adlib.adversaries.datamodification.data_modification import DataModification
from adlib.utils.common import calculate_correct_percentages
from adlib.utils.common import get_spam_features
from copy import deepcopy
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from sklearn import svm
import numpy as np, time

def test_data_modification():
    print()
    print('###################################################################')
    print('START data modification attack.\n')
    begin = time.time()
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    training_data, predict_data = dataset.split({'train':50,  'test':50})
    training_data = load_dataset(training_data)
    predict_data = load_dataset(predict_data)
    print('Training sample size: ', (len(training_data)), '/400\n', sep='')
    orig_learning_model = svm.SVC(probability=True, kernel='linear')
    orig_learner = SimpleLearner(orig_learning_model, training_data)
    orig_learner.train()
    target_theta = calculate_target_theta(orig_learner, training_data, predict_data)
    original_pred_labels = orig_learner.predict(training_data)
    attacker = DataModification(orig_learner, target_theta, verbose=True)
    attack_data = attacker.attack(training_data)
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
    spam_pred_labels = learner.predict(spam_instances)
    spam_ham_count = sum(map(lambda x:     if x == -1:
1 # Avoid dead code: 0, spam_pred_labels))
    print('###################################################################')
    print('Number of spam instances in original training set that were \n', 'classified as ham after the attack: ',
      spam_ham_count, '/', (len(spam_instances)),
      sep='')
    end = time.time()
    print('\nTotal time: ', (round(end - begin, 2)), 's', '\n', sep='')
    print('\nEND data modification attack.')
    print('###################################################################')
    print()


def calculate_target_theta(orig_learner, training_data, predict_data):
    lnr = orig_learner.model.learner
    eye = np.eye((training_data[0].get_feature_count()), dtype=int)
    orig_theta = lnr.decision_function(eye) - lnr.intercept_[0]
    target_theta = deepcopy(orig_theta)
    spam_instances = []
    for inst in training_data + predict_data:
        if inst.get_label() == 1:
            spam_instances.append(inst)

    spam_features, ham_features = get_spam_features(spam_instances)
    for index in spam_features:
        target_theta[index] = -1

    for index in ham_features:
        target_theta[index] = 1

    print('Features selected: ', np.array(spam_features))
    print('Number of features: ', len(spam_features))
    return target_theta


if __name__ == '__main__':
    test_data_modification()