# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/actionsbox.py
# Compiled at: 2013-04-11 17:47:52
"""Actions box"""
import logging
LOGGER = logging.getLogger('controls.actionsbox')
from PyQt4 import QtGui

class ActionsBox(QtGui.QWidget):
    """A box containing actions to be applied to a view

    :param gui_context: a :class:`camelot.admin.action.base.GuiContext` object
    :param parent: a :class:`PyQt4.QtGui.QWidget` object
    
    """

    def __init__(self, gui_context, parent):
        LOGGER.debug('create actions box')
        super(ActionsBox, self).__init__(parent)
        self.gui_context = gui_context

    def set_actions(self, actions):
        LOGGER.debug('setting actions')
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(2)
        for action in actions:
            action_widget = action.render(self.gui_context, self)
            layout.addWidget(action_widget)

        self.setLayout(layout)