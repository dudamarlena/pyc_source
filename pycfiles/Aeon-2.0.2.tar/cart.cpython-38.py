# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/plot/cart.py
# Compiled at: 2020-04-28 06:22:50
# Size of source mod 2**32: 3505 bytes
__doc__ = 'Plotting functions used with cartopy.'
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.transforms import offset_copy
from mpl_toolkits.axes_grid1 import AxesGrid
from .text import fmt_lonlat
__all__ = ('GeoAxesGrid', 'label_global_map_gridlines')

class GeoAxesGrid(AxesGrid):
    """GeoAxesGrid"""

    def __init__(self, fig, rect, nrows_ncols, projection, **axesgrid_kw):
        axesgrid_kw['axes_class'] = (
         GeoAxes, {'map_projection': projection})
        axesgrid_kw['label_mode'] = ''
        (super(GeoAxesGrid, self).__init__)(fig, rect, nrows_ncols, **axesgrid_kw)


def label_global_map_gridlines(fig, ax, xticks=[], yticks=[], xoff=-10, yoff=-10, degree=False, **text_kw):
    """
    Label gridlines of a global cartopy map.

    Parameters
    ----------
    fig: matplotlib.figure.Figure
        Figure object.
    ax: cartopy.mpl.geoaxes.GeoAxesSubplot
        Cartopy axes.
    xticks: array-like, optional
        Sequence of longitude ticks.
    yticks: array-like, optional
        Sequence of latitude ticks.
    xoff: float, optional
        Longitude label offset from the axis (units are points).
        If negative (by default), the labels are drawn at the east boundary,
        otherwise at the west boundary.
    yoff: float, optional
        Latitude label offset from the axis (units are points).
        If negative (by default), the labels are drawn at the south boundary,
        otherwise at the north boundary.
    degree: bool, optional
        Add a degree symbol to tick labels.
    **text_kw: dict, optional
        Label text properties.
    """
    extent = ax.get_extent(crs=(ccrs.PlateCarree()))
    if xoff <= 0:
        xpos = extent[0]
    else:
        xpos = extent[1]
    if yoff <= 0:
        ypos = extent[2]
    else:
        ypos = extent[3]
    geodetic_trans = ccrs.Geodetic()
    xlab_kw = ylab_kw = {**{'va':'center',  'ha':'center'}, **text_kw}
    for xtick in xticks:
        s = fmt_lonlat(xtick, 'lon', degree=degree)
        text_transform = offset_copy((geodetic_trans._as_mpl_transform(ax)),
          fig=fig, units='points', x=0, y=yoff)
        (ax.text)(xtick, ypos, s, transform=text_transform, **xlab_kw)

    for ytick in yticks:
        s = fmt_lonlat(ytick, 'lat', degree=degree)
        text_transform = offset_copy((geodetic_trans._as_mpl_transform(ax)),
          fig=fig, units='points', x=xoff, y=0)
        (ax.text)(xpos, ytick, s, transform=text_transform, **ylab_kw)