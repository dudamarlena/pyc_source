# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/tests/test_parser.py
# Compiled at: 2018-08-27 10:06:18
# Size of source mod 2**32: 1818 bytes
"""Tests for Blitz3D parser."""
from pytest import raises
from .. import parser, ast

def single_statement(instruction: ast.Statement) -> ast.Program:
    """Create body with one instruction."""
    return ast.Program((instruction,))


def test_intlit():
    """Check integer literal parser."""
    assert parser.get_ast('10') == single_statement(ast.IntLiteral(10))


def test_floatlit():
    """Check float literal parser."""
    assert parser.get_ast('10.5') == single_statement(ast.FloatLiteral(10.5))


def test_strlit():
    """Check string literal parser."""
    assert parser.get_ast('"Hello"') == single_statement(ast.StrLiteral('Hello'))


def test_proccall():
    """Check procedure call."""
    if not parser.get_ast('MyFunc') == single_statement(ast.ProcedureCall(ast.Identifier('MyFunc'), tuple())):
        raise AssertionError
    else:
        assert parser.get_ast('MyFunc 10') == single_statement(ast.ProcedureCall(ast.Identifier('MyFunc'), (ast.IntLiteral(10),)))
        procargs = (
         ast.IntLiteral(10),
         ast.FloatLiteral(15.5),
         ast.StrLiteral('abacaba'),
         ast.Identifier('hello'))
        assert parser.get_ast('MyFunc 10, 15.5, "abacaba", hello') == single_statement(ast.ProcedureCall(ast.Identifier('MyFunc'), procargs))


def test_multiple_instruction():
    """Check multiple instruction."""
    assert parser.get_ast('10\n20') == ast.Program((ast.IntLiteral(10),
     ast.IntLiteral(20)))


def test_error():
    """Check error log."""
    with raises(SyntaxError) as (exc):
        parser.get_ast('10 20')
    if not exc.value.msg == "Unexpected INTLIT '20' at 1:4":
        raise AssertionError
    else:
        with raises(SyntaxError) as (exc):
            parser.get_ast('Hello 10,')
        assert exc.value.msg == 'Unexpected EOF'