# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/fee_slider.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 2735 bytes
import threading
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QToolTip
from electrum.i18n import _

class FeeSlider(QSlider):

    def __init__(self, window, config, callback):
        QSlider.__init__(self, Qt.Horizontal)
        self.config = config
        self.window = window
        self.callback = callback
        self.dyn = False
        self.lock = threading.RLock()
        self.update()
        self.valueChanged.connect(self.moved)
        self._active = True

    def moved(self, pos):
        with self.lock:
            if self.dyn:
                fee_rate = self.config.depth_to_fee(pos) if self.config.use_mempool_fees() else self.config.eta_to_fee(pos)
            else:
                fee_rate = self.config.static_fee(pos)
            tooltip = self.get_tooltip(pos, fee_rate)
            QToolTip.showText(QCursor.pos(), tooltip, self)
            self.setToolTip(tooltip)
            self.callback(self.dyn, pos, fee_rate)

    def get_tooltip(self, pos, fee_rate):
        mempool = self.config.use_mempool_fees()
        target, estimate = self.config.get_fee_text(pos, self.dyn, mempool, fee_rate)
        if self.dyn:
            return _('Target') + ': ' + target + '\n' + _('Current rate') + ': ' + estimate
        return _('Fixed rate') + ': ' + target + '\n' + _('Estimate') + ': ' + estimate

    def update(self):
        with self.lock:
            self.dyn = self.config.is_dynfee()
            mempool = self.config.use_mempool_fees()
            maxp, pos, fee_rate = self.config.get_fee_slider(self.dyn, mempool)
            self.setRange(0, maxp)
            self.setValue(pos)
            tooltip = self.get_tooltip(pos, fee_rate)
            self.setToolTip(tooltip)

    def activate(self):
        self._active = True
        self.setStyleSheet('')

    def deactivate(self):
        self._active = False
        self.setStyleSheet('\n            QSlider::groove:horizontal {\n                border: 1px solid #999999;\n                height: 8px;\n                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #B1B1B1);\n                margin: 2px 0;\n            }\n\n            QSlider::handle:horizontal {\n                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n                border: 1px solid #5c5c5c;\n                width: 12px;\n                margin: -2px 0;\n                border-radius: 3px;\n            }\n            ')

    def is_active(self):
        return self._active