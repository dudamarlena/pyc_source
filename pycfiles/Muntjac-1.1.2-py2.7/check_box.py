# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/check_box.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a switch button."""
from warnings import warn
from muntjac.ui.button import Button, IClickListener
from muntjac.data.property import IProperty

class CheckBox(Button):
    CLIENT_WIDGET = None

    def __init__(self, *args):
        """Creates a new switch button.

        @param args: tuple of the form
            - (caption, initialState)
              1. the caption of the switch button
              2. the initial state of the switch button
            - (caption, listener)
              1. the caption of the switch button
              2. the click listener
            - (caption, target, methodName)
              1. the Button caption.
              2. the Object having the method for listening button clicks.
              3. the name of the method in target object, that receives
                 button click events.
            - (state, dataSource)
              1. the Initial state of the switch-button.
              2. boolean property
            - (caption)
              1. the switch button caption
        """
        nargs = len(args)
        if nargs == 0:
            super(CheckBox, self).__init__()
            self.setSwitchMode(True)
        elif nargs == 1:
            caption, = args
            super(CheckBox, self).__init__(caption, False)
        elif nargs == 2:
            if isinstance(args[1], IClickListener):
                caption, listener = args
                super(CheckBox, self).__init__(caption, listener)
                self.setSwitchMode(True)
            elif isinstance(args[1], IProperty):
                caption, dataSource = args
                super(CheckBox, self).__init__(caption, dataSource)
                self.setSwitchMode(True)
            else:
                caption, initialState = args
                super(CheckBox, self).__init__(caption, initialState)
        elif nargs == 3:
            caption, target, methodName = args
            super(CheckBox, self).__init__(caption, target, methodName)
            self.setSwitchMode(True)
        else:
            raise ValueError, 'too many arguments'

    def setSwitchMode(self, switchMode):
        warn('CheckBox is always in switch mode', DeprecationWarning)
        if self._switchMode and not switchMode:
            raise NotImplementedError, 'CheckBox is always in switch mode (consider using a Button)'
        super(CheckBox, self).setSwitchMode(True)

    def setDisableOnClick(self, disableOnClick):
        raise NotImplementedError, 'CheckBox does not support disable on click'