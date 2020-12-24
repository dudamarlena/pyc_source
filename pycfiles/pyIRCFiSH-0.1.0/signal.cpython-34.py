# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/signal.py
# Compiled at: 2015-10-08 05:15:41
# Size of source mod 2**32: 3056 bytes
__doc__ = 'Decorator and helpers connecting the PyIRC event system to Taillight.'
from collections import defaultdict
from inspect import getmembers
from logging import getLogger
from taillight.signal import UnsharedSignal
from taillight import ANY
try:
    from enum import Enum
except ImportError:
    from PyIRC.util.enum import Enum

_logger = getLogger(__name__)

def event(hclass, event_name, priority=UnsharedSignal.PRIORITY_NORMAL, listener=ANY):
    """Tag a function as an event for later binding.

    This function is a decorator.

    :param hclass:
        Name of the event class.

    :param event_name:
        Name of the event.

    :param priority:
        Priority of the signal

    :param listener:
        Listener of the signal.

    """
    if isinstance(event_name, Enum):
        event_name = event_name.value
    name = (hclass, event_name)

    def wrapped(function):
        if not hasattr(function, '_signal'):
            function._signal = list()
        function._signal.append((name, priority, listener))
        return function

    return wrapped


class SignalDict(dict):
    """SignalDict"""

    def __missing__(self, key):
        value = self[key] = UnsharedSignal(key)
        return value


class SignalStorage:
    """SignalStorage"""

    @staticmethod
    def _signal_pred(member):
        return hasattr(member, '_signal')

    def __init__(self):
        self.signals = SignalDict()
        self.signal_slots = defaultdict(list)

    def bind(self, inst):
        """Bind slots from `inst` to their respective signals."""
        slots = self.signal_slots[id(inst)]
        for _, function in getmembers(inst, self._signal_pred):
            for param in function._signal:
                signal = self.get_signal(param[0])
                slots.append(signal.add(function, *param[1:]))

    def unbind(self, inst):
        """Remove slots from `inst` from their respective signals."""
        for slot in self.signal_slots[id(inst)]:
            slot.signal.delete(slot)

    def get_bound(self, inst):
        """Get all the slots for `inst`."""
        return self.signal_slots[id(inst)]

    def get_signal(self, name):
        """Retrieve the specified signal for this PyIRC instance."""
        return self.signals[name]

    def __contains__(self, name):
        return name in self.signals