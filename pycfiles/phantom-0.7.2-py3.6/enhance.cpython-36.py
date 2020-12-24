# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\phantom\enhance.py
# Compiled at: 2019-08-20 13:10:50
# Size of source mod 2**32: 2234 bytes
"""
Image enhancement algorithms.
"""
import cv2, numpy as np

def lucy_richardson_deconv(img, num_iterations, sigmag):
    """" Lucy-Richardson Deconvolution Function
    // input-1 img: NxM matrix image
    // input-2 num_iterations: number of iterations
    // input-3 sigma: sigma of point spread function (PSF)
    // output result: deconvolution result
    """
    epsilon = 2.2204e-16
    win_size = 8 * sigmag + 1
    j1 = img.copy()
    j2 = img.copy()
    w_i = img.copy()
    im_r = img.copy()
    t1 = np.zeros((img.shape), dtype=(np.float32))
    t2 = np.zeros((img.shape), dtype=(np.float32))
    tmp1 = np.zeros((img.shape), dtype=(np.float32))
    tmp2 = np.zeros((img.shape), dtype=(np.float32))
    lambda_ = 0
    for j in range(1, num_iterations):
        if j > 1:
            tmp1 = t1 * t2
            tmp2 = t2 * t2
            lambda_ = cv2.sumElems(tmp1)[0] / (cv2.sumElems(tmp2)[0] + epsilon)
        y = j1 + np.multiply(lambda_, np.subtract(j1, j2))
        y[y < 0] = 0
        re_blurred = cv2.GaussianBlur(y, (int(win_size), int(win_size)), sigmag)
        re_blurred[re_blurred <= 0] = epsilon
        cv2.divide(w_i, re_blurred, im_r, 1, cv2.CV_64F)
        im_r = im_r + epsilon
        im_r = cv2.GaussianBlur(im_r, (int(win_size), int(win_size)), sigmag)
        j2 = j1.copy()
        j1 = y * im_r
        t2 = t1.copy()
        t1 = j1 - y

    result = j1.copy()
    return result