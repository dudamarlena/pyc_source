# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/real_input_cost_sensitive.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1120 bytes
from sklearn.naive_bayes import BernoulliNB
from adlib.learners import SimpleLearner
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from adlib.adversaries import CostSensitive
dataset = EmailDataset(path='.data_reader/data/raw/trec05p-1/full', binary=False, raw=True)
training_, testing_ = dataset.split({'train':60,  'test':40})
training_data = load_dataset(training_)
testing_data = load_dataset(testing_)
learning_model = BernoulliNB()
learner = SimpleLearner(learning_model, training_data)
learner.train()
param = {}
param['Ua'] = [
 [
  0, 20], [0, 0]]
param['Vi'] = 0
param['Uc'] = [[1, -1], [-10, 1]]
param['scenario'] = None
adversary = CostSensitive()
adversary.set_params(param)
adversary.set_adversarial_params(learner, training_data)
predictions1 = learner.predict(testing_data)
adversary.attack(testing_data)
predictions2 = learner.predict(testing_data)
val = [testing_data[i].label for i in range(len(testing_data))]
print(val)
print(predictions1)
print(predictions2)