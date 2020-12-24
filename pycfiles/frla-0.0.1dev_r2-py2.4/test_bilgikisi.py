# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/tests/functional/test_bilgikisi.py
# Compiled at: 2008-10-13 05:04:51
from frla.tests import *

class TestBilgikisiController(TestController):
    __module__ = __name__

    def test_index(self):
        response = self.app.get(url_for(controller='bilgikisi'))