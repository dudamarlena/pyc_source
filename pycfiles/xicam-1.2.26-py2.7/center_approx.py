# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\center_approx.py
# Compiled at: 2018-09-13 23:16:46
import glob, os, time, numpy as np, fabio
from scipy import optimize
from scipy import signal
import saxs_calibration, peakfindingrem

def approx_width(r):
    """
    linearly varies the peak width between GISAXS, where peaks are
    thinner to GIWAXS, where peaks are fewer but wider.
    """
    return 0.047 * r + 1.8261


def tophat2(radius, scale=1):
    """
    convolution kernel, revolved to form a ring, with Mexican Hat
    profile along the radial direction.

    radius : peak position along the radius
    scale  : magnification factor
    """
    width = approx_width(radius)
    N = np.round(radius) + 3 * round(width) + 1
    x = np.arange(-N, N)
    x, y = np.meshgrid(x, x)
    t = np.sqrt(x ** 2 + y ** 2) - radius
    s = width
    a = scale / np.sqrt(2 * np.pi) / s ** 3
    w = a * (1 - (t / s) ** 2) * np.exp(-t ** 2 / s ** 2 / 2.0)
    return w


def calc_R(x, y, xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)


def f(c, x, y):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(x, y, *c)
    return Ri - Ri.mean()


def fitpointstocircle(cnt):
    """Fit a Nx2 array of points to a circle; return center, radius, and fit residue"""
    cnt = np.array(cnt.reshape((-1, 2)))
    if cnt.shape[0] < 3:
        return (None, None, None, None)
    else:
        x = cnt[:, 0]
        y = cnt[:, 1]
        x_m = np.mean(x)
        y_m = np.mean(y)
        center_estimate = (x_m, y_m)
        center, ier = optimize.leastsq(f, center_estimate, args=(x, y))
        xc, yc = center
        Ri = calc_R(x, y, *center)
        R = Ri.mean()
        residu = np.sum((Ri - R) ** 2)
        return (xc, yc, R, residu)


from xicam import debugtools

@debugtools.timeit
def center_approx(img, mask, log=False):
    if log:
        img = img.astype(np.float)
        with np.errstate(divide='ignore', invalid='ignore'):
            img = np.log(img * (img > 0) + 1)
    con = signal.fftconvolve(img.astype(int) * mask * (img > 0), img.astype(int) * mask * (img > 0)) / np.sqrt(signal.fftconvolve(np.ones_like(img), np.ones_like(img)))
    cen = np.array(np.unravel_index(con.argmax(), con.shape)) / 2.0
    return cen


def gisaxs_center_approx(img, log=False):
    img = img.astype(np.float)
    if log:
        with np.errstate(divide='ignore', invalid='ignore'):
            img = np.log(img + 3) - np.log(3)
    x = 0
    xcenter = 0
    y = 10000
    ycenter = 0
    for i in range(0, img.shape[1]):
        if x <= sum(img[:, i]):
            x = sum(img[:, i])
            xcenter = i

    q = 4 * sum(img[img.shape[0] - 5, :])
    i = 0
    x = np.sum(img[:, :150], axis=1)
    for i in range(1, np.size(x)):
        if x[i] == 0:
            x[i] = x[(i - 1)]

    t = np.size(x) - 20
    x = signal.convolve(signal.convolve(x[:t], signal.gaussian(7, std=4)), [1, -1])
    i = 0
    while y != np.min(x):
        y = x[i]
        ycenter = i - 6
        i = i + 1

    cen = (xcenter, ycenter)
    return cen


def refinecenter(dimg):
    imgcopy = dimg.rawdata.T
    d_spacings = np.array([58.367, 29.1835, 19.45567, 14.59175, 11.6734, 9.72783, 8.33814, 7.29587, 6.48522, 5.8367])
    geometry = dimg.experiment.getGeometry()
    fit_param = [
     'center_x', 'center_y', 'distance', 'rotation', 'tilt']
    fit_thread = saxs_calibration.FitThread(geometry, d_spacings, imgcopy, fit_param, 40)
    fit_thread.start()
    while fit_thread.is_alive():
        time.sleep(0.1)

    return (
     geometry.getFit2D()['centerX'], geometry.getFit2D()['centerY'])