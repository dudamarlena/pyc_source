# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/reader/test/test_reader.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2232 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.common.utils import read_as_string
import vipe.oozie.reader.reader
from vipe.oozie.graph import OozieGraph

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


def check_from_data_dir(dir_name):
    check('../../test/data/{}/workflow.xml'.format(dir_name), '../../test/data/{}/workflow.yaml'.format(dir_name))


def check(oozie_workflow_file_path, expected_pipeline_file_path):
    oozie_workflow = read_as_string(__name__, oozie_workflow_file_path)
    actual = vipe.oozie.reader.reader.read(oozie_workflow)
    expected_yaml = read_as_string(__name__, expected_pipeline_file_path)
    expected = OozieGraph.from_yaml_dump(expected_yaml)
    @py_assert1 = expected == actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected, actual)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None