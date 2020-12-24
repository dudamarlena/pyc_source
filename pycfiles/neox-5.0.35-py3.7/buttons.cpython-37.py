# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/buttons.py
# Compiled at: 2019-06-09 22:39:01
# Size of source mod 2**32: 521 bytes
from PyQt5.QtWidgets import QPushButton
__all__ = [
 'ActionButton']

class ActionButton(QPushButton):

    def __init__(self, action, method):
        super(ActionButton, self).__init__('')
        if action == 'ok':
            name = self.tr('&ACCEPT')
        else:
            name = self.tr('&CANCEL')
        self.setText(name)
        self.clicked.connect(method)
        if action == 'ok':
            self.setAutoDefault(True)
            self.setDefault(True)
        self.setObjectName('button_' + action)