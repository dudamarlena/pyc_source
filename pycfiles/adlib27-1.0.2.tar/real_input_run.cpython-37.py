# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/real_input_run.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 992 bytes
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from random import seed
from adlib.learners.svm_restrained import SVMRestrained
dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False, raw=True)
seed(1)
training_, testing_ = dataset.split({'train':60,  'test':40})
training_data = load_dataset(training_)
testing_data = load_dataset(testing_)
learner = SVMRestrained({'c_f':0.7,  'xmin':0.25,  'xmax':0.75}, training_data)
learner.train()
predictions = learner.predict(testing_data)
print(predictions)
print([testing_data[i].label for i in range(len(testing_data))])
pre_proba = learner.predict_proba(testing_data)
print(pre_proba)