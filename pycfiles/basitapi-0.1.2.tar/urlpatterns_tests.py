# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/DjangoProjects/basitapi/basitapi/tests/urlpatterns_tests.py
# Compiled at: 2013-01-16 05:29:16
from django.test import TestCase
from django.conf.urls import patterns
from basitapi.urlpatterns import format_suffix_patterns

class UrlPatternsTest(TestCase):

    def test_suffix(self):
        urlpatterns = patterns('', ('^$', 'test'), ('^api/user$', 'test'), ('^api$',
                                                                            'test'))
        _patterns = format_suffix_patterns(urlpatterns, replace=True)
        self.assertEqual(_patterns[0].resolve('.json').kwargs['format'], 'json')
        self.assertEqual(_patterns[1].resolve('api/user.xml').kwargs['format'], 'xml')
        self.assertEqual(_patterns[2].resolve('api.html').kwargs['format'], 'html')
        _patterns = format_suffix_patterns(urlpatterns)
        self.assertTrue(_patterns[0].resolve('.json').kwargs.has_key('format'))
        self.assertFalse(_patterns[1].resolve('').kwargs.has_key('format'))
        self.assertTrue(_patterns[2].resolve('api/user.json').kwargs.has_key('format'))
        self.assertFalse(_patterns[3].resolve('api/user').kwargs.has_key('format'))