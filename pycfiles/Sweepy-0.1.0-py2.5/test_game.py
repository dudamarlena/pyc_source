# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sweepy/tests/functional/test_game.py
# Compiled at: 2009-10-21 07:48:08
from sweepy.tests import *

class TestGameController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='game', action='index'))