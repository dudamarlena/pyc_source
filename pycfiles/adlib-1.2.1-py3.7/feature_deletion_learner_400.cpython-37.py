# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/feature_deletion_learner_400.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 5689 bytes
from sklearn import svm
from adlib.learners import SimpleLearner
import adlib.learners as learner
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from adlib.learners.feature_deletion import FeatureDeletion
from adlib.adversaries.feature_deletion import AdversaryFeatureDeletion
from sklearn import metrics
import numpy as np
from matplotlib import pyplot as plt

def summary(y_pred, y_true):
    if len(y_pred) != len(y_true):
        raise ValueError('lengths of two label lists do not match')
    acc = metrics.accuracy_score(y_true, y_pred)
    prec = metrics.precision_score(y_true, y_pred)
    rec = metrics.recall_score(y_true, y_pred)
    return 'accuracy: {0} \n precision: {1} \n recall: {2}\n'.format(acc, prec, rec)


def get_evasion_set(x_test, y_pred):
    ls = [x for x, y in zip(x_test, y_pred) if x.label == 1 if y == 1]
    print('{0} malicious instances are being detected initially')
    return (ls, [x.label for x in ls])


dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False, raw=True)
training_, testing_ = dataset.split({'train':60,  'test':40})
training_data = load_dataset(training_)
testing_data = load_dataset(testing_)
test_true_label = [x.label for x in testing_data]
learning_model = svm.SVC(probability=True, kernel='linear')
learner1 = SimpleLearner(learning_model, training_data)
learner1.train()
predictions = learner1.predict(testing_data)
print('======== initial prediction =========')
print(summary(predictions, test_true_label))
attacker = AdversaryFeatureDeletion(num_deletion=40, all_malicious=True)
attacker.set_adversarial_params(learner1, None)
new_testing_data = attacker.attack(testing_data)
w = learner1.model.learner.coef_[0]
b = learner1.model.learner.intercept_[0]
xaxis = range(len(w))
print('verbose prediction')
init_pred_val, init_pred_label = [0] * len(testing_data), [0] * len(testing_data)
atk_pred_val, atk_pred_label = [0] * len(testing_data), [0] * len(testing_data)
predictions2 = learner1.predict(new_testing_data)
print('========= post-attack prediction =========')
print(summary(predictions2, test_true_label))
for idx, (p1, p2) in enumerate(zip(init_pred_label, atk_pred_label)):
    if p1 != p2:
        print('Instance {} has successfully evaded, pre-attack value: {}, post attack: {}'.format(idx, init_pred_val[idx], atk_pred_val[idx]))

learner2 = FeatureDeletion(training_data, params={'hinge_loss_multiplier':20,  'max_feature_deletion':10})
learner2.train()
w2 = learner2.get_weight()[0]
b2 = learner2.get_constant()
print('training robust learner...')
print('initial b = {}'.format(b))
print('new b = {}'.format(b2))
f, axarr = plt.subplots(2, sharey=False)
axarr[0].plot(xaxis, w)
axarr[1].plot(xaxis, w2)
plt.show()
print('========= robust learner post-attack prediction =========')
pred3 = learner2.predict(new_testing_data)
print('true labels')
print(test_true_label)
print('predictions')
print(pred3)
print('number of new prediction: ' + str(len(pred3)))
print(summary(pred3, test_true_label))