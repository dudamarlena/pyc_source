# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cap1/Documents/GitHub/gesture-recognizer/gesture_recognizer/GestureRecognizer.py
# Compiled at: 2018-11-17 19:55:34
import cv2, numpy, os, threading, time, importlib.util

class GestureRecognizer(object):

    def __init__(self):
        pass

    def start_recognizing(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename_fist_rec = 'FistRecognizer.py'
        full_path = '%s/%s' % (dir_path, filename_fist_rec)
        spec = importlib.util.spec_from_file_location('FistRecognizer', full_path)
        gesture_recognition = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gesture_recognition)
        FistRecognizerService = gesture_recognition.FistRecognizer()
        thread = threading.Thread(target=FistRecognizerService.recognize_fist, args=())
        thread.daemon = True
        thread.start()