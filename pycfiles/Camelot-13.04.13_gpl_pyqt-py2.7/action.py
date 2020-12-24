# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action.py
# Compiled at: 2013-04-11 17:47:52
"""The action module contains various QAction classes, representing commands
that can be invoked via menus, toolbar buttons, and keyboard shortcuts."""
from PyQt4 import QtGui
from camelot.view.art import Icon
from camelot.core.utils import ugettext as _

class ActionFactory(object):
    """Utility class to generate some default actions we need
    in several places.
    
    Each method of this class, returns a certain action with
    a default text, icon and shortcut.
    """
    icon_copy = Icon('tango/16x16/actions/edit-copy.png')

    @classmethod
    def create_action(*a, **kw):
        """creates and returns a QAction object"""
        parent = kw['parent']
        text = kw['text']
        slot = kw.get('slot', None)
        shortcut = kw.get('shortcut', '')
        actionicon = kw.get('actionicon', '')
        tip = kw.get('tip', '')
        checkable = kw.get('checkable', False)
        widgetaction = kw.get('widgetaction', False)
        if widgetaction:
            action = QtGui.QWidgetAction(parent)
        else:
            action = QtGui.QAction(parent)
        action.setText(text)
        if actionicon:
            action.setIcon(actionicon.getQIcon())
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    @classmethod
    def copy(cls, parent, slot, **kwargs):
        default = dict(text=_('Copy'), slot=slot, parent=parent, shortcut=QtGui.QKeySequence.Copy, actionicon=Icon('tango/16x16/actions/edit-copy.png'), tip=_('Duplicate'))
        default.update(kwargs)
        return cls.create_action(**default)

    @classmethod
    def paste(cls, parent, slot, **kwargs):
        default = dict(text=_('Paste'), slot=slot, parent=parent, shortcut=QtGui.QKeySequence.Paste, actionicon=Icon('tango/16x16/actions/edit-paste.png'), tip=_('Paste content from clipboard'))
        default.update(kwargs)
        return cls.create_action(**default)