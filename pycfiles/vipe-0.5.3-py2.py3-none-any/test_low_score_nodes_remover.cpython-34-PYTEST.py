# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/test/test_low_score_nodes_remover.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2526 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import os.path
from vipe.common.utils import read_as_string
from vipe.pipeline.pipeline import Pipeline
from vipe.graphviz.low_score_nodes_remover import LowScoreNodesRemover
from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel

def test_separated():
    check_changed('separated')


def test_no_input():
    check_changed('no_input')


def test_no_input_not_lowest():
    check_no_changes('no_input_not_lowest')


def test_no_output():
    check_changed('no_output')


def test_no_output_not_lowest():
    check_no_changes('no_output_not_lowest')


def test_lowest_with_input_and_output():
    check_no_changes('lowest_with_input_and_output')


def test_output_going_nowhere():
    """ The case when the output of a node is not connected to anything.

    The node should probably be removed, but is not in the current
    implementation.
    """
    check_no_changes('output_going_nowhere')


def check_changed(dir_name):
    path = [
     'data', 'low_score_nodes_remover', dir_name]
    src_dir = os.path.join(*(path + ['pipeline.yaml']))
    pipeline_yaml = read_as_string(__name__, src_dir)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    remover = LowScoreNodesRemover(ImportanceScoreMap(DetailLevel.medium))
    actual = remover.run(pipeline)
    expected_yaml = read_as_string(__name__, os.path.join(*(path + ['expected.yaml'])))
    expected = Pipeline.from_yaml_dump(expected_yaml)
    @py_assert1 = expected == actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def check_no_changes(dir_name):
    src_dir = os.path.join('data', 'low_score_nodes_remover', dir_name, 'pipeline.yaml')
    pipeline_yaml = read_as_string(__name__, src_dir)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    remover = LowScoreNodesRemover(ImportanceScoreMap(DetailLevel.medium))
    actual = remover.run(pipeline)
    @py_assert1 = pipeline == actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (pipeline, actual)) % {'py0': @pytest_ar._saferepr(pipeline) if 'pipeline' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pipeline) else 'pipeline',  'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None