# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Speaker.py
# Compiled at: 2019-04-07 11:14:14


class Speaker:
    _sendAudio = None
    _sendText = None

    def __init__(self, _sendAudio=None, _sendText=None):
        self._sendAudio = _sendAudio
        self._sendText = _sendText

    def sendAudio(self, _audiodata):
        if self._sendAudio is not None:
            self._sendAudio(_audiodata)
        return

    def sendText(self, _text):
        if self._sendText is not None:
            self._sendText(_text)
        return