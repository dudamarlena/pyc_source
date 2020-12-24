# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/components/gui/main_window/gui.py
# Compiled at: 2020-05-08 05:58:29
# Size of source mod 2**32: 1309 bytes
from PySide2.QtWidgets import QPushButton, QMainWindow, QWidget, QVBoxLayout, QLabel, QAction
from PySide2.QtCore import Slot
from mamba_server.components.gui.about.about import About

class MainWindow(QMainWindow):

    def __init__(self, context):
        self.context = context
        super(MainWindow, self).__init__(context.get('app'))
        self.setWindowTitle('My Awesome App')
        layout = QVBoxLayout()
        self.click_me = QPushButton('Click me')
        self.click_me.clicked.connect(self.say_hello)
        layout.addWidget(self.click_me)
        self.click_me_label = QLabel('Named:')
        layout.addWidget(self.click_me_label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @Slot()
    def say_hello(self):
        self.click_me_label.setText('Hello!')


def execute(context):
    window = MainWindow(context)
    window.show()
    context.set('main_window', window)


if __name__ == '__main__':
    execute()