# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/refaction/tests/functional/test_website.py
# Compiled at: 2008-09-11 06:23:35
from refaction.tests import *

class TestWebsiteController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='website'))