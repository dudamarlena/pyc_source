# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/good_word_400.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 2057 bytes
from sklearn import svm
from adlib.learners import SimpleLearner
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from adlib.adversaries.good_word import GoodWord
from sklearn import metrics

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
    return (
     ls, [x.label for x in ls])


dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=True, raw=True)
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
attacker = GoodWord(n=500)
attacker.set_adversarial_params(learner1, testing_data)
new_testing_data = attacker.attack(testing_data)
predictions2 = learner1.predict(new_testing_data)
print('========= post-attack prediction =========')
print('post attack preds' + str(predictions2))
print(type(predictions2).__name__)
print(type(test_true_label).__name__)
print('true label' + str(test_true_label))
print(summary(predictions2, test_true_label))