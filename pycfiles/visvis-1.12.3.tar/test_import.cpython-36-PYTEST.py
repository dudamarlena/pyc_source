# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev\pylib\visvis\tests\test_import.py
# Compiled at: 2017-05-31 19:47:34
# Size of source mod 2**32: 213 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_visvis_import():
    import visvis as vv, visvis.vvio
    if not vv:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert1 = vv.vvio
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.vvio\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = vv.imread
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.imread\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = vv.imshow
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.imshow\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = vv.plot
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.plot\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = vv.Slider
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.Slider\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = vv.Axes
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.Axes\n}') % {'py0':@pytest_ar._saferepr(vv) if 'vv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vv) else 'vv',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None