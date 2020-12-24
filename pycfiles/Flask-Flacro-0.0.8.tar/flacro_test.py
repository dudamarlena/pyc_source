# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/lxch/686e26f8-c6d4-4448-8fe4-c19802726dcb/projects/current/public/python/flacro/tests/flacro_test.py
# Compiled at: 2014-03-25 12:11:06
from __future__ import with_statement
import sys, os
from flask import Flask, render_template, current_app
from tests import *

class FlacroBaseCase(FlacroTest):

    def test_bases(self):
        pass

    def test_macro_static(self):
        rv = self.app.test_client().get('/static_macro')
        self.assertIn('STATIC MACRO', rv.data)

    def test_macro_content(self):
        rv = self.app.test_client().get('/content_macro')
        self.assertIn('THING', rv.data)

    def test_macro_attr(self):
        rv = self.app.test_client().get('/attr_macro')
        self.assertIn('abc', rv.data)

    def test_macro_named(self):
        rv = self.app.test_client().get('/named_macro')
        self.assertIn('A NAMED MACRO RENDERED BY NAME', rv.data)
        self.assertIn('123', rv.data)


class PackagedMacrosTestCase(FlacroTest):

    def test_list(self):
        rv = self.app.test_client().get('/links_list')
        self.assertIn('l1', rv.data)
        self.assertIn('href="/one"', rv.data)
        self.assertIn('arbitrary=for_attr_macro_route', rv.data)
        self.assertIn('a plain item', rv.data)

    def test_accordian(self):
        rv = self.app.test_client().get('/accordian_macro')
        self.assertIn('accordian_test-accordion', rv.data)
        self.assertIn('#accordian_test', rv.data)

    def test_tabs(self):
        rv = self.app.test_client().get('/tabs_macro')
        self.assertIn('tabset-macro', rv.data)
        self.assertIn('tab-content', rv.data)
        rv = self.app.test_client().get('minimal_tabs_macro')
        self.assertIn('tabset', rv.data)
        self.assertIn('minimal', rv.data)


if __name__ == '__main__':
    unittest.main()