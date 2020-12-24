# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/smsshell/tests/functional/test_filter.py
# Compiled at: 2008-04-04 09:42:12
from smsshell.tests import *

class TestFilterController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='filter'))