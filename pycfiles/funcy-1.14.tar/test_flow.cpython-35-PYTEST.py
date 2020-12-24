# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/suor/projects/funcy/tests/test_flow.py
# Compiled at: 2017-06-11 10:44:58
# Size of source mod 2**32: 3852 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from funcy.flow import *

def test_silent():
    @py_assert2 = silent(int)
    @py_assert4 = 1
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = silent(int)
    @py_assert4 = '1'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = silent(int)
    @py_assert4 = 'hello'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = None
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py5)s)\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = str.upper
    @py_assert4 = silent(@py_assert2)
    @py_assert6 = 'hello'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 'HELLO'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.upper\n})\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(@py_assert2), 'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(silent) if 'silent' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(silent) else 'silent'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


class MyError(Exception):
    pass


def test_ignore():
    @py_assert2 = ignore(Exception)
    @py_assert6 = raiser(Exception)
    @py_assert8 = @py_assert2(@py_assert6)
    @py_assert10 = @py_assert8()
    @py_assert13 = None
    @py_assert12 = @py_assert10 is @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('is',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n})\n}()\n} is %(py14)s',), (@py_assert10, @py_assert13)) % {'py5': @pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception', 'py1': @pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(ignore) if 'ignore' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ignore) else 'ignore', 
         'py14': @pytest_ar._saferepr(@py_assert13), 'py4': @pytest_ar._saferepr(raiser) if 'raiser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raiser) else 'raiser'}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert2 = ignore(Exception)
    @py_assert6 = raiser(MyError)
    @py_assert8 = @py_assert2(@py_assert6)
    @py_assert10 = @py_assert8()
    @py_assert13 = None
    @py_assert12 = @py_assert10 is @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('is',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}(%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n})\n}()\n} is %(py14)s',), (@py_assert10, @py_assert13)) % {'py5': @pytest_ar._saferepr(MyError) if 'MyError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MyError) else 'MyError', 'py1': @pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(ignore) if 'ignore' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ignore) else 'ignore', 
         'py14': @pytest_ar._saferepr(@py_assert13), 'py4': @pytest_ar._saferepr(raiser) if 'raiser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raiser) else 'raiser'}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    @py_assert1 = (TypeError, MyError)
    @py_assert3 = ignore(@py_assert1)
    @py_assert7 = raiser(MyError)
    @py_assert9 = @py_assert3(@py_assert7)
    @py_assert11 = @py_assert9()
    @py_assert14 = None
    @py_assert13 = @py_assert11 is @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('is',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}(%(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n})\n}()\n} is %(py15)s',), (@py_assert11, @py_assert14)) % {'py5': @pytest_ar._saferepr(raiser) if 'raiser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raiser) else 'raiser', 'py12': @pytest_ar._saferepr(@py_assert11), 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py10': @pytest_ar._saferepr(@py_assert9), 'py15': @pytest_ar._saferepr(@py_assert14), 'py6': @pytest_ar._saferepr(MyError) if 'MyError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MyError) else 'MyError', 'py0': @pytest_ar._saferepr(ignore) if 'ignore' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ignore) else 'ignore', 
         'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    with pytest.raises(TypeError):
        ignore(MyError)(raiser(TypeError))()
    @py_assert2 = 42
    @py_assert4 = ignore(MyError, default=@py_assert2)
    @py_assert8 = raiser(MyError)
    @py_assert10 = @py_assert4(@py_assert8)
    @py_assert12 = @py_assert10()
    @py_assert15 = 42
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, default=%(py3)s)\n}(%(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n})\n}()\n} == %(py16)s',), (@py_assert12, @py_assert15)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(MyError) if 'MyError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MyError) else 'MyError', 'py13': @pytest_ar._saferepr(@py_assert12), 'py7': @pytest_ar._saferepr(MyError) if 'MyError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MyError) else 'MyError', 'py9': @pytest_ar._saferepr(@py_assert8), 'py6': @pytest_ar._saferepr(raiser) if 'raiser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raiser) else 'raiser', 
         'py3': @pytest_ar._saferepr(@py_assert2), 'py16': @pytest_ar._saferepr(@py_assert15), 'py0': @pytest_ar._saferepr(ignore) if 'ignore' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ignore) else 'ignore'}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None


def test_raiser():
    with pytest.raises(Exception) as (e):
        raiser()()
    @py_assert1 = e.type
    @py_assert3 = @py_assert1 is Exception
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} is %(py4)s', ), (@py_assert1, Exception)) % {'py4': @pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    with pytest.raises(MyError):
        raiser(MyError)()
    with pytest.raises(MyError) as (e):
        raiser(MyError, 'some message')()
    @py_assert1 = e.value
    @py_assert3 = @py_assert1.args
    @py_assert6 = ('some message', )
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.args\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    with pytest.raises(MyError):
        raiser(MyError('some message'))()
    with pytest.raises(MyError):
        raiser(MyError)('junk', keyword='junk')


def test_suppress():
    with suppress(Exception):
        raise Exception
    with suppress(Exception):
        raise MyError
    with pytest.raises(TypeError):
        with suppress(MyError):
            raise TypeError
    with suppress(TypeError, MyError):
        raise MyError


def test_retry():
    calls = []

    def failing(n=1):
        if len(calls) < n:
            calls.append(1)
            raise MyError
        return 1

    with pytest.raises(MyError):
        failing()
    calls = []
    @py_assert1 = 2
    @py_assert4 = retry(@py_assert1, MyError)
    @py_assert7 = @py_assert4(failing)
    @py_assert9 = @py_assert7()
    @py_assert12 = 1
    @py_assert11 = @py_assert9 == @py_assert12
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}(%(py6)s)\n}()\n} == %(py13)s',), (@py_assert9, @py_assert12)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py13': @pytest_ar._saferepr(@py_assert12), 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(failing) if 'failing' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(failing) else 'failing', 'py3': @pytest_ar._saferepr(MyError) if 'MyError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MyError) else 'MyError', 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry'}
        @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None
    calls = []
    with pytest.raises(MyError):
        retry(2, MyError)(failing)(2)


def test_retry_timeout(monkeypatch):
    timeouts = []
    monkeypatch.setattr('time.sleep', timeouts.append)

    def failing():
        raise MyError

    del timeouts[:]
    with pytest.raises(MyError):
        retry(11, MyError, timeout=1)(failing)()
    @py_assert2 = [
     1]
    @py_assert4 = 10
    @py_assert6 = @py_assert2 * @py_assert4
    @py_assert1 = timeouts == @py_assert6
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == (%(py3)s * %(py5)s)', ), (timeouts, @py_assert6)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(timeouts) if 'timeouts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timeouts) else 'timeouts'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert2 = @py_assert4 = @py_assert6 = None
    del timeouts[:]
    with pytest.raises(MyError):
        retry(4, MyError, timeout=lambda a: 2 ** a)(failing)()
    @py_assert2 = [
     1, 2, 4]
    @py_assert1 = timeouts == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (timeouts, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(timeouts) if 'timeouts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(timeouts) else 'timeouts'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_retry_many_errors():
    calls = []

    def failing(n=1):
        if len(calls) < n:
            calls.append(1)
            raise MyError
        return 1

    @py_assert1 = 2
    @py_assert3 = (
     MyError, RuntimeError)
    @py_assert5 = retry(@py_assert1, @py_assert3)
    @py_assert8 = @py_assert5(failing)
    @py_assert10 = @py_assert8()
    @py_assert13 = 1
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}(%(py7)s)\n}()\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(failing) if 'failing' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(failing) else 'failing', 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry', 'py14': @pytest_ar._saferepr(@py_assert13), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    calls = []
    @py_assert1 = 2
    @py_assert3 = [
     MyError, RuntimeError]
    @py_assert5 = retry(@py_assert1, @py_assert3)
    @py_assert8 = @py_assert5(failing)
    @py_assert10 = @py_assert8()
    @py_assert13 = 1
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}(%(py7)s)\n}()\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(failing) if 'failing' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(failing) else 'failing', 'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(retry) if 'retry' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retry) else 'retry', 'py14': @pytest_ar._saferepr(@py_assert13), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_fallback():
    @py_assert2 = raiser()
    @py_assert4 = lambda : 1
    @py_assert6 = fallback(@py_assert2, @py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s()\n}, %(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py1': @pytest_ar._saferepr(raiser) if 'raiser' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raiser) else 'raiser', 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(fallback) if 'fallback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fallback) else 'fallback'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    with pytest.raises(Exception):
        fallback((raiser(), MyError), lambda : 1)
    @py_assert1 = (
     raiser(MyError), MyError)
    @py_assert3 = lambda : 1
    @py_assert5 = fallback(@py_assert1, @py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(fallback) if 'fallback' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fallback) else 'fallback'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_limit_error_rate():
    calls = []

    @limit_error_rate(2, 60, MyError)
    def limited(x):
        calls.append(x)
        raise TypeError

    with pytest.raises(TypeError):
        limited(1)
    with pytest.raises(TypeError):
        limited(2)
    with pytest.raises(MyError):
        limited(3)
    @py_assert2 = [
     1, 2]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_post_processing():

    @post_processing(max)
    def my_max(l):
        return l

    @py_assert1 = [
     1, 3, 2]
    @py_assert3 = my_max(@py_assert1)
    @py_assert6 = 3
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(my_max) if 'my_max' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(my_max) else 'my_max'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_collecting():

    @collecting
    def doubles(l):
        for i in l:
            yield i * 2

    @py_assert1 = [1, 2]
    @py_assert3 = doubles(@py_assert1)
    @py_assert6 = [
     2, 4]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(doubles) if 'doubles' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doubles) else 'doubles'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_once():
    calls = []

    @once
    def call(n):
        calls.append(n)
        return n

    call(1)
    call(2)
    @py_assert2 = [1]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_once_per():
    calls = []

    @once_per('n')
    def call(n, x=None):
        calls.append(n)
        return n

    call(1)
    call(2)
    call(1, 42)
    @py_assert2 = [1, 2]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_once_per_args():
    calls = []

    @once_per_args
    def call(n, x=None):
        calls.append(n)
        return n

    call(1)
    call(2)
    call(1, 42)
    @py_assert2 = [1, 2, 1]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    call(1)
    @py_assert2 = [1, 2, 1]
    @py_assert1 = calls == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (calls, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(calls) if 'calls' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(calls) else 'calls'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None