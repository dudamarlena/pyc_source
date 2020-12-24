# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_metrics.py
# Compiled at: 2018-11-03 12:42:23
# Size of source mod 2**32: 3920 bytes
"""Any and all unit tests for the Metrics class (saber/metrics.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from .. import constants
from ..config import Config
from ..dataset import Dataset
from ..metrics import Metrics
from ..utils import model_utils
from .resources.dummy_constants import *
PATH_TO_METRICS_OUTPUT = 'totally/arbitrary'

@pytest.fixture
def dummy_config():
    """Returns an instance of a Config object."""
    dummy_config = Config(PATH_TO_DUMMY_CONFIG)
    return dummy_config


@pytest.fixture
def dummy_dataset():
    """Returns a single dummy Dataset instance after calling Dataset.load().
    """
    dataset = Dataset(directory=PATH_TO_DUMMY_DATASET_1, replace_rare_tokens=False)
    dataset.load()
    return dataset


@pytest.fixture
def dummy_output_dir(tmpdir, dummy_config):
    """Returns list of output directories."""
    dummy_config.output_folder = tmpdir.strpath
    output_dirs = model_utils.prepare_output_directory(dummy_config)
    return output_dirs


@pytest.fixture
def dummy_training_data(dummy_dataset):
    """Returns training data from `dummy_dataset`.
    """
    training_data = {'x_train':[
      dummy_dataset.idx_seq['train']['word'],
      dummy_dataset.idx_seq['train']['char']], 
     'x_valid':None, 
     'x_test':None, 
     'y_train':dummy_dataset.idx_seq['train']['tag'], 
     'y_valid':None, 
     'y_test':None}
    return training_data


@pytest.fixture
def dummy_metrics(dummy_config, dummy_dataset, dummy_training_data, dummy_output_dir):
    """Returns an instance of Metrics.
    """
    metrics = Metrics(config=dummy_config, training_data=dummy_training_data,
      index_map=(dummy_dataset.idx_to_tag),
      output_dir=dummy_output_dir,
      totally_arbitrary='arbitrary')
    return metrics


def test_attributes_after_initilization(dummy_config, dummy_dataset, dummy_output_dir, dummy_training_data, dummy_metrics):
    """Asserts instance attributes are initialized correctly when Metrics object is initialized."""
    @py_assert1 = dummy_metrics.config
    @py_assert3 = @py_assert1 is dummy_config
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.config\n} is %(py4)s', ), (@py_assert1, dummy_config)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = dummy_metrics.training_data
    @py_assert3 = @py_assert1 is dummy_training_data
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.training_data\n} is %(py4)s', ), (@py_assert1, dummy_training_data)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_training_data) if 'dummy_training_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_training_data) else 'dummy_training_data'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = dummy_metrics.index_map
    @py_assert5 = dummy_dataset.idx_to_tag
    @py_assert3 = @py_assert1 is @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.index_map\n} is %(py6)s\n{%(py6)s = %(py4)s.idx_to_tag\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_dataset) if 'dummy_dataset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_dataset) else 'dummy_dataset',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = dummy_metrics.output_dir
    @py_assert3 = @py_assert1 == dummy_output_dir
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.output_dir\n} == %(py4)s', ), (@py_assert1, dummy_output_dir)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(dummy_output_dir) if 'dummy_output_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_output_dir) else 'dummy_output_dir'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = dummy_metrics.current_epoch
    @py_assert4 = 0
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.current_epoch\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_metrics.performance_metrics
    @py_assert4 = {p:[] for p in constants.PARTITIONS}
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.performance_metrics\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = dummy_metrics.totally_arbitrary
    @py_assert4 = 'arbitrary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.totally_arbitrary\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(dummy_metrics) if 'dummy_metrics' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_metrics) else 'dummy_metrics',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_precision_recall_f1_support_value_error():
    """Asserts that call to `Metrics.get_precision_recall_f1_support` raises a `ValueError` error
    when an invalid value for parameter `criteria` is passed."""
    y_true = [
     ('test', 0, 3), ('test', 4, 7), ('test', 8, 11)]
    y_pred = [('test', 0, 3), ('test', 4, 7), ('test', 8, 11)]
    invalid_args = [
     'right ', 'LEFT', 'eXact', 0, []]
    for arg in invalid_args:
        with pytest.raises(ValueError):
            Metrics.get_precision_recall_f1_support(y_true, y_pred, criteria=arg)