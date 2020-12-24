# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_submodules.py
# Compiled at: 2017-04-26 17:15:42
import unittest, numpy as np
from yhat import Yhat, YhatModel
from yhat.submodules import detect_explicit_submodules
import os, json

class TestModel(YhatModel):
    FILES = [
     os.path.join(os.path.dirname(__file__), 'sub-sub-modules/run.py')]


class TestYhatJson(unittest.TestCase):

    def test_detect_explicit_submodule(self):
        submodules = detect_explicit_submodules(TestModel)
        has_run_py = False
        for submodule in submodules:
            if submodule['name'] == 'run.py':
                has_run_py = True

        self.assertTrue(has_run_py)

    def test_detect_submodule_in_deployment(self):
        yh = Yhat('greg', 'test', 'http://api.yhathq.com/')
        _, bundle = yh.deploy('TestModel', TestModel, globals(), sure=True, dry_run=True)
        self.assertEqual(len(bundle['modules']), 8)


if __name__ == '__main__':
    unittest.main()