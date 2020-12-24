# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/django_test/__init__.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 949 bytes
import os, plim
from plim import lexer as l
from plim import syntax
from plim.errors import PlimSyntaxError, ParserNotFound
from .. import TestCaseBase

class TestDjangoSyntax(TestCaseBase):

    def setUp(self):
        super(TestDjangoSyntax, self).setUp()
        self.preprocessor = plim.preprocessor_factory(syntax='django')

    def test_conditionals(self):
        test_case = 'if'
        source = self.get_file_contents(test_case + '_test.plim')
        result = self.get_file_contents(test_case + '_result.dtl')
        data = self.preprocessor(source)
        self.check_relevant_chars(data.strip(), result.strip())

    def test_loops(self):
        test_case = 'for'
        source = self.get_file_contents(test_case + '_test.plim')
        result = self.get_file_contents(test_case + '_result.dtl')
        data = self.preprocessor(source)
        self.check_relevant_chars(data.strip(), result.strip())