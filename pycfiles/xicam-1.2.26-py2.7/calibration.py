# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\calibration.py
# Compiled at: 2019-03-07 15:21:14
from pipeline import center_approx
import integration, numpy as np, peakfinding
from xicam import config
from pyFAI import calibrant
from functools import wraps
import msg
from xicam import threads
from scipy import signal

def calibrationAlgorithm(f):

    @wraps(f)
    def wrapped(*args, **kwargs):
        msg.showMessage('Calibrating...')
        msg.showBusy()
        runnable = threads.RunnableIterator(f, iterator_args=args, iterator_kwargs=kwargs, callback_slot=showProgress, finished_slot=calibrationFinish)
        threads.add_to_queue(runnable)

    return wrapped


def calibrationFinish():
    msg.showMessage('Calibration complete!', 4)
    msg.hideBusy()


def showProgress(value):
    msg.showProgress(value)


@calibrationAlgorithm
def fourierAutocorrelation(dimg, calibrantkey):
    yield 0
    if dimg.transformdata is None:
        return
    else:
        yield 20
        config.activeExperiment.center = center_approx.center_approx(dimg.transformdata, dimg.mask)
        yield 40
        radialprofile = integration.pixel_2Dintegrate(dimg, mask=dimg.mask)
        yield 60
        peaks = np.array(peakfinding.findpeaks(np.arange(len(radialprofile)), radialprofile)).T
        yield 80
        peaks = peaks[peaks[:, 1].argsort()[::-1]]
        for peak in peaks:
            if peak[0] > 15 and not np.isinf(peak[1]):
                bestpeak = peak[0]
                break

        yield 85
        N = 1
        stds = [ np.std((peaks[:, 0] / (np.arange(len(peaks)) + i))[:4]) for i in range(1, 5) ]
        if min(stds) < 10:
            N = np.argmin(stds) + 1
        msg.logMessage(('Using peak #', N, ' for calibration...'))
        yield 90
        calibrant1stpeak = calibrant.ALL_CALIBRANTS[calibrantkey].dSpacing[(N - 1)]
        tth = 2 * np.arcsin(0.5 * config.activeExperiment.getvalue('Wavelength') / calibrant1stpeak / 1e-10)
        tantth = np.tan(tth)
        sdd = bestpeak * config.activeExperiment.getvalue('Pixel Size X') / tantth
        config.activeExperiment.setvalue('Detector Distance', sdd)
        dimg.invalidatecache()
        yield 100
        return


@calibrationAlgorithm
def rickerWavelets(dimg, calibrantkey):
    yield 0
    if dimg.transformdata is None:
        return
    else:
        yield 1
        radii = np.arange(30, 100)
        img = dimg.transformdata
        maxval = 0
        center = np.array([0, 0], dtype=np.int)
        for i in range(len(radii)):
            yield int(96.0 * i / len(radii)) + 1
            w = center_approx.tophat2(radii[i], scale=1000)
            im2 = signal.fftconvolve(img, w, 'same')
            if im2.max() > maxval:
                maxval = im2.max()
                center = np.array(np.unravel_index(im2.argmax(), img.shape))

        config.activeExperiment.center = center
        yield 97
        radialprofile = integration.pixel_2Dintegrate(dimg, mask=dimg.mask)
        yield 98
        peaks = np.array(peakfinding.findpeaks(np.arange(len(radialprofile)), radialprofile)).T
        yield 99
        peaks = peaks[peaks[:, 1].argsort()[::-1]]
        for peak in peaks:
            if peak[0] > 25 and not np.isinf(peak[1]):
                bestpeak = peak[0]
                break

        calibrant1stpeak = calibrant.ALL_CALIBRANTS[calibrantkey].dSpacing[0]
        tth = 2 * np.arcsin(0.5 * config.activeExperiment.getvalue('Wavelength') / calibrant1stpeak / 1e-10)
        tantth = np.tan(tth)
        sdd = bestpeak * config.activeExperiment.getvalue('Pixel Size X') / tantth
        config.activeExperiment.setvalue('Detector Distance', sdd)
        dimg.invalidatecache()
        yield 100
        return


import saxs_calibration as sc

@calibrationAlgorithm
def dpdakRefine(dimg, calibrantkey):
    if dimg.transformdata is None:
        return
    else:
        d_spacings = np.array(sorted(calibrant.ALL_CALIBRANTS[calibrantkey].dSpacing, key=float, reverse=True))
        geometry = config.activeExperiment.getAI()
        data = dimg.rawdata
        print 'Start parameter:'
        print geometry.getFit2D()
        fit_param = [
         'distance', 'rotation', 'tilt', 'center_x', 'center_y']
        center = (
         geometry.getFit2D()['centerX'],
         geometry.getFit2D()['centerY'])
        radial_pos = sc.radial_array(center, data.shape)
        x_data, y_data = [], []
        for i in range(len(d_spacings)):
            yield 100 / len(d_spacings) * i
            maxima_x, maxima_y, radial_pos = sc.ring_maxima(geometry, d_spacings[i], data, radial_pos, 10)
            x_data.extend(maxima_x)
            y_data.extend(maxima_y)

        sc.fit_geometry(geometry, (
         np.array(x_data), np.array(y_data)), d_spacings, fit_param)
        print 'Final parameter:'
        print geometry.getFit2D()
        config.activeExperiment.setvalue('Detector Distance', geometry.get_dist())
        config.activeExperiment.center = (geometry.getFit2D()['centerX'], geometry.getFit2D()['centerY'])
        yield 100
        return