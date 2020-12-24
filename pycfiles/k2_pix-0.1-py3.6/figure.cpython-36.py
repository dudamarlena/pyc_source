# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/k2-pix/figure.py
# Compiled at: 2017-11-29 20:08:12
# Size of source mod 2**32: 4531 bytes
from __future__ import division, print_function, absolute_import
import imageio, numpy as np
from tqdm import tqdm
import warnings, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.image import imsave
import matplotlib.patheffects as path_effects
from matplotlib.colors import NoNorm
from astropy import log
from astropy import visualization
from astropy.wcs import WCS
import surveyquery

class K2Fig(object):
    __doc__ = 'Figure showing K2 target pixel stamp and sky survey image.'

    def __init__(self, TPF):
        self.TPF = TPF
        self.verbose = self.TPF.verbose

    def cut_levels(self, min_percent=1.0, max_percent=95.0, data_col='FLUX'):
        """Determine the cut levels for contrast stretching.

            Returns
            -------
            vmin, vmax : float, float
                Min and max cut levels.
            """
        sample = self.TPF.flux_binned()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='(.*)invalid value(.*)')
            vmin, vmax = np.percentile(sample[(sample > 0)], [
             min_percent, max_percent])
        return (
         vmin, vmax)

    def create_figure(self, output_filename, survey, stretch='log', vmin=1, vmax=None, min_percent=1, max_percent=95, cmap='gray', contour_color='red', data_col='FLUX'):
        """Returns a matplotlib Figure object that visualizes a frame.

        Parameters
        ----------

        vmin : float, optional
            Minimum cut level (default: 0).

        vmax : float, optional
            Maximum cut level (default: 5000).

        cmap : str, optional
            The matplotlib color map name.  The default is 'gray',
            can also be e.g. 'gist_heat'.

        raw : boolean, optional
            If `True`, show the raw pixel counts rather than
            the calibrated flux. Default: `False`.

        Returns
        -------
        image : array
            An array of unisgned integers of shape (x, y, 3),
            representing an RBG colour image x px wide and y px high.
        """
        flx = self.TPF.flux_binned()
        if vmax is None:
            vmin, vmax = self.cut_levels(min_percent, max_percent, data_col)
        else:
            shape = list(flx.shape)
            fig = plt.figure(figsize=shape)
            ax = plt.subplot(projection=(self.TPF.wcs))
            ax.set_xlabel('RA')
            ax.set_ylabel('Dec')
            if self.verbose:
                print('{} vmin/vmax = {}/{} (median={})'.format(data_col, vmin, vmax, np.nanmedian(flx)))
            if stretch == 'linear':
                stretch_fn = visualization.LinearStretch()
            else:
                if stretch == 'sqrt':
                    stretch_fn = visualization.SqrtStretch()
                else:
                    if stretch == 'power':
                        stretch_fn = visualization.PowerStretch(1.0)
                    else:
                        if stretch == 'log':
                            stretch_fn = visualization.LogStretch()
                        else:
                            if stretch == 'asinh':
                                stretch_fn = visualization.AsinhStretch(0.1)
                            else:
                                raise ValueError('Unknown stretch: {0}.'.format(stretch))
        transform = stretch_fn + visualization.ManualInterval(vmin=vmin, vmax=vmax)
        ax.imshow(((255 * transform(flx)).astype(int)), aspect='auto', origin='lower',
          interpolation='nearest',
          cmap=cmap,
          norm=(NoNorm()))
        ax.set_xticks([])
        ax.set_yticks([])
        current_ylims = ax.get_ylim()
        current_xlims = ax.get_xlim()
        pixels, header = surveyquery.getSVImg(self.TPF.position, survey)
        levels = np.linspace(np.min(pixels), np.percentile(pixels, 95), 10)
        ax.contour(pixels, transform=(ax.get_transform(WCS(header))), levels=levels,
          colors=contour_color)
        ax.set_xlim(current_xlims)
        ax.set_ylim(current_ylims)
        fig.canvas.draw()
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        return fig