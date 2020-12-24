# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/adversarial_learning_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1064 bytes
from adlib.adversaries.adversarial_learning import AdversarialLearning
from data_reader.dataset import EmailDataset
from data_reader.operations import load_dataset
from adlib.learners.simple_learner import SimpleLearner
from sklearn.linear_model import LinearRegression
dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False, raw=True)
training_, testing_ = dataset.split({'train':70,  'test':30})
training_data = load_dataset(training_)
testing_data = load_dataset(testing_)
learner_model = LinearRegression()
basic_learner = SimpleLearner(model=learner_model, training_instances=training_data)
basic_learner.train()
attacker = AdversarialLearning(threshold=10, learner=basic_learner)
attacker.set_adversarial_params(learner=basic_learner, training_instances=training_data)
attacked_instances = attacker.attack(testing_data)
predictions1 = basic_learner.predict(testing_data)
predictions2 = basic_learner.predict(attacked_instances)
print(predictions1, predictions2)