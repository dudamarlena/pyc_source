# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/group.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 2267 bytes
"""
Module that contains different group widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from tpQtLib.core import qtutils

class BaseGroup(QGroupBox, object):

    def __init__(self, name='', parent=None):
        super(BaseGroup, self).__init__(parent)
        self.setTitle(name)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.main_layout)
        self.ui()
        self.setup_signals()

    def ui(self):
        """
        Function that sets up the ui of the widget
        Override it on new widgets
        """
        pass

    def setup_signals(self):
        """
        Function that set up signals of the group widgets
        """
        pass

    def set_title(self, new_title):
        """
        Set the title of the group
        """
        self.setTitle(new_title)


class CollapsableGroup(BaseGroup, object):

    def __init__(self, name='', parent=None, collapsable=True):
        super(CollapsableGroup, self).__init__(name, parent)
        self._collapsable = collapsable

    def mousePRessEvent(self, event):
        super(CollapsableGroup, self).mousePressEvent(event)
        if not event.button() == Qt.LeftButton:
            return
        if self._collapsable:
            if event.y() < 30:
                self._base_widget.setVisible(not self._base_widget.isVisible())

    def set_collapsable(self, flag):
        """
        Sets if the group can be collapsed or not
        :param collapsable: flag
        """
        self._collapsable = flag

    def expand_group(self):
        """
        Expands the content of the group
        """
        self.setFixedSize(qtutils.QWIDGET_SIZE_MAX)
        self.setVisible(True)

    def collapse_group(self):
        """
        Collapse the content of the group
        """
        self._base_widget.setVisible(False)