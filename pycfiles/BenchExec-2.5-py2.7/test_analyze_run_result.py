# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_analyze_run_result.py
# Compiled at: 2019-11-28 13:06:29
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, sys, unittest
sys.dont_write_bytecode = True
from benchexec.util import ProcessExitCode
from benchexec.model import Run
from benchexec.result import *
from benchexec.tools.template import BaseTool
normal_result = ProcessExitCode(raw=0, value=0, signal=None)

class TestResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        logging.disable(logging.CRITICAL)

    def create_run(self, info_result=RESULT_UNKNOWN):
        runSet = lambda : None
        runSet.log_folder = b'.'
        runSet.result_files_folder = b'.'
        runSet.options = []
        runSet.real_name = None
        runSet.propertytag = None
        runSet.benchmark = lambda : None
        runSet.benchmark.base_dir = b'.'
        runSet.benchmark.benchmark_file = b'Test.xml'
        runSet.benchmark.columns = []
        runSet.benchmark.name = b'Test'
        runSet.benchmark.instance = b'Test'
        runSet.benchmark.rlimits = {}
        runSet.benchmark.tool = BaseTool()

        def determine_result(self, returncode, returnsignal, output, isTimeout=False):
            return info_result

        runSet.benchmark.tool.determine_result = determine_result
        return Run(identifier=b'test.c', sourcefiles=[b'test.c'], fileOptions=[], runSet=runSet)

    def test_simple(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(RESULT_UNKNOWN, run._analyze_result(normal_result, b'', False, None))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(RESULT_TRUE_PROP, run._analyze_result(normal_result, b'', False, None))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(RESULT_FALSE_REACH, run._analyze_result(normal_result, b'', False, None))
        return

    def test_timeout(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'TIMEOUT', run._analyze_result(normal_result, b'', True, None))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(b'TIMEOUT (' + RESULT_TRUE_PROP + b')', run._analyze_result(normal_result, b'', True, None))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(b'TIMEOUT (' + RESULT_FALSE_REACH + b')', run._analyze_result(normal_result, b'', True, None))
        run = self.create_run(info_result=b'SOME OTHER RESULT')
        self.assertEqual(b'TIMEOUT (SOME OTHER RESULT)', run._analyze_result(normal_result, b'', True, None))
        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(b'TIMEOUT', run._analyze_result(normal_result, b'', True, None))
        return

    def test_out_of_memory(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'OUT OF MEMORY', run._analyze_result(normal_result, b'', False, b'memory'))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(b'OUT OF MEMORY (' + RESULT_TRUE_PROP + b')', run._analyze_result(normal_result, b'', False, b'memory'))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(b'OUT OF MEMORY (' + RESULT_FALSE_REACH + b')', run._analyze_result(normal_result, b'', False, b'memory'))
        run = self.create_run(info_result=b'SOME OTHER RESULT')
        self.assertEqual(b'OUT OF MEMORY (SOME OTHER RESULT)', run._analyze_result(normal_result, b'', False, b'memory'))
        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(b'OUT OF MEMORY', run._analyze_result(normal_result, b'', False, b'memory'))

    def test_timeout_and_out_of_memory(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'TIMEOUT', run._analyze_result(normal_result, b'', True, b'memory'))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(b'TIMEOUT (' + RESULT_TRUE_PROP + b')', run._analyze_result(normal_result, b'', True, b'memory'))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(b'TIMEOUT (' + RESULT_FALSE_REACH + b')', run._analyze_result(normal_result, b'', True, b'memory'))
        run = self.create_run(info_result=b'SOME OTHER RESULT')
        self.assertEqual(b'TIMEOUT (SOME OTHER RESULT)', run._analyze_result(normal_result, b'', True, b'memory'))
        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(b'TIMEOUT', run._analyze_result(normal_result, b'', True, b'memory'))

    def test_returnsignal(self):

        def signal(sig):
            """Encode a signal as it would be returned by os.wait"""
            return ProcessExitCode(raw=sig, value=None, signal=sig)

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(b'TIMEOUT', run._analyze_result(signal(9), b'', True, None))
        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(b'OUT OF MEMORY', run._analyze_result(signal(9), b'', False, b'memory'))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(RESULT_TRUE_PROP, run._analyze_result(signal(9), b'', False, None))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(RESULT_FALSE_REACH, run._analyze_result(signal(9), b'', False, None))
        run = self.create_run(info_result=b'SOME OTHER RESULT')
        self.assertEqual(b'SOME OTHER RESULT', run._analyze_result(signal(9), b'', False, None))
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'KILLED BY SIGNAL 9', run._analyze_result(signal(9), b'', False, None))
        return

    def test_exitcode(self):

        def returnvalue(value):
            """Encode an exit of aprogram as it would be returned by os.wait"""
            return ProcessExitCode(raw=value << 8, value=value, signal=None)

        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'TIMEOUT (ERROR (1))', run._analyze_result(returnvalue(1), b'', True, None))
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'OUT OF MEMORY (ERROR (1))', run._analyze_result(returnvalue(1), b'', False, b'memory'))
        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(RESULT_TRUE_PROP, run._analyze_result(returnvalue(1), b'', False, None))
        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(RESULT_FALSE_REACH, run._analyze_result(returnvalue(1), b'', False, None))
        run = self.create_run(info_result=b'SOME OTHER RESULT')
        self.assertEqual(b'SOME OTHER RESULT', run._analyze_result(returnvalue(1), b'', False, None))
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(b'ERROR (1)', run._analyze_result(returnvalue(1), b'', False, None))
        return