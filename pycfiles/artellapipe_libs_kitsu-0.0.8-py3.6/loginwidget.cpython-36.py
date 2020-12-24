# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/kitsu/widgets/loginwidget.py
# Compiled at: 2020-05-13 18:50:00
# Size of source mod 2**32: 1629 bytes
"""
Module that contains implementation for Kitsu Login widget
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtCore import *
from Qt.QtWidgets import *
import tpDcc
from artellapipe.widgets import spinner

class KitsuLoginWidget(QFrame, object):

    def __init__(self, parent=None):
        super(KitsuLoginWidget, self).__init__(parent)
        self.setStyleSheet('#background {border-radius: 3px;border-style: solid;border-width: 1px;border-color: rgb(32,32,32);}')
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        kitsu_pixmap = tpDcc.ResourcesMgr().pixmap('kitsu', category='icons', theme='color')
        kitsu_icon = QLabel()
        kitsu_icon.setAlignment(Qt.AlignCenter)
        kitsu_icon.setPixmap(kitsu_pixmap)
        main_layout.addWidget(kitsu_icon)
        self.wait_spinner = spinner.WaitSpinner(spinner_type=(spinner.SpinnerType.Loading))
        self.wait_spinner._bg.setFrameShape(QFrame.NoFrame)
        self.wait_spinner._bg.setFrameShadow(QFrame.Plain)
        main_layout.addWidget(self.wait_spinner)