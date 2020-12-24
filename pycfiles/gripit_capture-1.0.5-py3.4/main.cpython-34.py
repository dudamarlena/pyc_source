# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/main.py
# Compiled at: 2017-01-25 08:38:31
# Size of source mod 2**32: 298 bytes
from webcam.camera import Camera
__camera = Camera()

def access():
    __camera.access()


def start_recording():
    __camera.start_recording()


def create_file(name):
    __camera.create_file(name)


def stop_recording():
    __camera.stop_recording()


def release():
    __camera.release()