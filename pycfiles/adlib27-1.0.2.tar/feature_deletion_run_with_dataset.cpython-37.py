# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/feature_deletion_run_with_dataset.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1280 bytes
import sys
from data_reader.operations import load_dataset
from sklearn import metrics
import adlib.learners as learner
from data_reader.dataset import EmailDataset
import matplotlib.pyplot as plt

def main(argv):
    """
    driver class that performs demo of the library
    """
    dataset = EmailDataset(path='../../data_reader/data/test/100_instance_debug.csv', raw=False)
    training_, testing_ = dataset.split({'train':60,  'test':40})
    training_data = load_dataset(training_)
    testing_data = load_dataset(testing_)
    clf2 = learner.FeatureDeletion(training_data, {'hinge_loss_multiplier':1,  'max_feature_deletion':30})
    clf2.train()
    y_predict = clf2.predict(testing_data[0])
    y_true = testing_data[0].label
    print(y_predict, y_true)
    score = metrics.accuracy_score([y_true], [y_predict])
    print('score = ' + str(score))
    wgt = clf2.decision_function()[0].tolist()[0]
    print(wgt)
    yaxis = [i for i in range(clf2.num_features)]
    plt.plot(yaxis, wgt)
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])