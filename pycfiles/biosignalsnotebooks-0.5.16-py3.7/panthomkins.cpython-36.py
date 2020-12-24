# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\panthomkins\panthomkins.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 2994 bytes
import numpy as np
from novainstrumentation.panthomkins.butterworth_filters import butter_bandpass_filter
from novainstrumentation.panthomkins.detect_panthomkins_peaks import detect_panthomkins_peaks
from novainstrumentation.panthomkins.rr_update import rr_1_update, rr_2_update, sync

def panthomkins(ecg_signal, fs, butterlow=8, butterhigh=30):
    ecg = ecg_signal - np.mean(ecg_signal)
    ecg = ecg / max(ecg)
    N = len(ecg)
    ecg_filter = butter_bandpass_filter(ecg, butterlow, butterhigh, fs)
    ecg_filter = 50.0 * ecg_filter ** 2.0
    pksInd = detect_panthomkins_peaks(ecg_filter, mpd=35)
    pks = ecg_filter[pksInd]
    SPKI = np.mean(pks) * 0.5
    NPKI = np.mean(pks) * 0.1
    threshold1 = NPKI + 0.25 * (SPKI - NPKI)
    threshold2 = 0.5 * threshold1
    rr_1 = np.ones(8) * 1.3 * fs
    rr_average_1 = np.mean(rr_1)
    rr_2 = np.ones(8) * 1.3 * fs
    rr_average_2 = np.mean(rr_2)
    rr_low_limit = 0.92 * rr_average_2
    rr_high_limit = 1.16 * rr_average_2
    NPeaks = len(pksInd)
    Found = np.ones((NPeaks, 3))
    Found[:, 1] = 1.3 * fs
    NFound = 0
    NFound_Old = NFound - 1
    flag = 0
    back = 0
    ii = 0
    while NPeaks - ii > 0:
        ii += 1
        if ii - back > 0:
            TH = threshold1
        else:
            TH = threshold2
        if pks[(ii - 1)] >= TH:
            NFound += 1
            Found[NFound - 1, :] = np.r_[(pksInd[(ii - 1)], pks[(ii - 1)], ii - 1)]
            if ii - back > 0:
                SPKI = 0.125 * pks[(ii - 1)] + 0.875 * SPKI
            else:
                SPKI = 0.25 * pks[(ii - 1)] + 0.75 * SPKI
        else:
            NPKI = 0.125 * pks[(ii - 1)] + 0.875 * NPKI
        threshold1 = NPKI + 0.25 * (SPKI - NPKI)
        threshold2 = 0.5 * threshold1
        if NFound_Old != NFound - 1:
            rr_1, rr_average_1 = rr_1_update(rr_1, NFound - 1, Found)
            rr_2, rr_average_2, flag, rr_low_limit, rr_high_limit = rr_2_update(rr_2, NFound - 1, Found, rr_low_limit, rr_high_limit)
            NFound_Old = NFound - 1
            if np.mod(NFound, 8) == 0:
                print(['Average of the 8 most recent HR is ',
                 str(rr_average_1 / fs * 60.0), ' (BPM)'])
                print('')
        if flag:
            print('Gap Found')
            flag = 0
            back = ii
            ii = Found[(-1, 2)]

    R = sync(Found, NFound, ecg, N)
    return R