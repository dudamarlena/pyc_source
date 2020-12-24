# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/pipeline/test/test_pipeline_data.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2284 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.common.utils import read_as_string
from vipe.pipeline.pipeline import Pipeline
from vipe.pipeline.pipeline_data import PipelineData

def test_simple():
    check('data/pipeline_simple.yaml', {'${workingDir}/producer/person': {'producers': [
                                                     'producer:person'], 
                                       'consumers': [
                                                     'mr_cloner:input']}, 
     '${workingDir}/producer/document': {'producers': [
                                                       'producer:document'], 
                                         'consumers': []}, 
     '${workingDir}/mr_cloner/age': {'producers': [
                                                   'mr_cloner:age'], 
                                     'consumers': []}, 
     '${workingDir}/mr_cloner/person': {'producers': [
                                                      'mr_cloner:person'], 
                                        'consumers': [
                                                      'cloner:person']}, 
     '${workingDir}/cloner/person': {'producers': [
                                                   'cloner:person'], 
                                     'consumers': [
                                                   'consumer:person']}})


def test_multiple_consumers_and_producers():
    check('data/pipeline_multiple_consumers_and_producers.yaml', {'${workingDir}/producer/person': {'producers': [
                                                     'producer:person'], 
                                       'consumers': [
                                                     'mr_cloner:input', 'java_cloner:person']}, 
     '${workingDir}/cloner/person': {'producers': [
                                                   'mr_cloner:person', 'java_cloner:person'], 
                                     'consumers': [
                                                   'consumer:person']}})


def check(pipeline_file_path, data_dict):
    pipeline_yaml = read_as_string(__name__, pipeline_file_path)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    actual_data = PipelineData.from_pipeline(pipeline)
    expected_data = PipelineData.from_basic_data_types(data_dict)
    @py_assert1 = expected_data == actual_data
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (expected_data, actual_data)) % {'py0': @pytest_ar._saferepr(expected_data) if 'expected_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_data) else 'expected_data',  'py2': @pytest_ar._saferepr(actual_data) if 'actual_data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_data) else 'actual_data'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None