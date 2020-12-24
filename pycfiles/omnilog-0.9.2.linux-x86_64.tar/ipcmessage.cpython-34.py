# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/ipcmessage.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 937 bytes


class IPCMessage(object):
    __doc__ = '\n    Comunication object between subsystems and main process.\n\n    '

    def __init__(self, subsystem, action, message):
        self._subsystem = subsystem
        self._action = action
        self._message = message

    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, subsystem):
        self._subsystem = subsystem

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    @property
    def message(self):
        return self._subsystem

    @message.setter
    def message(self, message):
        self._message = message

    def __str__(self):
        lm = []
        str = '{key} - {value}'
        for k, v in self.__dict__.items():
            lm.append(str.format(key=k[1:], value=v))

        return ' | '.join(lm)