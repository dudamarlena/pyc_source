# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/utils/RGB2video.py
# Compiled at: 2017-06-02 17:59:41
from __future__ import division, print_function, absolute_import
from builtins import range
import numpy as np

def RGB2video(data, nameFile='video', verbosity=1, indent=0, framerate=24, codec='mpeg4', threads=4):
    """

    :param data: np.array N x H x W x 3
    :param nameFile:
    :param verbosity:
    :param indent:
    :return:
    """
    from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter as fwv
    extension = '.mp4'
    fullNameVideo = nameFile + extension
    n_frame = data.shape[0]
    resolution = (data.shape[2], data.shape[1])
    print('Resolution: %d x %d fps: %d n_frames: %d' % (resolution[0], resolution[1], framerate, n_frame))
    print('Saving to file: ' + fullNameVideo)
    a = fwv(filename=fullNameVideo, codec=codec, size=resolution, fps=framerate, preset='slower', threads=threads)
    for i in range(n_frame):
        frame = data[i, :].astype('uint8')
        assert np.all(0 <= frame) and np.all(frame <= 255), 'Value of the pixels is not in [0-255]'
        a.write_frame(frame)

    a.close()
    return 0