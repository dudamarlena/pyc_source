# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/events.py
# Compiled at: 2016-08-21 12:54:46


class SettingsEvent(object):
    """ """

    def __init__(self, module=None):
        self.module = module


class SettingsBeforeSave(SettingsEvent):
    pass


class SettingsAfterSave(SettingsEvent):
    pass