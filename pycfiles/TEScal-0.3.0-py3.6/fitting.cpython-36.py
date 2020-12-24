# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tescal/fitting/fitting.py
# Compiled at: 2018-09-12 19:18:31
# Size of source mod 2**32: 24186 bytes
import numpy as np
from scipy.optimize import least_squares
import numpy as np
from numpy.fft import rfft, fft, ifft, fftfreq, rfftfreq
from tescal.plotting import plotnonlin

def ofamp(signal, template, psd, fs, withdelay=True, coupling='AC', lgcsigma=False, nconstrain=None):
    """
    Function for calculating the optimum amplitude of a pulse in data. Supports optimum filtering with
    and without time delay.
    
    Parameters
    ----------
        signal : ndarray
            The signal that we want to apply the optimum filter to (units should be Amps).
        template : ndarray
            The pulse template to be used for the optimum filter (should be normalized beforehand).
        psd : ndarray
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

    Returns
    -------
        amp : float
            The optimum amplitude calculated for the trace (in Amps).
        t0 : float
            The time shift calculated for the pulse (in s). Set to zero if withdelay is False.
        chi2 : float
            The reduced Chi^2 value calculated from the optimum filter.
        sigma : float, optional
            The optimal filter energy resolution (in Amps)
    """
    nbins = len(signal)
    timelen = nbins / fs
    df = fs / nbins
    v = fft(signal) / nbins
    s = fft(template) / nbins
    if len(psd) != len(v):
        raise ValueError('PSD length incompatible with signal size')
    if coupling == 'AC':
        psd[0] = np.inf
    else:
        phi = s.conjugate() / psd
        norm = np.real(np.dot(phi, s)) / df
        signalfilt = phi * v / norm
        if lgcsigma:
            sigma = 1 / (np.dot(phi, s).real * timelen) ** 0.5
        if withdelay:
            amps = np.real(ifft(signalfilt * nbins)) / df
            chi0 = np.real(np.dot(v.conjugate() / psd, v)) / df
            chit = amps ** 2 * norm
            chi = (chi0 - chit) / nbins
            amps = np.roll(amps, nbins // 2)
            chi = np.roll(chi, nbins // 2)
            if nconstrain is not None:
                if nconstrain > nbins:
                    nconstrain = nbins
                bestind = np.argmin(chi[nbins // 2 - nconstrain // 2:nbins // 2 + nconstrain // 2 + nconstrain % 2])
                bestind += nbins // 2 - nconstrain // 2
            else:
                bestind = np.argmin(chi)
            amp = amps[bestind]
            chi2 = chi[bestind]
            t0 = (bestind - nbins // 2) / fs
        else:
            amp = np.real(np.sum(signalfilt)) / df
        t0 = 0.0
        chi0 = np.real(np.dot(v.conjugate() / psd, v)) / df
        chit = amp ** 2 * norm
        chi2 = (chi0 - chit) / nbins
    if lgcsigma:
        return (amp, t0, chi2, sigma)
    else:
        return (
         amp, t0, chi2)


def chi2lowfreq(signal, template, amp, t0, psd, fs, fcutoff=10000):
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
        psd : ndarray
            The two-sided psd that will be used to describe the noise in the signal (in Amps^2/Hz).
        fs : float
            The sample rate of the data being taken (in Hz).
        fcutoff : float, optional
            The frequency (in Hz) that we should cut off the chi^2 when calculating the low frequency chi^2.
        
    Returns
    -------
        chi2low : float
            The low frequency chi^2 value (cut off at fcutoff) for the inputted values.
    """
    nbins = len(signal)
    df = fs / nbins
    v = fft(signal) / nbins
    s = fft(template) / nbins
    f = fftfreq(nbins, d=(1 / fs))
    chi2tot = df * np.abs(v / df - amp * np.exp(complex(-0.0, -2.0) * np.pi * f * t0) * s / df) ** 2 / psd
    chi2inds = np.abs(f) <= fcutoff
    chi2low = np.sum(chi2tot[chi2inds])
    return chi2low


class OFnonlin(object):
    __doc__ = '\n    This class provides the user with a non-linear optimum filter to estimate the amplitude,\n    rise time (optional), fall time, and time offset of a pulse. \n    \n    Attributes:\n    -----------\n        psd: ndarray \n            The power spectral density corresponding to the pulses that will be \n            used in the fit. Must be the full psd (positive and negative frequencies), \n            and should be properly normalized to whatever units the pulses will be in. \n        fs: int or float\n            The sample rate of the ADC\n        df: float\n            The delta frequency\n        freqs: ndarray\n            Array of frequencies corresponding to the psd\n        time: ndarray\n            Array of time bins corresponding to the pulse\n        template: ndarray\n            The time series pulse template to use as a guess for initial parameters\n        data: ndarray\n            FFT of the pulse that will be used in the fit\n        lgcdouble: bool\n            If False, only the Pulse hight, fall time, and time offset will be fit.\n            If True, the rise time of the pulse will be fit in addition to the above. \n        taurise: float\n            The user defined risetime of the pulse\n        error: ndarray\n            The uncertianty per frequency (the square root of the psd, devided by the errorscale)\n        dof: int\n            The number of degrees of freedom in the fit\n        norm: float\n            Normilization factor to go from continuous to FFT\n    \n    '

    def __init__(self, psd, fs, template=None):
        """
        Initialization of OFnonlin object
        
        Parameters
        ----------
            psd: ndarray 
                The power spectral density corresponding to the pulses that will be 
                used in the fit. Must be the full psd (positive and negative frequencies), 
                and should be properly normalized to whatever units the pulses will be in. 
            fs: int or float
                The sample rate of the ADC
            template: ndarray
                The time series pulse template to use as a guess for initial parameters
            
            
        """
        psd[0] = 1e+40
        self.psd = psd
        self.fs = fs
        self.df = fs / len(psd)
        self.freqs = np.fft.fftfreq(len(psd), 1 / fs)
        self.time = np.arange(len(psd)) / fs
        self.template = template
        self.data = None
        self.lgcdouble = False
        self.taurise = None
        self.error = None
        self.dof = None
        self.norm = np.sqrt(fs * len(psd))

    def twopole(self, A, tau_r, tau_f, t0):
        """
        Functional form of pulse in frequency domain with the amplitude, rise time,
        fall time, and time offset allowed to float. This is meant to be a private function
        
        Parameters
        ----------
            A: float
                Amplitude of pulse
            tau_r: float
                Rise time of two-pole pulse
            tau_f: float
                Fall time of two-pole pulse
            t0: float
                Time offset of two pole pulse
                
        Returns
        -------
            pulse: ndarray, complex
                Array of amplitude values as a function of freuqncy
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
            A: float
                Amplitude of pulse
            tau_r: float
                Rise time of two-pole pulse
            tau_f: float
                Fall time of two-pole pulse
            t0: float
                Time offset of two pole pulse
                
        Returns
        -------
            pulse: ndarray
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
            A: float
                Amplitude of pulse
            tau_f: float
                Fall time of two-pole pulse
            t0: float
                Time offset of two pole pulse
                
        Returns
        -------
            pulse: ndarray, complex
                Array of amplitude values as a function of freuqncy
        """
        tau_r = self.taurise
        return self.twopole(A, tau_r, tau_f, t0)

    def residuals(self, params):
        """
        Function ot calculate the weighted residuals to be minimized
        
        Parameters
        ----------
            params: tuple
                Tuple containing fit parameters
                
        Returns
        -------
            z1d: ndarray
                Array containing residuals per frequency bin. The complex data is flatted into
                single array
        """
        if self.lgcdouble:
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
            model: ndarray
                Array corresponding to pulse function (twopole or onepole) evaluated
                at the optimum values
                
        Returns
        -------
            chi2: float
                The reduced chi squared statistic
        """
        return sum(np.abs(self.data - model) ** 2 / self.error ** 2) / (len(self.data) - self.dof)

    def fit_falltimes(self, pulse, lgcdouble=False, errscale=1, guess=None, taurise=None, lgcfullrtn=False, lgcplot=False):
        """
        Function to do the fit
        
        Parameters
        ----------
            pulse: ndarray
                Time series traces to be fit
            lgcdouble: bool, optional
                If False, the twopole fit is done, if True, the one pole fit it done.
                Note, if True, the user must provide the value of taurise.
            errscale: float or int, optional
                A scale factor for the psd. Ex: if fitting an average, the errscale should be
                set to the number of traces used in the average
            guess: tuple, optional
                Guess of initial values for fit, must be the same size as the model being used for fit
            taurise: float, optional
                The value of the rise time of the pulse if the single pole function is being use for fit
            lgcfullrtn: bool, optional
                If False, only the best fit parameters are returned. If True, the errors in the fit parameters,
                the covariance matrix, and chi squared statistic are returned as well.
            lgcplot: bool, optional
                If True, diagnostic plots are returned. 
                
        Returns
        -------
            variables: tuple
                The best fit parameters
            errors: tuple
                The corresponding fit errors for the best fit parameters
            cov: ndarray
                The convariance matrix returned from the fit
            chi2: float
                The reduced chi squared statistic evaluated at the optimum point of the fit
                
        Raises
        ------
            ValueError
                if length of guess does not match the number of parameters needed in fit
                
        """
        self.data = np.fft.fft(pulse) / self.norm
        self.error = np.sqrt(self.psd / errscale)
        self.lgcdouble = lgcdouble
        if not lgcdouble:
            if taurise is None:
                raise ValueError('taurise must not be None if doing 1-pole fit.')
            else:
                self.taurise = taurise
        if guess is not None:
            if lgcdouble:
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
                maxind = np.argmax(self.template)
                ampguess = np.mean(self.template[maxind - 7:maxind + 7]) * ampscale
                tauval = 0.37 * ampguess
                tauind = np.argmin(np.abs(self.template[maxind:maxind + int(0.0003 * self.fs)] - tauval)) + maxind
                taufallguess = (tauind - maxind) / self.fs
                tauriseguess = 2e-05
                t0guess = maxind / self.fs
            else:
                maxind = np.argmax(pulse)
                ampguess = np.mean(pulse[maxind - 7:maxind + 7])
                tauval = 0.37 * ampguess
                tauind = np.argmin(np.abs(pulse[maxind:maxind + int(0.0003 * self.fs)] - tauval)) + maxind
                taufallguess = (tauind - maxind) / self.fs
                tauriseguess = 2e-05
                t0guess = maxind / self.fs
            if lgcdouble:
                self.dof = 4
                p0 = (ampguess, tauriseguess, taufallguess, t0guess)
                boundslower = (ampguess / 100, tauriseguess / 4, taufallguess / 4, t0guess - 30 / self.fs)
                boundsupper = (ampguess * 100, tauriseguess * 4, taufallguess * 4, t0guess + 30 / self.fs)
                bounds = (boundslower, boundsupper)
            else:
                self.dof = 3
                p0 = (ampguess, taufallguess, t0guess)
                boundslower = (ampguess / 100, taufallguess / 4, t0guess - 30 / self.fs)
                boundsupper = (ampguess * 100, taufallguess * 4, t0guess + 30 / self.fs)
                bounds = (boundslower, boundsupper)
            result = least_squares((self.residuals), x0=p0, bounds=bounds, x_scale=p0, jac='3-point', loss='linear',
              xtol=2.3e-16,
              ftol=2.3e-16)
            variables = result['x']
            if lgcdouble:
                chi2 = self.calcchi2(self.twopole(variables[0], variables[1], variables[2], variables[3]))
            else:
                chi2 = self.calcchi2(self.onepole(variables[0], variables[1], variables[2]))
            jac = result['jac']
            cov = np.linalg.inv(np.dot(np.transpose(jac), jac))
            errors = np.sqrt(cov.diagonal())
            if lgcplot:
                plotnonlin(self, pulse, variables)
            if lgcfullrtn:
                return (variables, errors, cov, chi2)
            else:
                return variables


class MuonTailFit(object):
    __doc__ = '\n    This class provides the user with a fitting routine to estimate the thermal muon tail fall time.\n    \n    Attributes:\n    -----------\n        psd: ndarray \n            The power spectral density corresponding to the pulses that will be \n            used in the fit. Must be the full psd (positive and negative frequencies), \n            and should be properly normalized to whatever units the pulses will be in. \n        fs: int or float\n            The sample rate of the ADC\n        df: float\n            The delta frequency\n        freqs: ndarray\n            Array of frequencies corresponding to the psd\n        time: ndarray\n            Array of time bins corresponding to the pulse\n        data: ndarray\n            FFT of the pulse that will be used in the fit\n        error: ndarray\n            The uncertainty per frequency (the square root of the psd, divided by the error scale)\n        dof: int\n            The number of degrees of freedom in the fit\n        norm: float\n            Normalization factor to go from continuous to FFT\n    \n    '

    def __init__(self, psd, fs):
        """
        Initialization of MuonTailFit object
        
        Parameters
        ----------
            psd: ndarray 
                The power spectral density corresponding to the pulses that will be 
                used in the fit. Must be the full psd (positive and negative frequencies), 
                and should be properly normalized to whatever units the pulses will be in. 
            fs: int or float
                The sample rate of the ADC
            
        """
        psd[0] = 1e+40
        self.psd = psd
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
        Functional form of pulse in time domain with the amplitude, rise time,
        fall time, and time offset allowed to float 
        
        Parameters
        ----------
            A: float
                Amplitude of pulse
            tau: float
                Fall time of muon tail
                
        Returns
        -------
            pulse: ndarray
                Array of amplitude values as a function of time
        """
        omega = 2 * np.pi * self.freqs
        pulse = A * tau / (1 + omega * tau * complex(0.0, 1.0))
        return pulse * np.sqrt(self.df)

    def residuals(self, params):
        """
        Function to calculate the weighted residuals to be minimized
        
        Parameters
        ----------
            params: tuple
                Tuple containing fit parameters
                
        Returns
        -------
            z1d: ndarray
                Array containing residuals per frequency bin. The complex data is flatted into
                single array
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
            model: ndarray
                Array corresponding to pulse function evaluated at the fitted values
                
        Returns
        -------
            chi2: float
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
            lgcfullrtn: bool, optional
                If False, only the best fit parameters are returned. If True, the errors in the fit parameters,
                the covariance matrix, and chi squared statistic are returned as well.
            errscale: float or int, optional
                A scale factor for the psd. Ex: if fitting an average, the errscale should be
                set to the number of traces used in the average

        Returns
        -------
            variables: tuple
                The best fit parameters
            errors: tuple
                The corresponding fit errors for the best fit parameters
            cov: ndarray
                The convariance matrix returned from the fit
            chi2: float
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