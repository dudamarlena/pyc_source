# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/test_parser.py
# Compiled at: 2013-12-09 06:33:17
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mio.parser import parse
from mio.lexer import tokenize
from mio.types.number import Number
from mio.types.string import String

def test_empty_message(mio):
    @py_assert2 = ''
    @py_assert4 = tokenize(@py_assert2)
    @py_assert6 = parse(@py_assert4)
    @py_assert8 = @py_assert6 is None
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} is %(py9)s',), (@py_assert6, None)) % {'py9': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None', 'py0': @pytest_ar._saferepr(parse) if 'parse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse) else 'parse', 'py1': @pytest_ar._saferepr(tokenize) if 'tokenize' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenize) else 'tokenize', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    return


def test_parens(mio):
    chain = parse(tokenize('(1)'))
    @py_assert1 = chain.name
    @py_assert4 = '()'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_parens2(mio):
    chain = parse(tokenize('x(1)'))
    @py_assert1 = chain.name
    @py_assert4 = 'x'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_parens3(mio):
    chain = parse(tokenize('x = (1)'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_brackets(mio):
    chain = parse(tokenize('[1]'))
    @py_assert1 = chain.name
    @py_assert4 = '[]'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_brackets2(mio):
    chain = parse(tokenize('x[1]'))
    @py_assert1 = chain.name
    @py_assert4 = 'x'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.name
    @py_assert6 = '[]'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = chain.next.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_brackets3(mio):
    chain = parse(tokenize('x = [1]'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '[]'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0].args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_braces(mio):
    chain = parse(tokenize('{1}'))
    @py_assert1 = chain.name
    @py_assert4 = '{}'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_braces2(mio):
    chain = parse(tokenize('x{1}'))
    @py_assert1 = chain.name
    @py_assert4 = 'x'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.name
    @py_assert6 = '{}'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = chain.next.args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_braces3(mio):
    chain = parse(tokenize('x = {1}'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '{}'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0].args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_number_message(mio):
    chain = parse(tokenize('1'))
    @py_assert1 = chain.name
    @py_assert5 = 1
    @py_assert7 = Number(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_string_message(mio):
    chain = parse(tokenize('"foo"'))
    @py_assert1 = chain.name
    @py_assert5 = 'foo'
    @py_assert7 = String(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(String) if 'String' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(String) else 'String', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_string_newline(mio):
    chain = parse(tokenize('"\\n"'))
    @py_assert1 = chain.name
    @py_assert4 = '\n'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_simple_assignment(mio):
    chain = parse(tokenize('x = 1'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert6 = 1
    @py_assert8 = Number(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    return


def test_multi_assignment(mio):
    chain = parse(tokenize('x = 1\ny = 2'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert6 = 1
    @py_assert8 = Number(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.name
    @py_assert6 = '\n'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.next
    @py_assert5 = @py_assert3.name
    @py_assert8 = 'set'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.next\n}.name\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert0 = chain.next.next.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'y'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.next.next.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert6 = 2
    @py_assert8 = Number(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    return


def test_grouped_assignment(mio):
    chain = parse(tokenize('x = (1)'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert5 = '()'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1].args[0]
    @py_assert4 = 1
    @py_assert6 = Number(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_complex_assignment(mio):
    chain = parse(tokenize('Foo x = 1'))
    @py_assert1 = chain.name
    @py_assert4 = 'Foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.name
    @py_assert6 = 'set'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = chain.next.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.next.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert6 = 1
    @py_assert8 = Number(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    return


def test_complex_assignment2(mio):
    chain = parse(tokenize('x = x + 1'))
    @py_assert1 = chain.name
    @py_assert4 = 'set'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = chain.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'x'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = chain.args[1]
    @py_assert2 = @py_assert0.next
    @py_assert4 = @py_assert2.name
    @py_assert7 = '+'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.next\n}.name\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert0 = chain.args[1].next.args[0]
    @py_assert2 = @py_assert0.name
    @py_assert6 = 1
    @py_assert8 = Number(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Number) if 'Number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Number) else 'Number', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    return


def test_chaining(mio):
    chain = parse(tokenize('Foo bar'))
    @py_assert1 = chain.name
    @py_assert4 = 'Foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = chain.next
    @py_assert3 = @py_assert1.name
    @py_assert6 = 'bar'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.next\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_operators(mio):
    chain = parse(tokenize('1 + 2'))
    @py_assert2 = repr(chain)
    @py_assert5 = '1 +(2)'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    chain = parse(tokenize('1 + 2 * 3'))
    @py_assert2 = repr(chain)
    @py_assert5 = '1 +(2) *(3)'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_operators2(mio):
    chain = parse(tokenize('[1] + [2]'))
    @py_assert2 = repr(chain)
    @py_assert5 = '[](1) +([](2))'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_operators_assignment(mio):
    chain = parse(tokenize('foo = method(\n1 +1\n)'))
    @py_assert2 = repr(chain)
    @py_assert5 = 'set(foo, method(\n 1 +(1) \n))'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_grouping(mio):
    chain = parse(tokenize('1 + (2 * 3)'))
    @py_assert2 = repr(chain)
    @py_assert5 = '1 +(2 *(3))'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_parse(mio):
    chain = mio.eval('Parser parse("1 + 2")')
    @py_assert2 = repr(chain)
    @py_assert5 = '1 +(2)'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_reshuffle(mio):
    chain = parse(tokenize('x is not None'))
    @py_assert2 = repr(chain)
    @py_assert5 = 'not(x is(None))'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(chain) if 'chain' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(chain) else 'chain', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return