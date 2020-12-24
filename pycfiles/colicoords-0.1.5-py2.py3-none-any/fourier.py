# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/fourier.py
# Compiled at: 2020-05-04 14:07:06
import numpy as np, scipy.interpolate as si, scipy.fftpack as sfft, scipy.optimize, sys
from six.moves import xrange
try:
    import fftlog
except ImportError:
    pass

def FFT_1D(x, f_x, N=None, compl=False):
    r"""
        This routine returns the 1D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`;
        the FT is already normalized.

        Parameters
        ----------

        `x`: array
            Abscissae.

        `f_x`: array
            Function sampled at `x`.

        `N`: integer, default = None
            Number of output points. If None, the same length of `x` is used.

        `compl`: boolean, default = False
            Return complex values.

        Returns
        ----------

        xf: array
            Frequencies in k_x (already sorted).

        yf: array
            Fourier transform (sorted by frequencies).
        """
    if len(x) != len(f_x):
        raise IndexError('x and f_x must have same length')
    if N == None:
        N = len(x)
    D = x[1] - x[0]
    xf_tmp = sfft.fftfreq(N, D) * 2.0 * np.pi
    yf_tmp = sfft.fft(f_x, N) * D
    xf, yf = (list(t) for t in zip(*sorted(zip(xf_tmp, yf_tmp))))
    xf = np.array(xf)
    yf = np.array(yf)
    if compl == False:
        yf = np.abs(yf)
    return (
     xf, yf)


def iFFT_1D(k, f_k, N=None, compl=False):
    r"""
        This routine returns the 1D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`;
        the inverse FT is already normalized.

        Parameters
        ----------

        `k`: array
            Abscissae.

        `f_k`: array
            Function sampled at `x`.

        `N`: integer, default = None
            Number of output points. If None, the same length of `x` is used.

        `compl`: boolean, default = False
            Return complex values.

        Returns
        ----------

        xf: array
            Frequencies in x (already sorted).

        yf: array
            Inverse Fourier transform (sorted by frequencies).
        """
    if len(k) != len(f_k):
        raise IndexError('k and f_k must have same length')
    if N == None:
        N = len(k)
    D = k[1] - k[0]
    xf_tmp = sfft.fftfreq(N, D) * 2.0 * np.pi
    yf_tmp = sfft.ifft(f_k, N) * D * N / (2.0 * np.pi)
    xf, yf = (list(t) for t in zip(*sorted(zip(xf_tmp, yf_tmp))))
    xf = np.array(xf)
    yf = np.array(yf)
    if compl == False:
        yf = np.abs(yf)
    return (
     xf, yf)


def FFT_2D(x, y, f_xy, compl=False, sort=True):
    r"""
        This routine returns the 2D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`; the FT is already normalized.

        Parameters
        ----------

        `x`: array
            Abscissa 1.

        `y`: array
            Abscissa 2.

        `f_xy`: 2D array
            Function sampled at (x,y).

        `compl`: boolean, default = False
            Return complex values.

        `sort`: boolean, dafault = True
            Return sorted frequencies and Fourier transform. If False, the NumPy order is used.

        Returns
        ----------

        KX: array
            Frequencies in k_x.

        KY: array
            Frequencies in k_y.

        F_KXKY: 2D array
            Fourier transform.
        """
    if f_xy.shape == (y.shape[0], x.shape[0]):
        f_xy = np.transpose(f_xy)

    def get_map(N):
        if N % 2 == 0:
            H = N // 2
            S = H
        else:
            H = (N + 1) // 2
            S = H - 1
        return [ i + S if i < H else i - H for i in xrange(N) ]

    Dx = x[1] - x[0]
    Dy = y[1] - y[0]
    Nx = len(x)
    Ny = len(y)
    KX_unsorted = sfft.fftfreq(Nx, Dx) * 2.0 * np.pi
    KY_unsorted = sfft.fftfreq(Ny, Dy) * 2.0 * np.pi
    f_kxky = np.fft.fft2(f_xy, axes=(-2, -1)) * Dx * Dy
    if sort:
        F_KXKY = np.zeros(f_kxky.shape, dtype=complex)
        mapX = get_map(Nx)
        mapY = get_map(Ny)
        for i, j in np.ndindex((Nx, Ny)):
            F_KXKY[(mapX[i], mapY[j])] = f_kxky[(i, j)]

        KX = np.sort(KX_unsorted)
        KY = np.sort(KY_unsorted)
    else:
        F_KXKY = f_kxky
        KX = KX_unsorted
        KY = KY_unsorted
    if compl == False:
        F_KXKY = np.abs(F_KXKY)
    return (
     KX, KY, F_KXKY)


def iFFT_2D(kx, ky, f_kxky, compl=False, sort=True):
    r"""
        This routine returns the inverse 2D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`; the FT is already normalized.

        Parameters
        ----------

        `kx`: array
            Abscissa 1.

        `ky`: array
            Abscissa 2.

        `f_kxky`: 2D array
            Function sampled at (kx,ky).

        `compl`: boolean, default = False
            Return complex values.

        `sort`: boolean, dafault = True
            Return sorted frequencies and Fourier transform. If False, the NumPy order is used.

        Returns
        ----------

        X: array
            Frequencies in x.

        Y: array
            Frequencies in y.

        F_XY: 2D array
            Fourier transform.
        """
    if f_kxky.shape == (ky.shape[0], kx.shape[0]):
        f_kxky = np.transpose(f_kxky)

    def get_map(N):
        if N % 2 == 0:
            H = N // 2
            S = H
        else:
            H = (N + 1) // 2
            S = H - 1
        return [ i + S if i < H else i - H for i in xrange(N) ]

    Dx = kx[1] - kx[0]
    Dy = ky[1] - ky[0]
    Nx = len(kx)
    Ny = len(ky)
    X_unsorted = sfft.fftfreq(Nx, Dx) * 2.0 * np.pi
    Y_unsorted = sfft.fftfreq(Ny, Dy) * 2.0 * np.pi
    f_xy = np.fft.ifft2(f_kxky, axes=(-2, -1)) * Dx * Dy * Nx * Ny / (2.0 * np.pi) ** 2.0
    if sort:
        F_XY = np.zeros(f_xy.shape, dtype=complex)
        mapX = get_map(Nx)
        mapY = get_map(Ny)
        for i, j in np.ndindex((Nx, Ny)):
            F_XY[(mapX[i], mapY[j])] = f_xy[(i, j)]

        X = np.sort(X_unsorted)
        Y = np.sort(Y_unsorted)
    else:
        F_XY = f_xy
        X = X_unsorted
        Y = Y_unsorted
    if compl == False:
        F_XY = np.abs(F_XY)
    return (
     X, Y, F_XY)


def FFT_3D(x, y, z, f_xyz, compl=False, sort=True):
    r"""
        This routine returns the 3D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`; the FT is already normalized.

        Parameters
        ----------

        `x`: array
            Abscissa 1.

        `y`: array
            Abscissa 2.

        `z`: array
            Abscissa 3.

        `f_xyz`: 3D array
            Function sampled at (x,y,z).

        `compl`: boolean, default = False
            Return complex values.

        `sort`: boolean, dafault = True
            Return sorted frequencies and Fourier transform. If False, the NumPy order is used.

        Returns
        ----------

        KX: array
            Frequencies in k_x.

        KY: array
            Frequencies in k_y.

        KZ: array
            Frequencies in k_z.

        F_KXKYKZ: 3D array
            Fourier transform.
        """
    if f_xyz.shape == (y.shape[0], x.shape[0], z.shape[0]):
        f_xyz = np.transpose(f_xyz, (1, 0, 2))

    def get_map(N):
        if N % 2 == 0:
            H = N // 2
            S = H
        else:
            H = (N + 1) // 2
            S = H - 1
        return [ i + S if i < H else i - H for i in xrange(N) ]

    Dx = x[1] - x[0]
    Dy = y[1] - y[0]
    Dz = z[1] - z[0]
    Nx = len(x)
    Ny = len(y)
    Nz = len(z)
    f_kxkykz = sfft.fftn(f_xyz, axes=(-3, -2, -1)) * Dx * Dy * Dz
    if sort:
        F_KXKYKZ = np.zeros(f_kxkykz.shape, dtype=complex)
        mapX = get_map(Nx)
        mapY = get_map(Ny)
        mapZ = get_map(Nz)
        for i, j, k in np.ndindex((Nx, Ny, Nz)):
            F_KXKYKZ[(mapX[i], mapY[j], mapZ[k])] = f_kxkykz[(i, j, k)]

        KX = np.sort(sfft.fftfreq(Nx, Dx) * 2.0 * np.pi)
        KY = np.sort(sfft.fftfreq(Ny, Dy) * 2.0 * np.pi)
        KZ = np.sort(sfft.fftfreq(Nz, Dz) * 2.0 * np.pi)
    else:
        F_KXKYKZ = f_kxkykz
        KX = sfft.fftfreq(Nx, Dx) * 2.0 * np.pi
        KY = sfft.fftfreq(Ny, Dy) * 2.0 * np.pi
        KZ = sfft.fftfreq(Nz, Dz) * 2.0 * np.pi
    if compl == False:
        F_KXKYKZ = np.abs(F_KXKYKZ)
    return (
     KX, KY, KZ, F_KXKYKZ)


def iFFT_3D(kx, ky, kz, f_kxkykz, compl=False, sort=True):
    r"""
        This routine returns the inverse 3D FFT of a linearly-spaced array.
        It returns the radian frequencies and the Fourier transform.
        N.B.: the frequencies and FT are sorted.
        Note on normalizations: the returned frequencies are :math:`2\pi\nu`; the FT is already normalized.

        Parameters
        ----------

        `kx`: array
            Abscissa 1.

        `ky`: array
            Abscissa 2.

        `kz`: array
            Abscissa 3.

        `f_kxkykz`: 3D array
            Function sampled at (kx,ky,kz).

        `compl`: boolean, default = False
            Return complex values.

        `sort`: boolean, dafault = True
            Return sorted frequencies and Fourier transform. If False, the NumPy order is used.

        Returns
        ----------

        X: array
            Frequencies in x.

        Y: array
            Frequencies in y.

        Z: array
            Frequencies in z.

        F_XYZ: 3D array
            Fourier transform.
        """
    if f_kxkykz.shape == (ky.shape[0], kx.shape[0], kz.shape[0]):
        f_kxkykz = np.transpose(f_kxkykz, (1, 0, 2))

    def get_map(N):
        if N % 2 == 0:
            H = N // 2
            S = H
        else:
            H = (N + 1) // 2
            S = H - 1
        return [ i + S if i < H else i - H for i in xrange(N) ]

    Dx = kx[1] - kx[0]
    Dy = ky[1] - ky[0]
    Dz = kz[1] - kz[0]
    Nx = len(kx)
    Ny = len(ky)
    Nz = len(kz)
    f_xyz = sfft.ifftn(f_kxkykz, axes=(-3, -2, -1)) * Dx * Dy * Dz * Nx * Ny * Nz / (2.0 * np.pi) ** 3.0
    if sort:
        F_XYZ = np.zeros(f_xyz.shape, dtype=complex)
        mapX = get_map(Nx)
        mapY = get_map(Ny)
        mapZ = get_map(Nz)
        for i, j, k in np.ndindex((Nx, Ny, Nz)):
            F_XYZ[(mapX[i], mapY[j], mapZ[k])] = f_xyz[(i, j, k)]

        X = np.sort(sfft.fftfreq(Nx, Dx) * 2.0 * np.pi)
        Y = np.sort(sfft.fftfreq(Ny, Dy) * 2.0 * np.pi)
        Z = np.sort(sfft.fftfreq(Nz, Dz) * 2.0 * np.pi)
    else:
        F_XYZ = f_xyz
        X = sfft.fftfreq(Nx, Dx) * 2.0 * np.pi
        Y = sfft.fftfreq(Ny, Dy) * 2.0 * np.pi
        Z = sfft.fftfreq(Nz, Dz) * 2.0 * np.pi
    if compl == False:
        F_XYZ = np.abs(F_XYZ)
    return (
     X, Y, Z, F_XYZ)


def FFT_iso_3D(r, f, N=4096):
    r"""
        This routine returns the FFT of a radially symmetric function.
        It employs the ``FFTlog`` module, which in turn makes use of the Hankel transform: therefore the function
        that will be actually transformed is :math:`f(r) \ (2\pi r)^{1.5}/k^{1.5}`.
        N.B. Since the integral is performed in log-space, the exponent of `r` is 1.5 instead of 0.5.
        The computation is

        .. math ::

          f(k) = \int_0^\infty dr \ 4\pi r^2 \ f(r) \ j_0(kr)

        Parameters
        ----------

        `r`: array
            Abscissae of function, log-spaced.

        `f`: array
            ordinates of function.

        `N`: int, default = 4096
            Number of output points

        Returns
        ----------

        kk: array
            Frequencies.

        Fk: array
            Transformed array.
        """
    mu = 0.5
    q = 0
    kr = 1
    kropt = 1
    tdir = 1
    logrc = (np.max(np.log10(r)) + np.min(np.log10(r))) / 2.0
    dlogr = (np.max(np.log10(r)) - np.min(np.log10(r))) / N
    dlnr = dlogr * np.log(10.0)
    if N % 2 == 0:
        nc = N / 2
    else:
        nc = (N + 1) / 2
    r_t = 10.0 ** (logrc + (np.arange(1, N + 1) - nc) * dlogr)
    funct = si.interp1d(r, f, kind='cubic', fill_value='extrapolate')
    ar = funct(r_t) * (2.0 * np.pi * r_t) ** 1.5
    kr, xsave, ok = fftlog.fhti(N, mu, dlnr, q, kr, kropt)
    logkc = np.log10(kr) - logrc
    ak = fftlog.fht(ar.copy(), xsave, tdir)
    if N % 2 == 0:
        kk = 10.0 ** (logkc + (np.arange(N) - nc) * dlogr)
    else:
        kk = 10.0 ** (logkc + (np.arange(1, N + 1) - nc) * dlogr)
    Fk = ak / kk ** 1.5
    return (
     kk, Fk)


def iFFT_iso_3D(k, f, N=4096):
    r"""
        This routine returns the inverse FFT of a radially symmetric function.
        It employs the ``FFTlog`` module, which in turn makes use of the Hankel transform: therefore the function
        that will be actually transformed is :math:`f(k) \ k^{1.5}/(2\pi r)^{1.5}`.
        N.B. Since the integral is performed in log-space, the exponent of `r` is 1.5 instead of 0.5.
        The computation is

        .. math ::

          f(r) = \int_0^\infty \frac{dk \ k^2}{2\pi^2} \ f(k) \ j_0(kr)

        Parameters
        ----------

        `k`: array
            Abscissae of function, log-spaced.

        `f`: array
            ordinates of function.

        `N`: int, default = 4096
            Number of output points

        Returns
        ----------

        rr: array
            Frequencies.

        Fr: array
            Transformed array.
        """
    mu = 0.5
    q = 0
    kr = 1
    kropt = 1
    tdir = -1
    logkc = (np.max(np.log10(k)) + np.min(np.log10(k))) / 2.0
    dlogk = (np.max(np.log10(k)) - np.min(np.log10(k))) / N
    dlnk = dlogk * np.log(10.0)
    if N % 2 == 0:
        nc = N / 2
    else:
        nc = (N + 1) / 2
    k_t = 10.0 ** (logkc + (np.arange(1, N + 1) - nc) * dlogk)
    funct = si.interp1d(k, f, kind='cubic', fill_value='extrapolate')
    ak = funct(k_t) * k_t ** 1.5
    kr, xsave, ok = fftlog.fhti(N, mu, dlnk, q, kr, kropt)
    logrc = np.log10(kr) - logkc
    ar = fftlog.fht(ak.copy(), xsave, tdir)
    if N % 2 == 0:
        rr = 10.0 ** (logrc + (np.arange(N) - nc) * dlogk)
    else:
        rr = 10.0 ** (logrc + (np.arange(1, N + 1) - nc) * dlogk)
    Fr = ar / (2 * np.pi * rr) ** 1.5
    return (
     rr, Fr)


def Hankel(r, f, N=4096, order=0.5):
    r"""
        This routine returns the Hankel transform of order :math:`\nu` of a log-spaced function.
        The computation is

        .. math ::

          f_\nu(k) = \int_0^\infty \ dr \ r \ f(r) \ J_\nu(kr)

        .. warning::

         Because of log-spacing, an extra `r` factor has been already added in the code.

        .. warning::

         If ``order = 0.5`` it is similar to the 3D Fourier transform of a spherically symmetric function.

        Parameters
        ----------

        `r`: array
            Abscissae of function, log-spaced.

        `f`: array
            ordinates of function.

        `N`: int, default = 4096
            Number of output points

        `order`: float, default = 0.5
            Order of the transform (Bessel polynomial).

        Returns
        ----------

        kk: array
            Frequencies.

        Fk: array
            Transformed array.
        """
    mu = order
    q = 0
    kr = 1
    kropt = 1
    tdir = 1
    logrc = (np.max(np.log10(r)) + np.min(np.log10(r))) / 2.0
    dlogr = (np.max(np.log10(r)) - np.min(np.log10(r))) / N
    dlnr = dlogr * np.log(10.0)
    if N % 2 == 0:
        nc = N / 2
    else:
        nc = (N + 1) / 2
    r_t = 10.0 ** (logrc + (np.arange(1, N + 1) - nc) * dlogr)
    funct = si.interp1d(r, f, kind='cubic', fill_value='extrapolate')
    ar = funct(r_t) * r_t
    kr, xsave, ok = fftlog.fhti(N, mu, dlnr, q, kr, kropt)
    logkc = np.log10(kr) - logrc
    Fk = fftlog.fht(ar.copy(), xsave, tdir)
    if N % 2 == 0:
        kk = 10.0 ** (logkc + (np.arange(N) - nc) * dlogr)
    else:
        kk = 10.0 ** (logkc + (np.arange(1, N + 1) - nc) * dlogr)
    Fk /= kk
    return (
     kk, Fk)


def iHankel(k, f, N=4096, order=0.5):
    r"""
        This routine returns the inverse Hankel transform of order :math:`\nu` of a log-spaced function.
        The computation is

        .. math ::

          f(r) = \int_0^\infty \ dk \ k \ f(k) \ J_\nu(kr)

        .. warning::

         Because of log-spacing, an extra `k` factor has been already added in the code.

        .. warning::

         If ``order = 0.5`` it is similar to the 3D Fourier transform of a spherically symmetric function.

        Parameters
        ----------

        `k`: array
            Abscissae of function, log-spaced.

        `f`: array
            ordinates of function.

        `N`: int, default = 4096
            Number of output points

        `order`: float, default = 0.5
            Order of the transform (Bessel polynomial).

        Returns
        ----------

        rr: array
            Frequencies.

        Fr: array
            Transformed array.
        """
    mu = order
    q = 0
    kr = 1
    kropt = 1
    tdir = -1
    logkc = (np.max(np.log10(k)) + np.min(np.log10(k))) / 2.0
    dlogk = (np.max(np.log10(k)) - np.min(np.log10(k))) / N
    dlnk = dlogk * np.log(10.0)
    if N % 2 == 0:
        nc = N / 2
    else:
        nc = (N + 1) / 2
    k_t = 10.0 ** (logkc + (np.arange(1, N + 1) - nc) * dlogk)
    funct = si.interp1d(k, f, kind='cubic', fill_value='extrapolate')
    ak = funct(k_t) * k_t
    kr, xsave, ok = fftlog.fhti(N, mu, dlnk, q, kr, kropt)
    logrc = np.log10(kr) - logkc
    Fr = fftlog.fht(ak.copy(), xsave, tdir)
    if N % 2 == 0:
        rr = 10.0 ** (logrc + (np.arange(N) - nc) * dlogk)
    else:
        rr = 10.0 ** (logrc + (np.arange(1, N + 1) - nc) * dlogk)
    Fr /= rr
    return (
     rr, Fr)