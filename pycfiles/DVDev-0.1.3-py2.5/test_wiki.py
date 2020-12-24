# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/tests/functional/test_wiki.py
# Compiled at: 2009-04-17 21:11:42
from dvdev.tests import *

class TestWikiController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='wiki', action='index'))

    def test_view(self):
        response = self.app.get(url(controller='wiki', action='view'))
        response = self.app.get(url(controller='wiki', action='view'))