# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/tests/functional/test_login.py
# Compiled at: 2007-09-06 07:54:22
from authxpprojectname.tests import *

class TestLoginController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='login'))