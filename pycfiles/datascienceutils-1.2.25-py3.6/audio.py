# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/features/audio.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 1337 bytes
import numpy as np, os, pandas as pd, python_speech_features as psf

def mfcc_features(input_sound):
    import scipy.io.wavfile as wav
    rate, signal = wav.read(input_sound)
    mfcc_feat = psf.mfcc(signal, rate)
    return pd.DataFrame(mfcc_feat, columns=(range(mfcc_feat.shape[1])))


def filter_bank_energies(input_sound):
    import scipy.io.wavfile as wav
    rate, signal = wav.read(input_sound)
    fbank_feat = psf.fbank(signal, rate)
    res = pd.DataFrame((fbank_feat[0]), columns=(range(fbank_feat[0].shape[1])))
    res['coefficients'] = fbank_feat[1]
    return res


def spectral_subband_centroids(input_sound):
    import scipy.io.wavfile as wav
    rate, signal = wav.read(input_sound)
    ssc_feat = psf.ssc(signal, rate)
    return pd.DataFrame(ssc_feat, columns=(range(ssc_feat.shape[1])))


def lpc_features(input_sound):
    import audiolazy as al
    signal = al.WavStream(input_sound)
    blk = signal.take(np.inf)
    lpc_feat = al.lazy_lpc.lpc(blk)


def all_features(file_name):
    res = dict()
    input_sound = os.path.join(settings.INP_AUDIO_PATH, file_name + '.wav')
    res['mfcc'] = mfcc_features(input_sound)
    res['ssc'] = spectral_subband_centroids(input_sound)
    res['fbank'] = filter_bank_energies(input_sound)
    return res