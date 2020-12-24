# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/correlation.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 14772 bytes
"""

This module is for functions specific to time correlation

"""
from __future__ import absolute_import, division, print_function
import logging, time, numpy as np
from . import utils as core
from . import roi
from lmfit import minimize, Model, Parameters
logger = logging.getLogger(__name__)

def multi_tau_auto_corr(num_levels, num_bufs, labels, images):
    """
    This function computes one-time correlations.

    It uses a scheme to achieve long-time correlations inexpensively
    by downsampling the data, iteratively combining successive frames.

    The longest lag time computed is num_levels * num_bufs.

    Parameters
    ----------
    num_levels : int
        how many generations of downsampling to perform, i.e.,
        the depth of the binomial tree of averaged frames

    num_bufs : int, must be even
        maximum lag step to compute in each generation of
        downsampling

    labels : array
        labeled array of the same shape as the image stack;
        each ROI is represented by a distinct label (i.e., integer)

    images : iterable of 2D arrays
        dimensions are: (rr, cc)

    Returns
    -------
    g2 : array
        matrix of normalized intensity-intensity autocorrelation
        shape (num_levels, number of labels(ROI))

    lag_steps : array
        delay or lag steps for the multiple tau analysis
        shape num_levels

    Notes
    -----

    The normalized intensity-intensity time-autocorrelation function
    is defined as

    :math ::
        g_2(q, t') = \x0crac{<I(q, t)I(q, t + t')> }{<I(q, t)>^2}

    ; t' > 0

    Here, I(q, t) refers to the scattering strength at the momentum
    transfer vector q in reciprocal space at time t, and the brackets
    <...> refer to averages over time t. The quantity t' denotes the
    delay time

    This implementation is based on code in the language Yorick
    by Mark Sutton, based on published work. [1]_

    References
    ----------

    .. [1] D. Lumma, L. B. Lurio, S. G. J. Mochrie and M. Sutton,
        "Area detector based photon correlation in the regime of
        short data batches: Data reduction for dynamic x-ray
        scattering," Rev. Sci. Instrum., vol 70, p 3274-3289, 2000.

    """
    if num_bufs % 2 != 0:
        raise ValueError('number of channels(number of buffers) in multiple-taus (must be even)')
    if hasattr(images, 'frame_shape') and labels.shape != images.frame_shape:
        raise ValueError('Shape of the image stack should be equal to shape of the labels array')
    label_mask, pixel_list = roi.extract_label_indices(labels)
    num_rois = np.max(label_mask)
    num_pixels = np.bincount(label_mask, minlength=num_rois + 1)
    num_pixels = num_pixels[1:]
    if np.any(num_pixels == 0):
        raise ValueError("Number of pixels of the required roi's cannot be zero, num_pixels = {0}".format(num_pixels))
    G = np.zeros(((num_levels + 1) * num_bufs / 2, num_rois), dtype=np.float64)
    past_intensity_norm = np.zeros(((num_levels + 1) * num_bufs / 2, num_rois), dtype=np.float64)
    future_intensity_norm = np.zeros(((num_levels + 1) * num_bufs / 2, num_rois), dtype=np.float64)
    buf = np.zeros((num_levels, num_bufs, np.sum(num_pixels)), dtype=np.float64)
    track_level = np.zeros(num_levels)
    cur = np.ones(num_levels, dtype=np.int64)
    img_per_level = np.zeros(num_levels, dtype=np.int64)
    start_time = time.time()
    for n, img in enumerate(images):
        cur[0] = (1 + cur[0]) % num_bufs
        buf[(0, cur[0] - 1)] = np.ravel(img)[pixel_list]
        _process(buf, G, past_intensity_norm, future_intensity_norm, label_mask, num_bufs, num_pixels, img_per_level, level=0, buf_no=cur[0] - 1)
        processing = num_levels > 1
        level = 1
        while processing:
            if not track_level[level]:
                track_level[level] = 1
                processing = False
            else:
                prev = 1 + (cur[(level - 1)] - 2) % num_bufs
                cur[level] = 1 + cur[level] % num_bufs
                buf[(level, cur[level] - 1)] = (buf[(level - 1, prev - 1)] + buf[(level - 1,
                 cur[(level - 1)] - 1)]) / 2
                track_level[level] = 0
                _process(buf, G, past_intensity_norm, future_intensity_norm, label_mask, num_bufs, num_pixels, img_per_level, level=level, buf_no=cur[level] - 1)
                level += 1
                processing = level < num_levels

    end_time = time.time()
    logger.info('Processing time for {0} images took {1} seconds.'.format(n, end_time - start_time))
    if len(np.where(past_intensity_norm == 0)[0]) != 0:
        g_max = np.where(past_intensity_norm == 0)[0][0]
    else:
        g_max = past_intensity_norm.shape[0]
    g2 = G[:g_max] / (past_intensity_norm[:g_max] * future_intensity_norm[:g_max])
    tot_channels, lag_steps = core.multi_tau_lags(num_levels, num_bufs)
    lag_steps = lag_steps[:g_max]
    return (
     g2, lag_steps)


def _process(buf, G, past_intensity_norm, future_intensity_norm, label_mask, num_bufs, num_pixels, img_per_level, level, buf_no):
    """
    Internal helper function. This modifies inputs in place.

    This helper function calculates G, past_intensity_norm and
    future_intensity_norm at each level, symmetric normalization is used.

    Parameters
    ----------
    buf : array
        image data array to use for correlation

    G : array
        matrix of auto-correlation function without
        normalizations

    past_intensity_norm : array
        matrix of past intensity normalizations

    future_intensity_norm : array
        matrix of future intensity normalizations

    label_mask : array
        labels of the required region of interests(roi's)

    num_bufs : int, even
        number of buffers(channels)

    num_pixels : array
        number of pixels in certain roi's
        roi's, dimensions are : [number of roi's]X1

    img_per_level : array
        to track how many images processed in each level

    level : int
        the current multi-tau level

    buf_no : int
        the current buffer number

    Notes
    -----
    :math ::
        G   = <I(       au)I(   au + delay)>

    :math ::
        past_intensity_norm = <I(       au)>

    :math ::
        future_intensity_norm = <I(     au + delay)>

    """
    img_per_level[level] += 1
    if level == 0:
        i_min = 0
    else:
        i_min = num_bufs // 2
    for i in range(i_min, min(img_per_level[level], num_bufs)):
        t_index = level * num_bufs / 2 + i
        delay_no = (buf_no - i) % num_bufs
        past_img = buf[(level, delay_no)]
        future_img = buf[(level, buf_no)]
        tmp_binned = np.bincount(label_mask, weights=past_img * future_img)[1:]
        G[t_index] += (tmp_binned / num_pixels - G[t_index]) / (img_per_level[level] - i)
        pi_binned = np.bincount(label_mask, weights=past_img)[1:]
        past_intensity_norm[t_index] += (pi_binned / num_pixels - past_intensity_norm[t_index]) / (img_per_level[level] - i)
        fi_binned = np.bincount(label_mask, weights=future_img)[1:]
        future_intensity_norm[t_index] += (fi_binned / num_pixels - future_intensity_norm[t_index]) / (img_per_level[level] - i)


def auto_corr_scat_factor(lags, beta, relaxation_rate, baseline=1):
    """
    This model will provide normalized intensity-intensity time
    correlation data to be minimized.

    Parameters
    ----------
    lags : array
        delay time

    beta : float
        optical contrast (speckle contrast), a sample-independent
        beamline parameter

    relaxation_rate : float
        relaxation time associated with the samples dynamics.

    baseline : float, optional
        baseline of one time correlation
        equal to one for ergodic samples

    Returns
    -------
    g2 : array
        normalized intensity-intensity time autocorreltion

    Notes :
    -------
    The intensity-intensity autocorrelation g2 is connected to the intermediate
    scattering factor(ISF) g1

    :math ::
        g_2(q,  au) = \x08eta_1[g_1(q,     au)]^{2} + g_\\infty

    For a system undergoing  diffusive dynamics,

    :math ::
        g_1(q,  au) = e^{-\\gamma(q)     au}

    :math ::
       g_2(q,   au) = \x08eta_1 e^{-2\\gamma(q)     au} + g_\\infty

    These implementation are based on published work. [1]_

    References
    ----------
    .. [1] L. Li, P. Kwasniewski, D. Orsi, L. Wiegart, L. Cristofolini,
       C. Caronna and A. Fluerasu, " Photon statistics and speckle
       visibility spectroscopy with partially coherent X-rays,"
       J. Synchrotron Rad. vol 21, p 1288-1295, 2014

    """
    return beta * np.exp(-2 * relaxation_rate * lags) + baseline