# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\Documents\GitHub\fourMs\MGT-python\musicalgestures\__init__.py
# Compiled at: 2020-04-27 09:15:08
# Size of source mod 2**32: 5058 bytes
import os
from musicalgestures._input_test import mg_input_test
from musicalgestures._videoreader import mg_videoreader
from musicalgestures._flow import Flow

class MgObject:
    __doc__ = " \n    Initializes Musical Gestures data structure from a video file.\n\n    Attributes\n    ----------\n    - filename : str\n\n        Path to the video file.\n    - filtertype : {'Regular', 'Binary', 'Blob'}, optional\n\n        The `filtertype` parameter for the `motion()` method.\n        `Regular` turns all values below `thresh` to 0.\n        `Binary` turns all values below `thresh` to 0, above `thresh` to 1.\n        `Blob` removes individual pixels with erosion method.\n\n    - thresh : float, optional\n\n        The `thresh` parameter for the `motion()` method.\n        A number in the range of 0 to 1. Default is 0.05.\n        Eliminates pixel values less than given threshold.\n    - starttime : int or float, optional\n\n        Trims the video from this start time (s).\n    - endtime : int or float, optional\n\n        Trims the video until this end time (s).\n    - blur : {'None', 'Average'}, optional\n\n        The `blur` parameter for the `motion()` method.\n        `Average` to apply a 10px * 10px blurring filter, `None` otherwise.\n    - skip : int, optional\n\n        Time-shrinks the video by skipping (discarding) every n frames determined by `skip`.\n    - rotate : int or float, optional\n\n        Rotates the video by a `rotate` degrees.\n    - color : bool, optional\n\n        Default is `True`. If `False`, converts the video to grayscale and sets every method in grayscale mode.\n    - contrast : int or float, optional\n\n        Applies +/- 100 contrast to video.\n    - brightness : int or float, optional\n\n        Applies +/- 100 brightness to video.\n    - crop : {'none', 'manual', 'auto'}, optional\n\n        If `manual`, opens a window displaying the first frame of the input video file,\n        where the user can draw a rectangle to which cropping is applied.\n        If `auto` the cropping function attempts to determine the area of significant motion \n        and applies the cropping to that area.\n\n    - keep_all : bool, optional\n\n        Default is `False`. If `True`, preserves an output video file after each used preprocessing stage.\n    "

    def __init__(self, filename, filtertype='Regular', thresh=0.05, starttime=0, endtime=0, blur='None', skip=0, rotate=0, color=True, contrast=0, brightness=0, crop='None', keep_all=False, returned_by_process=False):
        self.filename = filename
        self.of = os.path.splitext(self.filename)[0]
        self.fex = os.path.splitext(self.filename)[1]
        self.color = color
        self.starttime = starttime
        self.endtime = endtime
        self.skip = skip
        self.filtertype = filtertype
        self.thresh = thresh
        self.blur = blur
        self.contrast = contrast
        self.brightness = brightness
        self.crop = crop
        self.rotate = rotate
        self.keep_all = keep_all
        self.returned_by_process = returned_by_process
        self.test_input()
        self.get_video()
        self.flow = Flow(self.filename, self.color)

    import musicalgestures._motionvideo as motion
    from musicalgestures._motionvideo import plot_motion_metrics
    from musicalgestures._cropvideo import mg_cropvideo, find_motion_box, find_total_motion_box
    import musicalgestures._show as show
    from musicalgestures._history import history
    import musicalgestures._average as average

    def test_input(self):
        """ Gives feedback to user if initialization from input went wrong. """
        mg_input_test(self.filename, self.filtertype, self.thresh, self.starttime, self.endtime, self.blur, self.skip)

    def get_video(self):
        """ Creates a video attribute to the Musical Gestures object with the given correct settings. """
        self.length, self.width, self.height, self.fps, self.endtime, self.of, self.fex = mg_videoreader(filename=(self.filename),
          starttime=(self.starttime),
          endtime=(self.endtime),
          skip=(self.skip),
          rotate=(self.rotate),
          contrast=(self.contrast),
          brightness=(self.brightness),
          crop=(self.crop),
          color=(self.color),
          returned_by_process=(self.returned_by_process),
          keep_all=(self.keep_all))
        self.filename = self.of + self.fex

    def __repr__(self):
        return f"MgObject('{self.filename}')"