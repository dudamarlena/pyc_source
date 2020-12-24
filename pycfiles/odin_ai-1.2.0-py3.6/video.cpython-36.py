# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/preprocessing/video.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 770 bytes
from __future__ import print_function, division, absolute_import
import numpy as np

def read(path, boxes=None):
    """
  Return
  ------
  Always return 3D images
  (n_frames, channels, width, height)
  """
    import imageio
    vid = imageio.get_reader(path)
    metadata = vid.get_meta_data()
    fps = metadata['fps']
    nb_frames = metadata['nframes']
    if boxes is not None:
        pass
    print(nb_frames)
    exit()
    try:
        frames = []
        for i in vid:
            if i.ndim == 3:
                i = i.transpose(2, 1, 0)
            else:
                i = np.expand_dims(i.transpose(1, 0), 1)
            frames.append(i)

    except RuntimeError:
        pass

    frames = np.array(frames, dtype=(frames[0].dtype))
    return (frames, fps)