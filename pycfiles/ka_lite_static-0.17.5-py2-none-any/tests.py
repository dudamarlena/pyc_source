# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/webdesign/tests.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import unittest
from django.contrib.webdesign.lorem_ipsum import *
from django.template import loader, Context

class WebdesignTest(unittest.TestCase):

    def test_words(self):
        self.assertEqual(words(7), b'lorem ipsum dolor sit amet consectetur adipisicing')

    def test_paragraphs(self):
        self.assertEqual(paragraphs(1), [
         b'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'])

    def test_lorem_tag(self):
        t = loader.get_template_from_string(b'{% load webdesign %}{% lorem 3 w %}')
        self.assertEqual(t.render(Context({})), b'lorem ipsum dolor')