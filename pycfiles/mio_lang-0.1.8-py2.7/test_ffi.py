# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_ffi.py
# Compiled at: 2013-11-11 04:41:49
from datetime import date

def test_ffi(mio):
    mio.eval('\ndate = FFI clone("date", """\nfrom datetime import date\n\n\n__all__ = ("today",)\n\n\ndef today():\n    return date.today().strftime("%B %d, %Y")\n""")\n    ')
    today = date.today().strftime('%B %d, %Y')
    assert mio.eval('date today()') == today
    mio.eval('del("date")')


def test_ffi_repr(mio):
    mio.eval('\nfoo = FFI clone("foo", """\ndef foo():\n    return "Foobar!"\n""")\n    ')
    assert repr(mio.eval('foo')) == "FFI(name='foo', file=None)"


def test_ffi_attrs(mio):
    mio.eval('\nfoo = FFI clone("foo", """\nx = 1\n\n\ndef foo():\n    return "Foobar!"\n""")\n    ')
    assert mio.eval('foo foo()') == 'Foobar!'
    assert mio.eval('foo x') == 1


def test_ffi_fromfile(mio, tmpdir):
    with tmpdir.ensure('foo.py').open('w') as (f):
        f.write('\nx = 1\n\n\ndef foo():\n    return "Foobar!"\n')
    foo = mio.eval(('foo = FFI fromfile("{0:s}")').format(str(tmpdir.join('foo.py'))))
    assert foo.type == 'FFI'
    assert foo.module is not None
    assert foo.name == 'foo'
    assert foo.file == str(tmpdir.join('foo.py'))
    assert mio.eval('foo foo()') == 'Foobar!'
    assert mio.eval('foo x') == 1
    return


def test_ffi_importall(mio):
    mio.eval('\ndate = FFI clone("date", """\nfrom datetime import date\n\n\ndef foo():\n    return "foo"\n\n\ndef today():\n    return date.today().strftime("%B %d, %Y")\n\n\n__all__ = ("today",)\n""")\n    ')
    assert mio.eval('date keys') == ['today']