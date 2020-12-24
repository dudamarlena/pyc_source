# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/tests/functional/test_sale.py
# Compiled at: 2008-05-10 21:47:59
from subicpos.tests import *

class TestSaleController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='sale'))