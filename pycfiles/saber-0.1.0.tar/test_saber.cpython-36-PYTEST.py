# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_saber.py
# Compiled at: 2019-01-14 18:15:15
# Size of source mod 2**32: 12804 bytes
"""Any and all unit tests for the `Saber` class (saber/utils/saber.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from ..config import Config
from ..dataset import Dataset
from ..embeddings import Embeddings
from ..models.base_model import BaseKerasModel
from ..preprocessor import Preprocessor
from ..saber import MissingStepException, Saber
from .resources import helpers
from .resources.dummy_constants import *

@pytest.fixture
def dummy_config_single_dataset():
    """Returns instance of `Config` after parsing the dummy config file. Ensures that
    `replace_rare_tokens` argument is False.
    """
    return Config(PATH_TO_DUMMY_CONFIG)


@pytest.fixture
def dummy_dataset_1():
    """Returns a single dummy Dataset instance after calling Dataset.load().
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
def saber_blank(dummy_config_single_dataset):
    """Returns instance of `Saber` initialized with the dummy config file and no dataset.
    """
    return Saber(config=dummy_config_single_dataset, totally_arbitrary='arbitrary')


@pytest.fixture
def saber_single_dataset(dummy_config_single_dataset):
    """Returns instance of `Saber` initialized with the dummy config file and a single dataset.
    """
    saber = Saber(config=dummy_config_single_dataset)
    saber.load_dataset(directory=PATH_TO_DUMMY_DATASET_1)
    return saber


@pytest.fixture
def saber_single_dataset_embeddings(dummy_config_single_dataset):
    """Returns instance of `Saber` initialized with the dummy config file, a single dataset and
    embeddings.
    """
    saber = Saber(config=dummy_config_single_dataset)
    saber.load_dataset(directory=PATH_TO_DUMMY_DATASET_1)
    saber.load_embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, binary=False)
    return saber


@pytest.fixture
def saber_single_dataset_model(dummy_config_single_dataset):
    """Returns an instance of `Saber` initialized with the dummy config file, a single dataset
    a Keras model."""
    saber = Saber(config=dummy_config_single_dataset)
    saber.load_dataset(directory=PATH_TO_DUMMY_DATASET_1)
    saber.build()
    return saber


@pytest.fixture
def dummy_config_compound_dataset():
    """Returns an instance of a `Config` after parsing the dummy config file. Ensures that
    `replace_rare_tokens` argument is False.
    """
    compound_dataset = [
     PATH_TO_DUMMY_DATASET_1, PATH_TO_DUMMY_DATASET_2]
    cli_arguments = {'dataset_folder': compound_dataset}
    dummy_config = Config(PATH_TO_DUMMY_CONFIG)
    dummy_config.harmonize_args(cli_arguments)
    return dummy_config


@pytest.fixture
def saber_compound_dataset(dummy_config_compound_dataset):
    """Returns an instance of `Saber` initialized with the dummy config file and a compound dataset.
    The compound dataset is just two copies of the dataset, this makes writing tests much
    simpler.
    """
    compound_dataset = [
     PATH_TO_DUMMY_DATASET_1, PATH_TO_DUMMY_DATASET_1]
    saber = Saber(config=dummy_config_compound_dataset)
    saber.load_dataset(directory=compound_dataset)
    return saber


@pytest.fixture
def saber_compound_dataset_model(dummy_config_compound_dataset):
    """Returns an instance of `Saber` initialized with the dummy config file, a single dataset
    a Keras model."""
    saber = Saber(config=dummy_config_compound_dataset)
    saber.load_dataset(directory=[PATH_TO_DUMMY_DATASET_1, PATH_TO_DUMMY_DATASET_2])
    saber.build()
    return saber


def test_attributes_after_initilization_of_model(saber_blank, dummy_config_single_dataset):
    """Asserts instance attributes are initialized correctly when `Saber` object is created.
    """
    @py_assert1 = saber_blank.config
    @py_assert3 = @py_assert1 is dummy_config_single_dataset
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config_single_dataset)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config_single_dataset) if 'dummy_config_single_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config_single_dataset) else 'dummy_config_single_dataset'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = saber_blank.preprocessor
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.preprocessor\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = saber_blank.datasets
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.datasets\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = saber_blank.embeddings
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.embeddings\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = saber_blank.model
    @py_assert4 = None
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.model\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = saber_blank.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(saber_blank) if 'saber_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_blank) else 'saber_blank',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_load_single_dataset(saber_single_dataset):
    """Assert that the `datasets` attribute of a `Saber` instance was updated as expected after
    call to `Saber.load_dataset()` when a single dataset was provided.
    """
    @py_assert1 = [isinstance(ds, Dataset) for ds in saber_single_dataset.datasets]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_load_dataset_value_error(saber_single_dataset):
    """Asserts that `Saber` object raises a ValueError when we try to load a dataset but have
    not specified a path to that dataset (`Saber.config.dataset_folder` is False).
    """
    saber_single_dataset.config.dataset_folder = ''
    with pytest.raises(ValueError):
        saber_single_dataset.load_dataset()


def test_tag_to_idx_after_load_single_dataset_with_transfer(dummy_dataset_2, saber_single_dataset_model):
    """Asserts that `saber.datasets[0].type_to_idx['tag']` is unchanged after we load a single
    target dataset for transfer learning.
    """
    expected = dummy_dataset_2.type_to_idx['tag']
    saber_single_dataset_model.load_dataset(PATH_TO_DUMMY_DATASET_2)
    actual = saber_single_dataset_model.datasets[0].type_to_idx['tag']
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_load_embeddings(saber_single_dataset_embeddings):
    """Assert that the `embeddings` attribute of a `Saber` instance was updated as expected after
    call to `Saber.load_embeddings()`
    """
    @py_assert2 = saber_single_dataset_embeddings.embeddings
    @py_assert5 = isinstance(@py_assert2, Embeddings)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.embeddings\n}, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(saber_single_dataset_embeddings) if 'saber_single_dataset_embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_single_dataset_embeddings) else 'saber_single_dataset_embeddings',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(Embeddings) if 'Embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Embeddings) else 'Embeddings',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None


def test_load_embeddings_with_load_all(saber_single_dataset):
    """Assert that the `datasets` and `embeddings` attributes of a `Saber` instance are updated as
    expected after call to `Saber.load_embeddings()`
    """
    dataset = saber_single_dataset.datasets[0]
    word_types, char_types = list(dataset.type_to_idx['word']), list(dataset.type_to_idx['char'])
    expected = {'word':Preprocessor.type_to_idx(word_types, DUMMY_TOKEN_MAP),  'char':Preprocessor.type_to_idx(char_types, DUMMY_CHAR_MAP)}
    saber_single_dataset.load_embeddings(filepath=PATH_TO_DUMMY_EMBEDDINGS, binary=False,
      load_all=True)
    helpers.assert_type_to_idx_as_expected(dataset.type_to_idx, expected)
    @py_assert2 = saber_single_dataset.embeddings
    @py_assert5 = isinstance(@py_assert2, Embeddings)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.embeddings\n}, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(saber_single_dataset) if 'saber_single_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_single_dataset) else 'saber_single_dataset',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(Embeddings) if 'Embeddings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Embeddings) else 'Embeddings',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None


def test_load_embeddings_missing_step_exception(saber_blank):
    """Asserts that `Saber` object raises a MissingStepException when we try to load embeddings
    without first loading a dataset (`Saber.datasets` is None).
    """
    with pytest.raises(MissingStepException):
        saber_blank.load_embeddings()


def test_load_embeddings_value_error(saber_single_dataset):
    """Asserts that `Saber` object raises a ValueError when we try to load embeddings but have
    not specified a filepath to those embeddings (`Saber.config.pretrained_embeddings` is False).
    """
    saber_single_dataset.config.pretrained_embeddings = ''
    with pytest.raises(ValueError):
        saber_single_dataset.load_embeddings()


def test_build_single_dataset(saber_single_dataset_model):
    """Assert that the `model` attribute of a `Saber` instance was updated as expected after
    call to `Saber.build()` when single dataset was loaded.
    """
    @py_assert2 = saber_single_dataset_model.model
    @py_assert5 = isinstance(@py_assert2, BaseKerasModel)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.model\n}, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(saber_single_dataset_model) if 'saber_single_dataset_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_single_dataset_model) else 'saber_single_dataset_model',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(BaseKerasModel) if 'BaseKerasModel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BaseKerasModel) else 'BaseKerasModel',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None


def test_build_missing_step_exception(saber_blank):
    """Asserts that `Saber` object raises a MissingStepException when we try to build the model
    without first loading a dataset (`Saber.datasets` is None).
    """
    with pytest.raises(MissingStepException):
        saber_blank.build()


def test_build_value_error(saber_single_dataset):
    """Asserts that `Saber` object raises a ValueError when we try to load a model with an invalid
    name (i.e. `Saber.config.model_name` is not in `constants.MODEL_NAMES`).
    """
    model_name = 'this is not valid'
    with pytest.raises(ValueError):
        saber_single_dataset.build(model_name)


def test_train_no_dataset_missing_step_exception(saber_blank):
    """Asserts that `Saber` object raises a MissingStepException when we try to train the model
    without first loading a dataset (`Saber.datasets` is None).
    """
    with pytest.raises(MissingStepException):
        saber_blank.train()


def test_train_no_model_missing_step_exception(saber_single_dataset):
    """Asserts that `Saber` object raises a MissingStepException when we try to train the model
    without first building the model (`Saber.model` is None).
    """
    with pytest.raises(MissingStepException):
        saber_single_dataset.train()


def test_annotate_single(saber_single_dataset_model):
    """Asserts that call to `Saber.annotate()` returns the expected results with a single dataset
    loaded."""
    test = 'This is a simple test. With multiple sentences'
    expected = {'text':test,  'ents':[]}
    actual = saber_single_dataset_model.annotate(test)
    actual['ents'] = []
    @py_assert1 = expected == actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_predict_blank_or_invalid(saber_single_dataset_model):
    """Asserts that call to `Saber.predict()` raises a ValueError when a falsy text argument
    is passed."""
    blank_text_test = ''
    none_test = None
    empty_list_test = []
    false_bool_test = False
    with pytest.raises(ValueError):
        saber_single_dataset_model.annotate(blank_text_test)
    with pytest.raises(ValueError):
        saber_single_dataset_model.annotate(none_test)
    with pytest.raises(ValueError):
        saber_single_dataset_model.annotate(empty_list_test)
    with pytest.raises(ValueError):
        saber_single_dataset_model.annotate(false_bool_test)


def test_load_compound_dataset(saber_compound_dataset):
    """Assert that the `datasets` attribute of a `Saber` instance was updated as expected after
    call to `Saber.load_dataset()` when a compound dataset was provided.
    """
    @py_assert1 = [isinstance(ds, Dataset) for ds in saber_compound_dataset.datasets]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_tag_to_idx_after_load_compound_dataset_with_transfer(dummy_dataset_1, dummy_dataset_2, saber_single_dataset_model):
    """Asserts that `type_to_idx['tag']` is unchanged after we load a compound target dataset for
    transfer learning.
    """
    expected = [
     dummy_dataset_1.type_to_idx['tag'],
     dummy_dataset_2.type_to_idx['tag']]
    saber_compound_dataset_model = saber_single_dataset_model
    saber_compound_dataset_model.load_dataset([PATH_TO_DUMMY_DATASET_1, PATH_TO_DUMMY_DATASET_2])
    actual = [ds.type_to_idx['tag'] for ds in saber_compound_dataset_model.datasets]
    for i, result in enumerate(actual):
        @py_assert2 = expected[i]
        @py_assert1 = result == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_build_compound_dataset(saber_compound_dataset_model):
    """Assert that the `model` attribute of a `Saber` instance was updated as expected after
    call to `Saber.build()` when compound dataset was loaded.
    """
    @py_assert2 = saber_compound_dataset_model.model
    @py_assert5 = isinstance(@py_assert2, BaseKerasModel)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.model\n}, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(saber_compound_dataset_model) if 'saber_compound_dataset_model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(saber_compound_dataset_model) else 'saber_compound_dataset_model',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(BaseKerasModel) if 'BaseKerasModel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BaseKerasModel) else 'BaseKerasModel',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None