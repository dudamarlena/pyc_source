# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\arc_finder.py
# Compiled at: 2018-08-27 17:21:06
import glob, os, numpy as np, scipy
from scipy import signal
import fabio, matplotlib.pyplot as plt, center_approx, integration, peakfindingrem, peakfinding, scipy.optimize as optimize, scipy.stats
from scipy import interpolate
from lmfit import minimize, Parameters
import cv2
from scipy.ndimage import filters
from scipy.fftpack import rfft, irfft
from skimage.restoration import denoise_bilateral
demo = True

def findpeaks(Y):
    Y = np.nan_to_num(Y)
    peakindices = scipy.signal.find_peaks_cwt(Y, np.arange(20, 100), noise_perc=5, min_length=10)
    return peakindices


def arcmask(img, cen, Rrange, Thetarange):
    y, x = np.indices(img.shape)
    r = np.sqrt((x - cen[0]) ** 2 + (y - cen[1]) ** 2)
    theta = np.arctan2(y - cen[1], x - cen[0]) / (2 * np.pi) * 360.0
    mask = (min(Rrange) < r) & (r < max(Rrange)) & (min(Thetarange) < theta) & (theta < max(Thetarange))
    return mask


def scanforarcs(radialprofile, cen):
    peakmax, peakmin = peakfindingrem.peakdet(range(len(radialprofile)), radialprofile, 10)
    peakind = peakmax[:, 0]
    return peakind


def mirroredgaussian(theta, a, b, c, d):
    val = (gaussian(theta, a, b, c, d) + gaussian(2 * np.pi - theta, a, b, c, d)) / 2.0
    return val


def gaussian(x, a, b, c, d):
    val = abs(a) * np.exp(-(x - b) ** 2.0 / c ** 2.0) + abs(d)
    return val


def vonmises(x, A, mu, kappa):
    return A * scipy.stats.vonmises.pdf(2 * (x - mu), kappa)


def mirroredvonmises(x, A, mu, kappa, floor):
    return A * (scipy.stats.vonmises.pdf(2 * (mu - x), kappa) + scipy.stats.vonmises.pdf(2 * (mu - x), kappa)) / 2 + floor


tworoot2ln2 = 2.0 * np.sqrt(2.0 * np.log(2.0))

def residual(params, x, data):
    A = params['A'].value
    mu = params['mu'].value
    kappa = params['kappa'].value
    floor = params['floor'].value
    model = mirroredvonmises(x, A, mu, kappa, floor)
    return data - model


def gaussianresidual(params, x, data, sig=1):
    A = params['A'].value
    mu = params['mu'].value
    sigma = params['sigma'].value
    floor = params['floor'].value
    model = gaussian(x, A, mu, sigma, floor)
    resids = data - model
    weighted = np.sqrt(resids ** 2 / sig ** 2)
    return weighted


def findgisaxsarcs(img, cen, experiment):
    radialprofile = integration.pixel_2Dintegrate(img, (cen[1], cen[0]), experiment.mask)
    arcs = peakfinding.findpeaks(None, radialprofile, (100, 50), gaussianwidthsigma=3, minimumsigma=100)
    plt.plot(radialprofile)
    plt.plot(arcs[0], arcs[1], 'ok')
    arcs = arcs[0]
    output = []
    _, unique = np.unique(arcs, return_index=True)
    for qmu in arcs[unique]:
        chiprofile = np.nan_to_num(integration.chi_2Dintegrate(img, (cen[1], cen[0]), qmu, mask=experiment.mask))
        plt.plot(np.arange(0, np.pi, 1 / 30.0), chiprofile, 'r')
        missingpointfloor = np.percentile(chiprofile, 15)
        badpoints = np.where(chiprofile < missingpointfloor)[0]
        goodpoints = np.where(chiprofile >= missingpointfloor)[0]
        chiprofile[badpoints] = np.interp(badpoints, goodpoints, chiprofile[goodpoints])
        plt.plot(np.arange(0, np.pi, 1 / 30.0), chiprofile, 'k')
        try:
            params = Parameters()
            params.add('A', value=np.max(chiprofile), min=0)
            params.add('mu', value=np.pi / 2, min=0, max=np.pi)
            params.add('kappa', value=0.1, min=0)
            params.add('floor', value=0.1, min=0)
            x = np.arange(0, np.pi, 1 / 30.0)
            out = minimize(residual, params, args=(x, chiprofile))
            print params
        except RuntimeError:
            print 'Fit failed at ' + qmu
            continue

        if params['kappa'].stderr > 100 or params['A'].stderr > 100:
            isring = True
        else:
            isring = False
        popt = [params['A'].value, params['mu'].value, params['kappa'].value, params['floor'].value]
        A, chimu, kappa, baseline = popt
        FWHM = np.arccos(np.log(0.5 * np.exp(kappa) + 0.5 * np.exp(-kappa)) / kappa)
        output.append([qmu, A, chimu, FWHM, baseline, isring])

    return output


def inpaint(img, mask):
    filled = None
    if False:
        img = img / (2 ^ 15) * 255
        plt.imshow(img.astype(np.uint8))
        plt.show()
        plt.imshow(mask)
        plt.show()
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask.astype(np.uint8), kernel, iterations=1)
        filled = cv2.inpaint(img.astype(np.uint8), mask.astype(np.uint8), 3, cv2.INPAINT_TELEA)
        plt.imshow(img)
        plt.show()
        return
    else:
        if True:
            valid = ~mask.astype(np.bool)
            coords = np.array(np.nonzero(valid)).T
            values = img[valid]
            it = interpolate.LinearNDInterpolator(coords, values)
            filled = it(list(np.ndindex(img.shape))).reshape(img.shape)
            plt.imshow(np.rot90(filled))
            plt.show()
        return filled


def findmaxs(orig):
    img = orig.copy()
    img = filters.gaussian_filter(img, 3)
    img = filters.minimum_filter(img, 4)
    img = filters.median_filter(img, 4)
    img -= np.min(img)
    img = denoise_bilateral(img, sigma_range=0.5, sigma_spatial=15)
    maxima = (img == filters.maximum_filter(img, (10, 10))) & (filters.maximum_filter(img, (50,
                                                                                            50)) > 1.5 * filters.minimum_filter(img, (50,
                                                                                                                                      50))) & (img > 2)
    maximachis, maximaqs = np.where(maxima == 1)
    plt.imshow(np.rot90(orig), interpolation='nearest')
    plt.plot(maximachis, 1000 - maximaqs, 'o', markersize=10, markeredgecolor='red', markerfacecolor='None', mew='4')
    plt.ylim([1000, 0])
    plt.xlim([0, 1000])
    plt.show()
    return (
     maximachis, maximaqs)


def fitarc(chiprofile):
    try:
        params = Parameters()
        params.add('A', value=np.max(chiprofile), min=0)
        params.add('mu', value=np.pi / 2, min=0, max=np.pi)
        params.add('kappa', value=0.1, min=0)
        params.add('floor', value=0.1, min=0)
        x = np.arange(0, np.pi, 1 / 30.0)
        out = minimize(residual, params, args=(x, chiprofile))
        print params
    except RuntimeError:
        print 'Fit failed.'

    if params['kappa'].stderr > 100 or params['A'].stderr > 100:
        isring = True
    else:
        isring = False
    popt = [params['A'].value, params['mu'].value, params['kappa'].value, params['floor'].value]
    A, chimu, kappa, baseline = popt
    FWHM = np.arccos(np.log(0.5 * np.exp(kappa) + 0.5 * np.exp(-kappa)) / kappa)
    return (
     A, chimu, FWHM, baseline, isring)


def fitarcgaussian(chiprofile, chi):
    try:
        params = Parameters()
        x = np.arange(np.size(chiprofile))
        roi = np.ones_like(chiprofile)
        roi[(chi - 30):(chi + 30)] = 0.0001
        params.add('A', value=np.max(chiprofile * (1 - roi)), min=0)
        params.add('mu', value=chi, min=0, max=len(chiprofile))
        params.add('sigma', value=20, min=0)
        params.add('floor', value=0.1, min=0)
        out = minimize(gaussianresidual, params, args=(x, chiprofile, roi), method='nelder')
    except RuntimeError:
        print 'Fit failed.'

    if params['sigma'].stderr > 100 or params['A'].stderr > 100:
        isring = False
    else:
        isring = False
    popt = [params['A'].value, params['mu'].value, params['sigma'].value, params['floor'].value]
    return popt


def findgisaxsarcs2(img, experiment):
    img = img.T.copy()
    cake, _, _ = integration.cake(img, experiment, mask=experiment.mask)
    maskcake, _, _ = integration.cake(experiment.mask.T, experiment)
    from fabio import edfimage
    fabimg = edfimage.edfimage(cake)
    filename = 'cake.edf'
    fabimg.write(filename)
    fabimg = edfimage.edfimage(maskcake)
    filename = 'cake_MASK.edf'
    fabimg.write(filename)
    img = inpaint(cake, maskcake)
    fabimg = edfimage.edfimage(img)
    filename = 'cake_LINEAR_INFILL.edf'
    fabimg.write(filename)
    maxchis, maxqs = findmaxs(img)
    out = []
    for chi, q in zip(maxchis, maxqs):
        slice = img[:, q - 5:q + 5]
        if np.max(slice) / np.min(slice) < 2:
            pass
        chiprofile = np.sum(slice, axis=1)
        x = np.arange(np.size(chiprofile))
        params = fitarcgaussian(chiprofile, chi)
        if params['mu'] > chi + 5 or params['mu'] < chi - 5:
            continue
        params.add('q', value=q)
        out.append(params)

    return out


if __name__ == '__main__':
    import xicam.config
    experiment = xicam.config.experiment()
    experiment.setvalue('Detector', 'pilatus2m')
    experiment.setvalue('Pixel Size X', 0.000172)
    experiment.setvalue('Pixel Size Y', 0.000172)
    experiment.mask = experiment.getDetector().calc_mask()
    for imgpath in glob.glob(os.path.join('../GISAXS samples/', '*.edf')):
        print 'Opening', imgpath
        img = fabio.open(imgpath).data
        cen = center_approx.gisaxs_center_approx(img)
        experiment.setcenter(cen)
        arcs = findgisaxsarcs2(img, experiment)
        ax = plt.gca()
        plt.axvline(cen[0], color='r')
        plt.axhline(cen[1], color='r')
        plt.imshow(np.log(img))
        from matplotlib.patches import Arc
        qratio = 1.78
        for arc in arcs:
            print arc
            if not np.isnan(arc['sigma'].value):
                if False:
                    arcartist = [Arc(xy=cen, width=arc['q'] * 2, height=arc['q'] * 2, angle=-90, theta1=0, theta2=360)]
                    ax.add_artist(arcartist[0])
                    arcartist[0].set_lw(3)
                else:
                    angle = -arc['mu'].value / 1000 * 360
                    theta1 = -abs(arc['sigma'].value * tworoot2ln2) / 1000 * 360 / 2
                    theta2 = abs(arc['sigma'].value * tworoot2ln2) / 1000 * 360 / 2
                    arcartist = [
                     Arc(xy=cen, width=arc['q'].value * 2 * qratio, height=arc['q'].value * 2 * qratio, angle=angle, theta1=theta1, theta2=theta2)]
                    for artist in arcartist:
                        ax.add_artist(artist)
                        artist.set_lw(3)

        plt.show()