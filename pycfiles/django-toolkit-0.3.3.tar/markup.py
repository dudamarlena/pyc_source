# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/tests/markup.py
# Compiled at: 2015-04-28 19:33:49
from django.utils import unittest
from django_toolkit.markup.html import get_anchor_href, get_anchor_contents

class HtmlGetAnchorHrefTestCase(unittest.TestCase):

    def test_finds_single_href(self):
        self.assertEquals(get_anchor_href('<a href="http://example.com">Test</a>'), [
         'http://example.com'])

    def test_finds_two_hrefs(self):
        self.assertEquals(get_anchor_href('<a href="http://example.com">Test</a><a href="http://example2.com">Test 2</a>'), [
         'http://example.com', 'http://example2.com'])

    def test_finds_two_duplicates(self):
        self.assertEquals(get_anchor_href('<a href="http://example.com">Test</a><a href="http://example.com">Test 2</a>'), [
         'http://example.com', 'http://example.com'])

    def test_finds_hrefs_inside_otherstuff(self):
        self.assertEquals(get_anchor_href('Here is a <a href="http://example.com/?blah=1234&something-else=KKdjfkdksa">link</a> to somewhere...'), [
         'http://example.com/?blah=1234&something-else=KKdjfkdksa'])


class HtmlGetAnchorHtmlTestCase(unittest.TestCase):

    def test_finds_single_href(self):
        self.assertEquals(get_anchor_contents('<a href="http://example.com">Test</a>'), [
         'Test'])

    def test_finds_two_hrefs(self):
        self.assertEquals(get_anchor_contents('<a href="http://example.com">Test</a><a href="http://example2.com">Test 2</a>'), [
         'Test', 'Test 2'])

    def test_finds_two_duplicates(self):
        self.assertEquals(get_anchor_contents('<a href="http://example.com">Test</a><a href="http://example.com">Test</a>'), [
         'Test', 'Test'])

    def test_finds_hrefs_inside_otherstuff(self):
        self.assertEquals(get_anchor_contents('Here is a <a href="http://example.com/?blah=1234&something-else=KKdjfkdksa">link</a> to somewhere...'), [
         'link'])