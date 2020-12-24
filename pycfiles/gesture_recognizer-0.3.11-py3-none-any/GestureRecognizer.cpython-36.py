# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cap1/Documents/GitHub/gesture-recognizer/gesture_recognizer/GestureRecognizer.py
# Compiled at: 2018-11-18 05:23:46
# Size of source mod 2**32: 908 bytes
import cv2, numpy, os, threading, time, importlib.util

class GestureRecognizer(object):

    def __init__(self, interval=0.03333333333333333, print_pos=True):
        self.interval = interval
        self.print_pos = print_pos

    def start_recognizing(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename_fist_rec = 'FistRecognizer.py'
        full_path = '%s/%s' % (dir_path, filename_fist_rec)
        spec = importlib.util.spec_from_file_location('FistRecognizer', full_path)
        gesture_recognition = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gesture_recognition)
        self.gesture = gesture_recognition.FistRecognizer(self.interval, self.print_pos)
        thread = threading.Thread(target=(self.gesture.recognize_fist), args=())
        thread.daemon = True
        thread.start()