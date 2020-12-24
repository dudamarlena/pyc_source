# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_benchmark_definition.py
# Compiled at: 2019-11-28 13:06:29
import collections, tempfile, unittest
from unittest.mock import patch
import yaml
from benchexec.model import Benchmark
import benchexec.result, benchexec.util as util
DummyConfig = collections.namedtuple('DummyConfig', [
 'name',
 'output_path',
 'container',
 'timelimit',
 'walltimelimit',
 'memorylimit',
 'corelimit',
 'num_of_threads',
 'selected_run_definitions',
 'selected_sourcefile_sets',
 'description_file'])(None, 'test', False, None, None, None, None, None, None, None, None)
ALL_TEST_TASKS = {'false_other_sub_task.yml': 'other_subproperty', 
   'false_sub_task.yml': 'sub', 
   'false_sub2_task.yml': 'sub2', 
   'false_task.yml': 'expected_verdict: false', 
   'true_task.yml': 'expected_verdict: true', 
   'unknown_task.yml': ''}

def mock_expand_filename_pattern(pattern, base_dir):
    if pattern == '*.yml':
        return list(ALL_TEST_TASKS.keys()) + ['other_task.yml']
    return [
     pattern]


def mock_load_task_def_file(f):
    if f in ('false_other_sub_task.yml', 'false_sub_task.yml', 'false_sub2_task.yml'):
        content = ('\n            input_files: {}.c\n            properties:\n                - property_file: test.prp\n                  expected_verdict: false\n                  subproperty: {}\n                - property_file: other.prp\n                  expected_verdict: false\n            ').format(f, ALL_TEST_TASKS[f])
    elif f in ALL_TEST_TASKS:
        content = ('\n            input_files: {}.c\n            properties:\n                - property_file: test.prp\n                  {}\n                - property_file: other.prp\n                  expected_verdict: false\n            ').format(f, ALL_TEST_TASKS[f])
    elif f == 'other_task.yml':
        content = '\n            input_files: d.yml.c\n            properties:\n                - property_file: other.prp\n                  expected_verdict: false\n            '
    return yaml.safe_load(content)


def mock_property_create(property_file, allow_unknown):
    assert property_file == 'test.prp'
    assert allow_unknown
    return benchexec.result.Property('test.prp', False, False, 'test', None)


class TestBenchmarkDefinition(unittest.TestCase):
    """
    Unit tests for reading benchmark definitions,
    testing mostly the classes from benchexec.model.
    """

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True

    @patch('benchexec.model.load_task_definition_file', new=mock_load_task_def_file)
    @patch('benchexec.result.Property.create', new=mock_property_create)
    @patch('benchexec.util.expand_filename_pattern', new=mock_expand_filename_pattern)
    @patch('os.path.samefile', new=lambda a, b: a == b)
    def parse_benchmark_definition(self, content):
        with tempfile.NamedTemporaryFile(prefix='BenchExec_test_benchmark_definition_', suffix='.xml', mode='w+') as (temp):
            temp.write(content)
            temp.flush()
            return Benchmark(temp.name, DummyConfig, util.read_local_time())

    def check_task_filter(self, filter_attr, expected):
        benchmark_definitions = [
         '\n            <benchmark tool="dummy">\n              <propertyfile {}>test.prp</propertyfile>\n              <tasks><include>*.yml</include></tasks>\n              <rundefinition/>\n            </benchmark>\n            ',
         '\n            <benchmark tool="dummy">\n              <tasks>\n                <propertyfile {}>test.prp</propertyfile>\n                <include>*.yml</include>\n              </tasks>\n              <rundefinition/>\n            </benchmark>\n            ',
         '\n            <benchmark tool="dummy">\n              <tasks>\n                <include>*.yml</include>\n              </tasks>\n              <rundefinition>\n                <propertyfile {}>test.prp</propertyfile>\n              </rundefinition>\n            </benchmark>\n            ']
        for bench_def in benchmark_definitions:
            benchmark = self.parse_benchmark_definition(bench_def.format(filter_attr))
            run_ids = [ run.identifier for run in benchmark.run_sets[0].runs ]
            self.assertListEqual(run_ids, sorted(expected))

    def test_expected_verdict_no_filter(self):
        self.check_task_filter('', ALL_TEST_TASKS.keys())

    def test_expected_verdict_true_filter(self):
        self.check_task_filter('expectedverdict="true"', ['true_task.yml'])

    def test_expected_verdict_false_filter(self):
        false_tasks = [ f for f in ALL_TEST_TASKS.keys() if f.startswith('false') ]
        self.check_task_filter('expectedverdict="false"', false_tasks)

    def test_expected_verdict_false_subproperty_filter(self):
        self.check_task_filter('expectedverdict="false(sub)"', ['false_sub_task.yml'])

    def test_expected_verdict_unknown_filter(self):
        self.check_task_filter('expectedverdict="unknown"', ['unknown_task.yml'])

    def test_expected_verdict_false_subproperties_filter(self):
        benchmark_definition = '\n            <benchmark tool="dummy">\n              <tasks>\n                <propertyfile expectedverdict="false(sub)">test.prp</propertyfile>\n                <include>*.yml</include>\n              </tasks>\n              <tasks>\n                <propertyfile expectedverdict="false(sub2)">test.prp</propertyfile>\n                <include>*.yml</include>\n              </tasks>\n              <rundefinition/>\n            </benchmark>\n            '
        benchmark = self.parse_benchmark_definition(benchmark_definition)
        run_ids = [ run.identifier for run in benchmark.run_sets[0].runs ]
        self.assertListEqual(run_ids, ['false_sub_task.yml', 'false_sub2_task.yml'])