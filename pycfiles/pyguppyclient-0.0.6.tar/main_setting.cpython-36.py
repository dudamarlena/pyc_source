# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\Tools\main_setting.py
# Compiled at: 2019-04-15 07:52:22
# Size of source mod 2**32: 2321 bytes
import os
from collections import OrderedDict
from PyQt5.QtCore import QStandardPaths, QObject, QSettings
from PyQt5.QtWidgets import qApp
from Tools.BasePara import setting_path

class SettingInfo(QObject):
    settings = QSettings(setting_path, QSettings.IniFormat)

    def __init__(self, parent=None):
        super().__init__(parent)

    def restoreSettings(self):
        global target_path
        s = self.settings
        try:
            appName = qApp.applicationFilePath().split('/')[(-1)] + '.lnk'
            startapp = QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0]
            target_path = os.path.join(startapp, appName)
        except:
            import traceback
            print(traceback.format_exc())

        try:
            self.restoreState(s.value('window_info/windowState'))
            self.restoreGeometry(s.value('window_info/geometry'))
        except:
            pass

    def closeEvent(self, e):
        """

        :param e:
        :param args:
        :param kwargs:
        :return:
        """
        print('close')
        self.settings.setValue('window_info/windowState', self.saveState())
        self.settings.setValue('window_info/geometry', self.saveGeometry())
        DEBUG_SEC = self.settings.value('DEBUG/DEBUG_SEC', 6000)
        self.settings.setValue('DEBUG/DEBUG_SEC', DEBUG_SEC)