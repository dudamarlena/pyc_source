# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/external/wavelet.py
# Compiled at: 2016-03-24 07:03:54
__doc__ = '\nContinuous wavelet transform module for Python. Includes a collection\nof routines for wavelet transform and statistical analysis via FFT\nalgorithm. This module references to the numpy, scipy and pylab Python\npackages.\n\nDISCLAIMER\n    This module is based on routines provided by C. Torrence and G.\n    Compo available at http://paos.colorado.edu/research/wavelets/\n    and on routines provided by A. Brazhe available at\n    http://cell.biophys.msu.ru/static/swan/.\n    \n    Modifications were done by R. Dussurget for implementing the pure\n    gaussian wavelet function (DOG, m=0).\n\n    This software may be used, copied, or redistributed as long as it\n    is not sold and this copyright notice is reproduced on each copy\n    made. This routine is provided as is without any express or implied\n    warranties whatsoever.\n\nAUTHOR\n    Sebastian Krieger\n    email: sebastian@nublia.com\n\nREVISION\n    3 (2013-07-18 10:17 +0200)\n    2 (2011-04-28 17:57 -0300)\n    1 (2010-12-24 21:59 -0300)\n\nREFERENCES\n    [1] Mallat, Stephane G. (1999). A wavelet tour of signal processing\n    [2] Addison, Paul S. The illustrated wavelet transform handbook\n    [3] Torrence, Christopher and Compo, Gilbert P. (1998). A Practical\n        Guide to Wavelet Analysis\n\n'
__version__ = '$Revision: 2 $'
from numpy import arange, ceil, concatenate, conjugate, cos, exp, isnan, log, log2, ones, pi, prod, real, sqrt, zeros, polyval
from numpy.fft import fft, ifft, fftfreq
from numpy.lib.polynomial import polyval
from pylab import find
from scipy.special import gamma, erf
from scipy.stats import chi2
from scipy.special.orthogonal import hermitenorm

class morlet:
    """Implements the Morlet wavelet class.

    Note that the input parameters f and f0 are angular frequencies.
    f0 should be more than 0.8 for this function to be correct, its
    default value is f0=6.

    """
    name = 'Morlet'

    def __init__(self, f0=6.0):
        self._set_f0(f0)

    def psi_ft(self, f):
        """Fourier transform of the approximate Morlet wavelet."""
        return pi ** (-0.25) * exp(-0.5 * (f - self.f0) ** 2.0)

    def psi(self, t):
        """Morlet wavelet as described in Torrence and Compo (1998)"""
        return pi ** (-0.25) * exp(complex(0.0, 1.0) * self.f0 * t - t ** 2.0 / 2.0)

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 4 * pi / (self.f0 + sqrt(2 + self.f0 ** 2))

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return 1.0 / sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_f0(self, f0):
        self.f0 = f0
        self.dofmin = 2
        if self.f0 == 6.0:
            self.cdelta = 0.776
            self.gamma = 2.32
            self.deltaj0 = 0.6
        else:
            self.cdelta = -1
            self.gamma = -1
            self.deltaj0 = -1


class paul:
    """Implements the Paul wavelet class.

    Note that the input parameter f is the angular frequency and that
    the default order for this wavelet is m=4.

    """
    name = 'Paul'

    def __init__(self, m=4):
        self._set_m(m)

    def psi_ft(self, f):
        """Fourier transform of the Paul wavelet."""
        return 2 ** self.m / sqrt(self.m * prod(range(2, 2 * self.m))) * f ** self.m * exp(-f) * (f > 0)

    def psi(self, t):
        """Paul wavelet as described in Torrence and Compo (1998)"""
        return 2 ** self.m * complex(0.0, 1.0) ** self.m * prod(range(2, self.m - 1)) / sqrt(pi * prod(range(2, 2 * self.m + 1))) * (1 - complex(0.0, 1.0) * t) ** (-(self.m + 1))

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 4 * pi / (2 * self.m + 1)

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_m(self, m):
        self.m = m
        self.dofmin = 2
        if self.m == 4:
            self.cdelta = 1.132
            self.gamma = 1.17
            self.deltaj0 = 1.5
        else:
            self.cdelta = -1
            self.gamma = -1
            self.deltaj0 = -1


class dog:
    """Implements the derivative of a Guassian wavelet class.

    Note that the input parameter f is the angular frequency and that
    for m=2 the DOG becomes the Mexican hat wavelet, which is then
    default.

    """
    name = 'DOG'

    def __init__(self, m=2):
        self._set_m(m)

    def psi_ft(self, f):
        """Fourier transform of the DOG wavelet."""
        res = (complex(0.0, -1.0)) ** self.m / sqrt(gamma(self.m + 0.5)) * f ** self.m * exp(-0.5 * f ** 2)
        if self.m == 0:
            res[0] = 0.0
        return res

    def psi(self, t):
        """DOG wavelet as described in Torrence and Compo (1998)

        The derivative of a Gaussian of order n can be determined using
        the probabilistic Hermite polynomials. They are explicitly
        written as:
            Hn(x) = 2 ** (-n / s) * n! * sum ((-1) ** m) * (2 ** 0.5 *
                x) ** (n - 2 * m) / (m! * (n - 2*m)!)
        or in the recursive form:
            Hn(x) = x * Hn(x) - nHn-1(x)

        Source: http://www.ask.com/wiki/Hermite_polynomials

        """
        p = hermitenorm(self.m)
        res = (-1) ** (self.m + 1) * polyval(p, t) * exp(-t ** 2 / 2) / sqrt(gamma(self.m + 0.5))
        if self.m == 0:
            res -= res.mean()
        return res

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 2 * pi / sqrt(self.m + 0.5)

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return 1.0 / sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_m(self, m):
        self.m = m
        self.dofmin = 1
        if self.m == 2:
            self.cdelta = 3.541
            self.gamma = 1.43
            self.deltaj0 = 1.4
        elif self.m == 6:
            self.cdelta = 1.966
            self.gamma = 1.37
            self.deltaj0 = 0.97
        elif self.m == 0:
            self.cdelta = 7.011324
            self.gamma = -1
            self.deltaj0 = -1
        else:
            self.cdelta = -1
            self.gamma = -1
            self.deltaj0 = -1


class mexican_hat(dog):
    """Implements the Mexican hat wavelet class.

    This class inherits the DOG class using m=2.

    """
    name = 'Mexican hat'

    def __init__(self):
        self._set_m(2)


def fftconv(x, y):
    """ Convolution of x and y using the FFT convolution theorem. """
    N = len(x)
    n = int(2 ** ceil(log2(N))) + 1
    X, Y, x_y = fft(x, n), fft(y, n), []
    for i in range(n):
        x_y.append(X[i] * Y[i])

    return ifft(x_y)[4:N + 4]


def cwt(signal, dt, dj=0.25, s0=-1, J=-1, wavelet=morlet()):
    """Continuous wavelet transform of the signal at specified scales.

    PARAMETERS
        signal (array like) :
            Input signal array
        dt (float) :
            Sample spacing.
        dj (float, optional) :
            Spacing between discrete scales. Default value is 0.25.
            Smaller values will result in better scale resolution, but
            slower calculation and plot.
        s0 (float, optional) :
            Smallest scale of the wavelet. Default value is 2*dt.
        J (float, optional) :
            Number of scales less one. Scales range from s0 up to
            s0 * 2**(J * dj), which gives a total of (J + 1) scales.
            Default is J = (log2(N*dt/so))/dj.
        wavelet (class, optional) :
            Mother wavelet class. Default is Morlet()

    RETURNS
        W (array like) :
            Wavelet transform according to the selected mother wavelet.
            Has (J+1) x N dimensions.
        sj (array like) :
            Vector of scale indices given by sj = s0 * 2**(j * dj),
            j={0, 1, ..., J}.
        freqs (array like) :
            Vector of Fourier frequencies (in 1 / time units) that
            corresponds to the wavelet scales.
        coi (array like) :
            Returns the cone of influence, which is a vector of N
            points containing the maximum Fourier period of useful
            information at that particular time. Periods greater than
            those are subject to edge effects.
        fft (array like) :
            Normalized fast Fourier transform of the input signal.
        fft_freqs (array like):
            Fourier frequencies (in 1/time units) for the calculated
            FFT spectrum.

    EXAMPLE
        mother = wavelet.Morlet(6.)
        wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(var,
            0.25, 0.25, 0.5, 28, mother)

    """
    n0 = len(signal)
    if s0 == -1:
        s0 = 2 * dt / wavelet.flambda()
    if J == -1:
        J = int(log2(n0 * dt / s0) / dj)
    N = n0
    signal_ft = fft(signal, N)
    ftfreqs = 2 * pi * fftfreq(N, dt)
    sj = s0 * 2.0 ** (arange(0, J + 1) * dj)
    freqs = 1.0 / (wavelet.flambda() * sj)
    W = zeros((len(sj), N), 'complex')
    D = zeros((len(sj), N), 'complex')
    for n, s in enumerate(sj):
        psi_ft_bar = (s * ftfreqs[1] * N) ** 0.5 * conjugate(wavelet.psi_ft(s * ftfreqs))
        W[n, :] = ifft(signal_ft * psi_ft_bar, N)
        D[n, :] = ifft(psi_ft_bar, N)

    sel = ~isnan(W).all(axis=1)
    sj = sj[sel]
    freqs = freqs[sel]
    W = W[sel, :]
    coi = n0 / 2.0 - abs(arange(0, n0) - (n0 - 1) / 2)
    coi = wavelet.flambda() * wavelet.coi() * dt * coi
    return (
     W[:, :n0], sj, freqs, coi, D[:, :n0], signal_ft[1:N / 2] / N ** 0.5,
     ftfreqs[1:N / 2] / (2.0 * pi))


def icwt(W, sj, dt, dj=0.25, w=morlet()):
    """Inverse continuous wavelet transform.

    PARAMETERS
        W (array like):
            Wavelet transform, the result of the cwt function.
        sj (array like):
            Vector of scale indices as returned by the cwt function.
        dt (float) :
            Sample spacing.
        dj (float, optional) :
            Spacing between discrete scales as used in the cwt
            function. Default value is 0.25.
        w (class, optional) :
            Mother wavelet class. Default is Morlet()

    RETURNS
        iW (array like) :
            Inverse wavelet transform.

    EXAMPLE
        mother = wavelet.Morlet(6.)
        wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(var,
            0.25, 0.25, 0.5, 28, mother)
        iwave = wavelet.icwt(wave, scales, 0.25, 0.25, mother)

    """
    a, b = W.shape
    c = sj.size
    if a == c:
        sj = (ones([b, 1]) * sj).transpose()
    elif b == c:
        sj = ones([a, 1]) * sj
    else:
        raise Warning, 'Input array dimensions do not match.'
    iW = dj * sqrt(dt) / w.cdelta * w.psi(0) * (real(W) / sj).sum(axis=0)
    return iW


def significance(signal, dt, scales, sigma_test=0, alpha=0.0, significance_level=0.95, dof=-1, wavelet=morlet()):
    """
    Significance testing for the onde dimensional wavelet transform.

    PARAMETERS
        signal (array like or float) :
            Input signal array. If a float number is given, then the
            variance is assumed to have this value. If an array is
            given, then its variance is automatically computed.
        dt (float, optional) :
            Sample spacing. Default is 1.0.
        scales (array like) :
            Vector of scale indices given returned by cwt function.
        sigma_test (int, optional) :
            Sets the type of significance test to be performed.
            Accepted values are 0, 1 or 2. If omitted assume 0.

            If set to 0, performs a regular chi-square test, according
            to Torrence and Compo (1998) equation 18.

            If set to 1, performs a time-average test (equation 23). In
            this case, dof should be set to the number of local wavelet
            spectra that where averaged together. For the global
            wavelet spectra it would be dof=N, the number of points in
            the time-series.

            If set to 2, performs a scale-average test (equations 25 to
            28). In this case dof should be set to a two element vector
            [s1, s2], which gives the scale range that were averaged
            together. If, for example, the average between scales 2 and
            8 was taken, then dof=[2, 8].
        alpha (float, optional) :
            Lag-1 autocorrelation, used for the significance levels.
            Default is 0.0.
        significance_level (float, optional) :
            Significance level to use. Default is 0.95.
        dof (variant, optional) :
            Degrees of freedom for significance test to be set
            according to the type set in sigma_test.
        wavelet (class, optional) :
            Mother wavelet class. Default is Morlet().

    RETURNS
        signif (array like) :
            Significance levels as a function of scale.
        fft_theor (array like):
            Theoretical red-noise spectrum as a function of period.

    """
    try:
        n0 = len(signal)
    except:
        n0 = 1

    J = len(scales) - 1
    s0 = min(scales)
    dj = log2(scales[1] / scales[0])
    if n0 == 1:
        variance = signal
    else:
        variance = signal.std() ** 2
    period = scales * wavelet.flambda()
    freq = dt / period
    dofmin = wavelet.dofmin
    Cdelta = wavelet.cdelta
    gamma_fac = wavelet.gamma
    dj0 = wavelet.deltaj0
    pk = lambda k, a, N: (1 - a ** 2) / (1 + a ** 2 - 2 * a * cos(2 * pi * k / N))
    fft_theor = pk(freq, alpha, n0)
    fft_theor = variance * fft_theor
    signif = fft_theor
    try:
        if dof == -1:
            dof = dofmin
    except:
        pass

    if sigma_test == 0:
        dof = dofmin
        chisquare = chi2.ppf(significance_level, dof) / dof
        signif = fft_theor * chisquare
    elif sigma_test == 1:
        if len(dof) == 1:
            dof = zeros(1, J + 1) + dof
        sel = find(dof < 1)
        dof[sel] = 1
        dof = dofmin * (1 + (dof * dt / gamma_fac / scales) ** 2) ** 0.5
        sel = find(dof < dofmin)
        dof[sel] = dofmin
        for n, d in enumerate(dof):
            chisquare = chi2.ppf(significance_level, d) / d
            signif[n] = fft_theor[n] * chisquare

    elif sigma_test == 2:
        if len(dof) != 2:
            raise Exception, 'DOF must be set to [s1, s2], the range of scale-averages'
        if Cdelta == -1:
            raise Exception, 'Cdelta and dj0 not defined for %s with f0=%f' % (
             wavelet.name, wavelet.f0)
        s1, s2 = dof
        sel = find((scales >= s1) & (scales <= s2))
        navg = sel.size
        if navg == 0:
            raise Exception, 'No valid scales between %d and %d.' % (s1, s2)
        Savg = 1 / sum(1.0 / scales[sel])
        Smid = exp((log(s1) + log(s2)) / 2.0)
        dof = dofmin * navg * Savg / Smid * (1 + (navg * dj / dj0) ** 2) ** 0.5
        fft_theor = Savg * sum(fft_theor[sel] / scales[sel])
        chisquare = chi2.ppf(significance_level, dof) / dof
        signif = dj * dt / Cdelta / Savg * fft_theor * chisquare
    else:
        raise Exception, 'sigma_test must be either 0, 1, or 2.'
    return (
     signif, fft_theor)