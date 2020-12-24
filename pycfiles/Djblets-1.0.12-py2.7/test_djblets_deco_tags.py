# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_djblets_deco_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_deco."""
from __future__ import unicode_literals
from django.template import Context, Template, TemplateSyntaxError
from djblets.testing.testcases import TagTest

class BoxTagTests(TagTest):
    """Unit tests for the {% box %} template tag."""

    def test_plain(self):
        """Testing {% box %}"""
        t = Template(b'{% load djblets_deco %}{% box %}content{% endbox %}')
        self.assertHTMLEqual(t.render(Context({})), b'<div class="box-container"><div class="box"><div class="box-inner">\ncontent\n  </div></div></div>')

    def test_with_class(self):
        """Testing {% box %} with CSS class"""
        t = Template(b'{% load djblets_deco %}{% box "class" %}content{% endbox %}')
        self.assertHTMLEqual(t.render(Context({})), b'<div class="box-container"><div class="box class"><div class="box-inner">\ncontent\n  </div></div></div>')

    def test_with_extra_arg_error(self):
        """Testing {% box %} with extra argument error"""
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load djblets_deco %}{% box "class" "foo" %}content{% endbox %}')


class ErrorBoxTests(TagTest):
    """Unit tests for the {% errorbox %} template tag."""

    def test_plain(self):
        """Testing {% errorbox %}"""
        t = Template(b'{% load djblets_deco %}{% errorbox %}content{% enderrorbox %}')
        self.assertHTMLEqual(t.render(Context({})), b'<div class="errorbox">\ncontent\n</div>')

    def test_with_id(self):
        """Testing {% errorbox %} with element ID"""
        t = Template(b'{% load djblets_deco %}{% errorbox "id" %}content{% enderrorbox %}')
        self.assertHTMLEqual(t.render(Context({})), b'<div class="errorbox" id="id">\ncontent\n</div>')

    def test_with_extra_arg_error(self):
        """Testing {% errorbox %} with extra argument error"""
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load djblets_deco %}{% box "class" "foo" "foo" %}content{% endbox %}')