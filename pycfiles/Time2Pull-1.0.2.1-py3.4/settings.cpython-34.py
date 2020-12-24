# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/time2pull/settings.py
# Compiled at: 2014-06-16 15:45:18
# Size of source mod 2**32: 2169 bytes
"""
Contains the application settings
"""
from PyQt5 import QtCore
import sys
from time2pull.constants import TrayIconType

class Settings:

    def __init__(self):
        self._settings = QtCore.QSettings('Time2Pull')

    @property
    def repositories(self):
        ret_val = self._settings.value('repositories', '')
        if not ret_val:
            ret_val = []
        elif isinstance(ret_val, str):
            ret_val = [
             ret_val]
        return sorted(ret_val)

    @repositories.setter
    def repositories(self, value):
        self._settings.setValue('repositories', value)

    @property
    def tray_icon_type(self):
        default = TrayIconType.dark if sys.platform == 'darwin' else TrayIconType.light
        val = int(self._settings.value('tray_icon_type', int(default)))
        return TrayIconType(val)

    @tray_icon_type.setter
    def tray_icon_type(self, value):
        self._settings.setValue('tray_icon_type', int(value))

    @property
    def hide_on_startup(self):
        return bool(int(self._settings.value('hide_on_startup', 0)))

    @hide_on_startup.setter
    def hide_on_startup(self, value):
        self._settings.setValue('hide_on_startup', int(value))

    @property
    def show_msg(self):
        return bool(int(self._settings.value('show_msg', '1')))

    @show_msg.setter
    def show_msg(self, value):
        self._settings.setValue('show_msg', int(value))

    @property
    def play_sound(self):
        return bool(int(self._settings.value('play_sound', '1')))

    @play_sound.setter
    def play_sound(self, value):
        self._settings.setValue('play_sound', int(value))

    @property
    def geometry(self):
        v = self._settings.value('geometry')
        if v:
            return bytes(v)

    @geometry.setter
    def geometry(self, geometry):
        self._settings.setValue('geometry', geometry)

    @property
    def state(self):
        v = self._settings.value('state')
        if v:
            return bytes(v)

    @state.setter
    def state(self, state):
        self._settings.setValue('state', state)