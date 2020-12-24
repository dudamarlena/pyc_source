# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_slice/audio.py
# Compiled at: 2019-06-11 23:51:07
# Size of source mod 2**32: 740 bytes
import numpy as np

def quiet_sections(audio_clip, chunk_width, threshold=0.01):
    assert type(chunk_width) is int
    silent_sections = []
    current_loud = False
    for i, chunk in enumerate(audio_clip.iter_chunks(chunksize=chunk_width)):
        a = np.max(chunk)
        if not current_loud:
            if a >= threshold:
                start_loud = i * chunk_width / audio_clip.fps
                current_loud = True
            elif a < threshold:
                silent_sections.append((
                 start_loud, i * chunk_width / audio_clip.fps))
                current_loud = False

    return silent_sections