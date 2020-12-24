# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\UUI\Components\C_SplashScreen.py
# Compiled at: 2019-04-13 14:49:35
# Size of source mod 2**32: 2238 bytes
import time
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QDesktopWidget, QApplication
from Tools.BasePara import setting_path

class C_QSplashScreen(QSplashScreen):

    def __init__(self):
        super().__init__()
        s = QSettings(setting_path, QSettings.IniFormat)
        font = QFont()
        font.setPointSize(30)
        font.setFamily('黑体')
        self.setFont(font)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        label1 = QLabel('高压电网监控\n系统软件V1.0\n\n', self)
        label1.setAlignment(Qt.AlignCenter)
        gs_name = s.value('SYSTME/gs_name', '杭州三联智能科技有限公司')
        label2 = QLabel(gs_name)
        layout.addWidget(label1)
        if s.value('SYSTEM/show_gs', True) != 'false':
            layout.addWidget(label2)
        self.setLayout(layout)

    def effect(self):
        self.show()
        self.center()
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.02
            if newOpacity > 1:
                break
            self.setWindowOpacity(newOpacity)
            t -= 1
            QApplication.processEvents()
            time.sleep(0.02)

        time.sleep(0.5)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.02
            if newOpacity < 0:
                break
            self.setWindowOpacity(newOpacity)
            t -= 1
            QApplication.processEvents()
            time.sleep(0.01)

        self.setWindowOpacity(0)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)