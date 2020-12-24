# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/tests/functional/test_item.py
# Compiled at: 2008-07-28 05:37:25
from divimon.tests import *

class TestItemController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='item'))