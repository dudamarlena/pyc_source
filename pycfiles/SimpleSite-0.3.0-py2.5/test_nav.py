# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/tests/functional/test_nav.py
# Compiled at: 2008-11-06 12:29:00
from simplesite.tests import *

class TestNavController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nav', action='index'))