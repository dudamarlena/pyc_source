# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/test_model_utils.py
# Compiled at: 2018-11-03 12:42:23
# Size of source mod 2**32: 5651 bytes
"""Any and all unit tests for the model_utils (saber/utils/model_utils.py).
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from keras.callbacks import ModelCheckpoint, TensorBoard
import pytest
from ..config import Config
from ..utils import model_utils
from .resources.dummy_constants import *

@pytest.fixture
def dummy_config():
    """Returns an instance of a Config object."""
    return Config(PATH_TO_DUMMY_CONFIG)


@pytest.fixture
def dummy_output_dir(tmpdir, dummy_config):
    """Returns list of output directories."""
    dummy_config.output_folder = tmpdir.strpath
    output_dirs = model_utils.prepare_output_directory(dummy_config)
    return output_dirs


def test_prepare_output_directory(dummy_config, dummy_output_dir):
    """Assert that `model_utils.prepare_output_directory()` creates the expected directories
    with the expected content.
    """
    @py_assert1 = [os.path.isdir(dir_) for dir_ in dummy_output_dir]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [os.path.isfile(os.path.join(dir_, 'config.ini')) for dir_ in dummy_output_dir]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_prepare_pretrained_model_dir(dummy_config):
    """Asserts that filepath returned by `generic_utils.get_pretrained_model_dir()` is as expected.
    """
    dataset = os.path.basename(dummy_config.dataset_folder[0])
    expected = os.path.join(dummy_config.output_folder, constants.PRETRAINED_MODEL_DIR, dataset)
    @py_assert1 = model_utils.prepare_pretrained_model_dir
    @py_assert4 = @py_assert1(dummy_config)
    @py_assert6 = @py_assert4 == expected
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.prepare_pretrained_model_dir\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(model_utils) if 'model_utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model_utils) else 'model_utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dummy_config) if 'dummy_config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_config) else 'dummy_config',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_setup_checkpoint_callback(dummy_config, dummy_output_dir):
    """Check that we get the expected results from call to
    `model_utils.setup_checkpoint_callback()`.
    """
    simple_actual = model_utils.setup_checkpoint_callback(dummy_config, dummy_output_dir)
    blank_actual = model_utils.setup_checkpoint_callback(dummy_config, [])
    @py_assert2 = len(dummy_output_dir)
    @py_assert7 = len(simple_actual)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(dummy_output_dir) if 'dummy_output_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_output_dir) else 'dummy_output_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(simple_actual) if 'simple_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_actual) else 'simple_actual',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = [isinstance(x, ModelCheckpoint) for x in simple_actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = []
    @py_assert1 = blank_actual == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (blank_actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(blank_actual) if 'blank_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_actual) else 'blank_actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_setup_tensorboard_callback(dummy_output_dir):
    """Check that we get the expected results from call to
    `model_utils.setup_tensorboard_callback()`.
    """
    simple_actual = model_utils.setup_tensorboard_callback(dummy_output_dir)
    blank_actual = model_utils.setup_tensorboard_callback([])
    @py_assert2 = len(dummy_output_dir)
    @py_assert7 = len(simple_actual)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(dummy_output_dir) if 'dummy_output_dir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dummy_output_dir) else 'dummy_output_dir',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(simple_actual) if 'simple_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(simple_actual) else 'simple_actual',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = [isinstance(x, TensorBoard) for x in simple_actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = []
    @py_assert1 = blank_actual == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (blank_actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(blank_actual) if 'blank_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_actual) else 'blank_actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_setup_metrics_callback():
    """
    """
    pass


def test_setup_callbacks(dummy_config, dummy_output_dir):
    """Check that we get the expected results from call to
    `model_utils.setup_callbacks()`.
    """
    dummy_config.tensorboard = True
    with_tensorboard_actual = model_utils.setup_callbacks(dummy_config, dummy_output_dir)
    dummy_config.tensorboard = False
    without_tensorboard_actual = model_utils.setup_callbacks(dummy_config, dummy_output_dir)
    blank_actual = []
    @py_assert1 = [len(x) == len(dummy_output_dir) for x in with_tensorboard_actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [len(x) == len(dummy_output_dir) for x in without_tensorboard_actual]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [isinstance(x, ModelCheckpoint) for x in with_tensorboard_actual[0]]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [isinstance(x, TensorBoard) for x in with_tensorboard_actual[1]]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = [isinstance(x, ModelCheckpoint) for x in without_tensorboard_actual[0]]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = []
    @py_assert1 = blank_actual == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (blank_actual, @py_assert2)) % {'py0':@pytest_ar._saferepr(blank_actual) if 'blank_actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(blank_actual) else 'blank_actual',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_precision_recall_f1_support():
    """Asserts that model_utils.precision_recall_f1_support returns the expected values."""
    TP_dummy = 100
    FP_dummy = 10
    FN_dummy = 20
    prec_dummy = TP_dummy / (TP_dummy + FP_dummy)
    rec_dummy = TP_dummy / (TP_dummy + FN_dummy)
    f1_dummy = 2 * prec_dummy * rec_dummy / (prec_dummy + rec_dummy)
    support_dummy = TP_dummy + FN_dummy
    test_scores_no_null = model_utils.precision_recall_f1_support(TP_dummy, FP_dummy, FN_dummy)
    test_scores_TP_null = model_utils.precision_recall_f1_support(0, FP_dummy, FN_dummy)
    test_scores_FP_null = model_utils.precision_recall_f1_support(TP_dummy, 0, FN_dummy)
    f1_FP_null = 2.0 * rec_dummy / (1.0 + rec_dummy)
    test_scores_FN_null = model_utils.precision_recall_f1_support(TP_dummy, FP_dummy, 0)
    f1_FN_null = 2 * prec_dummy * 1.0 / (prec_dummy + 1.0)
    test_scores_all_null = model_utils.precision_recall_f1_support(0, 0, 0)
    @py_assert2 = (
     prec_dummy, rec_dummy, f1_dummy, support_dummy)
    @py_assert1 = test_scores_no_null == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (test_scores_no_null, @py_assert2)) % {'py0':@pytest_ar._saferepr(test_scores_no_null) if 'test_scores_no_null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_scores_no_null) else 'test_scores_no_null',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = (0.0, 0.0, 0.0, FN_dummy)
    @py_assert1 = test_scores_TP_null == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (test_scores_TP_null, @py_assert2)) % {'py0':@pytest_ar._saferepr(test_scores_TP_null) if 'test_scores_TP_null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_scores_TP_null) else 'test_scores_TP_null',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = (1.0, rec_dummy, f1_FP_null, support_dummy)
    @py_assert1 = test_scores_FP_null == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (test_scores_FP_null, @py_assert2)) % {'py0':@pytest_ar._saferepr(test_scores_FP_null) if 'test_scores_FP_null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_scores_FP_null) else 'test_scores_FP_null',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = (prec_dummy, 1.0, f1_FN_null, TP_dummy)
    @py_assert1 = test_scores_FN_null == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (test_scores_FN_null, @py_assert2)) % {'py0':@pytest_ar._saferepr(test_scores_FN_null) if 'test_scores_FN_null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_scores_FN_null) else 'test_scores_FN_null',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = (0.0, 0.0, 0.0, 0)
    @py_assert1 = test_scores_all_null == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (test_scores_all_null, @py_assert2)) % {'py0':@pytest_ar._saferepr(test_scores_all_null) if 'test_scores_all_null' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_scores_all_null) else 'test_scores_all_null',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None