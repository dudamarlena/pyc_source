# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/messages.py
# Compiled at: 2017-12-04 23:29:30
# Size of source mod 2**32: 1506 bytes
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel
__all__ = [
 'MessageBar']

class MessageBar(QHBoxLayout):

    def __init__(self):
        super(MessageBar, self).__init__()
        self.type = 'ready'
        self.setObjectName('layout_info')
        self.setContentsMargins(0, 0, 0, 0)
        self.label_info = QLabel('', alignment=(Qt.AlignCenter))
        self.label_info.setObjectName('label_message')
        self.addWidget((self.label_info), stretch=0)
        self.update_style()

    def update_style(self):
        font_style = 'color: #ffffff;'
        min_height = 'min-height: 50px;'
        bgr_attr = 'background-color: '
        if self.type == 'info':
            color = 'rgba(80, 190, 220, 0.8);'
        else:
            if self.type == 'warning':
                color = 'rgba(223, 38, 38, 0.8);'
            else:
                if self.type in ('question', 'response'):
                    color = 'rgba(64, 158, 19, 0.8);'
                else:
                    color = 'rgba(210, 84, 168, 0.8);'
        bgr_style = bgr_attr + color
        self.label_info.setStyleSheet(font_style + bgr_style + min_height)

    def set(self, msg, additional_info=None):
        type_, msg_string = self.stack_messages.get(msg)
        if additional_info:
            msg_string = msg_string % additional_info
        self.label_info.setText(msg_string)
        self.type = type_
        self.update_style()

    def load_stack(self, messages):
        self.stack_messages = messages