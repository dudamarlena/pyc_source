# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\latex\test_macro.py
# Compiled at: 2016-12-20 04:02:06
# Size of source mod 2**32: 3195 bytes
from unittest import TestCase, main
from flap.latex.macros import Invocation

class InvocationTests(TestCase):

    def setUp(self):
        self._name = 'foo'
        self._invocation = Invocation()

    def test_name_definition(self):
        self._invocation.name = self._name
        self.assertEqual(self._name, self._invocation.name)

    def test_defining_named_arguments(self):
        self._invocation.append_argument('bar', ['a', 'b', 'c'])
        self.assertEqual(['a', 'b', 'c'], self._invocation.argument('bar'))

    def test_as_text(self):
        self._invocation.name = [
         '\\foo']
        self._invocation.append_argument('options', [each for each in '[this is a text]'])
        self._invocation.append(['-', '---'])
        self._invocation.append_argument('link', [each for each in '{link/to/a/file.tex}'])
        self.assertEqual('\\foo[this is a text]----{link/to/a/file.tex}', self._invocation.as_text)

    def test_conversion_to_token_list(self):
        self._invocation.name = [
         '\\foo']
        self._invocation.append_argument('options', [each for each in '[this is a text]'])
        self._invocation.append([each for each in '----'])
        self._invocation.append_argument('link', [each for each in '{link/to/a/file.tex}'])
        self.assertEqual([
         '\\foo'] + [each for each in '[this is a text]'] + [each for each in '----'] + [each for each in '{link/to/a/file.tex}'], self._invocation.as_tokens)

    def test_iterating_over_items(self):
        self._invocation.name = '\\foo'
        self._invocation.append_argument('options', 'this is a text')
        self._invocation.append('----')
        self._invocation.append_argument('link', '{link/to/a/file.tex}')
        self.assertEqual({'options': 'this is a text', 
         'link': '{link/to/a/file.tex}'}, self._invocation.arguments)

    def test_argument_substitution(self):
        self._invocation.name = '\\foo'
        self._invocation.append_argument('text', ['z', 'y', 'x'])
        self.assertEqual('bar', self._invocation.substitute('text', 'bar').arguments['text'])

    def test_argument(self):
        self._invocation.name = [
         '\\foo']
        self._invocation.append_argument('link', ['p1', ',', 'p2'])
        self.assertEquals(['\\foo'], self._invocation.name)


if __name__ == '__main__':
    main()