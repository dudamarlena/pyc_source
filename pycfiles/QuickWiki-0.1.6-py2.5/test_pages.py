# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/tests/functional/test_pages.py
# Compiled at: 2009-02-23 12:50:50
from quickwiki.tests import *

class TestPagesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pages', action='index'))
        self.assert_('Title List' in response)
        self.assert_('FrontPage' in response)