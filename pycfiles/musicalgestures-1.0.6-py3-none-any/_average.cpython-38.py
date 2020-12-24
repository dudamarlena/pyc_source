# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\Documents\GitHub\fourMs\MGT-python\musicalgestures\_average.py
# Compiled at: 2020-04-26 14:42:10
# Size of source mod 2**32: 2271 bytes
import cv2, numpy as np, os
from musicalgestures._utils import MgImage, MgProgressbar

def mg_average_image(self, filename='', normalize=True):
    """
    Finds and saves an average image of an input video file.

    Parameters
    ----------
    - filename : str, optional

        Path to the input video file. If not specified the video file pointed to by the MgObject is used.
    - normalize : bool, optional

        Default is `True`. If `True`, normalizes pixel values in the output image.

    Outputs
    -------
    - `filename`_average.png

    Returns
    -------
    - MgImage

        A new MgImage pointing to the output '_average' image file.
    """
    if filename == '':
        filename = self.filename
    else:
        of = os.path.splitext(filename)[0]
        video = cv2.VideoCapture(filename)
        ret, frame = video.read()
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.color == False:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average = frame.astype(np.float) / length
        pb = MgProgressbar(total=length, prefix='Rendering average image:')
        ii = 0
        while video.isOpened():
            ret, frame = video.read()
            if ret == True:
                if self.color == False:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = np.array(frame)
                frame = frame.astype(np.float)
                average += frame / length
            else:
                pb.progress(length)
                break
            pb.progress(ii)
            ii += 1

        if self.color == False:
            average = cv2.cvtColor(average.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        if normalize:
            average = average.astype(np.uint8)
            norm_average = np.zeros_like(average)
            norm_average = cv2.normalize(average, norm_average, 0, 255, cv2.NORM_MINMAX)
            cv2.imwrite(of + '_average.png', norm_average.astype(np.uint8))
        else:
            cv2.imwrite(of + '_average.png', average.astype(np.uint8))
    return MgImage(of + '_average.png')