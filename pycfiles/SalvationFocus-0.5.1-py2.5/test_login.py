# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/tests/functional/test_login.py
# Compiled at: 2008-02-28 15:45:46
from salvationfocus.tests import *

class TestLoginController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='login'))