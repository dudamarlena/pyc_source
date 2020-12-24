# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_sexpr.py
# Compiled at: 2017-04-09 08:14:40
# Size of source mod 2**32: 3632 bytes
import pytest
from pygcrypt.gctypes.sexpression import SExpression
from pygcrypt.gctypes.mpi import MPIopaque, MPIint

def test_init(context):
    s_expr = SExpression('(test (a "123"))')
    if not repr(s_expr) == 'SExpression(b\'(test \\n (a "123")\\n )\\n\')':
        raise AssertionError
    else:
        s_expr = SExpression('(test (a %d)(b %s)(c %b))', 10, 'Hello World', 3, '123')
        assert repr(s_expr) == 'SExpression(b\'(test \\n (a "10")\\n (b "Hello World")\\n (c "123")\\n )\\n\')'
        s_expr2 = SExpression(s_expr.sexp)
        assert repr(s_expr2) == 'SExpression(b\'(test \\n (a "10")\\n (b "Hello World")\\n (c "123")\\n )\\n\')'


def test_getitem(context):
    s_expr = SExpression('(a "hello World")')
    if not print(s_expr['a']) == print('(hello World)'):
        raise AssertionError
    else:
        assert print(s_expr[0]) == print('(a)')
        assert print(s_expr[0:1]) == print('(a "hello World")')
    with pytest.raises(IndexError):
        s_expr[4]
        s_expr[(-1)]
        s_expr[3:5]


def test_carcdr(context):
    s_expr = SExpression('(tests (test1 "123") (test2 "456"))')
    if not str(s_expr.car) == "SExpression(b'(tests)\\n')":
        raise AssertionError
    else:
        assert str(s_expr.cdr) == 'SExpression(b\'(\\n (test1 "123")\\n (test2 "456")\\n )\\n\')'
        assert str(s_expr.cdr.car.car) == "SExpression(b'(test1)\\n')"


def test_extract(context):
    s_expr = SExpression('(test (a "123") (b "-123") (longitem "Ohai world"))')
    ret = s_expr.extract('a')
    if not ret['a'] == 3224115:
        raise AssertionError
    else:
        ret = s_expr.extract('-b', 'test')
        assert ret['b'] == 758198835
        ret = s_expr.extract("/'longitem'")
        assert isinstance(ret["'longitem'"], MPIopaque) == True
        assert ret["'longitem'"] == 'Ohai world'


def test_keys(context):
    s_expr = SExpression('(test (flags) (a "123") (b "-123") (longitem "Ohai world"))')
    if not s_expr.keys() == ['test', 'flags', 'a', 'b', 'longitem']:
        raise AssertionError
    else:
        assert s_expr['test'].keys() == ['flags', 'a', 'b', 'longitem']
        s_expr = SExpression('(a "123")')
        assert s_expr.keys() == ['a']


def test_iterate(context):
    s_expr = SExpression('(test (inside (a "123") (b "-123")) (longitem "Ohai world"))')
    iter_expr = [sexp for sexp in s_expr]
    assert iter_expr == [SExpression('(test)'), SExpression('(inside (a "123") (b "-123"))'), SExpression('(longitem "Ohai world")')]


def test_contains(context):
    s_expr = SExpression('(test (a "123") (b "-123") (longitem "Ohai world"))')
    if not ('test' in s_expr) == True:
        raise AssertionError
    elif not ('yadayada' in s_expr) == False:
        raise AssertionError


def test_setitem(context):
    s_expr = SExpression('(test (a "123") (b "-123") (longitem "Ohai world"))')
    s_expr['jumbo'] = 'Jumbo humbo jumbo!'
    assert repr(s_expr['jumbo']) == 'SExpression(b\'("Jumbo humbo jumbo!")\\n\')'
    with pytest.raises(Exception):
        s_expr['jumbo'] = 'Jumbo humbo jumbo-to!'


def test_delitem(context):
    s_expr = SExpression('(test (a "123")(b "-123"))')
    del s_expr['a']
    assert repr(s_expr) == "SExpression(b'(test \\n (b -123)\\n )\\n')"


def test_length(context):
    s_expr = SExpression('(test (a "123")(b "-123"))')
    assert len(s_expr) == 3


def test_fromdict(context):
    dict_a = {'a': MPIint(1)}
    dict_b = {'a': '123'}
    dict_c = {'a': 'Hello World'}
    dict_d = {'a': {'b':'Test',  'c':123}}
    if not str(SExpression.from_dict(dict_a)) == str(SExpression('(a %m)', MPIint(1))):
        raise AssertionError
    else:
        if not str(SExpression.from_dict(dict_b)) == str(SExpression('(a %s)', '123')):
            raise AssertionError
        elif not str(SExpression.from_dict(dict_c)) == str(SExpression('(a %b)', 11, 'Hello World')):
            raise AssertionError
        assert str(SExpression.from_dict(dict_d)) == str(SExpression('(a (b %b)(c %d))', 4, 'Test', 123))