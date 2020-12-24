# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/AXKeyboard.py
# Compiled at: 2012-08-03 19:46:40
import Quartz
from AXKeyCodeConstants import *
modKeyFlagConstants = {COMMAND: Quartz.kCGEventFlagMaskCommand, 
   SHIFT: Quartz.kCGEventFlagMaskShift, 
   OPTION: Quartz.kCGEventFlagMaskAlternate, 
   CONTROL: Quartz.kCGEventFlagMaskControl}

def loadKeyboard():
    """ Load a given keyboard mapping (of characters to virtual key codes)

       Default is US keyboard
       Parameters: None (relies on the internationalization settings)
       Returns: A dictionary representing the current keyboard mapping (of
                characters to keycodes)
   """
    keyboardLayout = {}
    keyboardLayout = DEFAULT_KEYBOARD
    keyboardLayout.update(specialKeys)
    return keyboardLayout