# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/exp_runner/wav_processor.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 585 bytes
import glob, soundfile as sf, numpy as np, librosa

def merge_dir(pattern, sr=16000, slience_second=4):
    file_list = glob.glob(pattern)
    slience = np.zeros(slience_second * sr)
    d = ()
    for f in file_list:
        data, sr = librosa.core.load(f, sr=sr)
        librosa.output.write_wav(f, data, sr, norm=True)
        data, sr = librosa.core.load(f, sr=sr)
        d += (data,)
        d += (slience,)

    data = np.concatenate(d)
    print('merge: ', data.shape)
    return data