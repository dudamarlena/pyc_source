# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gdelraye/Documents/workspace/plotsettings/build/lib/plotsettings/test/test_labelling.py
# Compiled at: 2014-10-20 14:55:39
"""
Tests for plot labelling routines

Created on Oct 20, 2014

@author: gdelraye
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy
from matplotlib import pyplot
from mpl_toolkits.axes_grid1 import AxesGrid
from plotsettings.set import is_colorbar

def test_colorbardetector():
    """Test whether the colorbar detecting functionality works for both
    normal subplots (e.g. those created by pyplot) and AxesGrid subplots.
    """

    def bivariate_plot():
        """Create test data
        """
        delta = 0.5
        extent = (-3, 4, -4, 3)
        x = numpy.arange(-3.0, 4.001, delta)
        y = numpy.arange(-4.0, 3.001, delta)
        X, Y = numpy.meshgrid(x, y)
        Z1 = pyplot.mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = pyplot.mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        Z = (Z1 - Z2) * 10
        return (Z, extent)

    fig, ax = pyplot.subplots(1, 1)
    z, extent = bivariate_plot()
    im = ax.imshow(z, extent=extent, origin='lower')
    pyplot.colorbar(im)
    axis_list = fig.get_axes()
    axis, colorbar = axis_list
    @py_assert2 = is_colorbar(axis)
    @py_assert4 = @py_assert2 == False
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, False)) % {'py0': @pytest_ar._saferepr(is_colorbar) if 'is_colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_colorbar) else 'is_colorbar', 'py1': @pytest_ar._saferepr(axis) if 'axis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(axis) else 'axis', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = is_colorbar(colorbar)
    @py_assert4 = @py_assert2 == True
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, True)) % {'py0': @pytest_ar._saferepr(is_colorbar) if 'is_colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_colorbar) else 'is_colorbar', 'py1': @pytest_ar._saferepr(colorbar) if 'colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(colorbar) else 'colorbar', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    fig = pyplot.figure()
    grid = AxesGrid(fig, 111, nrows_ncols=(1, 1), cbar_location='bottom', cbar_pad=0.25, cbar_size='15%')
    im = grid[0].imshow(z, extent=extent, origin='lower')
    grid.cbar_axes[0].colorbar(im)
    axis_list = fig.get_axes()
    axis, colorbar = axis_list
    @py_assert2 = is_colorbar(axis)
    @py_assert4 = @py_assert2 == False
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, False)) % {'py0': @pytest_ar._saferepr(is_colorbar) if 'is_colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_colorbar) else 'is_colorbar', 'py1': @pytest_ar._saferepr(axis) if 'axis' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(axis) else 'axis', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = is_colorbar(colorbar)
    @py_assert4 = @py_assert2 == True
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, True)) % {'py0': @pytest_ar._saferepr(is_colorbar) if 'is_colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_colorbar) else 'is_colorbar', 'py1': @pytest_ar._saferepr(colorbar) if 'colorbar' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(colorbar) else 'colorbar', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    return