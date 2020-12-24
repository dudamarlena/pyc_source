# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trevor/projects/pythonanywhere-cli/source/tests/test_snakesay.py
# Compiled at: 2017-10-12 16:35:20
# Size of source mod 2**32: 863 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pythonanywhere_cli.snakesay import snakesay, MESSAGE

def test_nothing():
    @py_assert0 = '~<:>>>>>>>>>'
    @py_assert4 = snakesay()
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s()\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(snakesay) if 'snakesay' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(snakesay) else 'snakesay',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = snakesay()
    @py_assert5 = MESSAGE.format
    @py_assert7 = '<  >'
    @py_assert9 = @py_assert5(bubble=@py_assert7)
    @py_assert3 = @py_assert1 == @py_assert9
    if not @py_assert3:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == %(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.format\n}(bubble=%(py8)s)\n}', ), (@py_assert1, @py_assert9)) % {'py0':@pytest_ar._saferepr(snakesay) if 'snakesay' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(snakesay) else 'snakesay',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(MESSAGE) if 'MESSAGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MESSAGE) else 'MESSAGE',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_one_line():
    @py_assert0 = '< hi there >'
    @py_assert4 = 'hi there'
    @py_assert6 = snakesay(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(snakesay) if 'snakesay' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(snakesay) else 'snakesay',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_two_lines():
    two_lines = 'a' * 81
    message = snakesay(two_lines)
    print(message)
    @py_assert0 = '/ aaaaaa'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'aaaaaa \\'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '\\ aaaaaa'
    @py_assert2 = @py_assert0 in message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_three_lines():
    three_lines = 'a' * 80 * 2 + 'a'
    long_message = snakesay(three_lines)
    print(long_message)
    @py_assert0 = '/ aaaaaa'
    @py_assert2 = @py_assert0 in long_message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, long_message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(long_message) if 'long_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(long_message) else 'long_message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'aaaaaa \\'
    @py_assert2 = @py_assert0 in long_message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, long_message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(long_message) if 'long_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(long_message) else 'long_message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '| aaaaaa'
    @py_assert2 = @py_assert0 in long_message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, long_message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(long_message) if 'long_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(long_message) else 'long_message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'aaaaaa |'
    @py_assert2 = @py_assert0 in long_message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, long_message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(long_message) if 'long_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(long_message) else 'long_message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '\\ aaaaaa'
    @py_assert2 = @py_assert0 in long_message
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, long_message)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(long_message) if 'long_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(long_message) else 'long_message'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_multiple_arguments():
    @py_assert0 = '< hi there >'
    @py_assert4 = 'hi'
    @py_assert6 = 'there'
    @py_assert8 = snakesay(@py_assert4, @py_assert6)
    @py_assert2 = @py_assert0 in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py9)s\n{%(py9)s = %(py3)s(%(py5)s, %(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(snakesay) if 'snakesay' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(snakesay) else 'snakesay',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None