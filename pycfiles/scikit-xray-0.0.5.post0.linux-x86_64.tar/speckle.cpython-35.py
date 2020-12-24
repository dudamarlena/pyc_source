# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/speckle.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 11506 bytes
"""
X-ray speckle visibility spectroscopy(XSVS) - Dynamic information of
the speckle patterns are obtained by analyzing the speckle statistics
and calculating the speckle contrast in single scattering patterns.

This module will provide XSVS analysis tools
"""
from __future__ import absolute_import, division, print_function
import six, numpy as np, time
from . import roi
from .utils import bin_edges_to_centers, geometric_series
import logging
logger = logging.getLogger(__name__)

def xsvs(image_sets, label_array, number_of_img, timebin_num=2, max_cts=None):
    """
    This function will provide the probability density of detecting photons
    for different integration times.

    The experimental probability density P(K) of detecting photons K is
    obtained by histogramming the speckle counts over an ensemble of
    equivalent pixels and over a number of speckle patterns recorded
    with the same integration time T under the same condition.

    Parameters
    ----------
    image_sets : array
        sets of images
    label_array : array
        labeled array; 0 is background.
        Each ROI is represented by a distinct label (i.e., integer).
    number_of_img : int
        number of images (how far to go with integration times when finding
        the time_bin, using skxray.utils.geometric function)
    timebin_num : int, optional
        integration time; default is 2
    max_cts : int, optional
       the brightest pixel in any ROI in any image in the image set.
       defaults to using skxray.core.roi.roi_max_counts to determine
       the brightest pixel in any of the ROIs

    Returns
    -------
    prob_k_all : array
        probability density of detecting photons
    prob_k_std_dev : array
        standard deviation of probability density of detecting photons

    Notes
    -----
    These implementation is based on following references
    References: text [1]_, text [2]_

    .. [1] L. Li, P. Kwasniewski, D. Oris, L Wiegart, L. Cristofolini,
       C. Carona and A. Fluerasu , "Photon statistics and speckle visibility
       spectroscopy with partially coherent x-rays" J. Synchrotron Rad.,
       vol 21, p 1288-1295, 2014.

    .. [2] R. Bandyopadhyay, A. S. Gittings, S. S. Suh, P.K. Dixon and
       D.J. Durian "Speckle-visibilty Spectroscopy: A tool to study
       time-varying dynamics" Rev. Sci. Instrum. vol 76, p  093110, 2005.

    There is an example in https://github.com/scikit-xray/scikit-xray-examples
    It will demonstrate the use of these functions in this module for
    experimental data.

    """
    if max_cts is None:
        max_cts = roi.roi_max_counts(image_sets, label_array)
    labels, indices = roi.extract_label_indices(label_array)
    u_labels = list(np.unique(labels))
    num_roi = len(u_labels)
    time_bin = geometric_series(timebin_num, number_of_img)
    num_times = len(time_bin)
    num_pixels = np.bincount(labels, minlength=num_roi + 1)[1:]
    prob_k_all = np.zeros([num_times, num_roi], dtype=np.object)
    prob_k_pow_all = np.zeros_like(prob_k_all)
    prob_k_std_dev = np.zeros_like(prob_k_all)
    bin_edges = np.zeros(prob_k_all.shape[0], dtype=prob_k_all.dtype)
    for i in range(num_times):
        bin_edges[i] = np.arange(max_cts * 2 ** i)

    start_time = time.time()
    for i, images in enumerate(image_sets):
        buf = np.zeros([num_times, timebin_num], dtype=np.object)
        track_level = np.zeros(num_times)
        cur = np.full(num_times, timebin_num)
        img_per_level = np.zeros(num_times, dtype=np.int64)
        prob_k = np.zeros_like(prob_k_all)
        prob_k_pow = np.zeros_like(prob_k_all)
        for n, img in enumerate(images):
            cur[0] = (1 + cur[0]) % timebin_num
            buf[(0, cur[0] - 1)] = np.ravel(img)[indices]
            _process(num_roi, 0, cur[0] - 1, buf, img_per_level, labels, max_cts, bin_edges[0], prob_k, prob_k_pow)
            level = 1
            while level < num_times:
                if not track_level[level]:
                    track_level[level] = 1
                else:
                    prev = 1 + (cur[(level - 1)] - 2) % timebin_num
                    cur[level] = 1 + cur[level] % timebin_num
                    buf[(level, cur[level] - 1)] = buf[(level - 1,
                     prev - 1)] + buf[(level - 1,
                     cur[(level - 1)] - 1)]
                    track_level[level] = 0
                    _process(num_roi, level, cur[level] - 1, buf, img_per_level, labels, max_cts, bin_edges[level], prob_k, prob_k_pow)
                    level += 1

            prob_k_all += (prob_k - prob_k_all) / (i + 1)
            prob_k_pow_all += (prob_k_pow - prob_k_pow_all) / (i + 1)

    prob_k_std_dev = np.power(prob_k_pow_all - np.power(prob_k_all, 2), 0.5)
    logger.info('Processing time for XSVS took %s seconds.', time.time() - start_time)
    return (prob_k_all, prob_k_std_dev)


def _process(num_roi, level, buf_no, buf, img_per_level, labels, max_cts, bin_edges, prob_k, prob_k_pow):
    """
    Internal helper function. This modifies inputs in place.

    This helper function calculate probability of detecting photons for
    each integration time.

    .. warning :: This function mutates the input values.

    Parameters
    ----------
    num_roi : int
        number of ROI's
    level : int
        current time level(integration time)
    buf_no : int
        current buffer number
    buf : array
        image data array to use for XSVS
    img_per_level : int
        to track how many images processed in each level
    labels : array
        labels of the required region of interests(ROI's)
    max_cts: int
        maximum pixel count
    bin_edges : array
        bin edges for each integration times and each ROI
    prob_k : array
        probability density of detecting photons
    prob_k_pow : array
        squares of probability density of detecting photons
    """
    img_per_level[level] += 1
    u_labels = list(np.unique(labels))
    for j, label in enumerate(u_labels):
        roi_data = buf[(level, buf_no)][(labels == label)]
        spe_hist, bin_edges = np.histogram(roi_data, bins=bin_edges, density=True)
        spe_hist = np.nan_to_num(spe_hist)
        prob_k[(level, j)] += (spe_hist - prob_k[(level, j)]) / img_per_level[level]
        prob_k_pow[(level, j)] += (np.power(spe_hist, 2) - prob_k_pow[(level, j)]) / img_per_level[level]


def normalize_bin_edges(num_times, num_rois, mean_roi, max_cts):
    """
    This will provide the normalized bin edges and bin centers for each
    integration time.

    Parameters
    ----------
    num_times : int
        number of integration times for XSVS
    num_rois : int
        number of ROI's
    mean_roi : array
        mean intensity of each ROI
        shape (number of ROI's)
    max_cts : int
        maximum pixel counts

    Returns
    -------
    norm_bin_edges : array
        normalized speckle count bin edges
         shape (num_times, num_rois)
    norm_bin_centers :array
        normalized speckle count bin centers
        shape (num_times, num_rois)
    """
    norm_bin_edges = np.zeros((num_times, num_rois), dtype=object)
    norm_bin_centers = np.zeros_like(norm_bin_edges)
    for i in range(num_times):
        for j in range(num_rois):
            norm_bin_edges[(i, j)] = np.arange(max_cts * 2 ** i) / (mean_roi[j] * 2 ** i)
            norm_bin_centers[(i, j)] = bin_edges_to_centers(norm_bin_edges[(i, j)])

    return (
     norm_bin_edges, norm_bin_centers)