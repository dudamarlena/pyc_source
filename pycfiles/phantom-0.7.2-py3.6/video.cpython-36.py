# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\phantom\video.py
# Compiled at: 2019-10-24 15:53:30
# Size of source mod 2**32: 1611 bytes
"""
Miscelanous utilities that allow to easily work with video.

Mostly wraps OpenCVs classes and functions to give an easy interface. Mostly
aimed at making the examples easier to understand.s
"""
import cv2
from itertools import cycle

class Video:

    def __init__(self, path):
        """
        Iterable video class, it allows writing code of the form:

            >>> vid = phantom.video.Video(path_to_file)
            >>> for frame in vid:
            >>>     process(frame)
        
        :param path: path to the video.
        """
        self.path = path

    def __iterator(self):
        cap = cv2.VideoCapture(self.path)
        status, frame = cap.read()
        while status:
            yield frame
            status, frame = cap.read()

        cap.release()

    def __iter__(self):
        return self._Video__iterator()


def play_list(images, delay=10, esc_key='q', title='phantom playback'):
    """
    Plays a sequence of images as a video, using cv2.imshow().

    * NOT IMPLEMENTED*

    :param images: list of np.ndarray/cv2 images.
    :param delay: how many miliseconds to way for a keypress.
    :param esc_key: (one char string) which keypress will end the playback.
    :param title: title for the playback window
    """
    pass