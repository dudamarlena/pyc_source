# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/converter/test/test_iis_converter.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 3147 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import pytest
from vipe.common.utils import read_as_string
from vipe.oozie.graph import OozieGraph
from vipe.pipeline.pipeline import Pipeline
from vipe.oozie.converter.iis import IISPipelineConverter
from vipe.oozie.converter.converter import convert

def test_bypass():
    check_from_data_dir('bypass')


def test_conditional():
    check_from_data_dir('conditional')


def test_distcp():
    check_from_data_dir('distcp')


def test_fork():
    check_from_data_dir('fork')


def test_fs():
    check_from_data_dir('fs')


def test_generatesschema():
    check_from_data_dir('generateschema')


def test_global_section():
    check_from_data_dir('global_section')


def test_hadoopstreaming():
    check_from_data_dir('hadoopstreaming')


def test_hive():
    check_from_data_dir('hive')


def test_i_o_paths_parameters():
    check_from_data_dir('i_o_paths_parameters')


def test_java():
    check_from_data_dir('java')


def test_javamapreduce():
    check_from_data_dir('javamapreduce')


def test_javamapreduce_multipleoutput():
    check_from_data_dir('javamapreduce_multipleoutput')


def test_pig():
    check_from_data_dir('pig')


def test_subworkflow():
    check_from_data_dir('subworkflow')


def test_subworkflow_with_root_ports():
    check_from_data_dir('subworkflow_with_root_ports')


def test_java_with_reserved_node_name_lowercase():
    check_from_data_dir('java_with_reserved_node_name_lowercase')


def test_java_with_reserved_node_name_uppercase():
    with pytest.raises(Exception):
        convert_oozie_yaml_to_pipeline('../../test/data/{}/workflow.yaml'.format('java_with_reserved_node_name_uppercase'))


def check_from_data_dir(dir_name):
    check('../../test/data/{}/workflow.yaml'.format(dir_name), '../../test/data/{}/pipeline.yaml'.format(dir_name))


def convert_oozie_yaml_to_pipeline(oozie_workflow_file_path):
    oozie_yaml = read_as_string(__name__, oozie_workflow_file_path)
    oozie_graph = OozieGraph.from_yaml_dump(oozie_yaml)
    pipeline = convert(oozie_graph, IISPipelineConverter())
    return pipeline


def check(oozie_workflow_file_path, expected_pipeline_file_path):
    actual_pipeline = convert_oozie_yaml_to_pipeline(oozie_workflow_file_path)
    expected_pipeline_yaml = read_as_string(__name__, expected_pipeline_file_path)
    expected = Pipeline.from_yaml_dump(expected_pipeline_yaml)
    @py_assert1 = expected == actual_pipeline
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual_pipeline)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2': @pytest_ar._saferepr(actual_pipeline) if 'actual_pipeline' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_pipeline) else 'actual_pipeline'}
        @py_format5 = (@pytest_ar._format_assertmsg('expected={},\nactual={}'.format(expected, actual_pipeline)) + '\n>assert %(py4)s') % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None