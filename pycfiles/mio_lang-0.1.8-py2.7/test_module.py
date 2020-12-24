# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_module.py
# Compiled at: 2013-12-08 17:19:04


def test_module(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    foo = mio.eval(('foo = Module clone("foo", "{0:s}")').format(str(tmpdir.join('foo.mio'))))
    assert repr(foo) == ('Module(name={0:s}, file={1:s})').format(repr('foo'), repr(str(tmpdir.join('foo.mio'))))
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('del("foo")')


def test_module_import(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    foo = mio.eval(('foo = Module clone("foo", "{0:s}")').format(str(tmpdir.join('foo.mio'))))
    assert repr(foo) == ('Module(name={0:s}, file={1:s})').format(repr('foo'), repr(str(tmpdir.join('foo.mio'))))
    mio.eval('foo import("hello")')
    mio.eval('hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('del("foo")')


def test_package(mio, tmpdir, capfd):
    path = tmpdir.ensure('foo', dir=True)
    with path.join('__init__.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n\n            bar = import(bar)\n        ')
    with path.join('bar.mio').open('w') as (f):
        f.write('\n            foobar = block(\n                print("Foobar!")\n            )\n        ')
    mio.eval(('Importer paths insert(0, "{0:s}")').format(str(tmpdir)))
    foo = mio.eval('foo = import(foo)')
    assert repr(foo) == ('Module(name={0:s}, file={1:s})').format(repr('foo'), repr(str(path.join('__init__.mio'))))
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('foo bar foobar()')
    out, err = capfd.readouterr()
    assert out == 'Foobar!\n'
    mio.eval('del("foo")')