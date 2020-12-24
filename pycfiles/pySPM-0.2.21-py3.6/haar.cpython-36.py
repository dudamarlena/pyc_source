# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\utils\haar.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 1567 bytes
import numpy as np, copy, pywt

def sign(abs_var, sign_var):
    return abs(abs_var) * (1 - np.where(sign_var < 0, 2 * sign_var, sign_var))


def hfilter(diff_image, var_image, threshold=1, ndamp=10):
    """
    This code was inspired from: https://github.com/spacetelescope/sprint_notebooks/blob/master/lucy_damped_haar.ipynb
    I believe it was initially written by Justin Ely: https://github.com/justincely
    It was buggy and not working properly with every image sizes.
    I have thus exchanged it by using pyWavelet (pywt) and a custom function htrans
    to calculate the matrix for the var_image.
    """
    him, coeff_slices = pywt.coeffs_to_array((pywt.wavedec2(diff_image.astype(np.float), 'haar')), padding=0)
    dvarim = htrans(var_image.astype(np.float))
    sqhim = (him / threshold) ** 2 / dvarim
    index = np.where(sqhim < 1)
    if len(index[0]) == 0:
        return diff_image
    else:
        sqhim = sqhim[index] * (ndamp * sqhim[index] ** (ndamp - 1) - (ndamp - 1) * sqhim[index] ** ndamp)
        him[index] = sign(threshold * np.sqrt(dvarim[index] * sqhim), him[index])
        return pywt.waverec2(pywt.array_to_coeffs(him, coeff_slices, output_format='wavedec2'), 'haar')[:diff_image.shape[0], :diff_image.shape[1]]


def htrans(A):
    h0 = A
    res = []
    while h0.shape[0] > 1 and h0.shape[1] > 1:
        h0, (hx, hy, hc) = pywt.dwt2(h0, 'haar')
        res = [(h0, h0, h0)] + res

    out, _ = pywt.coeffs_to_array(([h0] + res), padding=1)
    return out