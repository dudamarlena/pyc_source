# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev\pylib\visvis\tests\test_functions.py
# Compiled at: 2017-05-31 19:52:05
# Size of source mod 2**32: 375 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os

def test_im_read_write():
    import visvis as vv
    im = vv.imread('astronaut.png')
    @py_assert1 = im.shape
    @py_assert4 = (512, 512, 3)
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(im) if 'im' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(im) else 'im',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    vv.imwrite(os.path.expanduser('~/astronaut2.png'), im)


def test_mesh_read_write():
    import visvis as vv
    m = vv.meshRead('bunny.ssdf')
    @py_assert3 = vv.BaseMesh
    @py_assert5 = isinstance(m, @py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py1)s, %(py4)s\n{%(py4)s = %(py2)s.BaseMesh\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm',  'py2':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert3 = @py_assert5 = None
    vv.meshWrite(os.path.expanduser('~/bunny2.stl'), m)