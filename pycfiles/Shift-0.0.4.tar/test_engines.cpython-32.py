# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrew/Documents/repos/Shift/shift/tests/test_engines.py
# Compiled at: 2012-07-28 22:46:34
from __future__ import print_function
from . import BaseTestCase, parameters, parametrize, shift
from .helpers import skip_if, is_pypy, is_python3
import os, sys
from glob import glob
import unittest, yaml
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
test_spec = os.path.join(file_path, 'spec.yaml')
with open(test_spec, 'rb') as (f):
    test_details = list(yaml.load_all(f.read()))

def generate_name(idx, param):
    return 'test_with_' + param['test_name']


def strip_trailing(s):
    if s.endswith('\n'):
        s = s[0:-1]
    return s


@parametrize
class TestTemplates(BaseTestCase):

    def setup(self):
        self.shift = shift.Shift(template_root=file_path)

    @parameters(test_details, name_func=generate_name)
    def test_with(self, details):
        template = self.shift.new(details['template_file'])
        if template is None:
            return
        else:
            if 'params' in details:
                params = details['params']
            else:
                params = {}
            rendered = template.render(params)
            expected_path = os.path.join(file_path, details['output_file'])
            with open(expected_path, 'rb') as (f):
                expected = f.read()
            if is_python3():
                expected = str(expected, 'utf-8')
            expected = strip_trailing(expected.replace('\r\n', '\n'))
            rendered = strip_trailing(rendered.replace('\r\n', '\n'))
            self.assert_equal(rendered, expected)
            self.assert_not_equal(rendered + 'BREAK', expected)
            return


class TestSpecificEngines(BaseTestCase):

    def setup(self):
        self.shift = shift.Shift(template_root=file_path)

    def clean_newlines(self, expected, rendered):
        expected = strip_trailing(expected.replace('\r\n', '\n'))
        rendered = strip_trailing(rendered.replace('\r\n', '\n'))
        return (
         expected, rendered)

    @skip_if(is_pypy(), "The Cheetah template engine doesn't work on PyPy")
    def test_cheetah_template_engine(self):
        if not shift.engines.CheetahTemplate.initialized:
            return
        template = self.shift.new('cheetah.cheetah')
        rendered = template.render({'name': 'Andrew'})
        expected_path = os.path.join(file_path, 'cheetah.cheetah.out')
        with open(expected_path, 'rb') as (f):
            expected = f.read()
        expected, rendered = self.clean_newlines(expected, rendered)
        self.assert_equal(rendered, expected)

    @skip_if(is_pypy(), "The misaka template engine doesn't work on PyPy")
    def test_misaka_template_engine(self):
        if not shift.engines.MarkdownMisakaTemplate.initialized:
            return
        path = os.path.join(file_path, 'markdown.md')
        expected_path = os.path.join(file_path, 'markdown.md.out')
        template = shift.engines.MarkdownMisakaTemplate(template_path=path)
        rendered = template.render()
        with open(expected_path, 'rb') as (f):
            expected = f.read()
        if is_python3():
            expected = str(expected, 'utf-8')
        expected, rendered = self.clean_newlines(expected, rendered)
        self.assert_equal(rendered, expected)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTemplates))
    suite.addTest(unittest.makeSuite(TestSpecificEngines))
    return suite


def main():
    """
    This runs the our tests, suitable for a command-line application
    """
    try:
        unittest.main(defaultTest='suite')
    except Exception as e:
        print('Exception: {0!s}'.format(e))


if __name__ == '__main__':
    main()