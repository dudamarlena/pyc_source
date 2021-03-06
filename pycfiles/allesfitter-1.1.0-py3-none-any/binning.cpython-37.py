# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/exoworlds/lightcurves/binning.py
# Compiled at: 2018-11-09 10:56:49
# Size of source mod 2**32: 10723 bytes
"""
Created on Sun Mar 13 21:18:27 2016

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research,
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109,
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
    """
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt

def binning1D(arr, bin_width, setting='mean', normalize=False):
    """ WARNING: this does not respect boundaries between different night; 
    will average data from different nights"""
    N_time = len(arr)
    N_bins = np.int64(np.ceil(1.0 * N_time / bin_width))
    binarr, binarr_err = np.zeros((2, N_bins))
    bin_width = int(bin_width)
    if setting == 'mean':
        for nn in range(N_bins):
            binarr[nn] = np.nanmean(arr[nn * bin_width:(nn + 1) * bin_width])
            binarr_err[nn] = np.nanstd(arr[nn * bin_width:(nn + 1) * bin_width])

    if setting == 'median':
        for nn in range(N_bins):
            binarr[nn] = np.nanmedian(arr[nn * bin_width:(nn + 1) * bin_width])
            binarr_err[nn] = 1.48 * np.nanmedian(abs(arr[nn * bin_width:(nn + 1) * bin_width] - binarr[nn]))

    if normalize == True:
        med = np.nanmedian(binarr)
        binarr /= med
        binarr_err /= med
    return (binarr, binarr_err)


def binning2D(arr, bin_width, setting='mean', normalize=False, axis=1):
    """ WARNING: this does not respect boundaries between different night; 
    will average data from different nights"""
    N_time = arr.shape[1]
    N_objs = arr.shape[0]
    N_bins = np.int64(np.ceil(1.0 * N_time / bin_width))
    binarr, binarr_err = np.zeros((2, N_objs, N_bins))
    bin_width = int(bin_width)
    if setting == 'mean':
        for nn in range(N_bins):
            binarr[:, nn] = np.nanmean((arr[:, nn * bin_width:(nn + 1) * bin_width]), axis=axis)
            binarr_err[:, nn] = np.nanstd((arr[:, nn * bin_width:(nn + 1) * bin_width]), axis=axis)

    if setting == 'median':
        for nn in range(N_bins):
            binarr[:, nn] = np.nanmedian((arr[:, nn * bin_width:(nn + 1) * bin_width]), axis=axis)
            binarr_err[:, nn] = 1.48 * np.nanmedian(abs(arr[:, nn * bin_width:(nn + 1) * bin_width] - binarr[:, nn]))

    if normalize == True:
        med = np.nanmedian(binarr)
        binarr /= med
        binarr_err /= med
    return (
     binarr, binarr_err)


def bin_edge_indices(time1D, bin_width, timegap, N_time):
    """ DETERMINE ALL THE BIN-EDGE-INDICES (TO NOT BIN OVER DIFFERENT NIGHTS)"""
    ind_end_of_night = np.append(np.where(np.diff(time1D) > timegap)[0], len(np.diff(time1D) - 1))
    N_nights = len(ind_end_of_night)
    first_ind = [
     0]
    last_ind = []
    i = 0
    while (first_ind[(-1)] < N_time) & (i < N_nights):
        if first_ind[(-1)] + bin_width < ind_end_of_night[i]:
            last_ind.append(first_ind[(-1)] + bin_width)
        else:
            last_ind.append(ind_end_of_night[i])
            i += 1
        first_ind.append(last_ind[(-1)] + 1)

    del first_ind[-1]
    return (
     first_ind, last_ind)


def binning1D_per_night(time, arr, bin_width, timegap=3600, setting='mean', normalize=False):
    """ If time and arr are 1D arrays """
    N_time = len(arr)
    bin_width = int(bin_width)
    first_ind, last_ind = bin_edge_indices(time, bin_width, timegap, N_time)
    N_bins = len(first_ind)
    bintime, binarr, binarr_err = np.zeros((3, N_bins)) * np.nan
    if setting == 'mean':
        for nn in range(N_bins):
            if last_ind[nn] > first_ind[nn]:
                bintime[nn] = np.nanmean(time[first_ind[nn]:last_ind[nn]])
                if np.isnan(arr[first_ind[nn]:last_ind[nn]]).all() == False:
                    binarr[nn] = np.nanmean(arr[first_ind[nn]:last_ind[nn]])
                    binarr_err[nn] = np.nanstd(arr[first_ind[nn]:last_ind[nn]])

    else:
        if setting == 'median':
            for nn in range(N_bins):
                if last_ind[nn] > first_ind[nn]:
                    bintime[nn] = np.nanmedian(time[first_ind[nn]:last_ind[nn]])
                    if np.isnan(arr[first_ind[nn]:last_ind[nn]]).all() == False:
                        binarr[nn] = np.nanmedian(arr[first_ind[nn]:last_ind[nn]])
                        binarr_err[nn] = 1.48 * np.nanmedian(abs(arr[first_ind[nn]:last_ind[nn]] - binarr[nn]))

        if normalize == True:
            med = np.nanmedian(binarr)
            binarr /= med
            binarr_err /= med
        return (bintime, binarr, binarr_err)


def binning2D_per_night(time, arr, bin_width, timegap=3600, setting='mean', normalize=False, axis=1):
    """ If time and arr are each a 2D array, with different objs on x and different time stamps on y"""
    N_time = arr.shape[1]
    N_objs = arr.shape[0]
    bin_width = int(bin_width)
    first_ind, last_ind = bin_edge_indices(time[0, :], bin_width, timegap, N_time)
    N_bins = len(first_ind)
    bintime, binarr, binarr_err = np.zeros((3, N_objs, N_bins))
    if setting == 'mean':
        for nn in range(N_bins):
            bintime[:, nn] = np.nanmean((time[:, first_ind[nn]:last_ind[nn]]), axis=axis)
            binarr[:, nn] = np.nanmean((arr[:, first_ind[nn]:last_ind[nn]]), axis=axis)
            binarr_err[:, nn] = np.nanstd((arr[:, first_ind[nn]:last_ind[nn]]), axis=axis)

    else:
        if setting == 'median':
            for nn in range(N_bins):
                bintime[:, nn] = np.nanmedian((time[:, first_ind[nn]:last_ind[nn]]), axis=axis)
                binarr[:, nn] = np.nanmedian((arr[:, first_ind[nn]:last_ind[nn]]), axis=axis)
                binarr_err[:, nn] = 1.48 * np.nanmedian(abs(arr[:, first_ind[nn]:last_ind[nn]] - binarr[:, nn]))

        if normalize == True:
            med = np.nanmedian(binarr)
            binarr /= med
            binarr_err /= med
        return (bintime, binarr, binarr_err)


def binning1D_per_night_list(time, arr, bin_width, timegap=3600, setting='mean', normalize=False):
    """ different style of program, same application """
    N = len(time)
    bin_width = int(bin_width)
    bintime = []
    binarr = []
    binarr_err = []
    ind_end_of_night = np.append(np.where(np.diff(time) > timegap)[0], len(np.diff(time) - 1))
    N_nights = len(ind_end_of_night)
    first_ind = 0
    i = 0
    if setting == 'mean':
        while (first_ind < N) & (i < N_nights):
            if first_ind + bin_width < ind_end_of_night[i]:
                last_ind = first_ind + bin_width
            else:
                last_ind = ind_end_of_night[i]
                i += 1
            bintime.append(np.nanmean(time[first_ind:last_ind]))
            binarr.append(np.nanmean(arr[first_ind:last_ind]))
            binarr_err.append(np.nanstd(arr[first_ind:last_ind]))
            first_ind = last_ind + 1

    else:
        if setting == 'median':
            while first_ind < N:
                if first_ind + bin_width < ind_end_of_night[i]:
                    last_ind = first_ind + bin_width
                else:
                    last_ind = ind_end_of_night[i]
                    i += 1
                bintime.append(np.nanmedian(time[first_ind:last_ind]))
                binarr.append(np.nanmedian(arr[first_ind:last_ind]))
                binarr_err.append(1.48 * np.nanmedian(abs(arr[first_ind:last_ind] - binarr[(-1)])))
                first_ind = last_ind

        bintime = np.array(bintime)
        binarr = np.array(binarr)
        binarr_err = np.array(binarr_err)
        if normalize == True:
            med = np.nanmedian(binarr)
            binarr /= med
            binarr_err /= med
        return (bintime, binarr, binarr_err)


if __name__ == '__main__':
    arr = np.array([[1, 2, 3, 4, 5, 6, 67, 68, 64, -10, -11, -13],
     [
      1, 2, 3, 4, 5, 6, 24, 28, 32, 10, 11, 13]])
    time = np.array([[1, 2, 3, 4, 5, 6, 10001, 10002, 10003, 20001, 20002, 20003],
     [
      1, 2, 3, 4, 5, 6.1, 10001, 10002.1, 10003.3, 20001, 20002, 20003]])
    bintime, binarr, _ = binning2D_per_night(time, arr, 6)
    plt.figure()
    plt.plot(time, arr, 'k.')
    plt.plot(bintime, binarr, 'r.')
    arr = np.array([1, 2, 3, 4, 5, 6, 67, 68, 64, -10, -11, -13])
    time = np.array([1, 2, 3, 4, 5, 6, 10001, 10002, 10003, 20001, 20002, 20003])
    bintime, binarr, _ = binning1D_per_night(time, arr, 6)
    plt.figure()
    plt.plot(time, arr, 'k.')
    plt.plot(bintime, binarr, 'r.')