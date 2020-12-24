# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/logmessage.py
# Compiled at: 2016-03-11 14:12:35
# Size of source mod 2**32: 1126 bytes


class LogMessage(object):
    __doc__ = '\n    Comunication object fopr passing logs through subsystems.\n\n    '

    def __init__(self, name, data, system_notifications, timestamp):
        self._name = name
        self._data = data
        self._timestamp = timestamp
        self._system_notifications = system_notifications

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def timestamp(self):
        return self._name

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property
    def system_notifications(self):
        return self._system_notifications

    @system_notifications.setter
    def system_notifications(self, system_notifications):
        self._timestamp = system_notifications

    def get_object(self):
        obj = {}
        for k, v in self.__dict__.items():
            obj[k[1:]] = v

        return obj