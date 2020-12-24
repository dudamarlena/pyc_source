# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_dependencies.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 1872 bytes
import time, unittest, requests
from okera import HAS_PANDAS, HAS_NUMPY, NO_PANDAS_RUNTIME_ERROR, NO_NUMPY_RUNTIME_ERROR
from okera.tests import pycerebro_test_common as common

class DependencyTests(unittest.TestCase):

    def test_no_pandas_assert(self):
        with common.get_planner() as (planner):
            HAS_NUMPY = True
            HAS_PANDAS = False
            try:
                planner.scan_as_pandas('okera_sample.sample')
            except RuntimeError as e:
                self.assertEqual(NO_PANDAS_RUNTIME_ERROR, str(e), msg='Expected NO_PANDAS_RUNTIME_ERROR but received other')

            planner.scan_as_json('okera_sample.sample')

    def test_no_numpy_assert(self):
        with common.get_planner() as (planner):
            HAS_NUMPY = False
            HAS_PANDAS = False
            try:
                planner.scan_as_json('okera_sample.sample')
            except RuntimeError as e:
                self.assertEqual(NO_NUMPY_RUNTIME_ERROR, str(e), msg='Expected NO_NUMPY_RUNTIME_ERROR but received other')

            try:
                planner.scan_as_pandas('okera_sample.sample')
            except RuntimeError as e:
                self.assertEqual(NO_PANDAS_RUNTIME_ERROR, str(e), msg='Expected NO_PANDAS_RUNTIME_ERROR but received other')

    def test_no_numpy_presto(self):
        with common.get_planner(dialect='presto') as (planner):
            HAS_NUMPY = False
            HAS_PANDAS = False
            planner.scan_as_json('select * from okera_sample.sample')


if __name__ == '__main__':
    unittest.main()