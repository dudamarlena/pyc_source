# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dotconf/tests/test_parser.py
# Compiled at: 2013-07-30 16:49:04
""" Dotconf's parser tests.
"""
from dotconf.parser import DotconfLexer, DotconfParser

def test_lexer():
    tokens = (
     ('name', 'NAME', 'name'),
     ('"test"', 'TEXT', 'test'),
     ("'test'", 'TEXT', 'test'),
     ("'te\\'st'", 'TEXT', "te'st"),
     ('42', 'NUMBER', 42),
     ('42.1', 'NUMBER', 42.1),
     ('+42', 'NUMBER', 42),
     ('+42.1', 'NUMBER', 42.1),
     ('-42', 'NUMBER', -42),
     ('-42.1', 'NUMBER', -42.1),
     ('{', 'LBRACE', '{'),
     ('}', 'RBRACE', '}'),
     ('=', 'ASSIGN', '='))
    for test, expected_type, expected_value in tokens:
        yield (
         check_token, test, expected_type, expected_value)


def check_token(test, expected_type, expected_value):
    lexer = DotconfLexer()
    lexer.input(test)
    token = lexer.next()
    assert token.type == expected_type
    assert token.value == expected_value


def test_parser_basic():
    test = '\n    daemon = yes  # This is a comment after an assignation\n    # This is comment\n    '
    parser = DotconfParser(test)
    output = parser.parse()
    assert output.get('daemon') is True


def test_parser_list():
    test = '\n    list1 = 1, 2, 3\n    list2 = 1, 2, 3,\n    list3 = 1,\n    list4 = 1,\n            2,\n            3\n    list5 = 1,\n            2,\n            3,\n    '
    parser = DotconfParser(test)
    output = parser.parse()
    assert output.get('list1') == [1, 2, 3]
    assert output.get('list2') == [1, 2, 3]
    assert output.get('list3') == [1]
    assert output.get('list4') == [1, 2, 3]
    assert output.get('list5') == [1, 2, 3]


def test_parser_section():
    test = "\n    section1 {\n        key = 'test'\n    }\n    section2 'arg' {}\n    section3 'arg1', 'arg2' {}\n    "
    parser = DotconfParser(test)
    output = parser.parse()
    assert tuple(output.subsections('section1'))[0].get('key') == 'test'
    assert tuple(output.subsections('section2'))[0].args == ['arg']
    assert tuple(output.subsections('section3'))[0].args == ['arg1', 'arg2']


def test_parser_empty():
    test = ''
    parser = DotconfParser(test)
    output = parser.parse()