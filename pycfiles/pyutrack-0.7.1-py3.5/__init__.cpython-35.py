# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/integration/__init__.py
# Compiled at: 2017-10-28 23:27:23
# Size of source mod 2**32: 323 bytes
import unittest, atexit
from tests import YouTrackServer, PyutrackTest
SERVER = YouTrackServer()

class IntegrationTest(PyutrackTest):
    unit = False

    @classmethod
    def setUpClass(cls):
        if not SERVER.running:
            SERVER.start()


atexit.register(lambda : SERVER.running and SERVER.stop())