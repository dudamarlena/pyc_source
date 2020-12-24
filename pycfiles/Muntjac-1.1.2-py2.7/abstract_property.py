# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/abstract_property.py
# Compiled at: 2013-04-04 15:36:37
"""Abstract base class for property implementations."""
from muntjac.data import property as prop
from muntjac.util import EventObject

class AbstractProperty(prop.IProperty, prop.IValueChangeNotifier, prop.IReadOnlyStatusChangeNotifier):
    """Abstract base class for L{IProperty} implementations.

    Handles listener management for L{ValueChangeListener}s and
    L{IReadOnlyStatusChangeListener}s.
    """

    def __init__(self):
        self._readOnlyStatusChangeListeners = list()
        self._valueChangeListeners = list()
        self._readOnly = None
        self._readOnlyStatusChangeCallbacks = dict()
        self._valueChangeCallbacks = dict()
        return

    def isReadOnly(self):
        """Override for additional restrictions on what is considered a
        read-only property.
        """
        return self._readOnly

    def setReadOnly(self, newStatus):
        oldStatus = self.isReadOnly()
        self._readOnly = newStatus
        if oldStatus != self.isReadOnly():
            self.fireReadOnlyStatusChange()

    def __str__(self):
        """Returns the value of the C{IProperty} in human readable
        textual format. The return value should be assignable to the
        C{setValue} method if the IProperty is not in read-only mode.

        @return: String representation of the value stored in the IProperty
        """
        value = self.getValue()
        if value is None:
            return
        else:
            return str(value)

    def addListener(self, listener, iface=None):
        """Registers a new read-only status change listener for this IProperty.

        @param listener:
                   the new Listener to be registered.
        """
        if isinstance(listener, prop.IReadOnlyStatusChangeListener) and (iface is None or issubclass(iface, prop.IReadOnlyStatusChangeListener)):
            self._readOnlyStatusChangeListeners.append(listener)
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)):
            self._valueChangeListeners.append(listener)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            self._readOnlyStatusChangeCallbacks[callback] = args
        elif issubclass(eventType, prop.ValueChangeEvent):
            self._valueChangeCallbacks[callback] = args
        else:
            super(AbstractProperty, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        """Removes a previously registered read-only status change listener.

        @param listener:
                   the listener to be removed.
        """
        if isinstance(listener, prop.IReadOnlyStatusChangeListener) and (iface is None or issubclass(iface, prop.IReadOnlyStatusChangeListener)):
            if listener in self._readOnlyStatusChangeListeners:
                self._readOnlyStatusChangeListeners.remove(listener)
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)):
            if listener in self._valueChangeListeners:
                self._valueChangeListeners.remove(listener)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            if callback in self._readOnlyStatusChangeCallbacks:
                del self._readOnlyStatusChangeCallbacks[callback]
        elif issubclass(eventType, prop.ValueChangeEvent):
            if callback in self._valueChangeCallbacks:
                del self._valueChangeCallbacks[callback]
        else:
            super(AbstractProperty, self).removeCallback(callback, eventType)
        return

    def fireReadOnlyStatusChange(self):
        """Sends a read only status change event to all registered listeners.
        """
        event = prop.IReadOnlyStatusChangeEvent(self)
        for listener in self._readOnlyStatusChangeListeners:
            listener.readOnlyStatusChange(event)

        for callback, args in self._readOnlyStatusChangeCallbacks.iteritems():
            callback(event, *args)

    def fireValueChange(self):
        """Sends a value change event to all registered listeners."""
        event = ValueChangeEvent(self)
        for listener in self._valueChangeListeners:
            listener.valueChange(event)

        for callback, args in self._valueChangeCallbacks.iteritems():
            callback(event, *args)

    def getListeners(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return list(self._valueChangeListeners)
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            return list(self._readOnlyStatusChangeListeners)
        return list()

    def getCallbacks(self, eventType):
        if issubclass(eventType, ValueChangeEvent):
            return dict(self._valueChangeCallbacks)
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            return dict(self._readOnlyStatusChangeCallbacks)
        return dict()


class IReadOnlyStatusChangeEvent(EventObject, prop.IProperty, prop.IReadOnlyStatusChangeEvent):
    """An C{Event} object specifying the IProperty whose read-only
    status has been changed.
    """

    def __init__(self, source):
        """Constructs a new read-only status change event for this object.

        @param source:
                   source object of the event.
        """
        super(IReadOnlyStatusChangeEvent, self).__init__(source)

    def getProperty(self):
        """Gets the IProperty whose read-only state has changed.

        @return: source IProperty of the event.
        """
        return self.getSource()


class ValueChangeEvent(EventObject, prop.ValueChangeEvent):
    """An C{Event} object specifying the IProperty whose value has
    been changed.
    """

    def __init__(self, source):
        """Constructs a new value change event for this object.

        @param source:
                   source object of the event.
        """
        super(ValueChangeEvent, self).__init__(source)

    def getProperty(self):
        """Gets the IProperty whose value has changed.

        @return: source IProperty of the event.
        """
        return self.getSource()