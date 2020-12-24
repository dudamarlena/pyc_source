# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\variation.py
# Compiled at: 2018-08-27 17:21:06
import numpy as np, loader, scipy.ndimage, warnings, variationoperators, msg

def variationiterator(simg, operationindex, roi=None):
    for i in range(len(simg)):
        yield simg.calcVariation(i, operationindex, roi)


def scanvariation(filepaths):
    simg = loader.multifilediffimage2(filepaths)
    for t in range(len(simg)):
        variationoperators.chisquared(simg, t, None)

    return


def filevariation(operationindex, filea, c, filec, roi=None):
    p = loader.loadimage(filea)
    n = loader.loadimage(filec)
    return variation(operationindex, p, c, n, roi)


def variation(operationindex, imga, imgb=None, imgc=None, roi=None):
    if imga is not None and imgb is not None and imgc is not None:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                p = scipy.ndimage.zoom(imga, 0.1, order=1)
                c = scipy.ndimage.zoom(imgb, 0.1, order=1)
                n = scipy.ndimage.zoom(imgc, 0.1, order=1)
                p = scipy.ndimage.gaussian_filter(p, 3)
                c = scipy.ndimage.gaussian_filter(c, 3)
                n = scipy.ndimage.gaussian_filter(n, 3)
                if roi is not None:
                    roi = scipy.ndimage.zoom(roi, 0.1, order=1)
                    roi = np.flipud(roi)
                else:
                    roi = 1
            with np.errstate(divide='ignore'):
                return variationoperators.operations.values()[operationindex](p, c, n, roi, None, None)
        except TypeError:
            msg.logMessage('Variation could not be determined for a frame.', msg.ERROR)

    else:
        msg.logMessage('Variation could not be determined for a frame.', msg.ERROR)
    return 0