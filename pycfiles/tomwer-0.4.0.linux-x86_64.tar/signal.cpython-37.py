# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/signal.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5988 bytes
__author__ = 'Dhruv Govil'
__copyright__ = 'Copyright 2016, Dhruv Govil'
__credits__ = ['Dhruv Govil', 'John Hood', 'Jason Viloria', 'Adric Worley',
 'Alex Widener']
__license__ = 'MIT'
__version__ = '1.1.1'
__maintainer__ = 'Dhruv Govil'
__email__ = 'dhruvagovil@gmail.com'
__status__ = 'Beta'
__date__ = '09/01/2018'
import inspect, weakref
from functools import partial

class Signal(object):
    __doc__ = '\n    The Signal is the core object that handles connection and emission .\n    \n    .. warning: This intends to work only for Signal/Slot executed in the same\n                thread.\n    '

    def __init__(self, *arg_types):
        super(Signal, self).__init__()
        self._block = False
        self._slots = []
        self._arguments_types = arg_types

    def emit(self, *args, **kwargs):
        """
        Calls all the connected slots with the provided args and kwargs unless block is activated
        """
        if self._block:
            return
        for slot in self._slots:
            if not slot:
                continue
            elif isinstance(slot, partial):
                slot()
            elif isinstance(slot, weakref.WeakKeyDictionary):
                for obj, method in slot.items():
                    method(obj, *args, **kwargs)

            elif isinstance(slot, weakref.ref):
                if slot() is not None:
                    (slot())(*args, **kwargs)

    def connect(self, slot):
        """
        Connects the signal to any callable object
        """
        if not callable(slot):
            raise ValueError("Connection to non-callable '%s' object failed" % slot.__class__.__name__)
        elif isinstance(slot, partial) or '<' in slot.__name__:
            if slot not in self._slots:
                self._slots.append(slot)
        elif inspect.ismethod(slot):
            slotSelf = slot.__self__
            slotDict = weakref.WeakKeyDictionary()
            slotDict[slotSelf] = slot.__func__
            if slotDict not in self._slots:
                self._slots.append(slotDict)
        else:
            newSlotRef = weakref.ref(slot)
            if newSlotRef not in self._slots:
                self._slots.append(newSlotRef)

    def disconnect(self, slot):
        """
        Disconnects the slot from the signal
        """
        if not callable(slot):
            return
            if inspect.ismethod(slot):
                slotSelf = slot.__self__
                for s in self._slots:
                    if isinstance(s, weakref.WeakKeyDictionary) and slotSelf in s and s[slotSelf] is slot.__func__:
                        self._slots.remove(s)
                        break

        elif isinstance(slot, partial) or '<' in slot.__name__:
            try:
                self._slots.remove(slot)
            except ValueError:
                pass

        else:
            try:
                self._slots.remove(weakref.ref(slot))
            except ValueError:
                pass

    def clear(self):
        """Clears the signal of all connected slots"""
        self._slots = []

    def block(self, isBlocked):
        """Sets blocking of the signal"""
        self._block = bool(isBlocked)