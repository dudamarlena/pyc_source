# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/qrwindow.py
# Compiled at: 2019-08-25 05:37:49
# Size of source mod 2**32: 1707 bytes
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from .qrcodewidget import QRCodeWidget
from electrum.i18n import _

class QR_Window(QWidget):

    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        self.setWindowTitle('Electrum-CHI - ' + _('Payment Request'))
        self.setMinimumSize(800, 800)
        self.setFocusPolicy(Qt.NoFocus)
        main_box = QHBoxLayout()
        self.qrw = QRCodeWidget()
        main_box.addWidget(self.qrw, 1)
        self.setLayout(main_box)