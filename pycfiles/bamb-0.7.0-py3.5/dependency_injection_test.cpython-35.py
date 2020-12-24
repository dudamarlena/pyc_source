# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/dependency_injection_test.py
# Compiled at: 2017-09-08 11:38:51
# Size of source mod 2**32: 616 bytes
import bamb, unittest
from domain import base
from bson.objectid import ObjectId
from domain import exceptions
from bamb import Bamb
from common import constants
from domain import task

class DependencyInjectionTest(unittest.TestCase):
    repo = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        app = Bamb.singleton()
        ts = app.get_bean(constants.SERVICE_TASK)
        t = task.Task('task 1')
        ts.save(t, key='43043920F2038193D1C8010C')
        t1 = ts.load('43043920F2038193D1C8010C')
        self.assertEqual(t1.name, 'task 1')