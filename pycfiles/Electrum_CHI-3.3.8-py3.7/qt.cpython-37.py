# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/virtualkeyboard/qt.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 1738 bytes
import random
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPushButton
from electrum.plugin import BasePlugin, hook
from electrum.i18n import _

class Plugin(BasePlugin):
    vkb = None
    vkb_index = 0

    @hook
    def password_dialog(self, pw, grid, pos):
        vkb_button = QPushButton(_('+'))
        vkb_button.setFixedWidth(20)
        vkb_button.clicked.connect(lambda : self.toggle_vkb(grid, pw))
        grid.addWidget(vkb_button, pos, 2)
        self.kb_pos = 2
        self.vkb = None

    def toggle_vkb(self, grid, pw):
        if self.vkb:
            grid.removeItem(self.vkb)
        self.vkb = self.virtual_keyboard(self.vkb_index, pw)
        grid.addLayout(self.vkb, self.kb_pos, 0, 1, 3)
        self.vkb_index += 1

    def virtual_keyboard(self, i, pw):
        i = i % 3
        if i == 0:
            chars = 'abcdefghijklmnopqrstuvwxyz '
        else:
            if i == 1:
                chars = 'ABCDEFGHIJKLMNOPQRTSUVWXYZ '
            else:
                if i == 2:
                    chars = '1234567890!?.,;:/%&()[]{}+-'
        n = len(chars)
        s = []
        for i in range(n):
            while True:
                k = random.randint(0, n - 1)
                if k not in s:
                    s.append(k)
                    break

        def add_target(t):
            return lambda : pw.setText(str(pw.text()) + t)

        vbox = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(2)
        for i in range(n):
            l_button = QPushButton(chars[s[i]])
            l_button.setFixedWidth(25)
            l_button.setFixedHeight(25)
            l_button.clicked.connect(add_target(chars[s[i]]))
            grid.addWidget(l_button, i // 6, i % 6)

        vbox.addLayout(grid)
        return vbox