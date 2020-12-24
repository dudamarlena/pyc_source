# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/utils.py
# Compiled at: 2019-10-16 04:45:09
# Size of source mod 2**32: 14830 bytes
"""Utility functions."""
import logging, numpy as np
from scipy.signal import periodogram
from tensorpac.methods.meth_pac import _kl_hr
from tensorpac.pac import _PacObj
logger = logging.getLogger('tensorpac')

def pac_vec(f_pha=(2, 30, 2, 1), f_amp=(60, 200, 10, 5)):
    """Generate cross-frequency coupling vectors.

    Parameters
    ----------
    f_pha, f_amp : tuple | (2, 30, 2, 1), (60, 200, 10, 5)
        Frequency parameters for phase and amplitude. Each argument inside the
        tuple mean (starting fcy, ending fcy, bandwidth, step).

    Returns
    -------
    f_pha, f_amp : array_like
        Arrays containing the pairs of phase and amplitude frequencies. Each
        vector have a shape of (N, 2).
    """
    if isinstance(f_pha, str):
        if f_pha == 'lres':
            f_pha = (2, 30, 2, 2)
    elif f_pha == 'mres':
        f_pha = (2, 30, 2, 1)
    else:
        if f_pha == 'hres':
            f_pha = (2, 30, 1, 0.5)
        elif isinstance(f_amp, str):
            if f_amp == 'lres':
                f_amp = (60, 160, 10, 10)
            else:
                if f_amp == 'mres':
                    f_amp = (60, 160, 5, 4)
                else:
                    if f_amp == 'hres':
                        f_amp = (60, 160, 4, 2)
    return (
     _check_freq(f_pha), _check_freq(f_amp))


def _check_freq(f):
    """Check the frequency definition."""
    f = np.atleast_2d(np.asarray(f))
    if len(f.reshape(-1)) == 1:
        raise ValueError('The length of f should at least be 2.')
    else:
        if 2 in f.shape:
            if f.shape[1] is not 2:
                f = f.T
        elif np.squeeze(f).shape == (4, ):
            f = _pair_vectors(*tuple(np.squeeze(f)))
        else:
            f = f.reshape(-1)
            f.sort()
            f = np.c_[(f[0:-1], f[1:])]
    return f


def _pair_vectors(f_start, f_end, f_width, f_step):
    fdown = np.arange(f_start, f_end - f_width, f_step)
    fup = np.arange(f_start + f_width, f_end, f_step)
    return np.c_[(fdown, fup)]


def pac_trivec(f_start=60.0, f_end=160.0, f_width=10.0):
    """Generate triangular vector.

    By contrast with the pac_vec function, this function generate frequency
    vector with an increasing frequency bandwidth.

    Parameters
    ----------
    f_start : float | 60.
        Starting frequency.
    f_end : float | 160.
        Ending frequency.
    f_width : float | 10.
        Frequency bandwidth increase between each band.

    Returns
    -------
    f : array_like
        The triangular vector.
    tridx : array_like
        The triangular index for the reconstruction.
    """
    starting = np.arange(f_start, f_end + f_width, f_width)
    f, tridx = np.array([]), np.array([])
    for num, k in enumerate(starting[0:-1]):
        le = len(starting) - (num + 1)
        fst = np.c_[(np.full(le, k), starting[num + 1:])]
        nfst = fst.shape[0]
        idx = np.c_[(np.flipud(np.arange(nfst)), np.full(nfst, num))]
        tridx = np.concatenate((tridx, idx), axis=0) if tridx.size else idx
        f = np.concatenate((f, fst), axis=0) if f.size else fst

    return (
     f, tridx)


class PSD(object):
    __doc__ = 'Power Spectrum Density for electrophysiological brain data.\n\n    Parameters\n    ----------\n    x : array_like\n        Array of data of shape (n_epochs, n_times)\n    sf : float\n        The sampling frequency.\n    '

    def __init__(self, x, sf):
        """Init."""
        if not (isinstance(x, np.ndarray) and x.ndim == 2):
            raise AssertionError('x should be a 2d array of shape (n_epochs, n_times)')
        self._n_trials, self._n_times = x.shape
        logger.info(f"Compute PSD over {self._n_trials} trials and {self._n_times} time points")
        self._freqs, self._psd = periodogram(x, fs=sf, window=None, nfft=(self._n_times),
          detrend='constant',
          return_onesided=True,
          scaling='density',
          axis=1)

    def plot(self, f_min=None, f_max=None, confidence=95, interp=None, log=False, grid=True):
        """Plot the PSD.

        Parameters
        ----------
        f_min, f_max : (int, float) | None
            Frequency bounds to use for plotting
        confidence : (int, float) | None
            Light gray confidence interval. If None, no interval will be
            displayed
        interp : int | None
            Line interpolation integer. For example, if interp is 10 the number
            of points is going to be multiply by 10
        log : bool | False
            Use a log scale representation
        grid : bool | True
            Add a grid to the plot

        Returns
        -------
        ax : Matplotlib axis
            The matplotlib axis that contains the figure
        """
        import matplotlib.pyplot as plt
        f_types = (
         int, float)
        xvec, yvec = self._freqs, self._psd
        if isinstance(interp, int):
            if interp > 1:
                from scipy.interpolate import interp1d
                xnew = np.linspace(xvec[0], xvec[(-1)], len(xvec) * interp)
                f = interp1d(xvec, yvec, kind='quadratic', axis=1)
                yvec = f(xnew)
                xvec = xnew
        f_min = xvec[0] if not isinstance(f_min, f_types) else f_min
        f_max = xvec[(-1)] if not isinstance(f_max, f_types) else f_max
        plt.plot(xvec, (yvec.mean(0)), color='black', label='mean PSD over trials')
        if isinstance(confidence, (int, float)):
            if 0 < confidence < 100:
                logger.info(f"    Add {confidence}th confidence interval")
                interval = (100.0 - confidence) / 2
                kw = dict(axis=0, interpolation='nearest')
                psd_min = (np.percentile)(yvec, interval, **kw)
                psd_max = (np.percentile)(yvec, (100.0 - interval), **kw)
                plt.fill_between(xvec, psd_max, psd_min, color='lightgray', alpha=0.5,
                  label=f"{confidence}th confidence interval")
                plt.legend()
        (
         plt.xlabel('Frequencies (Hz)'), plt.ylabel('Power (V**2/Hz)'))
        plt.title(f"PSD mean over {self._n_trials} trials")
        plt.xlim(f_min, f_max)
        if log:
            from matplotlib.ticker import ScalarFormatter
            plt.xscale('log', basex=10)
            plt.gca().xaxis.set_major_formatter(ScalarFormatter())
        if grid:
            plt.grid(color='grey', which='major', linestyle='-', linewidth=1.0,
              alpha=0.5)
            plt.grid(color='lightgrey', which='minor', linestyle='--', linewidth=0.5,
              alpha=0.5)
        return plt.gca()

    def show(self):
        """Display the PSD figure."""
        import matplotlib.pyplot as plt
        plt.show()

    @property
    def freqs(self):
        """Get the frequency vector."""
        return self._freqs

    @property
    def psd(self):
        """Get the psd value."""
        return self._psd


class BinAmplitude(_PacObj):
    __doc__ = "Bin the amplitude according to the phase.\n\n    Parameters\n    ----------\n    x : array_like\n        Array of data of shape (n_epochs, n_times)\n    sf : float\n        The sampling frequency\n    f_pha : tuple, list | [2, 4]\n        List of two floats describing the frequency bounds for extracting the\n        phase\n    f_amp : tuple, list | [60, 80]\n        List of two floats describing the frequency bounds for extracting the\n        amplitude\n    n_bins : int | 18\n        Number of bins to use to binarize the phase and the amplitude\n    dcomplex : {'wavelet', 'hilbert'}\n        Method for the complex definition. Use either 'hilbert' or\n        'wavelet'.\n    cycle : tuple | (3, 6)\n        Control the number of cycles for filtering (only if dcomplex is\n        'hilbert'). Should be a tuple of integers where the first one\n        refers to the number of cycles for the phase and the second for the\n        amplitude [#f5]_.\n    width : int | 7\n        Width of the Morlet's wavelet.\n    edges : int | None\n        Number of samples to discard to avoid edge effects due to filtering\n    "

    def __init__(self, x, sf, f_pha=[
 2, 4], f_amp=[60, 80], n_bins=18, dcomplex='hilbert', cycle=(3, 6), width=7, edges=None, n_jobs=-1):
        """Init."""
        _PacObj.__init__(self, f_pha=f_pha, f_amp=f_amp, dcomplex=dcomplex, cycle=cycle,
          width=width)
        x = np.atleast_2d(x)
        assert x.ndim <= 2, '`x` input should be an array of shape (n_epochs, n_times)'
        assert isinstance(sf, (int, float)), '`sf` input should be a integer or a float'
        assert all([isinstance(k, (int, float)) for k in f_pha]), '`f_pha` input should be a list of two integers / floats'
        assert all([isinstance(k, (int, float)) for k in f_amp]), '`f_amp` input should be a list of two integers / floats'
        assert isinstance(n_bins, int), '`n_bins` should be an integer'
        kw = dict(keepfilt=False, edges=edges, n_jobs=n_jobs)
        pha = (self.filter)(sf, x, 'phase', **kw)
        amp = (self.filter)(sf, x, 'amplitude', **kw)
        self._amplitude = _kl_hr(pha, amp, n_bins, mean_bins=False).squeeze()
        self.n_bins = n_bins

    def plot(self, unit='rad', **kw):
        """Plot the amplitude.

        Parameters
        ----------
        unit : {'rad', 'deg'}
            The unit to use for the phase. Use either 'deg' for degree or 'rad'
            for radians
        kw : dict | {}
            Additional inputs are passed to the matplotlib.pyplot.bar function

        Returns
        -------
        ax : Matplotlib axis
            The matplotlib axis that contains the figure
        """
        import matplotlib.pyplot as plt
        if not unit in ('rad', 'deg'):
            raise AssertionError
        elif unit == 'rad':
            self._phase = np.linspace(-np.pi, np.pi, self.n_bins)
            width = 2 * np.pi / self.n_bins
        else:
            if unit == 'deg':
                self._phase = np.linspace(-180, 180, self.n_bins)
                width = 360 / self.n_bins
        (plt.bar)(self._phase, self._amplitude.mean(1), width=width, **kw)
        plt.xlabel(f"Frequency phase ({self.n_bins} bins)")
        plt.ylabel('Amplitude')
        plt.title('Binned amplitude')
        plt.autoscale(enable=True, axis='x', tight=True)

    def show(self):
        """Show the figure."""
        import matplotlib.pyplot as plt
        plt.show()

    @property
    def amplitude(self):
        """Get the amplitude value."""
        return self._amplitude

    @property
    def phase(self):
        """Get the phase value."""
        return self._phase


class PLV(_PacObj):
    __doc__ = "Compute the Phase Locking Value (PLV).\n\n    The Phase Locking Value (PLV) can be used to measure the phase synchrony\n    across trials [#f1]_\n\n    Parameters\n    ----------\n    x : array_like\n        Array of data of shape (n_epochs, n_times)\n    sf : float\n        The sampling frequency\n    f_pha : tuple, list | [2, 4]\n        List of two floats describing the frequency bounds for extracting the\n        phase\n    dcomplex : {'wavelet', 'hilbert'}\n        Method for the complex definition. Use either 'hilbert' or\n        'wavelet'.\n    cycle : tuple | 3\n        Control the number of cycles for filtering the phase (only if dcomplex\n        is 'hilbert').\n    width : int | 7\n        Width of the Morlet's wavelet.\n    edges : int | None\n        Number of samples to discard to avoid edge effects due to filtering\n\n    References\n    ----------\n    .. [#f1] `Lachaux et al, 1999 <https://onlinelibrary.wiley.com/doi/abs/10.\n       1002/(SICI)1097-0193(1999)8:4%3C194::AID-HBM4%3E3.0.CO;2-C>`_\n    "

    def __init__(self, x, sf, f_pha=[
 2, 4], dcomplex='hilbert', cycle=3, width=7, edges=None, n_jobs=-1):
        """Init."""
        _PacObj.__init__(self, f_pha=f_pha, f_amp=[60, 80], dcomplex=dcomplex, cycle=(
         cycle, 6),
          width=width)
        x = np.atleast_2d(x)
        assert x.ndim <= 2, '`x` input should be an array of shape (n_epochs, n_times)'
        self._n_trials = x.shape[0]
        kw = dict(keepfilt=False, edges=edges, n_jobs=n_jobs)
        pha = (self.filter)(sf, x, 'phase', **kw)
        self._plv = np.abs(np.exp(complex(0.0, 1.0) * pha).mean(1)).squeeze()
        self._sf = sf

    def plot(self, time=None, **kw):
        """Plot the Phase Locking Value.

        Parameters
        ----------
        time : array_like | None
            Custom time vector to use
        kw : dict | {}
            Additional inputs are either pass to the matplotlib.pyplot.plot
            function if a single phase band is used, otherwise to the
            matplotlib.pyplot.pcolormesh function

        Returns
        -------
        ax : Matplotlib axis
            The matplotlib axis that contains the figure
        """
        import matplotlib.pyplot as plt
        n_pts = self._plv.shape[(-1)]
        if not isinstance(time, np.ndarray):
            time = np.arange(n_pts) / self._sf
        else:
            time = time[self._edges]
            assert len(time) == n_pts, 'The length of the time vector should be {n_pts}'
            if self._plv.ndim == 1:
                (plt.plot)(time, (self._plv), **kw)
            else:
                if self._plv.ndim == 2:
                    vmin = kw.get('vmin', np.percentile(self._plv, 1))
                    vmax = kw.get('vmax', np.percentile(self._plv, 99))
                    (plt.pcolormesh)(time, self.xvec, self._plv, vmin=vmin, vmax=vmax, **kw)
                    plt.colorbar()
                    plt.ylabel('Frequency for phase (Hz)')
        plt.xlabel('Time')
        plt.title(f"Phase Locking Value across {self._n_trials} trials")
        return plt.gca()

    def show(self):
        """Show the figure."""
        import matplotlib.pyplot as plt
        plt.show()

    @property
    def plv(self):
        """Get the plv value."""
        return self._plv