# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_fileRegexMap.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 4116 bytes
from __future__ import absolute_import
from unittest import TestCase, main
from blowdrycss.classparser import FileRegexMap
from blowdrycss.utilities import unittest_file_path
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class TestFileRegexMap(TestCase):

    def test_is_valid_extension_true(self):
        file_paths = [
         unittest_file_path('test_aspx', 'test.aspx'), unittest_file_path('test_jinja', 'test.jinja2')]
        for _path in file_paths:
            file_regex_map = FileRegexMap(file_path=_path)
            self.assertTrue((file_regex_map.is_valid_extension()), msg=_path)

    def test_is_valid_extension_whitespace(self):
        file_paths = [unittest_file_path('test_aspx', 'test.aspx  '), unittest_file_path('test_jinja', 'test.jinja2 ')]
        for _path in file_paths:
            file_regex_map = FileRegexMap(file_path=_path)
            self.assertTrue((file_regex_map.is_valid_extension()), msg=_path)

    def test_is_valid_extension_false(self):
        wrong_extensions = ['.wrong', '.squirrel', '.incorrect']
        file_path = unittest_file_path('test_aspx', 'test.aspx')
        for wrong_extension in wrong_extensions:
            file_regex_map = FileRegexMap(file_path=file_path)
            file_regex_map.extension = wrong_extension
            self.assertFalse(file_regex_map.is_valid_extension())

    def test_is_valid_extension_raises_OSError(self):
        file_paths = [
         unittest_file_path('test_files', 'test.wrong'), unittest_file_path('test_files', 'test.incorrect')]
        for _path in file_paths:
            self.assertRaises(OSError, FileRegexMap, _path)

    def test_regexes(self):
        sub_uri = ('://', )
        sub_js = ('//.*?\\n', '\\n', '/\\*.*?\\*/', '(domClass.add\\(\\s*.*?,\\s*["\\\'])',
                  '(domClass.add\\(\\s*.*?,\\s*["\\\'])', '(dojo.addClass\\(\\s*.*?,\\s*["\\\'])',
                  '(domClass.remove\\(\\s*.*?,\\s*["\\\'])', '(dojo.removeClass\\(\\s*.*?,\\s*["\\\'])',
                  '(YAHOO.util.Dom.addClass\\(\\s*.*?,\\s*["\\\'])', '(YAHOO.util.Dom.hasClass\\(\\s*.*?,\\s*["\\\'])',
                  '(YAHOO.util.Dom.removeClass\\(\\s*.*?,\\s*["\\\'])', '(.addClass\\(\\s*["\\\'])',
                  '(.removeClass\\(\\s*["\\\'])', '(\\$\\(\\s*["\\\']\\.)')
        sub_html = sub_uri + sub_js + ('<!--.*?-->', )
        sub_dotnet = sub_html + ('<%--.*?--%>', '<%.*?%>')
        js_substring = 'extract__class__set'
        findall_regex_js = (
         '.classList.add\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
         '.classList.remove\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
         '.className\\s*\\+?=\\s*.*?[\\\'"](.*?)["\\\']',
         '.getElementsByClassName\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
         '.setAttribute\\(\\s*[\\\'"]class["\\\']\\s*,\\s*[\\\'"](.*?)["\\\']\\s*\\)',
         js_substring + '\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)')
        expected_dicts = [
         {'sub_regexes':sub_dotnet, 
          'findall_regexes':('class=[\\\'"](.*?)["\\\']', ) + findall_regex_js},
         {'sub_regexes':('{.*?}?}', ) + sub_html + ('{#.*?#}', ), 
          'findall_regexes':('class=[\\\'"](.*?)["\\\']', ) + findall_regex_js}]
        file_paths = [
         unittest_file_path('test_aspx', 'test.aspx'), unittest_file_path('test_jinja', 'test.jinja2')]
        for i, _path in enumerate(file_paths):
            file_regex_map = FileRegexMap(file_path=_path)
            actual_dict = file_regex_map.regex_dict
            self.assertEqual(actual_dict, (expected_dicts[i]), msg=_path)


if __name__ == '__main__':
    main()