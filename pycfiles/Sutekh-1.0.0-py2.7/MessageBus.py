# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/MessageBus.py
# Compiled at: 2019-12-11 16:37:48
"""Message Bus for Sutekh"""
CONFIG_MSG, CARD_TEXT_MSG, DATABASE_MSG = range(3)

class MessageBus(object):
    """The actual message bus"""
    _dSubscriptions = {}

    @classmethod
    def subscribe(cls, oObject, sSignalName, fCallback):
        """Subscribe to a given signal on an object"""
        if oObject not in cls._dSubscriptions:
            cls._dSubscriptions[oObject] = {}
        dCallbacks = cls._dSubscriptions[oObject]
        if sSignalName not in dCallbacks:
            dCallbacks[sSignalName] = []
        dCallbacks[sSignalName].append(fCallback)

    @classmethod
    def publish(cls, oObject, sSignalName, *args, **kwargs):
        """Publish the signal to any subscribers"""
        if oObject not in cls._dSubscriptions:
            return
        dCallbacks = cls._dSubscriptions[oObject]
        if sSignalName not in dCallbacks:
            return
        for fCallback in dCallbacks[sSignalName]:
            fCallback(*args, **kwargs)

    @classmethod
    def unsubscribe(cls, oObject, sSignalName, fCallback):
        """Remove a callback from the list"""
        if oObject not in cls._dSubscriptions:
            return
        dCallbacks = cls._dSubscriptions[oObject]
        if sSignalName not in dCallbacks:
            return
        if fCallback not in dCallbacks[sSignalName]:
            return
        dCallbacks[sSignalName].remove(fCallback)

    @classmethod
    def clear(cls, oObject):
        """Clear all callbacks associated with the given object"""
        if oObject in cls._dSubscriptions:
            del cls._dSubscriptions[oObject]