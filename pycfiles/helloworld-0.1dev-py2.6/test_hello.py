# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\helloworld\tests\functional\test_hello.py
# Compiled at: 2010-12-05 16:58:13
from helloworld.tests import *

class TestHelloController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='hello', action='index'))