# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/tests/functional/test_robots.py
# Compiled at: 2007-10-17 12:11:24
from gazest.tests import *

class TestRobotsController(TestController):
    __module__ = __name__

    def test_index(self):
        response = self.app.get(url_for(controller='robots'))