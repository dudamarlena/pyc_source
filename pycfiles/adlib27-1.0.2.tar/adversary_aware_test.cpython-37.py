# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/adversary_aware_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1247 bytes
from adlib.adversaries.cost_sensitive import CostSensitive
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from adlib.learners.adversary_aware import AdversaryAware
from adlib.learners.simple_learner import SimpleLearner
from sklearn.naive_bayes import GaussianNB
dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False, raw=True)
training_, testing_ = dataset.split({'train':60,  'test':40})
training_data = load_dataset(training_)
testing_data = load_dataset(testing_)
learner_model = GaussianNB()
basic_learner = SimpleLearner(model=learner_model, training_instances=training_data)
basic_learner.train()
attacker = CostSensitive(binary=False)
param = {}
param['Ua'] = [[0, 20], [0, 0]]
param['Vi'] = 0
param['Uc'] = [[1, -1], [-10, 1]]
param['scenario'] = None
attacker.set_params(param)
attacker.set_adversarial_params(learner=basic_learner, training_instances=training_data)
learner = AdversaryAware(attacker=attacker, training_instances=training_data)
learner.train()
print(learner.get_params())
print(learner.predict(testing_data))