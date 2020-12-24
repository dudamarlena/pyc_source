# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/config.py
# Compiled at: 2019-10-07 10:13:11
# Size of source mod 2**32: 469 bytes
"""Tensorpac configuration."""
MI_BIASCORRECT = False
MI_DEMEAN = False
JOBLIB_CFG = dict()
try:
    import mne
    MNE_EPOCHS_TYPE = [
     mne.Epochs, mne.EpochsArray, mne.epochs.BaseEpochs]
except:
    MNE_EPOCHS_TYPE = []

CONFIG = dict(MI_BIASCORRECT=MI_BIASCORRECT, MI_DEMEAN=MI_DEMEAN, JOBLIB_CFG=JOBLIB_CFG,
  MNE_EPOCHS_TYPE=MNE_EPOCHS_TYPE)