# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_base_model.py
# Compiled at: 2019-01-14 19:54:23
# Size of source mod 2**32: 4413 bytes
"""Any and all unit tests for the BaseKerasModel (saber/models/base_model.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from ..config import Config
from ..dataset import Dataset
from ..embeddings import Embeddings
from ..models.base_model import BaseKerasModel
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
    model = BaseKerasModel(config=dummy_config, datasets=[
     dummy_dataset_1],
      totally_arbitrary='arbitrary')
    return model


@pytest.fixture
def single_model_embeddings(dummy_config, dummy_dataset_1, dummy_embeddings):
    """Returns an instance of MultiTaskLSTMCRF initialized with the default configuration file and
    loaded embeddings"""
    model = BaseKerasModel(config=dummy_config, datasets=[
     dummy_dataset_1],
      embeddings=dummy_embeddings,
      totally_arbitrary='arbitrary')
    return model


def test_compile_value_error(single_model):
    """Asserts that `BaseKerasModel._compile()` returns a ValueError when an invalid argument for
    `optimizer` is passed.
    """
    with pytest.raises(ValueError):
        single_model._compile('arbitrary', 'arbitrary', 'invalid')


def test_attributes_init_of_single_model(dummy_config, dummy_dataset_1, single_model):
    """Asserts instance attributes are initialized correctly when single `MultiTaskLSTMCRF` model is
    initialized without embeddings (`embeddings` attribute is None.)
    """
    @py_assert3 = isinstance(single_model, BaseKerasModel)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model) if 'single_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model) else 'single_model',  'py2':@pytest_ar._saferepr(BaseKerasModel) if 'BaseKerasModel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BaseKerasModel) else 'BaseKerasModel',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
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


def test_attributes_init_of_single_model_embeddings(dummy_config, dummy_dataset_1, dummy_embeddings, single_model_embeddings):
    """Asserts instance attributes are initialized correctly when single `MultiTaskLSTMCRF` model is
    initialized with embeddings (`embeddings` attribute is not None.)
    """
    @py_assert3 = isinstance(single_model_embeddings, BaseKerasModel)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(single_model_embeddings) if 'single_model_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(single_model_embeddings) else 'single_model_embeddings',  'py2':@pytest_ar._saferepr(BaseKerasModel) if 'BaseKerasModel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BaseKerasModel) else 'BaseKerasModel',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
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