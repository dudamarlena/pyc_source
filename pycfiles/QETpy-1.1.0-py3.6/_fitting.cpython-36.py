# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qetpy/core/_fitting.py
# Compiled at: 2019-02-07 14:38:29
# Size of source mod 2**32: 73559 bytes
import numpy as np
from scipy.optimize import least_squares
import numpy as np
from numpy.fft import rfft, fft, ifft, fftfreq, rfftfreq
from qetpy.plotting import plotnonlin
__all__ = ['OptimumFilter', 'ofamp', 'ofamp_pileup', 'ofamp_pileup_stationary', 'chi2lowfreq',
 'chi2_nopulse', 'OFnonlin', 'MuonTailFit']

def _argmin_chi2(chi2, nconstrain=None, lgcoutsidewindow=False, constraint_mask=None):
    """
    Helper function for finding the index for the minimum of a chi^2. Includes
    options for constraining the values of chi^2.
    
    Parameters
    ----------
    chi2 : ndarray
        An array containing the chi^2 to minimize. If `chi2` has dimension greater
        than 1, then it is minimized along the last axis.
    nconstrain : NoneType, int, optional
        This is the length of the window (in bins) out of which to constrain the 
        possible values to in the chi^2 minimization, centered on the middle value 
        of `chi2`. Default is None, where `chi2` is uncontrained.
    lgcoutsidewindow : bool, optional
        If False, then the function will minimize the chi^2 in the bins inside the 
        constrained window specified by `nconstrain`, which is the default behavior.
        If True, the function will minimize the chi^2 in the bins outside the range 
        specified by `nconstrain`.
    constraint_mask : NoneType, boolean ndarray, optional
        An additional constraint on the chi^2 to apply, which should be in the form 
        of a boolean mask. If left as None, no additional constraint is applied.
    
    Returns
    -------
    bestind : int, ndarray, float
        The index of the minimum of `chi2` given the constraints specified by 
        `nconstrain` and `lgcoutsidewindow`. If the dimension of `chi2` is greater
        than 1, then this will be an ndarray of ints.
    
    """
    nbins = chi2.shape[(-1)]
    if nconstrain is not None:
        if nconstrain > nbins:
            nconstrain = nbins
        else:
            if nconstrain <= 0:
                raise ValueError(f"nconstrain must be a positive integer less than {nbins}")
            if lgcoutsidewindow:
                inds = np.r_[0:nbins // 2 - nconstrain // 2, -nbins // 2 + nconstrain // 2 + nconstrain % 2:0]
                inds[(inds < 0)] += nbins
            else:
                inds = np.arange(nbins // 2 - nconstrain // 2, nbins // 2 + nconstrain // 2 + nconstrain % 2)
        if constraint_mask is not None:
            inds = inds[constraint_mask[inds]]
        if len(inds) != 0:
            bestind = np.argmin((chi2[(..., inds)]), axis=(-1))
            bestind = inds[bestind]
        else:
            bestind = np.nan
    else:
        if constraint_mask is None:
            bestind = np.argmin(chi2, axis=(-1))
        else:
            inds = np.flatnonzero(constraint_mask)
            if len(inds) != 0:
                bestind = np.argmin((chi2[(..., constraint_mask)]), axis=(-1))
                bestind = inds[bestind]
            else:
                bestind = np.nan
        return bestind


def _get_pulse_direction_constraint_mask(amps, pulse_direction_constraint=0):
    """
    Helper function for returning the constraint mask for positive or negative only
    going pulses.
    
    Parameters
    ----------
    amps : ndarray
        Array of the OF amplitudes to use when getting the constraint_mask.
    pulse_direction_constraint : int, optional
        Sets a constraint on the direction of the fitted pulse. If 0, then no constraint on the 
        pulse direction is set. If 1, then a positive pulse constraint is set for all fits. 
        If -1, then a negative pulse constraint is set for all fits. If any other value, then
        an ValueError will be raised.
        
    Returns
    -------
    constraint_mask : NoneType, ndarray
        If not constraint is set, this is set to None. If `pulse_direction_constraint` is 1 or -1, 
        then this is the boolean array of the constraint.
        
    """
    if pulse_direction_constraint == 0:
        constraint_mask = None
    else:
        if pulse_direction_constraint == 1:
            constraint_mask = amps > 0
        else:
            if pulse_direction_constraint == -1:
                constraint_mask = amps < 0
            else:
                raise ValueError('pulse_direction_constraint should be set to 0, 1, or -1')
    return constraint_mask


class OptimumFilter(object):
    __doc__ = '\n    Class for efficient calculation of the various different Optimum Filters. Written to minimize the\n    amount of repeated computations when running multiple on the same data.\n    \n    Attributes\n    ----------\n    psd : ndarray\n        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz)\n    psd0 : float\n        The value of the inputted PSD at the zero frequency bin. Used for ofamp_baseline in the\n        case that `OptimumFilter` is initialized with "AC" coupling.\n    nbins : int\n        The length of the trace/psd/template in bins.\n    fs : float\n        The sample rate of the data being taken (in Hz).\n    df : float\n        Equivalent to df/nbins, the frequency spacing of the Fourier Tranforms.\n    s : ndarray\n        The template converted to frequency space, with the normalization specified \n        by the `integralnorm` parameter in the initialization.\n    phi : ndarray\n        The optimum filter in frequency space.\n    norm : float\n        The normalization for the optimum filtered signal.\n    v : ndarray\n        The signal converted to frequency space.\n    signalfilt : ndarray\n        The optimum filtered signal in frequency space.\n    chi0 : float\n        The chi^2 value for just the signal part.\n    chit_withdelay : ndarray\n        The fitting part of the chi^2 for `ofamp_withdelay`.\n    amps_withdelay : ndarray\n        The possible amplitudes for `ofamp_withdelay`.\n    chi_withdelay : ndarray\n        The full chi^2 for `ofamp_withdelay`.\n    signalfilt_td : ndarray\n        The filtered signal converted back to time domain.\n    templatefilt_td : ndarray\n        The filtered template converted back to time domain.\n    times : ndarray\n        The possible time shift values.\n    freqs : ndarray\n        The frequencies matching the Fourier Transform of the data.\n    \n    '

    def __init__(self, signal, template, psd, fs, coupling='AC', integralnorm=False):
        """
        Initialization of the OptimumFilter class.
        
        Parameters
        ----------
        signal : ndarray
            The signal that we want to apply the optimum filter to (units should be Amps).
        template : ndarray
            The pulse template to be used for the optimum filter (should be normalized
            to a max height of 1 beforehand).
        psd : ndarray
            The two-sided psd that will be used to describe the noise in the 
            signal (in Amps^2/Hz)
        fs : ndarray
            The sample rate of the data being taken (in Hz).
        coupling : str, optional
            String that determines if the zero frequency bin of the psd should be 
            ignored (i.e. set to infinity) when calculating the optimum amplitude. 
            If set to 'AC', then ths zero frequency bin is ignored. If set to anything
            else, then the zero frequency bin is kept. Default is 'AC'.
        integralnorm : bool, optional
            If set to True, then `OptimumFilter` will normalize the template to an integral of 1,
            and any optimum filters will instead return the optimum integral in units of Coulombs. 
            If set to False, then the usual optimum filter amplitudes will be returned (in units 
            of Amps).
        
        """
        self.psd = np.zeros(len(psd))
        self.psd[:] = psd
        self.psd0 = psd[0]
        if coupling == 'AC':
            self.psd[0] = np.inf
        self.nbins = signal.shape[(-1)]
        self.fs = fs
        self.df = self.fs / self.nbins
        self.s = fft(template) / self.nbins / self.df
        if integralnorm:
            self.s /= self.s[0]
        self.phi = self.s.conjugate() / self.psd
        self.norm = np.real(np.dot(self.phi, self.s)) * self.df
        self.v = fft(signal, axis=(-1)) / self.nbins / self.df
        self.signalfilt = self.phi * self.v / self.norm
        self.chi0 = None
        self.chit_withdelay = None
        self.amps_withdelay = None
        self.chi_withdelay = None
        self.signalfilt_td = None
        self.templatefilt_td = None
        self.times = None
        self.freqs = None

    def update_signal(self, signal):
        """
        Method to update `OptimumFilter` with a new signal if the PSD and template
        are to remain the same.
        
        Parameters
        ----------
        signal : ndarray
            The signal that we want to apply the optimum filter to (units should be Amps).
        
        """
        self.v = fft(signal, axis=(-1)) / self.nbins / self.df
        self.signalfilt = self.phi * self.v / self.norm
        self.chi0 = None
        self.chit_withdelay = None
        self.signalfilt_td = None
        self.amps_withdelay = None
        self.chi_withdelay = None

    def energy_resolution(self):
        """
        Method to return the energy resolution for the optimum filter.
        
        Returns
        -------
        sigma : float
            The energy resolution of the optimum filter.
        
        """
        sigma = 1.0 / np.sqrt(self.norm)
        return sigma

    def time_resolution(self, amp):
        """
        Method to return the time resolution for the optimum filter for a specific fit.
        
        Parameters
        ----------
        amp : float
            The OF amplitude of the fit to use in the time resolution calculation.
            
        Returns
        -------
        sigma : float
            The time resolution of the optimum filter.
            
        """
        if self.freqs is None:
            self.freqs = fftfreq((self.nbins), d=(1.0 / self.fs))
        sigma = 1.0 / np.sqrt(amp ** 2 * np.sum((2 * np.pi * self.freqs) ** 2 * np.abs(self.s) ** 2 / self.psd) * self.df)
        return sigma

    def chi2_nopulse(self):
        """
        Method to return the chi^2 for there being no pulse in the signal.
        
        Returns
        -------
        chi0 : float
            The chi^2 value for there being no pulse.
        
        """
        if self.chi0 is None:
            self.chi0 = np.real(np.dot(self.v.conjugate() / self.psd, self.v) * self.df)
        return self.chi0

    def chi2_lowfreq(self, amp, t0, fcutoff=10000):
        """
        Method for calculating the low frequency chi^2 of the optimum filter, 
        given some cut off frequency.

        Parameters
        ----------
        amp : float
            The optimum amplitude calculated for the trace (in Amps).
        t0 : float
            The time shift calculated for the pulse (in s).
        fcutoff : float, optional
            The frequency (in Hz) that we should cut off the chi^2 when 
            calculating the low frequency chi^2. Default is 10 kHz.

        Returns
        -------
        chi2low : float
            The low frequency chi^2 value (cut off at fcutoff) for the inputted values.

        """
        if self.freqs is None:
            self.freqs = fftfreq((self.nbins), d=(1.0 / self.fs))
        chi2tot = self.df * np.abs(self.v - amp * np.exp(complex(-0.0, -2.0) * np.pi * t0 * self.freqs) * self.s) ** 2 / self.psd
        chi2inds = np.abs(self.freqs) <= fcutoff
        chi2low = np.sum(chi2tot[chi2inds])
        return chi2low

    def ofamp_nodelay(self):
        """
        Function for calculating the optimum amplitude of a pulse in data with no time
        shifting.
        
        Returns
        -------
        amp : float
            The optimum amplitude calculated for the trace (in Amps) with no time shifting
            allowed.
        chi2 : float
            The chi^2 value calculated from the optimum filter with no time shifting.

        """
        amp = np.real(np.sum((self.signalfilt), axis=(-1))) * self.df
        if self.chi0 is None:
            self.chi0 = np.real(np.dot(self.v.conjugate() / self.psd, self.v) * self.df)
        chit = amp ** 2 * self.norm
        chi2 = self.chi0 - chit
        return (
         amp, chi2)

    def ofamp_withdelay(self, nconstrain=None, lgcoutsidewindow=False, pulse_direction_constraint=0):
        """
        Function for calculating the optimum amplitude of a pulse in data with time delay.

        Parameters
        ----------
        nconstrain : int, NoneType, optional
            The length of the window (in bins) to constrain the possible t0 values to, 
            centered on the unshifted trigger. If left as None, then t0 is uncontrained. 
            If `nconstrain` is larger than `self.nbins`, then the function sets `nconstrain` 
            to `self.nbins`, as this is the maximum number of values that t0 can vary over.
        lgcoutsidewindow : bool, optional
            Boolean flag that is used to specify whether the Optimum Filter should look inside 
            `nconstrain` or outside it. If False, the filter will minimize the chi^2 in the 
            bins specified by `nconstrain`, which is the default behavior. If True, then it 
            will minimize the chi^2 in the bins that do not contain the constrained window.
        pulse_direction_constraint : int, optional
            Sets a constraint on the direction of the fitted pulse. If 0, then no constraint on the 
            pulse direction is set. If 1, then a positive pulse constraint is set for all fits. 
            If -1, then a negative pulse constraint is set for all fits. If any other value, then
            an ValueError will be raised.
            
        Returns
        -------
        amp : float
            The optimum amplitude calculated for the trace (in Amps).
        t0 : float
            The time shift calculated for the pulse (in s).
        chi2 : float
            The chi^2 value calculated from the optimum filter.

        """
        if self.signalfilt_td is None:
            self.signalfilt_td = np.real(ifft((self.signalfilt * self.nbins), axis=(-1))) * self.df
        else:
            if self.chi0 is None:
                self.chi0 = np.real(np.dot(self.v.conjugate() / self.psd, self.v) * self.df)
            else:
                if self.chit_withdelay is None:
                    self.chit_withdelay = self.signalfilt_td ** 2 * self.norm
                if self.chi_withdelay is None:
                    chi = self.chi0 - self.chit_withdelay
                    self.chi_withdelay = np.roll(chi, (self.nbins // 2), axis=(-1))
                if self.amps_withdelay is None:
                    self.amps_withdelay = np.roll((self.signalfilt_td), (self.nbins // 2), axis=(-1))
            constraint_mask = _get_pulse_direction_constraint_mask((self.amps_withdelay), pulse_direction_constraint=pulse_direction_constraint)
            bestind = _argmin_chi2((self.chi_withdelay), nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow,
              constraint_mask=constraint_mask)
            if np.isnan(bestind):
                amp = 0.0
                t0 = 0.0
                chi2 = self.chi0
            else:
                amp = self.amps_withdelay[bestind]
            t0 = (bestind - self.nbins // 2) / self.fs
            chi2 = self.chi_withdelay[bestind]
        return (amp, t0, chi2)

    def ofamp_pileup_iterative(self, a1, t1, nconstrain=None, lgcoutsidewindow=True, pulse_direction_constraint=0):
        """
        Function for calculating the optimum amplitude of a pileup pulse in data given
        the location of the triggered pulse.

        Parameters
        ----------
        a1 : float
            The OF amplitude (in Amps) to use for the "main" pulse, e.g. the triggered pulse.
        t1 : float
            The corresponding time offset (in seconds) to use for the "main" pulse, e.g. the 
            triggered pulse.
        nconstrain : int, NoneType, optional
            This is the length of the window (in bins) out of which to constrain the possible 
            t2 values to for the pileup pulse, centered on the unshifted trigger. If left as 
            None, then t2 is uncontrained. The value of nconstrain2 should be less than nbins.
        lgcoutsidewindow : bool, optional
            Boolean flag that is used to specify whether `OptimumFilter` should look for the 
            pileup pulse inside the bins specified by `nconstrain` or outside them. If True, 
            the filter will minimize the chi^2 in the bins outside the range specified by
            `nconstrain`, which is the default behavior. If False, then it will minimize the 
            chi^2 in the bins inside the constrained window specified by `nconstrain`.
        pulse_direction_constraint : int, optional
            Sets a constraint on the direction of the fitted pulse. If 0, then no constraint on the 
            pulse direction is set. If 1, then a positive pulse constraint is set for all fits. 
            If -1, then a negative pulse constraint is set for all fits. If any other value, then
            an ValueError will be raised.
            
        Returns
        -------
        a2 : float
            The optimum amplitude calculated for the pileup pulse (in Amps).
        t2 : float
            The time shift calculated for the pileup pulse (in s)
        chi2 : float
            The chi^2 value calculated for the pileup optimum filter.

        """
        if self.freqs is None:
            self.freqs = fftfreq((self.nbins), d=(1.0 / self.fs))
        else:
            if self.signalfilt_td is None:
                self.signalfilt_td = np.real(ifft((self.signalfilt * self.nbins), axis=(-1))) * self.df
            else:
                templatefilt_td = np.real(ifft(np.exp(complex(-0.0, -2.0) * np.pi * self.freqs * t1) * self.phi * self.s * self.nbins)) * self.df
                if self.times is None:
                    self.times = np.arange(-(self.nbins // 2), self.nbins // 2 + self.nbins % 2) / self.fs
                if self.chi0 is None:
                    self.chi0 = np.real(np.dot(self.v.conjugate() / self.psd, self.v)) * self.df
                a2s = self.signalfilt_td - a1 * templatefilt_td / self.norm
                if t1 < 0:
                    t1ind = int(t1 * self.fs + self.nbins)
                else:
                    t1ind = int(t1 * self.fs)
            chit = a1 ** 2 * self.norm - 2 * a1 * self.signalfilt_td[t1ind] * self.norm
            chil = a2s ** 2 * self.norm + 2 * a1 * a2s * templatefilt_td - 2 * a2s * self.signalfilt_td * self.norm
            chi = self.chi0 + chit + chil
            a2s = np.roll(a2s, self.nbins // 2)
            chi = np.roll(chi, self.nbins // 2)
            constraint_mask = _get_pulse_direction_constraint_mask(a2s, pulse_direction_constraint=pulse_direction_constraint)
            bestind = _argmin_chi2(chi, nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow,
              constraint_mask=constraint_mask)
            if np.isnan(bestind):
                a2 = 0.0
                t2 = 0.0
                chi2 = self.chi0 + chit
            else:
                a2 = a2s[bestind]
            t2 = self.times[bestind]
            chi2 = chi[bestind]
        return (a2, t2, chi2)

    def ofamp_pileup_stationary(self, nconstrain=None, lgcoutsidewindow=True):
        """
        Function for calculating the optimum amplitude of a pileup pulse in data, with the assumption
        that the triggered pulse is centered in the trace.

        Parameters
        ----------
        nconstrain : int, optional
            This is the length of the window (in bins) out of which to constrain the possible 
            t2 values to for the pileup pulse, centered on the unshifted trigger. If left as None, 
            then t2 is uncontrained. The value of nconstrain should be less than nbins.
        lgcoutsidewindow : bool, optional
            Boolean flag that is used to specify whether the filter should look for the pileup 
            pulse inside the bins specified by `nconstrain` or outside them. If True, the filter will 
            minimize the chi^2 in the bins outside the range specified by `nconstrain`, which is the 
            default behavior. If False, then it will minimize the chi^2 in the bins inside the 
            constrained window specified by nconstrain.
            
        Returns
        -------
        a1 : float
            The optimum amplitude (in Amps) calculated for the first pulse that was found, which
            is the triggered pulse.
        a2 : float
            The optimum amplitude calculated for the pileup pulse (in Amps).
        t2 : float
            The time shift calculated for the pileup pulse (in s)
        chi2 : float
            The reduced chi^2 value of the fit.

        """
        if self.signalfilt_td is None:
            self.signalfilt_td = np.real(ifft(self.signalfilt * self.nbins)) * self.df
        else:
            templatefilt_td = np.real(ifft(self.phi * self.s * self.nbins)) * self.df
            if self.times is None:
                self.times = np.arange(-(self.nbins // 2), self.nbins // 2 + self.nbins % 2) / self.fs
            denom = self.norm ** 2 - templatefilt_td ** 2
            a1s = np.zeros(self.nbins)
            a2s = np.zeros(self.nbins)
            a1s[1:] = (self.signalfilt_td[0] * self.norm ** 2 - self.signalfilt_td[1:] * self.norm * templatefilt_td[1:]) / denom[1:]
            a2s[1:] = (self.signalfilt_td[1:] * self.norm ** 2 - self.signalfilt_td[0] * self.norm * templatefilt_td[1:]) / denom[1:]
            a1s[0] = self.signalfilt_td[0] / (2 * self.norm)
            a2s[0] = self.signalfilt_td[0] / (2 * self.norm)
            if self.chi0 is None:
                self.chi0 = np.real(np.dot(self.v.conjugate() / self.psd, self.v)) * self.df
        chit = (a1s ** 2 + a2s ** 2) * self.norm + 2 * a1s * a2s * templatefilt_td
        chil = 2 * a1s * self.signalfilt_td[0] * self.norm + 2 * a2s * self.signalfilt_td * self.norm
        chi = self.chi0 + chit - chil
        a1s = np.roll(a1s, self.nbins // 2)
        a2s = np.roll(a2s, self.nbins // 2)
        chi = np.roll(chi, self.nbins // 2)
        bestind = _argmin_chi2(chi, nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow)
        a1 = a1s[bestind]
        a2 = a2s[bestind]
        chi2 = chi[bestind]
        t2 = self.times[bestind]
        return (
         a1, a2, t2, chi2)

    def ofamp_baseline(self, nconstrain=None, lgcoutsidewindow=False, pulse_direction_constraint=0):
        """
        Function for calculating the optimum amplitude of a pulse while taking into account
        the best fit baseline. If the window is constrained, the fit uses the baseline taken 
        from the unconstrained best fit and fixes it when looking elsewhere. This is to 
        reduce the shifting of the best fit amplitudes at times far from the true pulse.

        Parameters
        ----------
        nconstrain : int, NoneType, optional
            The length of the window (in bins) to constrain the possible t0 values to, 
            centered on the unshifted trigger. If left as None, then t0 is uncontrained. 
            If `nconstrain` is larger than `self.nbins`, then the function sets `nconstrain` 
            to `self.nbins`, as this is the maximum number of values that t0 can vary over.
        lgcoutsidewindow : bool, optional
            Boolean flag that is used to specify whether the Optimum Filter should look inside 
            `nconstrain` or outside it. If False, the filter will minimize the chi^2 in the 
            bins specified by `nconstrain`, which is the default behavior. If True, then it 
            will minimize the chi^2 in the bins that do not contain the constrained window.
        pulse_direction_constraint : int, optional
            Sets a constraint on the direction of the fitted pulse. If 0, then no constraint on the 
            pulse direction is set. If 1, then a positive pulse constraint is set for all fits. 
            If -1, then a negative pulse constraint is set for all fits. If any other value, then
            an ValueError will be raised.
            
        Returns
        -------
        amp : float
            The optimum amplitude calculated for the trace (in Amps).
        t0 : float
            The time shift calculated for the pulse (in s).
        chi2 : float
            The chi^2 value calculated from the optimum filter.

        """
        d = 1 / self.df
        if np.isinf(self.psd[0]):
            phi = self.phi.copy()
            phi[0] = self.s[0] / self.psd0
            norm = np.real(np.dot(phi, self.s)) * self.df
        else:
            phi = self.phi
            norm = self.norm
        b1 = np.real(ifft(phi * self.v)) * self.nbins * self.df
        b2 = np.real(phi[0] * d) * self.df
        c1 = np.real(self.v[0] * d / self.psd0) * self.df
        c2 = np.abs(d) ** 2 / self.psd0 * self.df
        amps = (b1 * c2 - b2 * c1) / (norm * c2 - b2 ** 2)
        baselines = (c1 - amps * b2) / c2
        chi2 = np.sum(np.abs(self.v) ** 2 / self.psd) * self.df
        if np.isinf(self.psd[0]):
            chi2 += np.abs(self.v[0]) ** 2 / self.psd0 * self.df
        else:
            chi2 += -2 * (amps * b1 + baselines * c1)
            chi2 += amps ** 2 * norm
            chi2 += 2 * amps * baselines * b2
            chi2 += baselines ** 2 * c2
            bestind = np.argmin(chi2)
            bs = baselines[bestind]
            amps_out = (b1 - bs * b2) / norm
            chi0 = np.sum(np.abs(self.v) ** 2 / self.psd) * self.df
            if np.isinf(self.psd[0]):
                chi0 += np.abs(self.v[0]) ** 2 / self.psd0 * self.df
            chi0 -= 2 * bs * c1
            chi0 += bs ** 2 * c2
            chi2 = chi0 - 2 * amps_out * b1
            chi2 += amps_out ** 2 * norm
            chi2 += 2 * amps_out * bs * b2
            amps_out = np.roll(amps_out, (self.nbins // 2), axis=(-1))
            chi2 = np.roll(chi2, (self.nbins // 2), axis=(-1))
            constraint_mask = _get_pulse_direction_constraint_mask(amps_out, pulse_direction_constraint=pulse_direction_constraint)
            bestind = _argmin_chi2(chi2, nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow,
              constraint_mask=constraint_mask)
            if np.isnan(bestind):
                amp = 0
                t0 = 0
                chi2 = chi0
            else:
                amp = amps_out[bestind]
            t0 = (bestind - self.nbins // 2) / self.fs
            chi2 = chi2[bestind]
        return (amp, t0, chi2)


def ofamp(signal, template, inputpsd, fs, withdelay=True, coupling='AC', lgcsigma=False, nconstrain=None, lgcoutsidewindow=False, integralnorm=False):
    """
    Function for calculating the optimum amplitude of a pulse in data. Supports optimum filtering with
    and without time delay.
    
    Parameters
    ----------
    signal : ndarray
        The signal that we want to apply the optimum filter to (units should be Amps). Can be an array
        of traces.
    template : ndarray
        The pulse template to be used for the optimum filter (should be normalized beforehand).
    inputpsd : ndarray
        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz)
    fs : float
        The sample rate of the data being taken (in Hz).
    withdelay : bool, optional
        Determines whether or not the optimum amplitude should be calculate with (True) or without
        (False) using a time delay. With the time delay, the pulse is assumed to be at any time in the trace.
        Without the time delay, the pulse is assumed to be directly in the middle of the trace. Default
        is True.
    coupling : str, optional
        String that determines if the zero frequency bin of the psd should be ignored (i.e. set to infinity)
        when calculating the optimum amplitude. If set to 'AC', then ths zero frequency bin is ignored. If
        set to anything else, then the zero frequency bin is kept. Default is 'AC'.
    lgcsigma : Boolean, optional
        If True, the estimated optimal filter energy resolution will be calculated and returned.
    nconstrain : int, NoneType, optional
        The length of the window (in bins) to constrain the possible t0 values to, centered on the unshifted 
        trigger. If left as None, then t0 is uncontrained. If nconstrain is larger than nbins, then 
        the function sets nconstrain to nbins, as this is the maximum number of values that t0 can vary
        over.
    lgcoutsidewindow : bool, optional
        Boolean flag that is used to specify whether ofamp should look inside nconstrain or outside it. 
        If False, ofamp will minimize the chi^2 in the bins specified by nconstrain, which is the 
        default behavior. If True, then ofamp will minimize the chi^2 in the bins that do not contain the
        constrained window.
    integralnorm : bool, optional
        If set to True, then ofamp will normalize the template to an integral of 1, and ofamp will instead
        return the optimal integral in units of Coulombs. If lgcsigma is set to True, then it will be 
        returned in units of Coulombs as well. If set to False, then the usual optimal filter amplitude
        will be returned (in units of Amps).

    Returns
    -------
    amp : float
        The optimum amplitude calculated for the trace (in Amps).
    t0 : float
        The time shift calculated for the pulse (in s). Set to zero if withdelay is False.
    chi2 : float
        The chi^2 value calculated from the optimum filter.
    sigma : float, optional
        The optimal filter energy resolution (in Amps)
        
    """
    psd = np.zeros(len(inputpsd))
    psd[:] = inputpsd
    if len(signal.shape) == 1:
        signal = signal[np.newaxis, :]
    nbins = signal.shape[(-1)]
    df = fs / nbins
    v = fft(signal, axis=(-1)) / nbins / df
    s = fft(template) / nbins / df
    if integralnorm:
        s /= s[0]
    if len(psd) != v.shape[(-1)]:
        raise ValueError('PSD length incompatible with signal size')
    if coupling == 'AC':
        psd[0] = np.inf
    else:
        phi = s.conjugate() / psd
        norm = np.real(np.dot(phi, s)) * df
        signalfilt = phi * v / norm
        if lgcsigma:
            sigma = 1 / (np.dot(phi, s).real * df) ** 0.5
        if withdelay:
            amps = np.real(ifft((signalfilt * nbins), axis=(-1))) * df
            chi0 = np.real(np.einsum('ij,ij->i', v.conjugate() / psd, v) * df)
            chit = amps ** 2 * norm
            chi = chi0[:, np.newaxis] - chit
            amps = np.roll(amps, (nbins // 2), axis=(-1))
            chi = np.roll(chi, (nbins // 2), axis=(-1))
            bestind = _argmin_chi2(chi, nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow)
            amp = np.diag(amps[:, bestind])
            chi2 = np.diag(chi[:, bestind])
            t0 = (bestind - nbins // 2) / fs
        else:
            amp = np.real(np.sum(signalfilt, axis=(-1))) * df
        t0 = np.zeros(len(amp))
        chi0 = np.real(np.einsum('ij,ij->i', v.conjugate() / psd, v) * df)
        chit = amp ** 2 * norm
        chi2 = chi0 - chit
    if len(amp) == 1:
        amp = amp[0]
        t0 = t0[0]
        chi2 = chi2[0]
    if lgcsigma:
        return (amp, t0, chi2, sigma)
    else:
        return (
         amp, t0, chi2)


def ofamp_pileup(signal, template, inputpsd, fs, a1=None, t1=None, coupling='AC', nconstrain1=None, nconstrain2=None, lgcoutsidewindow=True):
    """
    Function for calculating the optimum amplitude of a pileup pulse in data. Supports inputted the
    values of a previously known pulse for increased computational speed, but can be used on its
    own.
    
    Parameters
    ----------
    signal : ndarray
        The signal that we want to apply the optimum filter to (units should be Amps).
    template : ndarray
        The pulse template to be used for the optimum filter (should be normalized beforehand).
    inputpsd : ndarray
        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz)
    fs : float
        The sample rate of the data being taken (in Hz).
    a1 : float, optional
        The OF amplitude (in Amps) to use for the "main" pulse, e.g. the triggered pulse. This 
        should be calculated beforehand using ofamp. This is only used if t1 is also inputted.
    t1 : float, optional
        The corresponding time offset (in seconds) to use for the "main" pulse, e.g. the triggered
        pulse. As with a1, this should be calculated beforehand using ofamp. This is only used if a1
        is also inputted.
    coupling : str, optional
        String that determines if the zero frequency bin of the psd should be ignored (i.e. set to infinity)
        when calculating the optimum amplitude. If set to 'AC', then ths zero frequency bin is ignored. If
        set to anything else, then the zero frequency bin is kept. Default is 'AC'.
    nconstrain1 : int, NoneType, optional
        If t1 is left as None, this is the length of the window (in bins) to constrain the possible 
        t1 values to for the first pulse, centered on the unshifted trigger. If left as None, then 
        t1 is uncontrained. If nconstrain1 is larger than nbins, then the function sets nconstrain1 to 
        nbins, as this is the maximum number of values that t1 can vary over. This is only used if
        a1 or t1 is not given.
    nconstrain2 : int, NoneType, optional
        This is the length of the window (in bins) out of which to constrain the possible 
        t2 values to for the pileup pulse, centered on the unshifted trigger. If left as None, then 
        t2 is uncontrained. The value of nconstrain2 should be less than nbins.
    lgcoutsidewindow : bool, optional
        Boolean flag that is used to specify whether ofamp_pileup should look for the pileup pulse inside the
        bins specified by  nconstrain2 or outside them. If True, ofamp will minimize the chi^2 in the bins outside
        the range specified by nconstrain2, which is the default behavior. If False, then ofamp will minimize the
        chi^2 in the bins inside the constrained window specified by nconstrain2.

    Returns
    -------
    a1 : float
        The optimum amplitude (in Amps) calculated for the first pulse that was found, which
        is generally the triggered pulse.
    t1 : float
        The time shift calculated for the first pulse that was found (in s)
    a2 : float
        The optimum amplitude calculated for the pileup pulse (in Amps).
    t2 : float
        The time shift calculated for the pileup pulse (in s)
    chi2 : float
        The chi^2 value calculated for the pileup optimum filter.
        
    """
    psd = np.zeros(len(inputpsd))
    psd[:] = inputpsd
    nbins = len(signal)
    df = fs / nbins
    freqs = fftfreq(nbins, d=(1.0 / fs))
    omega = 2.0 * np.pi * freqs
    if a1 is None or t1 is None:
        a1, t1, _ = ofamp(signal, template, psd, fs, withdelay=True, coupling=coupling,
          nconstrain=nconstrain1)
    v = fft(signal) / nbins / df
    s = fft(template) / nbins / df
    if len(psd) != len(v):
        raise ValueError('PSD length incompatible with signal size')
    else:
        if coupling == 'AC':
            psd[0] = np.inf
        phi = s.conjugate() / psd
        norm = np.real(np.dot(phi, s)) * df
        signalfilt = phi * v / norm
        signalfilt_td = np.real(ifft(signalfilt * nbins)) * df
        templatefilt_td = np.real(ifft(np.exp(complex(-0.0, -1.0) * omega * t1) * phi * s * nbins)) * df
        times = np.arange(-(nbins // 2), nbins // 2 + nbins % 2) / fs
        a2s = signalfilt_td - a1 * templatefilt_td / norm
        chi0 = np.real(np.dot(v.conjugate() / psd, v)) * df
        chit = (a1 ** 2 + a2s ** 2) * norm + 2 * a1 * a2s * templatefilt_td
        if t1 < 0:
            t1ind = int(t1 * fs + nbins)
        else:
            t1ind = int(t1 * fs)
    chil = 2 * a1 * signalfilt_td[t1ind] * norm + 2 * a2s * signalfilt_td * norm
    chi = chi0 + chit - chil
    a2s = np.roll(a2s, nbins // 2)
    chi = np.roll(chi, nbins // 2)
    bestind = _argmin_chi2(chi, nconstrain=nconstrain2, lgcoutsidewindow=lgcoutsidewindow)
    a2 = a2s[bestind]
    chi2 = chi[bestind]
    t2 = times[bestind]
    return (
     a1, t1, a2, t2, chi2)


def ofamp_pileup_stationary(signal, template, inputpsd, fs, coupling='AC', nconstrain=None, lgcoutsidewindow=False):
    """
    Function for calculating the optimum amplitude of a pileup pulse in data, with the assumption
    that the triggered pulse is centered in the trace.
    
    Parameters
    ----------
    signal : ndarray
        The signal that we want to apply the optimum filter to (units should be Amps).
    template : ndarray
        The pulse template to be used for the optimum filter (should be normalized beforehand).
    inputpsd : ndarray
        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz)
    fs : float
        The sample rate of the data being taken (in Hz).
    coupling : str, optional
        String that determines if the zero frequency bin of the psd should be ignored (i.e. set to infinity)
        when calculating the optimum amplitude. If set to 'AC', then ths zero frequency bin is ignored. If
        set to anything else, then the zero frequency bin is kept. Default is 'AC'.
    nconstrain : int, NoneType, optional
        This is the length of the window (in bins) out of which to constrain the possible 
        t2 values to for the pileup pulse, centered on the unshifted trigger. If left as None, then 
        t2 is uncontrained. The value of nconstrain should be less than nbins.
    lgcoutsidewindow : bool, optional
        Boolean flag that is used to specify whether the function should look for the pileup pulse inside the
        bins specified by  nconstrain or outside them. If True, ofamp will minimize the chi^2 in the bins outside
        the range specified by nconstrain, which is the default behavior. If False, then ofamp will minimize the
        chi^2 in the bins inside the constrained window specified by nconstrain.

    Returns
    -------
    a1 : float
        The optimum amplitude (in Amps) calculated for the first pulse that was found, which
        is the triggered pulse.
    a2 : float
        The optimum amplitude calculated for the pileup pulse (in Amps).
    t2 : float
        The time shift calculated for the pileup pulse (in s)
    chi2 : float
        The reduced chi^2 value of the fit.
        
    """
    psd = np.zeros(len(inputpsd))
    psd[:] = inputpsd
    nbins = len(signal)
    df = fs / nbins
    v = fft(signal) / nbins / df
    s = fft(template) / nbins / df
    if len(psd) != len(v):
        raise ValueError('PSD length incompatible with signal size')
    if coupling == 'AC':
        psd[0] = np.inf
    phi = s.conjugate() / psd
    norm = np.real(np.dot(phi, s)) * df
    signalfilt = phi * v / norm
    signalfilt_td = np.real(ifft(signalfilt * nbins)) * df * norm
    templatefilt_td = np.real(ifft(phi * s * nbins)) * df
    times = np.arange(-(nbins // 2), nbins // 2 + nbins % 2) / fs
    denom = norm ** 2 - templatefilt_td ** 2
    a1s = np.zeros(nbins)
    a2s = np.zeros(nbins)
    a1s[1:] = (signalfilt_td[0] * norm - signalfilt_td[1:] * templatefilt_td[1:]) / denom[1:]
    a2s[1:] = (signalfilt_td[1:] * norm - signalfilt_td[0] * templatefilt_td[1:]) / denom[1:]
    a1s[0] = signalfilt_td[0] / (2 * norm ** 2)
    a2s[0] = signalfilt_td[0] / (2 * norm ** 2)
    chi0 = np.real(np.dot(v.conjugate() / psd, v)) * df
    chit = (a1s ** 2 + a2s ** 2) * norm + 2 * a1s * a2s * templatefilt_td
    chil = 2 * a1s * signalfilt_td[0] + 2 * a2s * signalfilt_td
    chi = chi0 + chit - chil
    a1s = np.roll(a1s, nbins // 2)
    a2s = np.roll(a2s, nbins // 2)
    chi = np.roll(chi, nbins // 2)
    bestind = _argmin_chi2(chi, nconstrain=nconstrain, lgcoutsidewindow=lgcoutsidewindow)
    a1 = a1s[bestind]
    a2 = a2s[bestind]
    chi2 = chi[bestind]
    t2 = times[bestind]
    return (
     a1, a2, t2, chi2)


def chi2lowfreq(signal, template, amp, t0, inputpsd, fs, fcutoff=10000, coupling='AC'):
    """
    Function for calculating the low frequency chi^2 of the optimum filter, given some cut off 
    frequency. This function does not calculate the optimum amplitude - it requires that ofamp
    has been run, and the fit has been loaded to this function.
    
    Parameters
    ----------
    signal : ndarray
        The signal that we want to calculate the low frequency chi^2 of (units should be Amps).
    template : ndarray
        The pulse template to be used for the low frequency chi^2 calculation (should be 
        normalized beforehand).
    amp : float
        The optimum amplitude calculated for the trace (in Amps).
    t0 : float
        The time shift calculated for the pulse (in s).
    inputpsd : ndarray
        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz).
    fs : float
        The sample rate of the data being taken (in Hz).
    fcutoff : float, optional
        The frequency (in Hz) that we should cut off the chi^2 when calculating the low frequency chi^2.
    coupling : str, optional
        String that determines if the zero frequency bin of the psd should be ignored (i.e. set to infinity)
        when calculating the optimum amplitude. If set to 'AC', then ths zero frequency bin is ignored. If
        set to anything else, then the zero frequency bin is kept. Default is 'AC'.
        
    Returns
    -------
    chi2low : float
        The low frequency chi^2 value (cut off at fcutoff) for the inputted values.
        
    """
    psd = np.zeros(len(inputpsd))
    psd[:] = inputpsd
    if coupling == 'AC':
        psd[0] = np.inf
    if len(signal.shape) == 1:
        signal = signal[np.newaxis, :]
    if np.isscalar(amp):
        amp = np.array([amp])
        t0 = np.array([t0])
    nbins = signal.shape[(-1)]
    df = fs / nbins
    v = fft(signal, axis=(-1)) / nbins / df
    s = fft(template) / nbins / df
    f = fftfreq(nbins, d=(1 / fs))
    chi2tot = df * np.abs(v - amp[:, np.newaxis] * np.exp(complex(-0.0, -2.0) * np.pi * t0[:, np.newaxis] * f[np.newaxis, :]) * s) ** 2 / psd
    chi2inds = np.abs(f) <= fcutoff
    chi2low = np.sum((chi2tot[:, chi2inds]), axis=(-1))
    if len(chi2low) == 1:
        chi2low = chi2low[0]
    return chi2low


def chi2_nopulse(signal, inputpsd, fs, coupling='AC'):
    """
    Function for calculating the chi^2 of a trace with the assumption that there is no pulse.
    
    Parameters
    ----------
    signal : ndarray
        The signal that we want to calculate the no pulse chi^2 of (units should be Amps).
    inputpsd : ndarray
        The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz).
    fs : float
        The sample rate of the data being taken (in Hz).
    coupling : str, optional
        String that determines if the zero frequency bin of the psd should be ignored (i.e. set to infinity)
        when calculating the no pulse chi^2 . If set to 'AC', then the zero frequency bin is ignored. If
        set to anything else, then the zero frequency bin is kept. Default is 'AC'.
        
    Returns
    -------
    chi2_0 : float
        The chi^2 value for there being no pulse.
        
    """
    psd = np.zeros(len(inputpsd))
    psd[:] = inputpsd
    nbins = signal.shape[(-1)]
    df = fs / nbins
    v = fft(signal, axis=(-1)) / nbins / df
    if coupling == 'AC':
        psd[0] = np.inf
    chi2_0 = df * np.sum((np.abs(v) ** 2 / psd), axis=(-1))
    return chi2_0


class OFnonlin(object):
    __doc__ = '\n    This class provides the user with a non-linear optimum filter to estimate the amplitude,\n    rise time (optional), fall time, and time offset of a pulse. \n    \n    Attributes:\n    -----------\n    psd : ndarray \n        The power spectral density corresponding to the pulses that will be \n        used in the fit. Must be the full psd (positive and negative frequencies), \n        and should be properly normalized to whatever units the pulses will be in. \n    fs : int or float\n        The sample rate of the ADC\n    df : float\n        The delta frequency\n    freqs : ndarray\n        Array of frequencies corresponding to the psd\n    time : ndarray\n        Array of time bins corresponding to the pulse\n    template : ndarray\n        The time series pulse template to use as a guess for initial parameters\n    data : ndarray\n        FFT of the pulse that will be used in the fit\n    lgcdouble : bool\n        If False, only the Pulse hight, fall time, and time offset will be fit.\n        If True, the rise time of the pulse will be fit in addition to the above. \n    taurise : float\n        The user defined risetime of the pulse\n    error : ndarray\n        The uncertianty per frequency (the square root of the psd, devided by the errorscale)\n    dof : int\n        The number of degrees of freedom in the fit\n    norm : float\n        Normalization factor to go from continuous to FFT\n    \n    '

    def __init__(self, psd, fs, template=None):
        """
        Initialization of OFnonlin object
        
        Parameters
        ----------
        psd : ndarray 
            The power spectral density corresponding to the pulses that will be 
            used in the fit. Must be the full psd (positive and negative frequencies), 
            and should be properly normalized to whatever units the pulses will be in. 
        fs : int or float
            The sample rate of the ADC
        template : ndarray
            The time series pulse template to use as a guess for initial parameters
            
        """
        self.psd = np.zeros(len(psd))
        self.psd[:] = psd
        self.psd[0] = 1e+40
        self.fs = fs
        self.df = fs / len(psd)
        self.freqs = np.fft.fftfreq(len(psd), 1 / fs)
        self.time = np.arange(len(psd)) / fs
        self.template = template
        self.data = None
        self.npolefit = 1
        self.taurise = None
        self.error = None
        self.dof = None
        self.norm = np.sqrt(fs * len(psd))

    def fourpole(self, A, B, C, tau_r, tau_f1, tau_f2, tau_f3, t0):
        """
        Functional form of pulse in frequency domain with 1 rise time and three fall times
        The rise time and one fall time share an amplitude (A). The second and third fall time 
        have independent amplitudes (B and C). The functional form (time domain) is:
        A*(1-exp(-t/    au_rise))*(exp(-t/      au_fall1)) + B*(exp(-t/ au_fall2)) + C*(exp(-t/ au_fall3)).
        Therefore, the "amplitudes" take on different meanings than in the one/two pole functions below
        
        3 rise/fall times, 2 amplitudes, and time offset allowed to float
        
        Parameters
        ----------
        A : float
            Amplitude for rise time and first fall time
        B : float
            Amplitude for second fall time
        C : float
            Amplitude for third fall time
        tau_r : float
            Rise time of pulse
        tau_f1 : float
            First fall time of pulse
        tau_f2 : float
            Second fall time of pulse
        tau_f3 : float
            Third fall time of pulse
        t0 : float
            Time offset of three pole pulse
                
        Returns
        -------
        pulse : ndarray, complex
            Array of amplitude values as a function of frequency
            
        """
        omega = 2 * np.pi * self.freqs
        phaseTDelay = np.exp(complex(-0.0, -1.0) * omega * t0)
        tau_rf1 = tau_f1 * tau_r / (tau_f1 + tau_r)
        pulse = (A * (tau_f1 / (1 + omega * tau_f1 * complex(0.0, 1.0)) - tau_rf1 / (1 + omega * tau_rf1 * complex(0.0, 1.0))) + B * (tau_f2 / (1 + omega * tau_f2 * complex(0.0, 1.0))) + C * (tau_f3 / (1 + omega * tau_f3 * complex(0.0, 1.0)))) * phaseTDelay
        return pulse * np.sqrt(self.df)

    def fourpoletime(self, A, B, C, tau_r, tau_f1, tau_f2, tau_f3, t0):
        """
        Functional form of pulse in time domain with 1 rise time and three fall times
        The rise time and one fall time share an amplitude (A). The second and third fall time 
        have independent amplitudes (B and C). Therefore, the "amplitudes" take on different
        meanings than in the one/two pole functions below
        
        3 rise/fall times, 2 amplitudes, and time offset allowed to float
        
        
        Parameters
        ----------
        A : float
            Amplitude for rise time and first fall time
        B : float
            Amplitude for second fall time
        C : float
            Amplitude for third fall time
        tau_r : float
            Rise time of pulse
        tau_f1 : float
            First fall time of pulse
        tau_f2 : float
            Second fall time of pulse
        tau_f3 : float
            Third fall time of pulse
        t0 : float
            Time offset of three pole pulse
            
        Returns
        -------
        pulse : ndarray
            Array of amplitude values as a function of time
        """
        pulse = A * (1 - np.exp(-self.time / tau_r)) * np.exp(-self.time / tau_f1) + B * np.exp(-self.time / tau_f2) + C * np.exp(-self.time / tau_f3)
        return np.roll(pulse, int(t0 * self.fs))

    def threepole(self, A, B, tau_r, tau_f1, tau_f2, t0):
        """
        Functional form of pulse in frequency domain with 1 rise time and two fall times
        The rise time and one fall time share an amplitude (A) and the second fall time 
        has an independent amplitude (B). The functional form (time domain) is:
        A*(1-exp(-t/    au_rise))*(exp(-t/      au_fall1)) + B*(exp(-t/ au_fall2)) and therefore
        the "amplitudes" take on different meanings than in the one/two pole functions below
        
        3 rise/fall times, 2 amplitudes, and time offset allowed to float
        
        Parameters
        ----------
        A : float
            Amplitude for rise time and first fall time
        B : float
            Amplitude for second fall time
        tau_r : float
            Rise time of pulse
        tau_f1 : float
            First fall time of pulse
        tau_f2 : float
            Second fall time of pulse
        t0 : float
            Time offset of three pole pulse
                
        Returns
        -------
        pulse : ndarray, complex
            Array of amplitude values as a function of frequency
            
        """
        omega = 2 * np.pi * self.freqs
        phaseTDelay = np.exp(complex(-0.0, -1.0) * omega * t0)
        tau_rf1 = tau_f1 * tau_r / (tau_f1 + tau_r)
        pulse = (A * (tau_f1 / (1 + omega * tau_f1 * complex(0.0, 1.0)) - tau_rf1 / (1 + omega * tau_rf1 * complex(0.0, 1.0))) + B * (tau_f2 / (1 + omega * tau_f2 * complex(0.0, 1.0)))) * phaseTDelay
        return pulse * np.sqrt(self.df)

    def threepoletime(self, A, B, tau_r, tau_f1, tau_f2, t0):
        """
        Functional form of pulse in time domain with 1 rise time and two fall times
        The rise time and one fall time share an amplitude (A) and the second fall time 
        has an independent amplitude (B). Therefore the "amplitudes" take on different
        meanings than in the one/two pole functions below
        
        3 rise/fall times, 2 amplitudes, and time offset allowed to float
        
        Parameters
        ----------
        A : float
            Amplitude for rise time and first fall time
        B : float
            Amplitude for second fall time
        tau_r : float
            Rise time of pulse
        tau_f1 : float
            First fall time of pulse
        tau_f2 : float
            Second fall time of pulse
        t0 : float
            Time offset of three pole pulse
            
        Returns
        -------
        pulse : ndarray
            Array of amplitude values as a function of time
        """
        pulse = A * (1 - np.exp(-self.time / tau_r)) * np.exp(-self.time / tau_f1) + B * np.exp(-self.time / tau_f2)
        return np.roll(pulse, int(t0 * self.fs))

    def twopole(self, A, tau_r, tau_f, t0):
        """
        Functional form of pulse in frequency domain with the amplitude, rise time,
        fall time, and time offset allowed to float. This is meant to be a private function
        
        Parameters
        ----------
        A : float
            Amplitude of pulse
        tau_r : float
            Rise time of two-pole pulse
        tau_f : float
            Fall time of two-pole pulse
        t0 : float
            Time offset of two pole pulse
                
        Returns
        -------
        pulse : ndarray, complex
            Array of amplitude values as a function of frequency
            
        """
        omega = 2 * np.pi * self.freqs
        delta = tau_r - tau_f
        rat = tau_r / tau_f
        amp = A / (rat ** (-tau_r / delta) - rat ** (-tau_f / delta))
        pulse = amp * np.abs(tau_r - tau_f) / (1 + omega * tau_f * complex(0.0, 1.0)) * 1 / (1 + omega * tau_r * complex(0.0, 1.0)) * np.exp(-omega * t0 * complex(0.0, 1.0))
        return pulse * np.sqrt(self.df)

    def twopoletime(self, A, tau_r, tau_f, t0):
        """
        Functional form of pulse in time domain with the amplitude, rise time,
        fall time, and time offset allowed to float 
        
        Parameters
        ----------
        A : float
            Amplitude of pulse
        tau_r : float
            Rise time of two-pole pulse
        tau_f : float
            Fall time of two-pole pulse
        t0 : float
            Time offset of two pole pulse
                
        Returns
        -------
        pulse : ndarray
            Array of amplitude values as a function of time
        """
        delta = tau_r - tau_f
        rat = tau_r / tau_f
        amp = A / (rat ** (-tau_r / delta) - rat ** (-tau_f / delta))
        pulse = amp * (np.exp(-self.time / tau_f) - np.exp(-self.time / tau_r))
        return np.roll(pulse, int(t0 * self.fs))

    def onepole(self, A, tau_f, t0):
        """
        Functional form of pulse in time domain with the amplitude,
        fall time, and time offset allowed to float, and the rise time 
        held constant
        
        Parameters
        ----------
        A : float
            Amplitude of pulse
        tau_f : float
            Fall time of two-pole pulse
        t0 : float
            Time offset of two pole pulse
                
        Returns
        -------
        pulse : ndarray, complex
            Array of amplitude values as a function of freuqncy
        """
        tau_r = self.taurise
        return self.twopole(A, tau_r, tau_f, t0)

    def residuals(self, params):
        """
        Function ot calculate the weighted residuals to be minimized
        
        Parameters
        ----------
        params : tuple
            Tuple containing fit parameters
                
        Returns
        -------
        z1d : ndarray
            Array containing residuals per frequency bin. The complex data is flatted into
            single array
        """
        if self.npolefit == 4:
            A, B, C, tau_r, tau_f1, tau_f2, tau_f3, t0 = params
            delta = self.data - self.fourpole(A, B, C, tau_r, tau_f1, tau_f2, tau_f3, t0)
        else:
            if self.npolefit == 3:
                A, B, tau_r, tau_f1, tau_f2, t0 = params
                delta = self.data - self.threepole(A, B, tau_r, tau_f1, tau_f2, t0)
            else:
                if self.npolefit == 2:
                    A, tau_r, tau_f, t0 = params
                    delta = self.data - self.twopole(A, tau_r, tau_f, t0)
                else:
                    A, tau_f, t0 = params
                    delta = self.data - self.onepole(A, tau_f, t0)
        z1d = np.zeros((self.data.size * 2), dtype=(np.float64))
        z1d[0:z1d.size:2] = delta.real / self.error
        z1d[1:z1d.size:2] = delta.imag / self.error
        return z1d

    def calcchi2(self, model):
        """
        Function to calculate the reduced chi square
        
        Parameters
        ----------
        model : ndarray
            Array corresponding to pulse function (twopole or onepole) evaluated
            at the optimum values
                
        Returns
        -------
        chi2 : float
            The reduced chi squared statistic
        """
        return sum(np.abs(self.data - model) ** 2 / self.error ** 2) / (len(self.data) - self.dof)

    def fit_falltimes(self, pulse, npolefit=1, errscale=1, guess=None, taurise=None, lgcfullrtn=False, lgcplot=False):
        """
        Function to do the fit
        
        Parameters
        ----------
        pulse : ndarray
            Time series traces to be fit
        npolefit: int, optional
            The number of poles to fit
            If 1, the one pole fit is done, the user must provide the value of taurise
            If 2, the two pole fit is done
            If 3, the three pole fit is done (1 rise 2 fall). Second fall time amplitude is independent
            If 4, the four pole fit is done (1 rise 3 fall). Second and third fall time amplitudes are independent
            If False, the twopole fit is done, if True, the one pole fit it done.
        errscale : float or int, optional
            A scale factor for the psd. Ex: if fitting an average, the errscale should be
            set to the number of traces used in the average
        guess : tuple, optional
            Guess of initial values for fit, must be the same size as the model being used for fit.
            If lgcdouble is True, then the order should be (ampguess, tauriseguess, taufallguess, t0guess).
            If lgcdouble is False, then the order should be (ampguess, taufallguess, t0guess).
        taurise : float, optional
            The value of the rise time of the pulse if the single pole function is being use for fit
        lgcfullrtn : bool, optional
            If False, only the best fit parameters are returned. If True, the errors in the fit parameters,
            the covariance matrix, and chi squared statistic are returned as well.
        lgcplot : bool, optional
            If True, diagnostic plots are returned. 
                
        Returns
        -------
        variables : tuple
            The best fit parameters
        errors : tuple
            The corresponding fit errors for the best fit parameters
        cov : ndarray
            The convariance matrix returned from the fit
        chi2 : float
            The reduced chi squared statistic evaluated at the optimum point of the fit
                
        Raises
        ------
        ValueError
            if length of guess does not match the number of parameters needed in fit
                
        """
        self.data = np.fft.fft(pulse) / self.norm
        self.error = np.sqrt(self.psd / errscale)
        self.npolefit = npolefit
        if self.npolefit == 1:
            if taurise is None:
                raise ValueError('taurise must not be None if doing 1-pole fit.')
            else:
                self.taurise = taurise
        if guess is not None:
            if self.npolefit == 4:
                if len(guess) != 8:
                    raise ValueError('Length of guess not compatible with 4-pole fit. Must be of format: guess = (A,B,C,taurise,taufall1,taufall2,taufall3,t0)')
                else:
                    Aguess, Bguess, Cguess, tauriseguess, taufall1guess, taufall2guess, taufall3guess, t0guess = guess
            else:
                if self.npolefit == 3:
                    if len(guess) != 6:
                        raise ValueError('Length of guess not compatible with 3-pole fit. Must be of format: guess = (A,B,taurise,taufall1,taufall2,t0)')
                    else:
                        Aguess, Bguess, tauriseguess, taufall1guess, taufall2guess, t0guess = guess
                else:
                    if self.npolefit == 2:
                        if len(guess) != 4:
                            raise ValueError('Length of guess not compatible with 2-pole fit. Must be of format: guess = (A,taurise,taufall,t0)')
                        else:
                            ampguess, tauriseguess, taufallguess, t0guess = guess
                    else:
                        if len(guess) != 3:
                            raise ValueError('Length of guess not compatible with 1-pole fit. Must be of format: guess = (A,taufall,t0)')
                        else:
                            ampguess, taufallguess, t0guess = guess
        else:
            if self.template is not None:
                ampscale = np.max(pulse) - np.min(pulse)
                templateforguess = self.template
            else:
                ampscale = 1
                templateforguess = pulse
            maxind = np.argmax(templateforguess)
            if self.npolefit == 4:
                Aguess = np.mean(templateforguess[maxind - 7:maxind + 7]) * ampscale
                Bguess = Aguess / 3
                Cguess = Aguess / 3
                tauriseguess = 2e-05
                taufall1guess = 0.0001
                taufall2guess = 0.0003
                taufall3guess = 0.0005
                t0guess = maxind / self.fs
            else:
                if self.npolefit == 3:
                    Aguess = np.mean(templateforguess[maxind - 7:maxind + 7]) * ampscale
                    Bguess = Aguess / 3
                    tauriseguess = 2e-05
                    taufall1guess = 0.0001
                    taufall2guess = 0.0003
                    t0guess = maxind / self.fs
                else:
                    ampguess = np.mean(templateforguess[maxind - 7:maxind + 7]) * ampscale
                    tauval = 0.37 * ampguess
                    tauind = np.argmin(np.abs(pulse[maxind + 1:maxind + 1 + int(0.0003 * self.fs)] - tauval)) + maxind + 1
                    taufallguess = (tauind - maxind) / self.fs
                    tauriseguess = 2e-05
                    t0guess = maxind / self.fs
                if self.npolefit == 4:
                    self.dof = 8
                    p0 = (Aguess, Bguess, Cguess, tauriseguess, taufall1guess, taufall2guess, taufall3guess, t0guess)
                    boundslower = (Aguess / 100, Bguess / 100, Cguess / 100, tauriseguess / 10, taufall1guess / 10, taufall2guess / 10, taufall3guess / 10, t0guess - 30 / self.fs)
                    boundsupper = (Aguess * 100, Bguess * 100, Cguess * 100, tauriseguess * 10, taufall1guess * 10, taufall2guess * 10, taufall3guess * 10, t0guess + 30 / self.fs)
                else:
                    if self.npolefit == 3:
                        self.dof = 6
                        p0 = (Aguess, Bguess, tauriseguess, taufall1guess, taufall2guess, t0guess)
                        boundslower = (Aguess / 100, Bguess / 100, tauriseguess / 10, taufall1guess / 10, taufall2guess / 10, t0guess - 30 / self.fs)
                        boundsupper = (Aguess * 100, Bguess * 100, tauriseguess * 10, taufall1guess * 10, taufall2guess * 10, t0guess + 30 / self.fs)
                    else:
                        if self.npolefit == 2:
                            self.dof = 4
                            p0 = (ampguess, tauriseguess, taufallguess, t0guess)
                            boundslower = (ampguess / 100, tauriseguess / 10, taufallguess / 10, t0guess - 30 / self.fs)
                            boundsupper = (ampguess * 100, tauriseguess * 10, taufallguess * 10, t0guess + 30 / self.fs)
                        else:
                            self.dof = 3
                            p0 = (ampguess, taufallguess, t0guess)
                            boundslower = (ampguess / 100, taufallguess / 10, t0guess - 30 / self.fs)
                            boundsupper = (ampguess * 100, taufallguess * 10, t0guess + 30 / self.fs)
                        bounds = (boundslower, boundsupper)
                        result = least_squares((self.residuals), x0=p0, bounds=bounds, x_scale=p0, jac='3-point', loss='linear',
                          xtol=2.3e-16,
                          ftol=2.3e-16)
                        variables = result['x']
                        if self.npolefit == 4:
                            chi2 = self.calcchi2(self.fourpole(variables[0], variables[1], variables[2], variables[3], variables[4], variables[5], variables[6], variables[7]))
                        else:
                            if self.npolefit == 3:
                                chi2 = self.calcchi2(self.threepole(variables[0], variables[1], variables[2], variables[3], variables[4], variables[5]))
                            else:
                                if self.npolefit == 2:
                                    chi2 = self.calcchi2(self.twopole(variables[0], variables[1], variables[2], variables[3]))
                                else:
                                    chi2 = self.calcchi2(self.onepole(variables[0], variables[1], variables[2]))
            jac = result['jac']
            cov = np.linalg.pinv(np.dot(np.transpose(jac), jac))
            errors = np.sqrt(cov.diagonal())
            if lgcplot:
                plotnonlin(self, pulse, variables, errors)
            if lgcfullrtn:
                return (variables, errors, cov, chi2)
            else:
                return variables


class MuonTailFit(object):
    __doc__ = '\n    This class provides the user with a fitting routine to estimate the thermal muon tail fall time.\n    \n    Attributes:\n    -----------\n    psd : ndarray \n        The power spectral density corresponding to the pulses that will be \n        used in the fit. Must be the full psd (positive and negative frequencies), \n        and should be properly normalized to whatever units the pulses will be in. \n    fs : int or float\n        The sample rate of the ADC\n    df : float\n        The delta frequency\n    freqs : ndarray\n        Array of frequencies corresponding to the psd\n    time : ndarray\n        Array of time bins corresponding to the pulse\n    data : ndarray\n        FFT of the pulse that will be used in the fit\n    error : ndarray\n        The uncertainty per frequency (the square root of the psd, divided by the error scale)\n    dof : int\n        The number of degrees of freedom in the fit\n    norm : float\n        Normalization factor to go from continuous to FFT\n    \n    '

    def __init__(self, psd, fs):
        """
        Initialization of MuonTailFit object
        
        Parameters
        ----------
        psd : ndarray 
            The power spectral density corresponding to the pulses that will be 
            used in the fit. Must be the full psd (positive and negative frequencies), 
            and should be properly normalized to whatever units the pulses will be in. 
        fs : int or float
            The sample rate of the ADC
            
        """
        self.psd = np.zeros(len(psd))
        self.psd[:] = psd
        self.fs = fs
        self.df = self.fs / len(self.psd)
        self.freqs = np.fft.fftfreq((len(psd)), d=(1 / self.fs))
        self.time = np.arange(len(self.psd)) / self.fs
        self.data = None
        self.taurise = None
        self.error = None
        self.dof = None
        self.norm = np.sqrt(self.fs * len(self.psd))

    def muontailfcn(self, A, tau):
        """
        Functional form of a thermal muon tail in time domain with the amplitude and fall time
        allowed to float.
        
        Parameters
        ----------
        A : float
            Amplitude of pulse
        tau : float
            Fall time of muon tail
                
        Returns
        -------
        pulse : ndarray
            Array of amplitude values as a function of time
        """
        omega = 2 * np.pi * self.freqs
        pulse = A * tau / (1 + omega * tau * complex(0.0, 1.0))
        return pulse * np.sqrt(self.df)

    def residuals(self, params):
        """
        Function to calculate the weighted residuals to be minimized.
        
        Parameters
        ----------
        params : tuple
            Tuple containing fit parameters
                
        Returns
        -------
        z1d : ndarray
            Array containing residuals per frequency bin. The complex data is flatted into
            single array.
        """
        A, tau = params
        delta = self.data - self.muontailfcn(A, tau)
        z1d = np.zeros((self.data.size * 2), dtype=(np.float64))
        z1d[0:z1d.size:2] = delta.real / self.error
        z1d[1:z1d.size:2] = delta.imag / self.error
        return z1d

    def calcchi2(self, model):
        """
        Function to calculate the chi square
        
        Parameters
        ----------
        model : ndarray
            Array corresponding to pulse function evaluated at the fitted values
                
        Returns
        -------
        chi2 : float
            The chi squared statistic
        """
        return np.sum(np.abs(self.data - model) ** 2 / self.error ** 2)

    def fitmuontail(self, signal, lgcfullrtn=False, errscale=1):
        """
        Function to do the fit
        
        Parameters
        ----------
        signal: ndarray
            Time series traces to be fit
        lgcfullrtn : bool, optional
            If False, only the best fit parameters are returned. If True, the errors in the fit parameters,
            the covariance matrix, and chi squared statistic are returned as well.
        errscale : float or int, optional
            A scale factor for the psd. Ex: if fitting an average, the errscale should be
            set to the number of traces used in the average

        Returns
        -------
        variables : tuple
            The best fit parameters
        errors : tuple
            The corresponding fit errors for the best fit parameters
        cov : ndarray
            The convariance matrix returned from the fit
        chi2 : float
            The chi squared statistic evaluated at the fit
        """
        self.data = np.fft.fft(signal) / self.norm
        self.error = np.sqrt(self.psd / errscale)
        ampguess = np.max(signal) - np.min(signal)
        tauguess = np.argmin(np.abs(signal - ampguess / np.e)) / self.fs
        p0 = (
         ampguess, tauguess)
        boundslower = (0, 0)
        boundsupper = (ampguess * 100, tauguess * 100)
        bounds = (boundslower, boundsupper)
        result = least_squares((self.residuals), x0=p0, bounds=bounds, x_scale=(np.abs(p0)), jac='3-point', loss='linear',
          xtol=2.3e-16,
          ftol=2.3e-16)
        variables = result['x']
        chi2 = self.calcchi2((self.muontailfcn)(*variables))
        jac = result['jac']
        cov = np.linalg.pinv(np.dot(np.transpose(jac), jac))
        errors = np.sqrt(cov.diagonal())
        if lgcfullrtn:
            return (variables, errors, cov, chi2)
        else:
            return variables