# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_importer.py
# Compiled at: 2013-10-26 11:56:27
from pytest import raises
from mio.errors import ImportError

def test_importer(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    mio.eval(('Importer paths insert(0, "{0:s}")').format(str(tmpdir)))
    assert str(tmpdir) in list(mio.eval('Importer paths'))
    mio.eval('foo = import(foo)')
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
    mio.eval('del("foo")')


def test_import_failure(mio):
    with raises(ImportError):
        mio.eval('import(blah)', reraise=True)