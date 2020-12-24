# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/tests/functional/test_inbox.py
# Compiled at: 2008-06-20 03:41:00
from pycrud.tests import *

class TestInboxController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='inbox'))