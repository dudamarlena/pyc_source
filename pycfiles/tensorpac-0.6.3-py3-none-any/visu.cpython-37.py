# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/visu.py
# Compiled at: 2019-10-16 05:00:33
# Size of source mod 2**32: 14470 bytes
"""Visualization functions."""
import numpy as np, logging
logger = logging.getLogger('tensorpac')

class _PacVisual(object):
    __doc__ = 'Main PAC plotting class.'

    def __init__(self):
        """Init."""
        self._autovmM = True

    def pacplot(self, pac, xvec, yvec, xlabel='', ylabel='', cblabel='', title='', cmap='viridis', vmin=None, vmax=None, under=None, over=None, bad=None, pvalues=None, p=0.05, interp=None, rmaxis=False, dpaxis=False, plotas='imshow', ncontours=5, levels=None, levelcmap='Reds', polar=False, colorbar=True, y=1.02, subplot=111):
        """Main plotting pac function.

        This method can be used to plot any 2D array.

        Parameters
        ----------
        pac : array_like
            A 2D array.
        xvec : array_like
            The vector to use for the x-axis.
        yvec : array_like
            The vector to use for the y-axis.
        xlabel : string | ''
            Label for the x-axis.
        ylabel : string | ''
            Label for the y-axis.
        cblabel : string | ''
            Label for the colorbar.
        title : string | ''
            Title of the plot.
        y : float | 1.02
            Title location.
        cmap : string | 'viridis'
            Name of one Matplotlib's colomap.
        vmin : float | None
            Threshold under which set the color to the uner parameter.
        vmax : float | None
            Threshold over which set the color in the over parameter.
        under : string | 'gray'
            Color for values under the vmin parameter.
        over : string | 'red'
            Color for values over the vmax parameter.
        bad : string | None
            Color for non-significant values.
        pvalues : array_like | None
            P-values to use for masking PAC values. The shape of this
            parameter must be the same as the shape as pac.
        p : float | .05
            If pvalues is pass, use this threshold for masking
            non-significant PAC.
        interp : tuple | None
            Tuple for controlling the 2D interpolation. For example,
            (.1, .1) will multiply the number of row and columns by 10.
        rmaxis : bool | False
            Remove unecessary axis.
        dpaxis : bool | False
            Despine axis.
        plotas : {'imshow', 'contour', 'pcolor'}
            Choose how to display the comodulogram, either using imshow
            ('imshow') or contours ('contour'). If you choose 'contour',
            use the ncontours parameter for controlling the number of
            contours.
        ncontours : int | 5
            Number of contours if plotas is 'contour'.
        levels : list | None
            Add significency levels. This parameter must be a sorted list
            of p-values to use as levels.
        levelcmap : string | Reds
            Colormap of signifiency levels.

        Returns
        -------
        gca: axes
            The current matplotlib axes.
        """
        if pac.ndim is not 2:
            raise ValueError('The PAC variable must have two dimensions.')
        else:
            try:
                import matplotlib.pyplot as plt
            except:
                raise ValueError('Matplotlib not installed.')

            if pvalues is None:
                pvalues = np.zeros_like(pac)
            if interp is not None:
                pac, xvec, yvec = mapinterpolation(pac, xvec, yvec, interp[0], interp[1])
                pvalues = mapinterpolation(pvalues, self.xvec, self.yvec, interp[0], interp[1])[0]
            pac = np.ma.masked_array(pac, mask=(pvalues >= p))
            if polar:
                plotas = 'pcolor'
                plt.subplot(subplot, projection='polar')
            elif vmin is None and vmax is None and self._autovmM:
                vmin, vmax = min(0, np.nanmin(pac)), max(0, np.nanmax(pac))
                if vmin < 0:
                    if vmax > 0:
                        vmax = max(vmax, -vmin)
                        vmin = -vmax
                toplot = pac.data if levels is not None else pac
                if plotas is 'imshow':
                    im = plt.imshow(toplot, aspect='auto', cmap=cmap, origin='upper', vmin=vmin,
                      vmax=vmax,
                      interpolation='none',
                      extent=[
                     xvec[0], xvec[(-1)], yvec[(-1)], yvec[0]])
                    plt.gca().invert_yaxis()
            elif plotas is 'contour':
                im = plt.contourf(xvec, yvec, toplot, ncontours, cmap=cmap, vmin=vmin,
                  vmax=vmax)
            else:
                if plotas is 'pcolor':
                    im = plt.pcolormesh(xvec, yvec, toplot, cmap=cmap, vmin=vmin, vmax=vmax,
                      antialiased=True)
                else:
                    raise ValueError("The plotas parameter must either be 'imshow' or 'contour'")
        if levels is not None:
            plt.contour(pvalues, extent=[xvec[0], xvec[(-1)], yvec[0], yvec[(-1)]], levels=levels,
              cmap=levelcmap)
        if under is not None:
            im.cmap.set_under(color=under)
        if over is not None:
            im.cmap.set_over(color=over)
        if bad is not None:
            im.cmap.set_bad(color=bad)
        plt.axis('tight')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title, y=y)
        plt.clim(vmin=vmin, vmax=vmax)
        if colorbar:
            cb = plt.colorbar(im, shrink=0.7, pad=0.01, aspect=10)
            cb.set_label(cblabel)
            cb.outline.set_visible(False)
        ax = plt.gca()
        if rmaxis:
            for loc, spine in ax.spines.items():
                if loc in ('top', 'right'):
                    spine.set_color('none')
                    (ax.tick_params)(**{loc: False})

        if dpaxis:
            for loc, spine in ax.spines.items():
                if loc in ('left', 'bottom'):
                    spine.set_position(('outward', 10))
                    spine.set_smart_bounds(True)

        if polar:
            ax.grid(True)
            ax.set_rlabel_position(0)
            ax.set_thetamin(-180)
            ax.set_thetamax(180)
            ax.set_thetagrids([-135, -90, -45, 0, 45, 90, 135, 180])
        return plt.gca()

    def show(self):
        """Display the figure."""
        import matplotlib.pyplot as plt
        plt.show()

    def savefig(self, filename, dpi=600):
        """Save the figure.

        Parameters
        ----------
        filename : string
            The name of the figure to save.
        dpi : int | 600
            DPI of the figure.
        """
        import matplotlib.pyplot as plt
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')


class _PacPlt(_PacVisual):
    __doc__ = 'Plotting class for :class:`tensorpac.Pac`.'

    def comodulogram(self, pac, xlabel='Frequency for phase (hz)', ylabel='Frequency for amplitude (hz)', cblabel='PAC values', **kwargs):
        """Plot PAC using comodulogram.

        Parameters
        ----------
        pac : array_like
            PAC array of shape (namp, pha)
        xlabel : string | 'Frequency for phase (hz)'
            Label for the phase axis.
        ylabel : string | 'Frequency for amplitude (hz)'
            Label for the amplitude axis.
        cblabel : string | 'PAC values'
            Colorbar.
        kwargs : dict
            Further arguments are passed to the pacplot() method.

        Returns
        -------
        gca : axes
            The current matplotlib axes.
        """
        if isinstance(pac, np.ndarray):
            if pac.ndim == 3:
                logger.warning('3d pac array has been given as an input. Only 2d arrays are supported for plotting. Taking the mean across the last dimension')
                pac = pac.mean(-1)
        xvec, yvec = self.xvec, self.yvec
        self._autovmM = True
        return (self.pacplot)(pac, xvec, yvec, xlabel, ylabel, cblabel, **kwargs)

    def triplot(self, pac, fvec, tridx, xlabel='Starting frequency (hz)', ylabel='Ending frequency (hz)', cblabel='PAC values', bad='lightgray', **kwargs):
        """Triangular plot.

        The triplot method is used to find the [starting, ending] frequency
        either for the phase or for the amplitude.

        Parameters
        ----------
        pac : array_like
            Pac array of shape (namp, npha)
        fvec : array_like
            The frequency vector returned by the pac_trivec function.
        tridx : array_like
            The index vector used to build the triangle. This argument is
            also returned by the pac_trivec function.
        xlabel : string | 'Starting frequency (hz)'
            Label for the phase axis.
        ylabel : string | 'Ending frequency (hz)'
            Label for the amplitude axis.
        cblabel : string | 'PAC values'
            Colorbar.
        bad : string | 'lightgray'
            Color for non-significant values.
        kwargs : dict
            Further arguments are passed to the pacplot() method.

        Returns
        -------
        gca : axes
            The current matplotlib axes.
        """
        pac, tridx = np.squeeze(pac), np.squeeze(tridx)
        if pac.ndim is not 1:
            raise ValueError('The PAC variable must be a row vector.')
        if len(pac) != tridx.shape[0]:
            raise ValueError('PAC and tridx variables must have the same length.')
        npac = tridx.max() + 2
        rpac = np.zeros((npac, npac), dtype=float)
        for num, k in enumerate(tridx):
            rpac[(k[0], k[1])] = pac[num]

        mask = np.zeros_like(rpac, dtype=bool)
        mask[np.triu_indices_from(mask)] = True
        rpac = np.ma.masked_array((np.flipud(rpac)), mask=mask)
        vector = fvec[(tridx[:, 0] == 0, 0)]
        xvec = yvec = np.append(vector, [fvec.max()])
        self._autovmM = False
        return (self.pacplot)(rpac, xvec, yvec, xlabel, ylabel, cblabel, bad=bad, **kwargs)


class _PolarPlt(_PacVisual):
    __doc__ = 'Plotting class for :class:`tensorpac.PreferredPhase`.'

    def polar(self, amp, xvec, yvec, interp=None, **kwargs):
        """Polar representation.

        This method is used to visualize amplitude as a function of phase using
        a polar (circle) representation.

        Parameters
        ----------
        amp : array_like
            2D array.
        xvec : array_like
            Vector for the x-axis.
        yvec : array_like
            Vector for the y-axis (phases).
        interp : float | None
            Interplation factor.
        kwargs : dict
            Further arguments are passed to the pacplot() method.

        Returns
        -------
        gca : axes
            The current matplotlib axes.
        """
        if interp is not None:
            amp, yvec, xvec = mapinterpolation(amp, yvec, xvec, interp, 1)
        self._autovmM = False
        return (self.pacplot)(amp, xvec, yvec, polar=True, **kwargs)


def mapinterpolation(data, x=None, y=None, interpx=1, interpy=1):
    """Interpolate a 2D map."""
    dim2, dim1 = data.shape
    if x is None:
        x = np.arange(0, dim1, interpx)
    if y is None:
        y = np.arange(0, dim2, interpy)
    xi, yi = np.meshgrid(np.arange(0, dim1 - 1, interpx), np.arange(0, dim2 - 1, interpy))
    datainterp = interp2(data, xi, yi)
    xveci = np.linspace(x[0], x[(-1)], datainterp.shape[0])
    yveci = np.linspace(y[0], y[(-1)], datainterp.shape[1])
    return (datainterp, xveci, yveci)


def interp2(z, xi, yi, extrapval=0):
    """Linear interpolation.

    This function is equivalent to interp2(z, xi, yi,'linear') in Matlab.

    Parameters
    ----------
    z : array_like
        Array to interpolate.
    xi : array_like
        Array of x coordinates where interpolation is required.
    yi : array_like
        Array of y coordinates where interpolation is required.
    extrapval : float | 0.
        Value for out of range positions.

    Returns
    -------
        f: array_like
            Extrapolated data.
    """
    x = xi.copy()
    y = yi.copy()
    nrows, ncols = z.shape
    if nrows < 2 or ncols < 2:
        raise Exception('z shape is too small')
    if not x.shape == y.shape:
        raise Exception('sizes of X indexes and Y-indexes must match')
    x_bad = (x < 0) | (x > ncols - 1)
    if x_bad.any():
        x[x_bad] = 0
    y_bad = (y < 0) | (y > nrows - 1)
    if y_bad.any():
        y[y_bad] = 0
    ndx = np.floor(y) * ncols + np.floor(x)
    ndx = ndx.astype('int32')
    d = x == ncols - 1
    x = x - np.floor(x)
    if d.any():
        x[d] += 1
        ndx[d] -= 1
    d = y == nrows - 1
    y = y - np.floor(y)
    if d.any():
        y[d] += 1
        ndx[d] -= ncols
    one_minus_t = 1 - y
    z = z.ravel()
    f = (z[ndx] * one_minus_t + z[(ndx + ncols)] * y) * (1 - x) + (z[(ndx + 1)] * one_minus_t + z[(ndx + ncols + 1)] * y) * x
    if x_bad.any():
        f[x_bad] = extrapval
    if y_bad.any():
        f[y_bad] = extrapval
    return f