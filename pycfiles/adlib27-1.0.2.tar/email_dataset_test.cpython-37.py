# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/datasets/email_dataset_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1956 bytes
import pytest
from random import seed
from data_reader.dataset import EmailDataset
from adlib.learners.simple_learner import SimpleLearner
from sklearn import svm

@pytest.fixture
def data():
    dataset = EmailDataset(path='./data_reader/data/test/100_instance_debug.csv', raw=False)
    seed(1)
    training_data, testing_data = dataset.split({'train':60,  'test':40})
    return {'training_data':training_data, 
     'testing_data':testing_data}


@pytest.fixture
def training_data(data):
    return data['training_data']


@pytest.fixture
def testing_data(data):
    return data['testing_data']


@pytest.fixture
def simple_learner(data):
    learning_model = svm.SVC(probability=True, kernel='linear')
    learner = SimpleLearner(learning_model, data['training_data'])
    return learner


@pytest.fixture
def empty_learner():
    return SimpleLearner()


def bad_dataset_params1():
    with pytest.raises(AttributeError) as (error):
        dataset = EmailDataset(raw=False)


def bad_dataset_params2():
    with pytest.raises(AttributeError) as (error):
        dataset = EmailDataset(raw=True)


def bad_dataset_params3():
    with pytest.raises(AttributeError) as (error):
        dataset = EmailDataset(path='notarealpath.pkl', features=[1, 2, 3], labels=[
         1])


def load_serialized():
    feat_val = data['training'][0].toarray()[0][0]
    if not feat_val == 1.0:
        assert feat_val == 0.0
    label_val = data['training'][1][0]
    if not label_val == 1.0:
        assert label_val == -1.0


def test_predict_returns_binary_label(simple_learner, testing_data):
    simple_learner.train()
    result = simple_learner.predict(testing_data[0])
    assert result in [SimpleLearner.positive_classification, SimpleLearner.negative_classification]