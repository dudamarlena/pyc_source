# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/tests/functional/test_site.py
# Compiled at: 2008-10-29 17:02:17
from StringIO import StringIO
from shakespeare.tests import *

class TestSiteController(TestController):

    def test_index(self):
        url = url_for(controller='site')
        res = self.app.get(url)
        print res
        assert 'Home' in res
        assert 'Welcome to the Open Shakespeare web interface' in res

    def test_guide(self):
        url = url_for(controller='site', action='guide')
        res = self.app.get(url)
        assert 'guide to the features of the Open Shakespeare web' in res