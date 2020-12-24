# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/process/tests/test_process_tools.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 1688 bytes
import logging
from unittest import TestCase
from functools import partial
from time import sleep
from foxylib.tools.process.process_tool import ProcessTool
logger = logging.getLogger(__name__)

class PP:

    @classmethod
    def f(cls, proc_name, secs):
        print('{0}: waiting {1} secs'.format(proc_name, secs))
        sleep(secs)
        print('{0}: done after {1} secs'.format(proc_name, secs))
        return proc_name


class ProcessToolTest(TestCase):

    def setUp(self):
        logging.basicConfig(level=(logging.DEBUG))

    def test_01(self):

        def func(proc_name, secs):
            print('{0}: waiting {1} secs'.format(proc_name, secs))
            sleep(secs)
            print('{0}: done after {1} secs'.format(proc_name, secs))
            return proc_name

        f = PP.f
        func_list = [
         partial(f, 'proc 00', 5),
         partial(f, 'proc 01', 10),
         partial(f, 'proc 02', 1),
         partial(f, 'proc 03', 3),
         partial(f, 'proc 04', 9),
         partial(f, 'proc 05', 2),
         partial(f, 'proc 06', 4),
         partial(f, 'proc 07', 7),
         partial(f, 'proc 08', 8),
         partial(f, 'proc 09', 6)]
        hyp = ProcessTool.func_list2result_list(func_list)
        ref = ['proc 00',
         'proc 01',
         'proc 02',
         'proc 03',
         'proc 04',
         'proc 05',
         'proc 06',
         'proc 07',
         'proc 08',
         'proc 09']
        self.assertEqual(hyp, ref)