# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/tests/functional/test_outbox.py
# Compiled at: 2008-06-20 03:41:00
from pycrud.tests import *

class TestOutboxController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='outbox'))