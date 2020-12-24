# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_templates.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
import unittest, os, time
from os.path import join
from fs.opener import open_fs
from moya.template.moyatemplates import MoyaTemplateEngine
from moya.archive import Archive
from moya.settings import SettingsContainer

class TestTemplates(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(os.path.dirname(__file__))
        templates_path = join(path, b'templates')
        self.fs = open_fs(templates_path)
        self.archive = Archive()
        self.archive.init_cache(b'templates', SettingsContainer.create(type=b'dict'))
        self.archive.init_cache(b'fragment', SettingsContainer.create(type=b'dict'))
        self.engine = MoyaTemplateEngine(self.archive, self.fs, {})

    def tearDown(self):
        self.fs.close()
        self.fs = None
        self.archive = None
        self.engine = None
        return

    def _render(self, *template_paths, **kwargs):
        return self.engine.render(template_paths, kwargs)

    def test_substitute(self):
        """Test template substitution"""
        tests = [
         (
          dict(fruit=b'apple'), b'My favorite fruit is apple'),
         (
          dict(fruit=b'pear'), b'My favorite fruit is pear'),
         (
          dict(), b'My favorite fruit is ')]
        for test_data, result in tests:
            html = self._render(b'simplesub.html', **test_data)
            self.assertEqual(result, html)

    def test_safe_substitute(self):
        """Test safe strings"""
        from moya.render import HTML
        html = self._render(b'simplesub.html', fruit=b'<em>oranges</em>')
        self.assertEqual(html, b'My favorite fruit is &lt;em&gt;oranges&lt;/em&gt;')
        html = self._render(b'simplesub.html', fruit=HTML(b'<em>oranges</em>'))
        self.assertEqual(html, b'My favorite fruit is <em>oranges</em>')

    def test_if(self):
        """Test template IF tag"""
        tests = [
         (
          dict(fruit=b'apple'), b'I like apples'),
         (
          dict(fruit=b'pear'), b'Pears are good'),
         (
          dict(), b"I don't like fruit")]
        for test_data, result in tests:
            html = self._render(b'if.html', **test_data)
            self.assertEqual(result, html)

    def test_for(self):
        """Test template FOR tag"""
        fruits = [
         b'apples', b'oranges', b'carrot', b'pears']
        tests = [
         (
          dict(fruits=fruits), b'I like apples, oranges, pears'),
         (
          dict(fruits=[]), b"I don't like fruit")]
        for test_data, result in tests:
            html = self._render(b'for.html', **test_data)
            self.assertEqual(result, html)

    def test_escape(self):
        """Test HTML escaping"""
        tests = [
         (
          dict(text=b'Stuff & things'), b'Stuff &amp; things'),
         (
          dict(text=b'<html>'), b'&lt;html&gt;')]
        for test_data, result in tests:
            html = self._render(b'escape.html', **test_data)
            self.assertEqual(result, html)

    def test_extends(self):
        """Test extending templates"""
        html = self._render(b'extends.html', title=b'Hello')
        self.assertEqual(html, b'<title>Hello</title>')

    def test_block(self):
        """Test extending templates"""
        html = self._render(b'extendsreplace.html')
        self.assertEqual(html, b'B\n')
        html = self._render(b'extendsreplaceexplicit.html')
        self.assertEqual(html, b'B\n')
        html = self._render(b'extendsappend.html')
        self.assertEqual(html, b'A\nB\n')
        html = self._render(b'extendsprepend.html')
        self.assertEqual(html, b'B\nA\n')

    def test_def(self):
        """Test def and call tags in templates"""
        html = self._render(b'def.html', fruit=b'apples')
        self.assertEqual(b'I like apples', html)

    def test_emit(self):
        """Test emit tag in template"""
        html = self._render(b'emit.html')
        self.assertEqual(html, b'{% ${nosubstitute} %}')

    def test_comments(self):
        """Test template comments"""
        html = self._render(b'comment.html')
        self.assertEqual(html, b'apples')
        html = self._render(b'comment2.html')
        self.assertEqual(html.splitlines()[0].rstrip(), b'0 1  3')

    def test_empty(self):
        """Test empty template"""
        html = self._render(b'empty.html')
        self.assertEqual(html, b'')

    def test_justtext(self):
        """Test plain text template"""
        html = self._render(b'justtext.html')
        self.assertEqual(html, b'Just\nText')

    def test_verbatim(self):
        """Test verbatim tag"""
        html = self._render(b'verbatim.html')
        self.assertEqual(b'{% for fruit in fruits %}${fruit}{% endfor %}', html)

    def test_cache(self):
        """Test cache tag"""
        html = self._render(b'cache.html')
        result_html = b'<ul><li>1</li><li>2</li><li>3</li></ul>'
        self.assertEqual(html, result_html)
        html = self._render(b'cache.html')
        result_html = b'<ul><li>1</li><li>2</li><li>3</li></ul>'
        self.assertEqual(html, result_html)
        time.sleep(0.1)
        html = self._render(b'cache.html')
        result_html = b'<ul><li>1</li><li>2</li><li>3</li></ul>'
        self.assertEqual(html, result_html)

    def test_whitespace(self):
        """Test syntax for whitespace removal"""
        html = self._render(b'whitespace.html')
        self.assertEqual(html, b'12345')