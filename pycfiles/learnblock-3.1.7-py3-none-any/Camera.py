# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Camera.py
# Compiled at: 2019-04-07 11:14:14
import copy, numpy as np
from threading import Lock

class Camera:
    """
    Camera devices.
    """
    __image = np.zeros((240, 320, 3), np.uint8)
    __newImageAvailable = False
    __mutexRead = Lock()

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def read(self):
        self.__mutexRead.acquire()
        img, new = self._readDevice()
        if new is True:
            self.__image = img
            self.__newImageAvailable = True
        self.__mutexRead.release()

    def getImage(self):
        self.__mutexRead.acquire()
        simage = copy.copy(self.__image)
        self.__mutexRead.release()
        return simage

    def disableNewImageAvailable(self):
        self.__newImageAvailable = False