# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qetpy/core/_didv.py
# Compiled at: 2018-12-05 13:45:53
# Size of source mod 2**32: 77297 bytes
import numpy as np
from numpy import pi
from scipy.optimize import least_squares, fsolve
from scipy.fftpack import fft, ifft, fftfreq
import qetpy.plotting as utils
from qetpy.utils import stdcomplex
__all__ = ['didvinitfromdata', 'DIDV']

def didvinitfromdata(tmean, didvmean, didvstd, offset, offset_err, fs, sgfreq, sgamp, rshunt, r0=0.3, r0_err=0.001, rload=0.01, rload_err=0.001, priors=None, invpriorscov=None, add180phase=False, dt0=1e-05):
    """
    Function to initialize and process a dIdV dataset without having all of the traces, but just the 
    parameters that are required for fitting. After running, this returns a DIDV class object that is
    ready for fitting.
    
    Parameters
    ----------
    tmean : ndarray
        The average trace in time domain, units of Amps
    didvstd : ndarray
        The complex standard deviation of the didv in frequency space for each frequency
    didvmean : ndarray
        The average trace converted to didv
    offset : float
        The offset (i.e. baseline value) of the didv trace, in Amps
    offset_err : float
        The error in the offset of the didv trace, in Amps
    fs : float
        Sample rate of the data taken, in Hz
    sgfreq : float
        Frequency of the signal generator, in Hz
    sgamp : float
        Amplitude of the signal generator, in Amps (equivalent to jitter in the QET bias)
    rshunt : float
        Shunt resistance in the circuit, Ohms
    r0 : float, optional
        Resistance of the TES in Ohms
    r0_err : float, optional
        Error in the resistance of the TES (Ohms)
    rload : float, optional
        Load resistance of the circuit (rload = rshunt + rparasitic), Ohms
    rload_err : float, optional
        Error in the load resistance, Ohms
    priors : ndarray, optional
        Prior known values of Irwin's TES parameters for the trace. 
        Should be in the order of (rload,r0,beta,l,L,tau0,dt)
    invpriorscov : ndarray, optional
        Inverse of the covariance matrix of the prior known values of 
        Irwin's TES parameters for the trace (any values that are set 
        to zero mean that we have no knowledge of that parameter) 
    add180phase : boolean, optional
        If the signal generator is out of phase (i.e. if it looks like --__ instead of __--), then this
        should be set to True. Adds half a period of the signal generator to the dt0 attribute
    dt0 : float, optional
        The value of the starting guess for the time offset of the didv when fitting. 
        The best way to use this value if it isn't converging well is to run the fit multiple times, 
        setting dt0 equal to the fit's next value, and seeing where the dt0 value converges. 
        The fit can have a difficult time finding the value on the first run if it the initial value 
        is far from the actual value, so a solution is to do this iteratively. 

    Returns
    -------
    didvobj : Object
        A DIDV class object that can be used to fit the dIdV and return 
        the fit parameters.
    
    """
    didvobj = DIDV(None, fs, sgfreq, sgamp, rshunt, r0=r0, r0_err=r0_err, rload=rload, rload_err=rload_err, add180phase=add180phase,
      priors=priors,
      invpriorscov=invpriorscov,
      dt0=dt0)
    didvobj.didvmean = didvmean
    didvobj.didvstd = didvstd
    didvobj.offset = offset
    didvobj.offset_err = offset_err
    didvobj.tmean = tmean
    didvobj.dt0 = dt0
    if didvobj.add180phase:
        didvobj.dt0 = didvobj.dt0 + 1 / (2 * didvobj.sgfreq)
    didvobj.time = np.arange(len(tmean)) / fs - didvobj.dt0
    didvobj.freq = np.fft.fftfreq((len(tmean)), d=(1.0 / fs))
    nbins = len(didvobj.tmean)
    nperiods = np.floor(nbins * didvobj.sgfreq / didvobj.fs)
    flatindstemp = list()
    for i in range(0, int(nperiods)):
        flatindlow = int((float(i) + 0.25) * didvobj.fs / didvobj.sgfreq) + int(didvobj.dt0 * didvobj.fs)
        flatindhigh = int((float(i) + 0.48) * didvobj.fs / didvobj.sgfreq) + int(didvobj.dt0 * didvobj.fs)
        flatindstemp.append(range(flatindlow, flatindhigh))

    flatinds = np.array(flatindstemp).flatten()
    didvobj.flatinds = flatinds[np.logical_and(flatinds > 0, flatinds < nbins)]
    return didvobj


def onepoleimpedance(freq, A, tau2):
    """
    Function to calculate the impedance (dvdi) of a TES with the 1-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms), superconducting: A=rload, normal: A = rload+Rn
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s), superconducting: tau2=L/rload, normal: tau2=L/(rload+Rn)
        
    Returns
    -------
    dvdi : array_like, float
        The complex impedance of the TES with the 1-pole fit
    
    """
    dvdi = A * (1.0 + complex(0.0, 2.0) * pi * freq * tau2)
    return dvdi


def onepoleadmittance(freq, A, tau2):
    """
    Function to calculate the admittance (didv) of a TES with the 1-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms), superconducting: A=rload, normal: A = rload+Rn
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s), superconducting: tau2=L/rload, normal: tau2=L/(rload+Rn)
        
    Returns
    -------
    1.0/dvdi : array_like, float
        The complex admittance of the TES with the 1-pole fit
    """
    dvdi = onepoleimpedance(freq, A, tau2)
    return 1.0 / dvdi


def twopoleimpedance(freq, A, B, tau1, tau2):
    """
    Function to calculate the impedance (dvdi) of a TES with the 2-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms), A = rload + r0*(1+beta)
    B : float
        The fit parameter B in the complex impedance (in Ohms), B = r0*l*(2+beta)/(1-l) (where l is Irwin's loop gain)
    tau1 : float
        The fit parameter tau1 in the complex impedance (in s), tau1=tau0/(1-l)
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s), tau2=L/(rload+r0*(1+beta))
        
    Returns
    -------
    dvdi : array_like, float
        The complex impedance of the TES with the 2-pole fit
    
    """
    dvdi = A * (1.0 + complex(0.0, 2.0) * pi * freq * tau2) + B / (1.0 + complex(0.0, 2.0) * pi * freq * tau1)
    return dvdi


def twopoleadmittance(freq, A, B, tau1, tau2):
    """
    Function to calculate the admittance (didv) of a TES with the 2-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms), A = rload + r0*(1+beta)
    B : float
        The fit parameter B in the complex impedance (in Ohms), B = r0*l*(2+beta)/(1-l) (where l is Irwin's loop gain)
    tau1 : float
        The fit parameter tau1 in the complex impedance (in s), tau1=tau0/(1-l)
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s), tau2=L/(rload+r0*(1+beta))
        
    Returns
    -------
    1.0/dvdi : array_like, float
        The complex admittance of the TES with the 2-pole fit
    
    """
    dvdi = twopoleimpedance(freq, A, B, tau1, tau2)
    return 1.0 / dvdi


def threepoleimpedance(freq, A, B, C, tau1, tau2, tau3):
    """
    Function to calculate the impedance (dvdi) of a TES with the 3-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms)
    B : float
        The fit parameter B in the complex impedance (in Ohms)
    C : float
        The fit parameter C in the complex impedance
    tau1 : float
        The fit parameter tau1 in the complex impedance (in s)
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s)
    tau3 : float
        The fit parameter tau3 in the complex impedance (in s)
        
    Returns
    -------
    dvdi : array_like, float
        The complex impedance of the TES with the 3-pole fit
    
    """
    dvdi = A * (1.0 + complex(0.0, 2.0) * pi * freq * tau2) + B / (1.0 + complex(0.0, 2.0) * pi * freq * tau1 - C / (1.0 + complex(0.0, 2.0) * pi * freq * tau3))
    return dvdi


def threepoleadmittance(freq, A, B, C, tau1, tau2, tau3):
    """
    Function to calculate the admittance (didv) of a TES with the 3-pole fit
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    A : float
        The fit parameter A in the complex impedance (in Ohms)
    B : float
        The fit parameter B in the complex impedance (in Ohms)
    C : float
        The fit parameter C in the complex impedance
    tau1 : float
        The fit parameter tau1 in the complex impedance (in s)
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s)
    tau3 : float
        The fit parameter tau3 in the complex impedance (in s)
        
    Returns
    -------
    1.0/dvdi : array_like, float
        The complex admittance of the TES with the 3-pole fit
    
    """
    dvdi = threepoleimpedance(freq, A, B, C, tau1, tau2, tau3)
    return 1.0 / dvdi


def twopoleimpedancepriors(freq, rload, r0, beta, l, L, tau0):
    """
    Function to calculate the impedance (dvdi) of a TES with the 2-pole fit from Irwin's TES parameters
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    rload : float
        The load resistance of the TES (in Ohms)
    r0 : float
        The resistance of the TES (in Ohms)
    beta : float
        The current sensitivity of the TES
    l : float
        Irwin's loop gain
    L : float
        The inductance in the TES circuit (in Henrys)
    tau0 : float
        The thermal time constant of the TES (in s)
        
    Returns
    -------
    dvdi : array_like, float
        The complex impedance of the TES with the 2-pole fit from Irwin's TES parameters
    
    """
    dvdi = rload + r0 * (1.0 + beta) + complex(0.0, 2.0) * pi * freq * L + r0 * l * (2.0 + beta) / (1.0 - l) * 1.0 / (1.0 + complex(0.0, 2.0) * freq * pi * tau0 / (1.0 - l))
    return dvdi


def twopoleadmittancepriors(freq, rload, r0, beta, l, L, tau0):
    """
    Function to calculate the admittance (didv) of a TES with the 2-pole fit from Irwin's TES parameters
    
    Parameters
    ----------
    freq : array_like, float
        The frequencies for which to calculate the admittance (in Hz)
    rload : float
        The load resistance of the TES (in Ohms)
    r0 : float
        The resistance of the TES (in Ohms)
    beta : float
        The current sensitivity of the TES, beta=d(log R)/d(log I)
    l : float
        Irwin's loop gain, l = P0*alpha/(G*Tc)
    L : float
        The inductance in the TES circuit (in Henrys)
    tau0 : float
        The thermal time constant of the TES (in s), tau0=C/G
        
    Returns
    -------
    1.0/dvdi : array_like, float
        The complex admittance of the TES with the 2-pole fit from Irwin's TES parameters
    
    """
    dvdi = twopoleimpedancepriors(freq, rload, r0, beta, l, L, tau0)
    return 1.0 / dvdi


def convolvedidv(x, A, B, C, tau1, tau2, tau3, sgamp, rshunt, sgfreq, dutycycle):
    """
    Function to convert the fitted TES parameters for the complex impedance 
    to a TES response to a square wave jitter in time domain.
    
    Parameters
    ----------
    x : array_like
        Time values for the trace (in s)
    A : float
        The fit parameter A in the complex impedance (in Ohms)
    B : float
        The fit parameter B in the complex impedance (in Ohms)
    C : float
        The fit parameter C in the complex impedance
    tau1 : float
        The fit parameter tau1 in the complex impedance (in s)
    tau2 : float
        The fit parameter tau2 in the complex impedance (in s)
    tau3 : float
        The fit parameter tau3 in the complex impedance (in s)
    sgamp : float
        The peak-to-peak size of the square wave jitter (in Amps)
    rshunt : float
        The shunt resistance of the TES electronics (in Ohms)
    sgfreq : float
        The frequency of the square wave jitter (in Hz)
    dutycycle : float
        The duty cycle of the square wave jitter (between 0 and 1)
        
    Returns
    -------
    np.real(st) : ndarray
        The response of a TES to a square wave jitter in time domain
        with the given fit parameters. The real part is taken in order 
        to ensure that the trace is real
    
    """
    tracelength = len(x)
    dx = x[1] - x[0]
    freq = fftfreq((len(x)), d=dx)
    ci = threepoleadmittance(freq, A, B, C, tau1, tau2, tau3)
    sf = np.zeros_like(freq) * complex(0.0, 0.0)
    if dutycycle == 0.5:
        oddinds = np.abs(np.mod(np.absolute(freq / sgfreq), 2) - 1) < 1e-08
        sf[oddinds] = complex(0.0, 1.0) / (pi * freq[oddinds] / sgfreq) * sgamp * rshunt * tracelength
    else:
        oddinds = np.abs(np.mod(np.abs(freq / sgfreq), 2) - 1) < 1e-08
        sf[oddinds] = complex(-0.0, -1.0) / (2.0 * pi * freq[oddinds] / sgfreq) * sgamp * rshunt * tracelength * (np.exp(complex(-0.0, -2.0) * pi * freq[oddinds] / sgfreq * dutycycle) - 1)
        eveninds = np.abs(np.mod(np.abs(freq / sgfreq) + 1, 2) - 1) < 1e-08
        eveninds[0] = False
        sf[eveninds] = complex(-0.0, -1.0) / (2.0 * pi * freq[eveninds] / sgfreq) * sgamp * rshunt * tracelength * (np.exp(complex(-0.0, -2.0) * pi * freq[eveninds] / sgfreq * dutycycle) - 1)
    sftes = sf * ci
    st = ifft(sftes)
    return np.real(st)


def squarewaveguessparams(trace, sgamp, rshunt):
    """
    Function to guess the fit parameters for the 1-pole fit.
    
    Parameters
    ----------
    trace : array_like
        The trace in time domain (in Amps).
    sgamp : float
        The peak-to-peak size of the square wave jitter (in Amps)
    rshunt : float
        Shunt resistance of the TES electronics (in Ohms)
        
    Returns
    -------
    A0 : float
        Guess of the fit parameter A (in Ohms)
    tau20 : float
        Guess of the fit parameter tau2 (in s)
    
    """
    di0 = max(trace) - min(trace)
    A0 = sgamp * rshunt / di0
    tau20 = 1e-06
    return (A0, tau20)


def guessdidvparams(trace, flatpts, sgamp, rshunt, L0=1e-07):
    """
    Function to find the fit parameters for either the 1-pole (A, tau2, dt),
    2-pole (A, B, tau1, tau2, dt), or 3-pole (A, B, C, tau1, tau2, tau3, dt) fit. 
    
    Parameters
    ----------
    trace : array_like
        The trace in time domain (in Amps)
    flatpts : array_like
        The flat parts of the trace (in Amps)
    sgamp : float
        The peak-to-peak size of the square wave jitter (in Amps)
    rshunt : float
        Shunt resistance of the TES electronics (in Ohms)
    L0 : float, optional
        The guess of the inductance (in Henries)
        
    Returns
    -------
    A0 : float
        Guess of the fit parameter A (in Ohms)
    B0 : float
        Guess of the fit parameter B (in Ohms)
    tau10 : float
        Guess of the fit parameter tau1 (in s)
    tau20 : float
        Guess of the fit parameter tau2 (in s)
    isloopgainsub1 : boolean
        Boolean flag that gives whether the loop gain is greater than one (False) or less than one (True)
        
    """
    dis_mean = np.mean(trace)
    flatpts_mean = np.mean(flatpts)
    isloopgainsub1 = flatpts_mean < dis_mean
    dis0 = 2 * np.abs(flatpts_mean - dis_mean)
    didv0 = dis0 / (sgamp * rshunt)
    dis_flat = np.max(trace) - flatpts_mean
    didvflat = dis_flat / (sgamp * rshunt)
    A0 = 1.0 / didvflat
    tau20 = L0 / A0
    if isloopgainsub1:
        B0 = 1.0 / didv0 - A0
        if B0 > 0.0:
            B0 = -B0
        tau10 = -0.0001
    else:
        B0 = -1.0 / didv0 - A0
        tau10 = -1e-05
    return (A0, B0, tau10, tau20, isloopgainsub1)


def fitdidv(freq, didv, yerr=None, A0=0.25, B0=-0.6, C0=-0.6, tau10=-1.0 / (2 * pi * 500.0), tau20=1.0 / (2 * pi * 100000.0), tau30=0.0, dt=-1e-05, poles=2, isloopgainsub1=None):
    """
    Function to find the fit parameters for either the 1-pole (A, tau2, dt), 
    2-pole (A, B, tau1, tau2, dt), or 3-pole (A, B, C, tau1, tau2, tau3, dt) fit. 
    
    Parameters
    ----------
    freq : ndarray
        Frequencies corresponding to the didv
    didv : ndarray
        Complex impedance extracted from the trace in frequency space
    yerr : ndarray, NoneType, optional
        Error at each frequency of the didv. Should be a complex number, 
        e.g. yerr = yerr_real + 1.0j * yerr_imag, where yerr_real is the 
        standard deviation of the real part of the didv, and yerr_imag is 
        the standard deviation of the imaginary part of the didv. If left as None,
        then each frequency will be assumed to be equally weighted.
    A0 : float, optional
        Guess of the fit parameter A (in Ohms). Default is 0.25.
    B0 : float, optional
        Guess of the fit parameter B (in Ohms). Default is -0.6.
    C0 : float, optional
        Guess of the fit parameter C (unitless). Default is -0.6.
    tau10 : float, optional
        Guess of the fit parameter tau1 (in s). Default is -1.0/(2*pi*5e2).
    tau20 : float, optional
        Guess of the fit parameter tau2 (in s). Default is 1.0/(2*pi*1e5).
    tau30 : float, optional
        Guess of the fit parameter tau3 (in s). Default is 0.0.
    dt : float, optional
        Guess of the time shift (in s). Default is -10.0e-6.
    poles : int, optional
        The number of poles to use in the fit (should be 1, 2, or 3). Default is 2.
    isloopgainsub1 : boolean, NoneType, optional
        If set, should be used to specify if the fit should be done assuming
        that the Irwin loop gain is less than 1 (True) or greater than 1 (False).
        Default is None, in which case loop gain less than 1 and greater than 1 
        fits will be done, returning the one with a lower Chi^2.
        
    Returns
    -------
    popt : ndarray
        The fitted parameters for the specificed number of poles
    pcov : ndarray
        The corresponding covariance matrix for the fitted parameters
    cost : float
        The cost of the the fit
        
    """
    if poles == 1:
        p0 = (A0, tau20, dt)
        bounds1 = ((0.0, 0.0, -np.inf), (np.inf, np.inf, np.inf))
        p02 = (
         -A0, tau20, dt)
        bounds2 = ((-np.inf, 0.0, -np.inf), (0.0, np.inf, np.inf))
    else:
        if poles == 2:
            p0 = (A0, B0, tau10, tau20, dt)
            bounds1 = ((0.0, -np.inf, -np.inf, 0.0, -np.inf), (np.inf, 0.0, 0.0, np.inf, np.inf))
            p02 = (
             A0, -B0, -tau10, tau20, dt)
            bounds2 = ((0.0, 0.0, 0.0, 0.0, -np.inf), (np.inf, np.inf, np.inf, np.inf, np.inf))
        else:
            if poles == 3:
                p0 = (A0, B0, C0, tau10, tau20, tau30, dt)
                bounds1 = ((0.0, -np.inf, -np.inf, -np.inf, 0.0, 0.0, -np.inf), (np.inf, 0.0, 0.0, 0.0, np.inf, np.inf, np.inf))
                p02 = (
                 A0, -B0, -C0, -tau10, tau20, tau30, dt)
                bounds2 = ((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -np.inf), (np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf))

    def residual(params):
        if poles == 1:
            A, tau2, dt = params
            ci = onepoleadmittance(freq, A, tau2) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        else:
            if poles == 2:
                A, B, tau1, tau2, dt = params
                ci = twopoleadmittance(freq, A, B, tau1, tau2) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
            else:
                if poles == 3:
                    A, B, C, tau1, tau2, tau3, dt = params
                    ci = threepoleadmittance(freq, A, B, C, tau1, tau2, tau3) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
            diff = didv - ci
            if yerr is None:
                weights = complex(1.0, 1.0)
            else:
                weights = 1.0 / yerr.real + complex(0.0, 1.0) / yerr.imag
        z1d = np.zeros((freq.size * 2), dtype=(np.float64))
        z1d[0:z1d.size:2] = diff.real * weights.real
        z1d[1:z1d.size:2] = diff.imag * weights.imag
        return z1d

    if isloopgainsub1 is None:
        res1 = least_squares(residual, p0, bounds=bounds1, loss='linear', max_nfev=1000, verbose=0, x_scale=(np.abs(p0)))
        res2 = least_squares(residual, p02, bounds=bounds2, loss='linear', max_nfev=1000, verbose=0, x_scale=(np.abs(p0)))
        if res1['cost'] < res2['cost']:
            res = res1
        else:
            res = res2
    else:
        if isloopgainsub1:
            res = least_squares(residual, p02, bounds=bounds2, loss='linear', max_nfev=1000, verbose=0, x_scale=(np.abs(p0)))
        else:
            res = least_squares(residual, p0, bounds=bounds1, loss='linear', max_nfev=1000, verbose=0, x_scale=(np.abs(p0)))
        popt = res['x']
        cost = res['cost']
        if not res['success']:
            print('Fit failed: ' + str(res['status']) + ', ' + str(poles) + '-pole Fit')
        pcovinv = np.dot(res['jac'].transpose(), res['jac'])
        pcov = np.linalg.inv(pcovinv)
        return (
         popt, pcov, cost)


def converttotesvalues(popt, pcov, r0, rload, r0_err=0.001, rload_err=0.001):
    """
    Function to convert the fit parameters for either 1-pole (A, tau2, dt),
    2-pole (A, B, tau1, tau2, dt), or 3-pole (A, B, C, tau1, tau2, tau3, dt)
    fit to the corresponding TES parameters: 1-pole (rtot, L, r0, rload, dt), 
    2-pole (rload, r0, beta, l, L, tau0, dt), and 3-pole (no conversion done).
    
    Parameters
    ----------
    popt : ndarray
        The fit parameters for either the 1-pole, 2-pole, or 3-pole fit
    pcov : ndarray
        The corresponding covariance matrix for the fit parameters
    r0 : float
        The resistance of the TES (in Ohms)
    rload : float
        The load resistance of the TES circuit (in Ohms)
    r0_err : float, optional
        The error in the r0 value (in Ohms). Default is 0.001.
    rload_err : float, optional
        The error in the rload value (in Ohms). Default is 0.001.
        
    Returns
    -------
    popt_out : ndarray
        The TES parameters for the specified fit
    pcov_out : ndarray
        The corresponding covariance matrix for the TES parameters
        
    """
    if len(popt) == 3:
        A = popt[0]
        tau2 = popt[1]
        dt = popt[2]
        rtot = A
        L = A * tau2
        popt_out = np.array([rtot, L, r0, rload, dt])
        pcov_orig = pcov
        pcov_in = np.zeros((5, 5))
        row, col = np.indices((2, 2))
        pcov_in[(row, col)] = pcov_orig[(row, col)]
        vardt = pcov_orig[(2, 2)]
        pcov_in[(2, 2)] = r0_err ** 2
        pcov_in[(3, 3)] = rload_err ** 2
        pcov_in[(4, 4)] = vardt
        jac = np.zeros((5, 5))
        jac[(0, 0)] = 1
        jac[(1, 0)] = tau2
        jac[(1, 1)] = A
        jac[(2, 2)] = 1
        jac[(3, 3)] = 1
        jac[(4, 4)] = 1
        jact = np.transpose(jac)
        pcov_out = np.dot(jac, np.dot(pcov_in, jact))
    else:
        if len(popt) == 5:
            A = popt[0]
            B = popt[1]
            tau1 = popt[2]
            tau2 = popt[3]
            dt = popt[4]
            pcov_orig = np.copy(pcov)
            pcov_in = np.zeros((7, 7))
            row, col = np.indices((4, 4))
            pcov_in[(row, col)] = np.copy(pcov_orig[(row, col)])
            vardt = pcov_orig[(4, 4)]
            pcov_in[(4, 4)] = rload_err ** 2
            pcov_in[(5, 5)] = r0_err ** 2
            pcov_in[(6, 6)] = vardt
            beta = (A - rload) / r0 - 1.0
            l = B / (A + B + r0 - rload)
            L = A * tau2
            tau = tau1 * (A + r0 - rload) / (A + B + r0 - rload)
            popt_out = np.array([rload, r0, beta, l, L, tau, dt])
            jac = np.zeros((7, 7))
            jac[(0, 4)] = 1.0
            jac[(1, 5)] = 1.0
            jac[(2, 0)] = 1.0 / r0
            jac[(2, 4)] = -1.0 / r0
            jac[(2, 5)] = -(A - rload) / r0 ** 2.0
            jac[(3, 0)] = -B / (A + B + r0 - rload) ** 2.0
            jac[(3, 1)] = (A + r0 - rload) / (A + B + r0 - rload) ** 2.0
            jac[(3, 4)] = B / (A + B + r0 - rload) ** 2.0
            jac[(3, 5)] = -B / (A + B + r0 - rload) ** 2.0
            jac[(4, 0)] = tau2
            jac[(4, 3)] = A
            jac[(5, 0)] = tau1 * B / (A + B + r0 - rload) ** 2.0
            jac[(5, 1)] = -tau1 * (A + r0 - rload) / (A + B + r0 - rload) ** 2.0
            jac[(5, 2)] = (A + r0 - rload) / (A + B + r0 - rload)
            jac[(5, 4)] = -B * tau1 / (A + B + r0 - rload) ** 2.0
            jac[(5, 5)] = B * tau1 / (A + B + r0 - rload) ** 2.0
            jac[(6, 6)] = 1.0
            jact = np.transpose(jac)
            pcov_out = np.dot(jac, np.dot(pcov_in, jact))
        else:
            if len(popt) == 7:
                popt_out = popt
                pcov_out = pcov
    return (
     popt_out, pcov_out)


def fitdidvpriors(freq, didv, priors, invpriorscov, yerr=None, rload=0.35, r0=0.13, beta=0.5, l=10.0, L=5e-07, tau0=0.0005, dt=-1e-05):
    """
    Function to directly fit Irwin's TES parameters (rload, r0, beta, l, L, tau0, dt)
    with the knowledge of prior known values any number of the parameters. 
    In order for the degeneracy of the parameters to be broken, at least 2 
    fit parameters should have priors knowledge. This is usually rload and r0, as 
    these can be known from IV data.
    
    Parameters
    ----------
    freq : ndarray
        Frequencies corresponding to the didv
    didv : ndarray
        Complex impedance extracted from the trace in frequency space
    priors : ndarray
        Prior known values of Irwin's TES parameters for the trace. 
        Should be in the order of (rload,r0,beta,l,L,tau0,dt)
    invpriorscov : ndarray
        Inverse of the covariance matrix of the prior known values of 
        Irwin's TES parameters for the trace (any values that are set 
        to zero mean that we have no knowledge of that parameter) 
    yerr : ndarray, optional
        Error at each frequency of the didv. Should be a complex number,
        e.g. yerr = yerr_real + 1.0j * yerr_imag, where yerr_real is the 
        standard deviation of the real part of the didv, and yerr_imag is 
        the standard deviation of the imaginary part of the didv. If left as None,
        then each frequency will be assumed to be equally weighted.
    rload : float, optional
        Guess of the load resistance of the TES circuit (in Ohms). Default is 0.35.
    r0 : float, optional
        Guess of the resistance of the TES (in Ohms). Default is 0.130.
    beta : float, optional
        Guess of the current sensitivity beta (unitless). Default is 0.5.
    l : float, optional
        Guess of Irwin's loop gain (unitless). Default is 10.0.
    L : float, optional
        Guess of the inductance (in Henrys). Default is 500.0e-9.
    tau0 : float, optional
        Guess of the thermal time constant (in s). Default is 500.0e-6.
    dt : float, optional
        Guess of the time shift (in s). Default is -10.0e-6.
        
    Returns
    -------
    popt : ndarray
        The fitted parameters in the order of (rload, r0, beta, l, L, tau0, dt)
    pcov : ndarray
        The corresponding covariance matrix for the fitted parameters
    cost : float
        The cost of the the fit
        
    """
    p0 = (
     rload, r0, beta, l, L, tau0, dt)
    bounds = ((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -np.inf), (np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf))

    def residualpriors(params, priors, invpriorscov):
        z1dpriors = np.sqrt((priors - params).dot(invpriorscov).dot(priors - params))
        return z1dpriors

    def residual(params):
        rload, r0, beta, l, L, tau0, dt = params
        ci = twopoleadmittancepriors(freq, rload, r0, beta, l, L, tau0) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        diff = didv - ci
        if yerr is None:
            weights = complex(1.0, 1.0)
        else:
            weights = 1.0 / yerr.real + complex(0.0, 1.0) / yerr.imag
        z1d = np.zeros((freq.size * 2 + 1), dtype=(np.float64))
        z1d[0:z1d.size - 1:2] = diff.real * weights.real
        z1d[1:z1d.size - 1:2] = diff.imag * weights.imag
        z1d[-1] = residualpriors(params, priors, invpriorscov)
        return z1d

    def jaca(params):
        popt = params
        rload = popt[0]
        r0 = popt[1]
        beta = popt[2]
        l = popt[3]
        L = popt[4]
        tau0 = popt[5]
        dt = popt[6]
        deriv1 = -1.0 / (complex(0.0, 2.0) * pi * freq * L + rload + r0 * (1.0 + beta) + r0 * l * (2.0 + beta) / (1.0 - l) * 1.0 / (1.0 + complex(0.0, 2.0) * pi * freq * tau0 / (1 - l))) ** 2
        dYdrload = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdrloadcomplex = deriv1 * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdrload[0:dYdrload.size:2] = np.real(dYdrloadcomplex)
        dYdrload[1:dYdrload.size:2] = np.imag(dYdrloadcomplex)
        dYdr0 = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdr0complex = deriv1 * (1.0 + beta + l * (2.0 + beta) / (1.0 - l + complex(0.0, 2.0) * pi * freq * tau0)) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdr0[0:dYdr0.size:2] = np.real(dYdr0complex)
        dYdr0[1:dYdr0.size:2] = np.imag(dYdr0complex)
        dYdbeta = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdbetacomplex = deriv1 * (r0 + complex(0.0, 2.0) * pi * freq * r0 * tau0) / (1.0 - l + complex(0.0, 2.0) * pi * freq * tau0) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdbeta[0:dYdbeta.size:2] = np.real(dYdbetacomplex)
        dYdbeta[1:dYdbeta.size:2] = np.imag(dYdbetacomplex)
        dYdl = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdlcomplex = deriv1 * r0 * (2.0 + beta) * (1.0 + complex(0.0, 2.0) * pi * freq * tau0) / (1.0 - l + complex(0.0, 2.0) * pi * freq * tau0) ** 2 * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdl[0:dYdl.size:2] = np.real(dYdlcomplex)
        dYdl[1:dYdl.size:2] = np.imag(dYdlcomplex)
        dYdL = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdLcomplex = deriv1 * complex(0.0, 2.0) * pi * freq * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdL[0:dYdL.size:2] = np.real(dYdLcomplex)
        dYdL[1:dYdL.size:2] = np.imag(dYdLcomplex)
        dYdtau0 = np.zeros((freq.size * 2), dtype=(np.float64))
        dYdtau0complex = deriv1 * complex(-0.0, -2.0) * pi * freq * l * r0 * (2.0 + beta) / (1.0 - l + complex(0.0, 2.0) * pi * freq * tau0) ** 2 * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYdtau0[0:dYdtau0.size:2] = np.real(dYdtau0complex)
        dYdtau0[1:dYdtau0.size:2] = np.imag(dYdtau0complex)
        dYddt = np.zeros((freq.size * 2), dtype=(np.float64))
        dYddtcomplex = complex(-0.0, -2.0) * pi * freq / (complex(0.0, 2.0) * pi * freq * L + rload + r0 * (1.0 + beta) + r0 * l * (2.0 + beta) / (1.0 - l) * 1.0 / (1.0 + complex(0.0, 2.0) * pi * freq * tau0 / (1 - l))) * np.exp(complex(-0.0, -2.0) * pi * freq * dt)
        dYddt[0:dYddt.size:2] = np.real(dYddtcomplex)
        dYddt[1:dYddt.size:2] = np.imag(dYddtcomplex)
        jac = np.column_stack((dYdrload, dYdr0, dYdbeta, dYdl, dYdL, dYdtau0, dYddt))
        return jac

    res = least_squares(residual, p0, bounds=bounds, loss='linear', max_nfev=1000, verbose=0, x_scale=(np.abs(p0)))
    popt = res['x']
    cost = res['cost']
    if not res['success']:
        print('Fit failed: ' + str(res['status']))
    else:
        if yerr is None:
            weights = complex(1.0, 1.0)
        else:
            weights = 1.0 / yerr.real + complex(0.0, 1.0) / yerr.imag
    weightvals = np.zeros((freq.size * 2), dtype=(np.float64))
    weightvals[0:weightvals.size:2] = weights.real ** 2
    weightvals[1:weightvals.size:2] = weights.imag ** 2
    jac = jaca(popt)
    jact = np.transpose(jac)
    wjac = np.zeros_like(jac)
    for ii in range(0, len(popt)):
        wjac[:, ii] = np.multiply(weightvals, jac[:, ii])

    pcovinv = np.dot(jact, wjac) + invpriorscov
    pcov = np.linalg.inv(pcovinv)
    return (
     popt, pcov, cost)


def convertfromtesvalues(popt, pcov):
    """
    Function to convert from Irwin's TES parameters (rload, r0, beta,
    l, L, tau0, dt) to the fit parameters (A, B, tau1, tau2, dt)
    
    Parameters
    ----------
    popt : ndarray
        Irwin's TES parameters in the order of (rload, r0, beta,
        l, L, tau0, dt), should be a 1-dimensional np.array of length 7
    pcov : ndarray
        The corresponding covariance matrix for Irwin's TES parameters.
        Should be a 2-dimensional, 7-by-7 np.array
        
    Returns
    -------
    popt_out : ndarray
        The fit parameters in the order of (A, B, tau1, tau2, dt)
    pcov_out : ndarray
        The corresponding covariance matrix for the fit parameters
        
    """
    rload = popt[0]
    r0 = popt[1]
    beta = popt[2]
    l = popt[3]
    L = popt[4]
    tau0 = popt[5]
    dt = popt[6]
    A = rload + r0 * (1.0 + beta)
    B = r0 * l / (1.0 - l) * (2.0 + beta)
    tau1 = tau0 / (1.0 - l)
    tau2 = L / (rload + r0 * (1.0 + beta))
    popt_out = np.array([A, B, tau1, tau2, dt])
    jac = np.zeros((5, 7))
    jac[(0, 0)] = 1.0
    jac[(0, 1)] = 1.0 + beta
    jac[(0, 2)] = r0
    jac[(1, 1)] = l / (1.0 - l) * (2.0 + beta)
    jac[(1, 2)] = l / (1.0 - l) * r0
    jac[(1, 3)] = r0 * (2.0 + beta) / (1.0 - l) + l / (1.0 - l) ** 2.0 * r0 * (2.0 + beta)
    jac[(2, 3)] = tau0 / (1.0 - l) ** 2.0
    jac[(2, 5)] = 1.0 / (1.0 - l)
    jac[(3, 0)] = -L / (rload + r0 * (1.0 + beta)) ** 2.0
    jac[(3, 1)] = -L * (1.0 + beta) / (rload + r0 * (1.0 + beta)) ** 2
    jac[(3, 2)] = -L * r0 / (rload + r0 * (1.0 + beta)) ** 2.0
    jac[(3, 4)] = 1.0 / (rload + r0 * (1.0 + beta))
    jac[(4, 6)] = 1.0
    jact = np.transpose(jac)
    pcov_out = np.dot(jac, np.dot(pcov, jact))
    return (
     popt_out, pcov_out)


def findpolefalltimes(params):
    """
    Function for taking TES params from a 1-pole, 2-pole, or 3-pole didv
    and calculating the falltimes (i.e. the values of the poles in the complex plane)
    
    Parameters
    ----------
    params : ndarray
        TES parameters for either 1-pole, 2-pole, or 3-pole didv. 
        This will be a 1-dimensional np.array of varying length, 
        depending on the fit. 1-pole fit has 3 parameters (A,tau2,dt), 
        2-pole fit has 5 parameters (A,B,tau1,tau2,dt), and 3-pole fit has 7 
        parameters (A,B,C,tau1,tau2,tau3,dt). The parameters should be in that 
        order, and any other number of parameters will print a warning and return zero.
        
    Returns
    -------
    np.sort(falltimes) : ndarray
        The falltimes for the didv fit, sorted from fastest to slowest.
        
    """
    if len(params) == 3:
        A, tau2, dt = params
        falltimes = np.array([tau2])
    else:
        if len(params) == 5:
            A, B, tau1, tau2, dt = params

            def twopoleequations(p):
                taup, taum = p
                eq1 = taup + taum - A / (A + B) * (tau1 + tau2)
                eq2 = taup * taum - A / (A + B) * tau1 * tau2
                return (eq1, eq2)

            taup, taum = fsolve(twopoleequations, (tau1, tau2))
            falltimes = np.array([taup, taum])
        else:
            if len(params) == 7:
                A, B, C, tau1, tau2, tau3, dt = params

                def threepoleequations(p):
                    taup, taum, taun = p
                    eq1 = taup + taum + taun - (A * tau1 + A * (1.0 - C) * tau2 + (A + B) * tau3) / (A * (1.0 - C) + B)
                    eq2 = taup * taum + taup * taun + taum * taun - (tau1 * tau2 + tau1 * tau3 + tau2 * tau3) * A / (A * (1.0 - C) + B)
                    eq3 = taup * taum * taun - tau1 * tau2 * tau3 * A / (A * (1.0 - C) + B)
                    return (eq1, eq2, eq3)

                taup, taum, taun = fsolve(threepoleequations, (tau1, tau2, tau3))
                falltimes = np.array([taup, taum, taun])
            else:
                print('Wrong number of input parameters, returning zero...')
                falltimes = np.zeros(1)
    return np.sort(falltimes)


def deconvolvedidv(x, trace, rshunt, sgamp, sgfreq, dutycycle):
    """
    Function for taking a trace with a known square wave jitter and 
    extracting the complex impedance via deconvolution of the square wave 
    and the TES response in frequency space.
    
    Parameters
    ----------
    x : ndarray
        Time values for the trace
    trace : ndarray
        The trace in time domain (in Amps)
    rshunt : float
        Shunt resistance for electronics (in Ohms)
    sgamp : float
        Peak to peak value of square wave jitter (in Amps,
        jitter in QET bias)
    sgfreq : float
        Frequency of square wave jitter
    dutycycle : float
        duty cycle of square wave jitter
        
    Returns
    -------
    freq : ndarray
        The frequencies that each point of the trace corresponds to
    didv : ndarray
        Complex impedance of the trace in frequency space
    zeroinds : ndarray
        Indices of the frequencies where the trace's Fourier Transform is zero. 
        Since we divide by the FT of the trace, we need to know which values should 
        be zero, so that we can ignore these points in the complex impedance.
        
    """
    tracelength = len(x)
    dx = x[1] - x[0]
    freq = fftfreq((len(x)), d=dx)
    st = fft(trace)
    sf = np.zeros_like(freq) * complex(0.0, 0.0)
    if dutycycle == 0.5:
        oddinds = np.abs(np.mod(np.absolute(freq / sgfreq), 2) - 1) < 1e-08
        sf[oddinds] = complex(0.0, 1.0) / (pi * freq[oddinds] / sgfreq) * sgamp * rshunt * tracelength
    else:
        oddinds = np.abs(np.mod(np.abs(freq / sgfreq), 2) - 1) < 1e-08
        sf[oddinds] = complex(-0.0, -1.0) / (2.0 * pi * freq[oddinds] / sgfreq) * sgamp * rshunt * tracelength * (np.exp(complex(-0.0, -2.0) * pi * freq[oddinds] / sgfreq * dutycycle) - 1)
        eveninds = np.abs(np.mod(np.abs(freq / sgfreq) + 1, 2) - 1) < 1e-08
        eveninds[0] = False
        sf[eveninds] = complex(-0.0, -1.0) / (2.0 * pi * freq[eveninds] / sgfreq) * sgamp * rshunt * tracelength * (np.exp(complex(-0.0, -2.0) * pi * freq[eveninds] / sgfreq * dutycycle) - 1)
    sf[tracelength // 2] = complex(0.0, 0.0)
    dvdi = sf / st
    zeroinds = np.abs(dvdi) < 1e-16
    dvdi[zeroinds] = complex(1.0, 1.0)
    didv = 1.0 / dvdi
    return (
     freq, didv, zeroinds)


class DIDV(object):
    __doc__ = "\n    Class for fitting a didv curve for different types of models of the didv. Also gives\n    various other useful values pertaining to the didv. This class supports doing 1, 2, and\n    3 pole fits, as well as a 2 pole priors fit. This is supported in a way that does\n    one dataset at a time.\n    \n    Attributes\n    ----------\n    rawtraces : ndarray\n        The array of rawtraces to use when fitting the didv. Should be of shape (number of\n        traces, length of trace in bins). This can be any units, as long as tracegain will \n        convert this to Amps.\n    fs : float\n        Sample rate of the data taken, in Hz\n    sgfreq : float\n        Frequency of the signal generator, in Hz\n    sgamp : float\n        Amplitude of the signal generator, in Amps (equivalent to jitter in the QET bias)\n    r0 : float\n        Resistance of the TES in Ohms\n    r0_err : float\n        Error in the resistance of the TES (Ohms)\n    rload : float\n        Load resistance of the circuit (rload = rshunt + rparasitic), Ohms\n    rload_err : float\n        Error in the load resistance, Ohms\n    rshunt : float\n        Shunt resistance in the circuit, Ohms\n    tracegain : float\n        The factor that the rawtraces should be divided by to convert the units to Amps. If rawtraces\n        already has units of Amps, then this should be set to 1.0\n    dutycycle : float\n        The duty cycle of the signal generator, should be a float between 0 and 1. Set to 0.5 by default\n    add180phase : boolean\n        If the signal generator is out of phase (i.e. if it looks like --__ instead of __--), then this\n        should be set to True. Adds half a period of the signal generator to the dt0 attribute\n    priors : ndarray\n        Prior known values of Irwin's TES parameters for the trace. \n        Should be in the order of (rload,r0,beta,l,L,tau0,dt)\n    invpriorscov : ndarray\n        Inverse of the covariance matrix of the prior known values of \n        Irwin's TES parameters for the trace (any values that are set \n        to zero mean that we have no knowledge of that parameter) \n    dt0 : float\n        The value of the starting guess for the time offset of the didv when fitting. \n        The best way to use this value if it isn't converging well is to run the fit multiple times, \n        setting dt0 equal to the fit's next value, and seeing where the dt0 value converges. \n        The fit can have a difficult time finding the value on the first run if it the initial value \n        is far from the actual value, so a solution is to do this iteratively. \n    freq : ndarray\n        The frequencies of the didv fit\n    time : ndarray\n        The times the didv trace\n    ntraces : float\n        The number of traces in the data\n    traces : ndarray\n        The traces being used in units of Amps and also truncated so as to include only an integer\n        number of signal generator periods\n    flatinds : ndarray\n        The indices where the traces are flat\n    tmean : ndarray\n        The average trace in time domain, units of Amps\n    zeroinds : ndarray\n        The indices of the didv fit in frequency space where the values should be zero\n    didvstd : ndarray\n        The complex standard deviation of the didv in frequency space for each frequency\n    didvmean : ndarray\n        The average trace converted to didv\n    offset : float\n        The offset (i.e. baseline value) of the didv trace, in Amps\n    offset_err : float\n        The error in the offset of the didv trace, in Amps\n    fitparams1 : ndarray\n        The fit parameters of the 1-pole fit, in order of (A, tau2, dt)\n    fitcov1 : ndarray\n        The corresponding covariance for the 1-pole fit parameters\n    fitcost1 : float\n        The cost of the 1-pole fit\n    irwinparams1 : ndarray\n        The Irwin parameters of the 1-pole fit, in order of (rtot, L , r0, rload, dt)\n    irwincov1 : ndarray\n        The corresponding covariance for the Irwin parameters for the 1-pole fit\n    falltimes1 : ndarray\n        The fall times of the 1-pole fit, same as tau2, in s\n    didvfit1_timedomain : ndarray\n        The 1-pole fit in time domain\n    didvfit1_freqdomain : ndarray\n        The 1-pole fit in frequency domain\n    fitparams2 : ndarray\n        The fit parameters of the 2-pole fit, in order of (A, B, tau1, tau2, dt)\n    fitcov2 : ndarray\n        The corresponding covariance for the 2-pole fit parameters\n    fitcost2 : float\n        The cost of the 2-pole fit\n    irwinparams2 : ndarray\n        The Irwin parameters of the 2-pole fit, in order of (rload, r0, beta, l, L, tau0, dt)\n    irwincov2 : ndarray\n        The corresponding covariance for the Irwin parameters for the 2-pole fit\n    falltimes2 : ndarray\n        The fall times of the 2-pole fit, tau_plus and tau_minus, in s\n    didvfit2_timedomain : ndarray\n        The 2-pole fit in time domain\n    didvfit2_freqdomain : ndarray\n        The 2-pole fit in frequency domain\n    fitparams3 : ndarray\n        The fit parameters of the 3-pole fit, in order of (A, B, C, tau1, tau2, tau3, dt)\n    fitcov3 : ndarray\n        The corresponding covariance for the 3-pole fit parameters\n    fitcost3 : float\n        The cost of the 3-pole fit\n    irwinparams3 : NoneType\n        The Irwin parameters of the 3-pole fit, this returns None now, as there is no model\n        that we convert to\n    irwincov3 : NoneType\n        The corresponding covariance for the Irwin parameters for the 3-pole fit,\n        also returns None\n    falltimes3 : ndarray\n        The fall times of the 3-pole fit in s\n    didvfit3_timedomain : ndarray\n        The 3-pole fit in time domain\n    didvfit3_freqdomain : ndarray\n        The 3-pole fit in frequency domain\n    fitparams2priors : ndarray\n        The fit parameters of the 2-pole priors fit, in order of (A, B, tau1, tau2, dt), converted from \n        the Irwin parameters\n    fitcov2priors : ndarray\n        The corresponding covariance for the 2-pole priors fit parameters\n    fitcost2priors : float\n        The cost of the 2-pole priors fit\n    irwinparams2priors : ndarray\n        The Irwin parameters of the 2-pole priors fit, in order of (rload, r0, beta, l, L, tau0, dt)\n    irwincov2priors : ndarray\n        The corresponding covariance for the Irwin parameters for the 2-pole priors fit\n    falltimes2priors : ndarray\n        The fall times of the 2-pole priors fit, tau_plus and tau_minus, in s\n    didvfit2priors_timedomain : ndarray\n        The 2-pole priors fit in time domain\n    didvfit2priors_freqdomain : ndarray\n        The 2-pole priors fit in frequency domain\n            \n    "

    def __init__(self, rawtraces, fs, sgfreq, sgamp, rshunt, tracegain=1.0, r0=0.3, r0_err=0.001, rload=0.01, rload_err=0.001, dutycycle=0.5, add180phase=False, priors=None, invpriorscov=None, dt0=1e-05):
        """
        Initialization of the DIDV class object
        
        Parameters
        ----------
        rawtraces : ndarray
            The array of rawtraces to use when fitting the didv. Should be of shape (number of
            traces, length of trace in bins). This can be any units, as long as tracegain will 
            convert this to Amps.
        fs : float
            Sample rate of the data taken, in Hz
        sgfreq : float
            Frequency of the signal generator, in Hz
        sgamp : float
            Amplitude of the signal generator, in Amps (equivalent to jitter in the QET bias)
        rshunt : float
            Shunt resistance in the circuit, Ohms
        tracegain : float, optional
            The factor that the rawtraces should be divided by to convert the units to Amps. If rawtraces
            already has units of Amps, then this should be set to 1.0
        r0 : float, optional
            Resistance of the TES in Ohms. Should be set if the Irwin parameters are desired.
        r0_err : float, optional
            Error in the resistance of the TES (Ohms). Should be set if the Irwin parameters are desired.
        rload : float, optional
            Load resistance of the circuit (rload = rshunt + rparasitic), Ohms. Should be set if the
            Irwin parameters are desired.
        rload_err : float,optional
            Error in the load resistance, Ohms. Should be set if the Irwin parameters are desired.
        dutycycle : float, optional
            The duty cycle of the signal generator, should be a float between 0 and 1. Set to 0.5 by default
        add180phase : boolean, optional
            If the signal generator is out of phase (i.e. if it looks like --__ instead of __--), then this
            should be set to True. Adds half a period of the signal generator to the dt0 attribute
        priors : ndarray, optional
            Prior known values of Irwin's TES parameters for the trace. 
            Should be in the order of (rload,r0,beta,l,L,tau0,dt)
        invpriorscov : ndarray, optional
            Inverse of the covariance matrix of the prior known values of 
            Irwin's TES parameters for the trace (any values that are set 
            to zero mean that we have no knowledge of that parameter) 
        dt0 : float, optional
            The value of the starting guess for the time offset of the didv when fitting. 
            The best way to use this value if it isn't converging well is to run the fit multiple times, 
            setting dt0 equal to the fit's next value, and seeing where the dt0 value converges. 
            The fit can have a difficult time finding the value on the first run if it the initial value 
            is far from the actual value, so a solution is to do this iteratively. 
        """
        self.rawtraces = rawtraces
        self.fs = fs
        self.sgfreq = sgfreq
        self.sgamp = sgamp
        self.r0 = r0
        self.r0_err = r0_err
        self.rload = rload
        self.rload_err = rload_err
        self.rshunt = rshunt
        self.tracegain = tracegain
        self.dutycycle = dutycycle
        self.add180phase = add180phase
        self.priors = priors
        self.invpriorscov = invpriorscov
        self.dt0 = dt0
        self.freq = None
        self.time = None
        self.ntraces = None
        self.traces = None
        self.flatinds = None
        self.tmean = None
        self.zeroinds = None
        self.didvstd = None
        self.didvmean = None
        self.offset = None
        self.offset_err = None
        self.fitparams1 = None
        self.fitcov1 = None
        self.fitcost1 = None
        self.irwinparams1 = None
        self.irwincov1 = None
        self.falltimes1 = None
        self.didvfit1_timedomain = None
        self.didvfit1_freqdomain = None
        self.fitparams2 = None
        self.fitcov2 = None
        self.fitcost2 = None
        self.irwinparams2 = None
        self.irwincov2 = None
        self.falltimes2 = None
        self.didvfit2_timedomain = None
        self.didvfit2_freqdomain = None
        self.fitparams3 = None
        self.fitcov3 = None
        self.fitcost3 = None
        self.irwinparams3 = None
        self.irwincov3 = None
        self.falltimes3 = None
        self.didvfit3_timedomain = None
        self.didvfit3_freqdomain = None
        self.fitparams2priors = None
        self.fitcov2priors = None
        self.fitcost2 = None
        self.irwinparams2priors = None
        self.irwincov2priors = None
        self.falltimes2priors = None
        self.didvfit2priors_timedomain = None
        self.didvfit2priors_freqdomain = None

    def processtraces(self):
        """
        This method processes the traces loaded to the DIDV class object. This sets 
        up the object for fitting.
        """
        dt = 1.0 / self.fs
        nbinsraw = len(self.rawtraces[0])
        bins = np.arange(0, nbinsraw)
        if self.add180phase:
            self.dt0 = self.dt0 + 1 / (2 * self.sgfreq)
        self.time = bins * dt - self.dt0
        period = 1.0 / self.sgfreq
        nperiods = np.floor(nbinsraw * dt / period)
        indmax = int(nperiods * self.fs / self.sgfreq)
        good_inds = range(0, indmax)
        self.time = self.time[good_inds]
        self.traces = self.rawtraces[:, good_inds] / self.tracegain
        nbins = len(self.traces[0])
        period_unscaled = self.fs / self.sgfreq
        flatindstemp = list()
        for i in range(0, int(nperiods)):
            flatindlow = int((float(i) + 0.25) * period_unscaled) + int(self.dt0 * self.fs)
            flatindhigh = int((float(i) + 0.48) * period_unscaled) + int(self.dt0 * self.fs)
            flatindstemp.append(range(flatindlow, flatindhigh))

        flatinds = np.array(flatindstemp).flatten()
        self.flatinds = flatinds[np.logical_and(flatinds > 0, flatinds < nbins)]
        didvs = list()
        for trace in self.traces:
            didvi = deconvolvedidv(self.time, trace, self.rshunt, self.sgamp, self.sgfreq, self.dutycycle)[1]
            didvs.append(didvi)

        didvs = np.array(didvs)
        cut = np.logical_not(np.isnan(didvs).any(axis=1))
        self.traces = self.traces[cut]
        didvs = didvs[cut]
        means = np.mean((self.traces), axis=1)
        self.tmean = np.mean((self.traces), axis=0)
        self.freq, self.zeroinds = deconvolvedidv(self.time, self.tmean, self.rshunt, self.sgamp, self.sgfreq, self.dutycycle)[::2]
        self.ntraces = len(self.traces)
        self.didvstd = stdcomplex(didvs) / np.sqrt(self.ntraces)
        self.didvstd[self.zeroinds] = complex(1e+20, 1e+20)
        self.didvmean = np.mean(didvs, axis=0)
        self.offset = np.mean(means)
        self.offset_err = np.std(means) / np.sqrt(self.ntraces)

    def dofit(self, poles):
        """
        This method does the fit that is specified by the variable poles. If the processtraces module
        has not been run yet, then this module will run that first. This module does not do the priors fit.
        
        Parameters
        ----------
        poles : int
            The fit that should be run. Should be 1, 2, or 3.
        """
        if self.tmean is None:
            self.processtraces()
        else:
            if poles == 1:
                A0_1pole, tau20_1pole = squarewaveguessparams(self.tmean, self.sgamp, self.rshunt)
                self.fitparams1, self.fitcov1, self.fitcost1 = fitdidv((self.freq), (self.didvmean), yerr=(self.didvstd), A0=A0_1pole, tau20=tau20_1pole, dt=(self.dt0), poles=poles, isloopgainsub1=False)
                self.irwinparams1, self.irwincov1 = converttotesvalues((self.fitparams1), (self.fitcov1), (self.r0), (self.rload), r0_err=(self.r0_err), rload_err=(self.rload_err))
                self.falltimes1 = findpolefalltimes(self.fitparams1)
                self.didvfit1_timedomain = convolvedidv(self.time, self.fitparams1[0], 0.0, 0.0, 0.0, self.fitparams1[1], 0.0, self.sgamp, self.rshunt, self.sgfreq, self.dutycycle) + self.offset
                self.didvfit1_freqdomain = onepoleadmittance(self.freq, self.fitparams1[0], self.fitparams1[1]) * np.exp(complex(-0.0, -2.0) * pi * self.freq * self.fitparams1[2])
            else:
                if poles == 2:
                    A0, B0, tau10, tau20, isloopgainsub1 = guessdidvparams((self.tmean), (self.tmean[self.flatinds]), (self.sgamp), (self.rshunt), L0=1e-07)
                    self.fitparams2, self.fitcov2, self.fitcost2 = fitdidv((self.freq), (self.didvmean), yerr=(self.didvstd), A0=A0, B0=B0, tau10=tau10, tau20=tau20, dt=(self.dt0), poles=poles, isloopgainsub1=isloopgainsub1)
                    self.irwinparams2, self.irwincov2 = converttotesvalues((self.fitparams2), (self.fitcov2), (self.r0), (self.rload), r0_err=(self.r0_err), rload_err=(self.rload_err))
                    self.falltimes2 = findpolefalltimes(self.fitparams2)
                    self.didvfit2_timedomain = convolvedidv(self.time, self.fitparams2[0], self.fitparams2[1], 0.0, self.fitparams2[2], self.fitparams2[3], 0.0, self.sgamp, self.rshunt, self.sgfreq, self.dutycycle) + self.offset
                    self.didvfit2_freqdomain = twopoleadmittance(self.freq, self.fitparams2[0], self.fitparams2[1], self.fitparams2[2], self.fitparams2[3]) * np.exp(complex(-0.0, -2.0) * pi * self.freq * self.fitparams2[4])
                else:
                    if poles == 3:
                        if self.fitparams2 is None:
                            A0, B0, tau10, tau20 = guessdidvparams((self.tmean), (self.tmean[self.flatinds]), (self.sgamp), (self.rshunt), L0=1e-07)[:-1]
                            B0 = -abs(B0)
                            C0 = -0.05
                            tau10 = -abs(tau10)
                            tau30 = 0.001
                            dt0 = self.dt0
                        else:
                            A0 = self.fitparams2[0]
                            B0 = -abs(self.fitparams2[1])
                            C0 = -0.05
                            tau10 = -abs(self.fitparams2[2])
                            tau20 = self.fitparams2[3]
                            tau30 = 0.001
                            dt0 = self.fitparams2[4]
                        isloopgainsub1 = guessdidvparams((self.tmean), (self.tmean[self.flatinds]), (self.sgamp), (self.rshunt), L0=1e-07)[(-1)]
                        self.fitparams3, self.fitcov3, self.fitcost3 = fitdidv((self.freq), (self.didvmean), yerr=(self.didvstd), A0=A0, B0=B0, C0=C0, tau10=tau10, tau20=tau20, tau30=tau30, dt=dt0, poles=3, isloopgainsub1=isloopgainsub1)
                        self.falltimes3 = findpolefalltimes(self.fitparams3)
                        self.didvfit3_timedomain = convolvedidv(self.time, self.fitparams3[0], self.fitparams3[1], self.fitparams3[2], self.fitparams3[3], self.fitparams3[4], self.fitparams3[5], self.sgamp, self.rshunt, self.sgfreq, self.dutycycle) + self.offset
                        self.didvfit3_freqdomain = threepoleadmittance(self.freq, self.fitparams3[0], self.fitparams3[1], self.fitparams3[2], self.fitparams3[3], self.fitparams3[4], self.fitparams3[5]) * np.exp(complex(-0.0, -2.0) * pi * self.freq * self.fitparams3[6])
                    else:
                        raise ValueError('The number of poles should be 1, 2, or 3.')

    def dopriorsfit(self):
        """
        This module runs the priorsfit, assuming that the priors and invpriorscov attributes have been set to
        the proper values.
        """
        if self.priors is None or self.invpriorscov is None:
            raise ValueError('Cannot do priors fit, priors values or inverse covariance matrix were not set')
        else:
            if self.tmean is None:
                self.processtraces()
            if self.irwinparams2 is None:
                A0, B0, tau10, tau20, isloopgainsub1 = guessdidvparams((self.tmean), (self.tmean[self.flatinds]), (self.sgamp), (self.rshunt), L0=1e-07)
                v2guess = np.array([A0, B0, tau10, tau20, self.dt0])
                priorsguess = converttotesvalues(v2guess, np.eye(5), self.r0, self.rload)[0]
                beta0 = abs(priorsguess[2])
                l0 = abs(priorsguess[3])
                L0 = abs(priorsguess[4])
                tau0 = abs(priorsguess[5])
                dt0 = self.dt0
            else:
                beta0 = abs(self.irwinparams2[2])
            l0 = abs(self.irwinparams2[3])
            L0 = abs(self.irwinparams2[4])
            tau0 = abs(self.irwinparams2[5])
            dt0 = self.irwinparams2[6]
        self.irwinparams2priors, self.irwincov2priors, self.irwincost2priors = fitdidvpriors((self.freq), (self.didvmean), (self.priors), (self.invpriorscov), yerr=(self.didvstd), r0=(abs(self.r0)), rload=(abs(self.rload)), beta=beta0, l=l0, L=L0, tau0=tau0, dt=dt0)
        self.fitparams2priors, self.fitcov2priors = convertfromtesvalues(self.irwinparams2priors, self.irwincov2priors)
        self.falltimes2priors = findpolefalltimes(self.fitparams2priors)
        self.didvfit2priors_timedomain = convolvedidv(self.time, self.fitparams2priors[0], self.fitparams2priors[1], 0.0, self.fitparams2priors[2], self.fitparams2priors[3], 0.0, self.sgamp, self.rshunt, self.sgfreq, self.dutycycle) + self.offset
        self.didvfit2priors_freqdomain = twopoleadmittancepriors(self.freq, self.irwinparams2priors[0], self.irwinparams2priors[1], self.irwinparams2priors[2], self.irwinparams2priors[3], self.irwinparams2priors[4], self.irwinparams2priors[5]) * np.exp(complex(-0.0, -2.0) * pi * self.freq * self.irwinparams2priors[6])

    def doallfits(self):
        """
        This module does all of the fits consecutively. The priors fit is not done if the 
        attributes priors and invpriorscov have not yet been set.
        """
        self.dofit(1)
        self.dofit(2)
        self.dofit(3)
        if self.priors is not None:
            if self.invpriorscov is not None:
                self.dopriorsfit()

    def get_irwinparams_dict(self, poles, lgcpriors=False):
        """
        Returns a dictionary with the irwin fit parameters for a given number of poles
        
        Parameters
        ----------
        poles: int
            The number of poles used for the fit
        lgcpriors: bool, optional
            If true, the values from the priors fit are returned
                
        Returns
        -------
        return_dict: dictionary
            The irwim parameters stored in a dictionary
        """
        return_dict = {}
        if poles == 1:
            if self.irwinparams1 is not None:
                return_dict['rtot'] = lgcpriors or self.irwinparams1[0]
                return_dict['L'] = self.irwinparams1[1]
                return_dict['r0'] = self.irwinparams1[2]
                return_dict['rload'] = self.irwinparams1[3]
                return_dict['dt'] = self.irwinparams1[4]
            else:
                print('Priors fit does not apply for single pole fit')
                return
                return return_dict
        if poles == 2:
            if not lgcpriors and self.irwinparams2 is not None:
                return_dict['rload'] = self.irwinparams2[0]
                return_dict['r0'] = self.irwinparams2[1]
                return_dict['beta'] = self.irwinparams2[2]
                return_dict['l'] = self.irwinparams2[3]
                return_dict['L'] = self.irwinparams2[4]
                return_dict['tau0'] = self.irwinparams2[5]
                return_dict['dt'] = self.irwinparams2[6]
                return_dict['tau_eff'] = self.falltimes2[(-1)]
                return return_dict
            else:
                if lgcpriors & (self.irwinparams2priors is not None):
                    return_dict['rload'] = self.irwinparams2priors[0]
                    return_dict['r0'] = self.irwinparams2priors[1]
                    return_dict['beta'] = self.irwinparams2priors[2]
                    return_dict['l'] = self.irwinparams2priors[3]
                    return_dict['L'] = self.irwinparams2priors[4]
                    return_dict['tau0'] = self.irwinparams2priors[5]
                    return_dict['dt'] = self.irwinparams2priors[6]
                    return_dict['tau_eff'] = self.falltimes2priors[(-1)]
                    return return_dict
                print('Priors fit has not been done yet')
                return
        if poles == 3:
            print('No Irwin Parameters for 3 pole fit')
            return
        raise ValueError('poles must be 1,2, or 3')

    def plot_full_trace(self, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
        """
        Module to plot the entire trace in time domain

        Parameters
        ----------
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
        """
        utils.plot_full_trace(self, poles=poles, plotpriors=plotpriors, lgcsave=lgcsave,
          savepath=savepath,
          savename=savename)

    def plot_single_period_of_trace(self, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
        """
        Module to plot a single period of the trace in time domain

        Parameters
        ----------
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
        """
        utils.plot_single_period_of_trace(self, poles=poles, plotpriors=plotpriors, lgcsave=lgcsave,
          savepath=savepath,
          savename=savename)

    def plot_zoomed_in_trace(self, poles='all', zoomfactor=0.1, plotpriors=True, lgcsave=False, savepath='', savename=''):
        """
        Module to plot a zoomed in portion of the trace in time domain. This plot zooms in on the
        overshoot of the didv.

        Parameters
        ----------
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        zoomfactor : float, optional, optional
            Number between zero and 1 to show different amounts of the zoomed in trace.
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
        """
        utils.plot_zoomed_in_trace(self, poles=poles, zoomfactor=zoomfactor, plotpriors=plotpriors, lgcsave=lgcsave,
          savepath=savepath,
          savename=savename)

    def plot_didv_flipped(self, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
        """
        Module to plot the flipped trace in time domain. This function should be used to 
        test if there are nonlinearities in the didv

        Parameters
        ----------
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
        """
        utils.plot_didv_flipped(self, poles=poles, plotpriors=plotpriors, lgcsave=lgcsave,
          savepath=savepath,
          savename=savename)

    def plot_re_im_didv(self, poles='all', plotpriors=True, lgcsave=False, savepath='', savename=''):
        """
        Module to plot the real and imaginary parts of the didv in frequency space.
        Currently creates two different plots.

        Parameters
        ----------
        poles : int, string, array_like, optional
            The pole fits that we want to plot. If set to "all", then plots
            all of the fits. Can also be set to just one of the fits. Can be set
            as an array of different fits, e.g. [1, 2]
        plotpriors : boolean, optional
            Boolean value on whether or not the priors fit should be plotted.
        lgcsave : boolean, optional
            Boolean value on whether or not the figure should be saved
        savepath : string, optional
            Where the figure should be saved. Saved in the current directory
            by default.
        savename : string, optional
            A string to append to the end of the file name if saving. Empty string
            by default.
        """
        utils.plot_re_im_didv(self, poles=poles, plotpriors=plotpriors, lgcsave=lgcsave,
          savepath=savepath,
          savename=savename)