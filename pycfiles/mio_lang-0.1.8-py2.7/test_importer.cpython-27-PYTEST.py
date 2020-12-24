# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/core/test_importer.py
# Compiled at: 2013-10-26 11:56:27
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises
from mio.errors import ImportError

def test_importer(mio, tmpdir, capfd):
    with tmpdir.ensure('foo.mio').open('w') as (f):
        f.write('\n            hello = block(\n                print("Hello World!")\n            )\n        ')
    mio.eval(('Importer paths insert(0, "{0:s}")').format(str(tmpdir)))
    @py_assert2 = str(tmpdir)
    @py_assert7 = mio.eval
    @py_assert9 = 'Importer paths'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert13 = list(@py_assert11)
    @py_assert4 = @py_assert2 in @py_assert13
    if not @py_assert4:
        @py_format15 = @pytest_ar._call_reprcompare(('in',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} in %(py14)s\n{%(py14)s = %(py5)s(%(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s.eval\n}(%(py10)s)\n})\n}',), (@py_assert2, @py_assert13)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str', 'py1': @pytest_ar._saferepr(tmpdir) if 'tmpdir' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmpdir) else 'tmpdir', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py6': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    mio.eval('foo = import(foo)')
    mio.eval('foo hello()')
    out, err = capfd.readouterr()
    @py_assert2 = 'Hello World!\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py3)s',), (out, @py_assert2)) % {'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    mio.eval('del("foo")')
    return


def test_import_failure(mio):
    with raises(ImportError):
        mio.eval('import(blah)', reraise=True)