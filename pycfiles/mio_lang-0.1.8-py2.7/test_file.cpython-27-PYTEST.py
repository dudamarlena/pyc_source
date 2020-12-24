# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/types/test_file.py
# Compiled at: 2013-11-11 04:41:49
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_repr(mio):
    file = mio.eval('File')
    @py_assert2 = repr(file)
    @py_assert5 = 'File'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    return


def test_repr2(mio, tmpdir):
    filename = str(tmpdir.ensure('test.txt'))
    file = mio.eval(('file = File clone() open("{0:s}", "r")').format(filename))
    @py_assert2 = repr(file)
    @py_assert5 = "File({0:s}, mode='r', state='open')"
    @py_assert7 = @py_assert5.format
    @py_assert11 = repr(filename)
    @py_assert13 = @py_assert7(@py_assert11)
    @py_assert4 = @py_assert2 == @py_assert13
    if not @py_assert4:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n})\n}',), (@py_assert2, @py_assert13)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py9': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py10': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert13 = None
    mio.eval('file close()')
    @py_assert2 = repr(file)
    @py_assert5 = "File({0:s}, mode='r', state='closed')"
    @py_assert7 = @py_assert5.format
    @py_assert11 = repr(filename)
    @py_assert13 = @py_assert7(@py_assert11)
    @py_assert4 = @py_assert2 == @py_assert13
    if not @py_assert4:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py14)s\n{%(py14)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n})\n}',), (@py_assert2, @py_assert13)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py9': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py0': @pytest_ar._saferepr(repr) if 'repr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(repr) else 'repr', 'py1': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py10': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert13 = None
    return


def test_open(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    file = mio.eval('File open("%s", "r")' % filename)
    @py_assert1 = file.value
    @py_assert3 = @py_assert1.name
    @py_assert5 = @py_assert3 == filename
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.name\n} == %(py6)s', ), (@py_assert3, filename)) % {'py0': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file.value
    @py_assert3 = @py_assert1.closed
    @py_assert5 = @py_assert3 is False
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.closed\n} is %(py6)s', ), (@py_assert3, False)) % {'py0': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = file.value
    @py_assert3 = @py_assert1.mode
    @py_assert6 = 'r'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.mode\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_open_status(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    mio.eval('f = File open("%s", "r")' % filename)
    @py_assert1 = mio.eval
    @py_assert3 = 'f filename'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == filename
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, filename)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py8': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'f closed'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'f mode'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'r'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_close(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    mio.eval('f = File open("%s", "r")' % filename)
    f = mio.eval('f')
    @py_assert1 = f.value
    @py_assert3 = @py_assert1.name
    @py_assert5 = @py_assert3 == filename
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.name\n} == %(py6)s', ), (@py_assert3, filename)) % {'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = f.value
    @py_assert3 = @py_assert1.closed
    @py_assert5 = @py_assert3 is False
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.closed\n} is %(py6)s', ), (@py_assert3, False)) % {'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = f.value
    @py_assert3 = @py_assert1.mode
    @py_assert6 = 'r'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.mode\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    mio.eval('f close()')
    @py_assert1 = f.value
    @py_assert3 = @py_assert1.closed
    @py_assert5 = @py_assert3 is True
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.value\n}.closed\n} is %(py6)s', ), (@py_assert3, True)) % {'py0': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_closed_status(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    mio.eval('f = File open("%s", "r")' % filename)
    @py_assert1 = mio.eval
    @py_assert3 = 'f filename'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == filename
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, filename)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py8': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'f closed'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'f mode'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'r'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    mio.eval('f close()')
    @py_assert1 = mio.eval
    @py_assert3 = 'f closed'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_read(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    @py_assert1 = mio.eval
    @py_assert3 = 'File open("%s", "r") read()'
    @py_assert6 = @py_assert3 % filename
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert9 = @py_assert7 == data
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}((%(py4)s %% %(py5)s))\n} == %(py10)s',), (@py_assert7, data)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py10': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = @py_assert9 = None
    return


def test_read_limited(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    @py_assert1 = mio.eval
    @py_assert3 = 'File open("%s", "r") read(5)'
    @py_assert6 = @py_assert3 % filename
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert10 = data[:5]
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}((%(py4)s %% %(py5)s))\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = @py_assert9 = @py_assert10 = None
    return


def test_readline(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!\nGoodbye World!'
    with filename.open('w') as (f):
        f.write(data)
    mio.eval('f = File open("%s", "r")' % filename)
    s = mio.eval('f readline()')
    @py_assert2 = 'Hello World!\n'
    @py_assert1 = s == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (s, @py_assert2)) % {'py0': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_write(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    mio.eval('f = File open("%s", "w") write("%s")' % (filename, data))
    mio.eval('f close()')
    @py_assert1 = mio.eval
    @py_assert3 = 'File open("%s", "r") read()'
    @py_assert6 = @py_assert3 % filename
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert9 = @py_assert7 == data
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}((%(py4)s %% %(py5)s))\n} == %(py10)s',), (@py_assert7, data)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py10': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = @py_assert9 = None
    return


def test_readlines(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = [
     'Hello World!', 'Goodbye World!']
    with filename.open('w') as (f):
        f.writelines(data)
    s = [('').join(data)]
    @py_assert1 = mio.eval
    @py_assert3 = 'File open("%s", "r") readlines()'
    @py_assert6 = @py_assert3 % filename
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert9 = @py_assert7 == s
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}((%(py4)s %% %(py5)s))\n} == %(py10)s',), (@py_assert7, s)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py10': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = @py_assert9 = None
    return


def test_writelines(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = [
     'Hello World!', 'Goodbye World!']
    mio.eval('lines = List clone()')
    for x in data:
        mio.eval('lines append("%s")' % x)

    mio.eval('f = File open("%s", "w")' % filename)
    mio.eval('f writelines(lines)')
    mio.eval('f close()')
    s = [
     ('').join(data)]
    @py_assert1 = filename.open
    @py_assert3 = 'r'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5.readlines
    @py_assert9 = @py_assert7()
    @py_assert11 = @py_assert9 == s
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.open\n}(%(py4)s)\n}.readlines\n}()\n} == %(py12)s',), (@py_assert9, s)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's', 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None
    @py_assert1 = mio.eval
    @py_assert3 = 'File open("%s", "r") readlines()'
    @py_assert6 = @py_assert3 % filename
    @py_assert7 = @py_assert1(@py_assert6)
    @py_assert9 = @py_assert7 == s
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}((%(py4)s %% %(py5)s))\n} == %(py10)s',), (@py_assert7, s)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py10': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert7 = @py_assert9 = None
    return


def test_iter(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    file = mio.eval('File open("%s", "r")' % filename)
    @py_assert3 = iter(file)
    @py_assert5 = list(@py_assert3)
    @py_assert8 = [data]
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(iter) if 'iter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iter) else 'iter', 'py2': @pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_pos(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    mio.eval('f = File open("%s", "r")' % filename)
    mio.eval('f read(1)')
    @py_assert1 = mio.eval
    @py_assert3 = 'f pos'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 1
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_seek(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    mio.eval('f = File open("%s", "r")' % filename)
    mio.eval('f read()') == data
    mio.eval('f seek(0)')
    mio.eval('f read()') == data


def test_truncate(mio, tmpdir):
    tmpdir.ensure('test.txt')
    filename = tmpdir.join('test.txt')
    data = 'Hello World!'
    with filename.open('w') as (f):
        f.write(data)
    mio.eval('f = File open("%s", "w+")' % filename)
    mio.eval('f read()') == data
    mio.eval('f truncate()')
    mio.eval('f seek(0)')
    mio.eval('f read()') == ''