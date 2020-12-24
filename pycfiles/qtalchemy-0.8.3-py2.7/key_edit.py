# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/widgets/key_edit.py
# Compiled at: 2013-09-07 09:08:02
"""
The PBKeyEdit provides data sensitive editting for foreign key edits::

- search button
- context menus - for what? (look up referenced entity)
"""
from PySide import QtCore, QtGui
from .button_edit import PBButtonEdit

class PBKeyEdit(PBButtonEdit):
    """
    PBKeyEdit is a QLineEdit derivative that offers a button on the right to 
    search for rows from a database table.  PBKeyEdit is best used in the 
    InputYoke infrastructure with a DomainEntity derived class.
    """

    def __init__(self, parent=None):
        PBButtonEdit.__init__(self, parent)
        self.button.setIcon(QtGui.QIcon(':/qtalchemy/widgets/edit-find-6.ico'))