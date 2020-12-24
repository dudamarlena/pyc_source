# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Display.py
# Compiled at: 2019-04-07 11:14:14


class Display:

    def __init__(self, _setEmotion, _setImage):
        self._setEmotion = _setEmotion
        self._setImage = _setImage

    def setEmotion(self, _emotion):
        self._setEmotion(_emotion)

    def setImage(self, _img):
        self._setImage(_img)