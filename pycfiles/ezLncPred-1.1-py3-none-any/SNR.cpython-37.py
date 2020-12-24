# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/PredLnc_GFStack/src/get_features_module/SNR.py
# Compiled at: 2019-09-05 08:38:59
# Size of source mod 2**32: 553 bytes
import numpy as np

def SNR(seq):
    Alist = DFT_nlist(seq, 'A')
    Glist = DFT_nlist(seq, 'G')
    Clist = DFT_nlist(seq, 'C')
    Tlist = DFT_nlist(seq, 'T')
    Plist = [abs(Alist[i]) ** 2 + abs(Glist[i]) ** 2 + abs(Clist[i]) ** 2 + abs(Tlist[i]) ** 2 for i in range(len(seq))]
    R = Plist[round(len(seq) / 3)] / (sum(Plist) / len(seq))
    return R


def DFT_nlist(seq, basic):
    nlist = []
    for i in range(len(seq)):
        if seq[i] == basic:
            nlist.append(1)
        else:
            nlist.append(0)

    nlist = np.fft.fft(nlist)
    return nlist