# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_djblets_email_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_email."""
from __future__ import unicode_literals
from django.template import Context, Template, TemplateSyntaxError
from djblets.testing.testcases import TagTest, TestCase
from djblets.util.templatetags.djblets_email import quote_text

class CondenseTagTests(TagTest):
    """Unit tests for the {% condense %} template tag."""
    tag_content = b'foo\nbar\n\n\n\n\n\n\nfoobar!'

    def test_with_defaults(self):
        """Testing {% condense %}"""
        t = Template(b'{% load djblets_email %}{% condense %}' + self.tag_content + b'{% endcondense %}')
        self.assertHTMLEqual(t.render(Context({})), b'foo\nbar\n\n\nfoobar!')

    def test_with_max_indents(self):
        """Testing {% condense %} with custom max_indents"""
        t = Template(b'{% load djblets_email %}{% condense 1 %}' + self.tag_content + b'{% endcondense %}')
        self.assertHTMLEqual(t.render(Context({})), b'foo\nbar\nfoobar!')


class QuotedEmailTagTests(TagTest):
    """Unit tests for the {% quoted_email %} template tag."""

    def test_basic_usage(self):
        """Testing {% quoted_email %}"""
        t = Template(b'{% load djblets_email %}{% quoted_email template_name %}')
        self.assertEqual(t.render(Context({b'template_name': b'testing/foo.html', 
           b'foo': b'baz', 
           b'bar': b'qux'})), b'> baz qux\n>')

    def test_with_invalid(self):
        """Testing {% quoted_email %} with invalid usage"""
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load djblets_email %}{% quoted_email %}content{% end_quoted_email %}')


class QuoteTextFilterTests(TestCase):
    """Unit tests for the {{...|quote_text}} template filter."""

    def test_with_default_level(self):
        """Testing {{...|quote_text}} with default quote level"""
        self.assertEqual(quote_text(b'foo\nbar'), b'> foo\n> bar')

    def testLevel2(self):
        """Testing {{...|quote_text}} with custom quote level"""
        self.assertEqual(quote_text(b'foo\nbar', 2), b'> > foo\n> > bar')