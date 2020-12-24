# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_multi_task_lstm_crf.py
# Compiled at: 2019-01-14 19:54:03
# Size of source mod 2**32: 9151 bytes
"""Any and all unit tests for the MultiTaskLSTMCRF (saber/models/multi_task_lstm_crf.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from keras.engine.training import Model
import pytest
from ..config import Config
from ..dataset import Dataset
from ..embeddings import Embeddings
from ..models.base_model import BaseKerasModel
from ..models.multi_task_lstm_crf import MultiTaskLSTMCRF
from .resources.dummy_constants import *

@pytest.fixture
def dummy_config():
    """Returns an instance of a Config object."""
    return Config(PATH_TO_DUMMY_CONFIG)


@pytest.fixture
def dummy_dataset_1():
    """Returns a single dummy Dataset instance after calling `Dataset.load()`.
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_1, replace_rare_tokens=False)
    dataset.load()
    return dataset


@pytest.fixture
def dummy_dataset_2():
    """Returns a single dummy Dataset instance after calling `Dataset.load()`.
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_2, replace_rare_tokens=False)
    dataset.load()
    return dataset


@pytest.fixture
def dummy_embeddings(dummy_dataset_1):
    """Returns an instance of an `Embeddings()` object AFTER the `.load()` method is called.
    """
    embeddings = Embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, token_map=(dummy_dataset_1.idx_to_tag))
    embeddings.load(binary=False)
    return embeddings


@pytest.fixture
def single_model(dummy_config, dummy_dataset_1, dummy_embeddings):
    """Returns an instance of MultiTaskLSTMCRF initialized with the default configuration."""
    model = MultiTaskLSTMCRF(config=dummy_config, datasets=[
     dummy_dataset_1],
      totally_arbitrary='arbitrary')
    return model


@pytest.fixture
def single_model_specify(single_model):
    """Returns an instance of MultiTaskLSTMCRF initialized with the default configuration file and
    a single specified model."""
    single_model.specify()
    return single_model


@pytest.fixture
def single_model_embeddings(dummy_config, dummy_dataset_1, dummy_embeddings):
    """Returns an instance of MultiTaskLSTMCRF initialized with the default configuration file and
    loaded embeddings"""
    model = MultiTaskLSTMCRF(config=dummy_config, datasets=[
     dummy_dataset_1],
      embeddings=dummy_embeddings,
      totally_arbitrary='arbitrary')
    return model


@pytest.fixture
def single_model_embeddings_specify(single_model_embeddings):
    """Returns an instance of MultiTaskLSTMCRF initialized with the default configuration file,
    loaded embeddings and single specified model."""
    single_model_embeddings.specify()
    return single_model_embeddings


def test_attributes_init_of_single_model(dummy_config, dummy_dataset_1, single_model):
    """Asserts instance attributes are initialized correctly when single `MultiTaskLSTMCRF` model is
    initialized without embeddings (`embeddings` attribute is None.)
    """
    @py_assert2 = (
     MultiTaskLSTMCRF, BaseKerasModel)
    @py_assert4 = isinstance(single_model, @py_assert2)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = single_model.config
    @py_assert3 = @py_assert1 is dummy_config
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config)) % {'py0':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = single_model.datasets[0]
    @py_assert2 = @py_assert0 is dummy_dataset_1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, dummy_dataset_1)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dummy_dataset_1) if 'dummy_dataset_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dataset_1) else 'dummy_dataset_1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = single_model.embeddings
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.embeddings\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = single_model.models
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.models\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = single_model.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_attributes_init_of_single_model_specify(dummy_config, dummy_dataset_1, single_model_specify):
    """Asserts instance attributes are initialized correctly when single `MultiTaskLSTMCRF`
    model is initialized without embeddings (`embeddings` attribute is None) and
    `MultiTaskLSTMCRF.specify()` has been called.
    """
    @py_assert2 = (
     MultiTaskLSTMCRF, BaseKerasModel)
    @py_assert4 = isinstance(single_model_specify, @py_assert2)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model_specify) if 'single_model_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_specify) else 'single_model_specify',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = single_model_specify.config
    @py_assert3 = @py_assert1 is dummy_config
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config)) % {'py0':@pytest_ar._saferepr(single_model_specify) if 'single_model_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_specify) else 'single_model_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = single_model_specify.datasets[0]
    @py_assert2 = @py_assert0 is dummy_dataset_1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, dummy_dataset_1)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dummy_dataset_1) if 'dummy_dataset_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dataset_1) else 'dummy_dataset_1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = single_model_specify.embeddings
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.embeddings\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model_specify) if 'single_model_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_specify) else 'single_model_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = [isinstance(model, Model) for model in single_model_specify.models]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = single_model_specify.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model_specify) if 'single_model_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_specify) else 'single_model_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_attributes_init_of_single_model_embeddings(dummy_config, dummy_dataset_1, dummy_embeddings, single_model_embeddings):
    """Asserts instance attributes are initialized correctly when single `MultiTaskLSTMCRF` model is
    initialized with embeddings (`embeddings` attribute is not None.)
    """
    @py_assert2 = (
     MultiTaskLSTMCRF, BaseKerasModel)
    @py_assert4 = isinstance(single_model_embeddings, @py_assert2)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = single_model_embeddings.config
    @py_assert3 = @py_assert1 is dummy_config
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config)) % {'py0':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = single_model_embeddings.datasets[0]
    @py_assert2 = @py_assert0 is dummy_dataset_1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, dummy_dataset_1)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dummy_dataset_1) if 'dummy_dataset_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dataset_1) else 'dummy_dataset_1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = single_model_embeddings.embeddings
    @py_assert3 = @py_assert1 is dummy_embeddings
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.embeddings\n} is %(py4)s', ), (@py_assert1, dummy_embeddings)) % {'py0':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_embeddings) if 'dummy_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings) else 'dummy_embeddings'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = single_model_embeddings.models
    @py_assert4 = []
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.models\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = single_model_embeddings.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_attributes_init_of_single_model_embeddings_specify(dummy_config, dummy_dataset_1, dummy_embeddings, single_model_embeddings_specify):
    """Asserts instance attributes are initialized correctly when single MultiTaskLSTMCRF
    model is initialized with embeddings (`embeddings` attribute is not None) and
    `MultiTaskLSTMCRF.specify()` has been called.
    """
    @py_assert2 = (
     MultiTaskLSTMCRF, BaseKerasModel)
    @py_assert4 = isinstance(single_model_embeddings_specify, @py_assert2)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model_embeddings_specify) if 'single_model_embeddings_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings_specify) else 'single_model_embeddings_specify',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert1 = single_model_embeddings_specify.config
    @py_assert3 = @py_assert1 is dummy_config
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config)) % {'py0':@pytest_ar._saferepr(single_model_embeddings_specify) if 'single_model_embeddings_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings_specify) else 'single_model_embeddings_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = single_model_embeddings_specify.datasets[0]
    @py_assert2 = @py_assert0 is dummy_dataset_1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, dummy_dataset_1)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(dummy_dataset_1) if 'dummy_dataset_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dataset_1) else 'dummy_dataset_1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = single_model_embeddings_specify.embeddings
    @py_assert3 = @py_assert1 is dummy_embeddings
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.embeddings\n} is %(py4)s', ), (@py_assert1, dummy_embeddings)) % {'py0':@pytest_ar._saferepr(single_model_embeddings_specify) if 'single_model_embeddings_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings_specify) else 'single_model_embeddings_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_embeddings) if 'dummy_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_embeddings) else 'dummy_embeddings'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [isinstance(model, Model) for model in single_model_embeddings_specify.models]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = single_model_embeddings_specify.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(single_model_embeddings_specify) if 'single_model_embeddings_specify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings_specify) else 'single_model_embeddings_specify',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_prepare_data_for_training(dummy_dataset_1, single_model):
    """Assert that the values returned from call to `BaseKerasModel.prepare_data_for_training()` are
    as expected.
    """
    training_data = single_model.prepare_data_for_training()
    partitions = ['x_train', 'y_train', 'x_valid', 'y_valid', 'x_test', 'y_test']
    @py_assert1 = (partition in data for data in training_data for partition in partitions)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (data['x_train'] == [dummy_dataset_1.idx_seq['train']['word'], dummy_dataset_1.idx_seq['train']['char']] for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (data['x_valid'] == [dummy_dataset_1.idx_seq['valid']['word'], dummy_dataset_1.idx_seq['valid']['char']] for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (data['x_test'] == [dummy_dataset_1.idx_seq['test']['word'], dummy_dataset_1.idx_seq['test']['char']] for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (np.array_equal(data['y_train'], dummy_dataset_1.idx_seq['train']['tag']) for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (np.array_equal(data['y_valid'], dummy_dataset_1.idx_seq['valid']['tag']) for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = (np.array_equal(data['y_test'], dummy_dataset_1.idx_seq['test']['tag']) for data in training_data)
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_crf_after_transfer(single_model_specify, dummy_dataset_2):
    """Asserts that the CRF output layer of a model is replaced with a new layer when
    `MultiTaskLSTMCRF.prepare_for_transfer()` is called by testing that the `name` attribute
    of the final layer.
    """
    test_model = single_model_specify
    expected_before_transfer = [
     'crf_classifier']
    actual_before_transfer = [model.layers[(-1)].name for model in test_model.models]
    test_model.prepare_for_transfer([dummy_dataset_2])
    expected_after_transfer = ['target_crf_classifier']
    actual_after_transfer = [model.layers[(-1)].name for model in test_model.models]
    @py_assert1 = actual_before_transfer == expected_before_transfer
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_before_transfer, expected_before_transfer)) % {'py0':@pytest_ar._saferepr(actual_before_transfer) if 'actual_before_transfer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_before_transfer) else 'actual_before_transfer',  'py2':@pytest_ar._saferepr(expected_before_transfer) if 'expected_before_transfer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_before_transfer) else 'expected_before_transfer'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = actual_after_transfer == expected_after_transfer
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual_after_transfer, expected_after_transfer)) % {'py0':@pytest_ar._saferepr(actual_after_transfer) if 'actual_after_transfer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_after_transfer) else 'actual_after_transfer',  'py2':@pytest_ar._saferepr(expected_after_transfer) if 'expected_after_transfer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_after_transfer) else 'expected_after_transfer'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None