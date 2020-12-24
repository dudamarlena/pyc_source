# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/refaction/tests/functional/test_db.py
# Compiled at: 2008-09-11 06:21:53
from refaction.tests import *

class TestDbController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='db'))