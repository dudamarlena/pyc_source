# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/functional/test_logs.py
# Compiled at: 2010-08-08 03:18:44
from pysvnmanager.tests import *

class TestLogsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='logs', action='index'))