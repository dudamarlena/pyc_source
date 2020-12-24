# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/tests/test_ast.py
# Compiled at: 2018-08-27 10:06:18
# Size of source mod 2**32: 4718 bytes
"""Test case for ast."""
from pytest import raises
from .. import ast

def test_frosen_dict():
    """Test frozen dict."""
    frozen_dict = ast.FrozenDict(a=10, b=20)
    if not len(frozen_dict) == 2:
        raise AssertionError
    else:
        if not [
         'a', 'b'] == sorted(frozen_dict):
            raise AssertionError
        else:
            if not frozen_dict['a'] == 10:
                raise AssertionError
            else:
                if not frozen_dict.a == 10:
                    raise AssertionError
                else:
                    assert frozen_dict['b'] == 20
                    assert frozen_dict.b == 20
                with raises(KeyError):
                    print(frozen_dict['c'])
                assert frozen_dict != {'a':10,  'b':20}
            other_frozen_dict = ast.FrozenDict(a=10, b=20)
            assert hash(frozen_dict) == hash(other_frozen_dict)
        assert frozen_dict == other_frozen_dict


def test_abstract_literal():
    """Test abstract literal."""
    value = 10
    lit = ast.Literal(value)
    if not lit['value'] == value:
        raise AssertionError
    else:
        assert str(lit) == str(value)
        assert repr(lit) == 'Literal(10)'


def test_integer_literal():
    """Test abstract literal."""
    value = 10
    lit = ast.IntLiteral(value)
    if not lit['value'] == value:
        raise AssertionError
    else:
        assert str(lit) == str(value)
        assert repr(lit) == 'IntLiteral({value})'.format(value=value)
    with raises(TypeError):
        ast.IntLiteral('string')


def test_float_literal():
    """Test float literal."""
    value = 10.0
    lit = ast.FloatLiteral(value)
    if not lit['value'] == value:
        raise AssertionError
    else:
        assert str(lit) == str(value)
        assert repr(lit) == 'FloatLiteral({value})'.format(value=value)
    with raises(TypeError):
        ast.FloatLiteral('string')


def test_string_literal():
    """Test string literal."""
    value = 'abacaba'
    lit = ast.StrLiteral(value)
    if not lit['value'] == value:
        raise AssertionError
    else:
        assert str(lit) == str(value)
        assert repr(lit) == "StrLiteral('{value}')".format(value=value)
    with raises(TypeError):
        ast.StrLiteral(10)


def test_unary_operator():
    """Test unary operator."""
    right = ast.IntLiteral(20)
    operator = '-'
    expr = ast.UnaryOp(operator, right)
    if not expr['op'] is operator:
        raise AssertionError
    else:
        if not expr['right'] is right:
            raise AssertionError
        elif not str(expr) == '-20':
            raise AssertionError
        assert repr(expr) == "UnaryOp('-', {right})".format(right=(repr(right)))
    with raises(TypeError):
        ast.UnaryOp(operator, 'not an expression')


def test_binary_operator():
    """Test binary operator."""
    left = ast.IntLiteral(10)
    right = ast.IntLiteral(20)
    operator = '+'
    expr = ast.BinaryOp(operator, left, right)
    if not expr['op'] is operator:
        raise AssertionError
    else:
        if not expr['left'] is left:
            raise AssertionError
        else:
            assert expr['right'] is right
            assert str(expr) == '(10 + 20)'
        assert repr(expr) == "BinaryOp('+', {left}, {right})".format(left=(repr(left)), right=(repr(right)))
    with raises(TypeError):
        ast.BinaryOp(operator, left, 'not an expression')


def test_procedure():
    """Test procedure."""
    procedure = ast.Identifier('Graphics')
    args = (ast.IntLiteral(800), ast.IntLiteral(600))
    statement = ast.ProcedureCall(procedure, args)
    if not statement['procedure'] is procedure:
        raise AssertionError
    else:
        if not statement['args'] is args:
            raise AssertionError
        elif not str(statement) == 'Graphics 800, 600':
            raise AssertionError
        assert repr(statement) == 'ProcedureCall({procedure}, {args})'.format(procedure=(repr(procedure)),
          args=(repr(args)))
    with raises(TypeError):
        ast.ProcedureCall(procedure, 'not an expression')


def test_body():
    """Check code blocks."""
    body_tuple = (
     ast.IntLiteral(10), ast.IntLiteral(20))
    body = ast.Body(body_tuple)
    if not body['statements'] is body_tuple:
        raise AssertionError
    else:
        assert str(body) == '  10\n  20'
        assert repr(body) == 'Body({body_tuple})'.format(body_tuple=(repr(body_tuple)))


def test_recursive_body():
    """Check revursive code blocks."""
    body_tuple = (
     ast.IntLiteral(10),
     ast.Body((ast.IntLiteral(20),
      ast.IntLiteral(30))),
     ast.IntLiteral(40))
    body = ast.Body(body_tuple)
    if not body['statements'] is body_tuple:
        raise AssertionError
    elif not str(body) == '  10\n    20\n    30\n  40':
        raise AssertionError


def test_program():
    """Check program block."""
    program_tuple = (
     ast.IntLiteral(10), ast.IntLiteral(20))
    program = ast.Program(program_tuple)
    if not program['statements'] is program_tuple:
        raise AssertionError
    else:
        assert str(program) == '10\n20'
        assert repr(program) == 'Program({program_tuple})'.format(program_tuple=(repr(program_tuple)))


def test_program_block():
    """Check  program and code blocks."""
    program_tuple = (
     ast.IntLiteral(10),
     ast.Body((ast.IntLiteral(20),
      ast.IntLiteral(30))),
     ast.IntLiteral(40))
    program = ast.Program(program_tuple)
    if not program['statements'] is program_tuple:
        raise AssertionError
    elif not str(program) == '10\n  20\n  30\n40':
        raise AssertionError