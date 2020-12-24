# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_djblets_utils_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_utils."""
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.http import HttpRequest
from django.template import Context, Template
from djblets.testing.testcases import TagTest, TestCase
from djblets.util.templatetags.djblets_utils import ageid, escapespaces, humanize_list, indent

class AgeIdTagTests(TagTest):
    """Unit tests for the {% ageid %} template tag."""

    def setUp(self):
        super(AgeIdTagTests, self).setUp()
        self.now = datetime.utcnow()
        self.context = {b'now': self.now, 
           b'minus1': self.now - timedelta(1), 
           b'minus2': self.now - timedelta(2), 
           b'minus3': self.now - timedelta(3), 
           b'minus4': self.now - timedelta(4)}

    def test_with_now(self):
        """Testing {% ageid %} with now"""
        self.assertEqual(ageid(self.now), b'age1')

    def test_with_now_minus_1_day(self):
        """Testing {% ageid %} with yesterday"""
        self.assertEqual(ageid(self.now - timedelta(1)), b'age2')

    def test_with_now_minus_2_days(self):
        """Testing {% ageid %} with two days ago"""
        self.assertEqual(ageid(self.now - timedelta(2)), b'age3')

    def test_with_now_minus_3_days(self):
        """Testing {% ageid %} with three days ago"""
        self.assertEqual(ageid(self.now - timedelta(3)), b'age4')

    def test_with_now_minus_4_days(self):
        """Testing {% ageid %} with four days ago"""
        self.assertEqual(ageid(self.now - timedelta(4)), b'age5')

    def test_with_non_datetime(self):
        """Testing {% ageid %} with non-datetime object"""

        class Foo:

            def __init__(self, now):
                self.day = now.day
                self.month = now.month
                self.year = now.year

        self.assertEqual(ageid(Foo(self.now)), b'age1')


class AttrTagTests(TestCase):
    """Unit tests for the {% attr %} template tag."""

    def test_with_value(self):
        """Testing {% attr %} with value"""
        t = Template(b'{% load djblets_utils %}<span{% attr "class" %}\n{%  if some_bool %}truthy{% endif %}\n{% endattr %}>')
        self.assertEqual(t.render(Context({b'some_bool': True})), b'<span class="truthy">')

    def test_without_value(self):
        """Testing {% attr %} with no value"""
        t = Template(b'{% load djblets_utils %}<span{% attr "class" %}\n{%  if some_bool %}falsy{% endif %}\n{% endattr %}>')
        self.assertEqual(t.render(Context({b'some_bool': False})), b'<span>')

    def test_escapes_value(self):
        """Testing {% attr %} escapes value"""
        t = Template(b'{% load djblets_utils %}<span{% attr "data-foo" %}<hello>{% endattr %}>')
        self.assertEqual(t.render(Context()), b'<span data-foo="&lt;hello&gt;">')

    def test_condenses_whitespace(self):
        """Testing {% attr %} condenses/strips extra whitespace by default"""
        t = Template(b'{% load djblets_utils %}<span{% attr "data-foo" %}\nsome    \n\nvalue\n{% endattr %}>')
        self.assertEqual(t.render(Context()), b'<span data-foo="some value">')

    def test_with_nocondense_preserves_whitespace(self):
        """Testing {% attr %} with "nocondense" option preserves whitespace"""
        t = Template(b'{% load djblets_utils %}<span{% attr "data-foo" nocondense %}\nsome    \n\nvalue\n{% endattr %}>')
        self.assertEqual(t.render(Context()), b'<span data-foo="\nsome    \n\nvalue\n">')


class DefineVarTagTests(TestCase):
    """Unit tests for the {% definevar %} template tag."""

    def test_basic_usage(self):
        """Testing {% definevar %}"""
        t = Template(b'{% load djblets_utils %}{% definevar "myvar" %}\ntest{{num}}\n{% enddefinevar %}{{myvar}}')
        self.assertEqual(t.render(Context({b'num': 123})), b'\ntest123\n')

    def test_with_strip(self):
        """Testing {% definevar %} with strip option"""
        t = Template(b'{% load djblets_utils %}{% definevar "myvar" strip %}\n<span>\n <strong>\n  test{{num}}\n </strong>\n</span>\n{% enddefinevar %}[{{myvar}}]')
        self.assertEqual(t.render(Context({b'num': 123})), b'[<span>\n <strong>\n  test123\n </strong>\n</span>]')

    def test_with_spaceless(self):
        """Testing {% definevar %} with spaceless option"""
        t = Template(b'{% load djblets_utils %}{% definevar "myvar" spaceless %}\n<span>\n <strong>\n  test{{num}}\n </strong>\n</span>\n{% enddefinevar %}[{{myvar}}]')
        self.assertEqual(t.render(Context({b'num': 123})), b'[<span><strong>\n  test123\n </strong></span>]')

    def test_with_unsafe(self):
        """Testing {% definevar %} with unsafe option"""
        t = Template(b'{% load djblets_utils %}{% definevar "myvar" unsafe %}<hello>{% enddefinevar %}{{myvar}}')
        self.assertEqual(t.render(Context()), b'&lt;hello&gt;')


class EscapeSpacesFilterTests(TestCase):
    """Unit tests for the {{...|escapespaces}} template filter."""

    def test_with_single_space(self):
        """Testing {{...|escapespaces}} with single space"""
        self.assertEqual(escapespaces(b'Hi there'), b'Hi there')

    def test_with_multiple_spaces(self):
        """Testing {{...|escapespaces}} with multiple consecutive spaces"""
        self.assertEqual(escapespaces(b'Hi  there'), b'Hi&nbsp; there')

    def test_with_newline(self):
        """Testing {{...|escapespaces}} with newline"""
        self.assertEqual(escapespaces(b'Hi  there\n'), b'Hi&nbsp; there<br />')


class HumanizeListFilterTests(TestCase):
    """Unit tests for the {{...|humanize_list}} template filter."""

    def test_with_empty_list(self):
        """Testing {{...|humanize_list}} with empty list"""
        self.assertEqual(humanize_list([]), b'')

    def test_with_1_item(self):
        """Testing {{...|humanize_list}} with 1 item"""
        self.assertEqual(humanize_list([b'a']), b'a')

    def test_with_2_items(self):
        """Testing {{...|humanize_list}} with 2 items"""
        self.assertEqual(humanize_list([b'a', b'b']), b'a and b')

    def test_with_3_items(self):
        """Testing {{...|humanize_list}} with 3 items"""
        self.assertEqual(humanize_list([b'a', b'b', b'c']), b'a, b and c')

    def test_with_4_items(self):
        """Testing {{...|humanize_list}} with 4 items"""
        self.assertEqual(humanize_list([b'a', b'b', b'c', b'd']), b'a, b, c, and d')


class IncludeAsStringTagTests(TestCase):
    """Unit tests for the {% include_as_string %} template tag."""

    def test_basic_usage(self):
        """Testing {% include_as_string %}"""
        t = Template(b'{% load djblets_utils %}{% include_as_string template_name %}')
        self.assertEqual(t.render(Context({b'template_name': b'testing/foo.html', 
           b'foo': 1, 
           b'bar': 2})), b"'1 2\\\n'")


class IndentFilterTests(TestCase):
    """Unit tests for the {{...|indent}} template filter."""

    def test_with_default_indent(self):
        """Testing {{...|indent}} with default indentation level"""
        self.assertEqual(indent(b'foo'), b'    foo')

    def test_with_custom_indent(self):
        """Testing {{...|indent}} with custom indentation level"""
        self.assertEqual(indent(b'foo', 3), b'   foo')

    def test_with_multiple_lines(self):
        """Testing {{...|indent}} with multiple lines"""
        self.assertEqual(indent(b'foo\nbar'), b'    foo\n    bar')


class QuerystringWithTagTests(TestCase):
    """Unit tests for the {% querystring_with %} template tag."""

    def test_basic_usage(self):
        """Testing {% querystring_with %}"""
        t = Template(b'{% load djblets_utils %}{% querystring_with "foo" "bar" %}')
        self.assertEqual(t.render(Context({b'request': HttpRequest()})), b'?foo=bar')

    def test_with_tag_existing_query(self):
        """Testing {% querystring_with %} with an existing query"""
        t = Template(b'{% load djblets_utils %}{% querystring_with "foo" "bar" %}')
        request = HttpRequest()
        request.GET = {b'a': b'1', 
           b'b': b'2'}
        self.assertEqual(t.render(Context({b'request': request})), b'?a=1&amp;b=2&amp;foo=bar')

    def test_with_existing_query_override(self):
        """Testing {% querystring_with %} with an existing query that gets
        overriden
        """
        t = Template(b'{% load djblets_utils %}{% querystring_with "foo" "bar" %}')
        request = HttpRequest()
        request.GET = {b'foo': b'foo', 
           b'bar': b'baz'}
        self.assertEqual(t.render(Context({b'request': request})), b'?bar=baz&amp;foo=bar')