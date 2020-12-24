# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/uri_fragment_utility.py
# Compiled at: 2013-04-04 15:36:34
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event as ComponentEvent

class IFragmentChangedListener(object):
    """Listener that listens changes in URI fragment."""

    def fragmentChanged(self, source):
        raise NotImplementedError


_FRAGMENT_CHANGED_METHOD = getattr(IFragmentChangedListener, 'fragmentChanged')

class UriFragmentUtility(AbstractComponent):
    """Experimental web browser dependent component for URI fragment (part
    after hash mark "#") reading and writing.

    Component can be used to workaround common ajax web applications pitfalls:
    bookmarking a program state and back button.
    """
    CLIENT_WIDGET = None

    def addListener(self, listener, iface=None):
        if isinstance(listener, IFragmentChangedListener) and (iface is None or issubclass(iface, IFragmentChangedListener)):
            self.registerListener(FragmentChangedEvent, listener, _FRAGMENT_CHANGED_METHOD)
        super(UriFragmentUtility, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, FragmentChangedEvent):
            self.registerCallback(FragmentChangedEvent, callback, None, *args)
        else:
            super(UriFragmentUtility, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IFragmentChangedListener) and (iface is None or issubclass(iface, IFragmentChangedListener)):
            self.withdrawListener(FragmentChangedEvent, listener, _FRAGMENT_CHANGED_METHOD)
        super(UriFragmentUtility, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, FragmentChangedEvent):
            self.withdrawCallback(FragmentChangedEvent, callback)
        else:
            super(UriFragmentUtility, self).removeCallback(callback, eventType)
        return

    def __init__(self):
        super(UriFragmentUtility, self).__init__()
        self._fragment = None
        self.setImmediate(True)
        return

    def paintContent(self, target):
        super(UriFragmentUtility, self).paintContent(target)
        value = self._fragment if self._fragment is not None else ''
        target.addVariable(self, 'fragment', value)
        return

    def changeVariables(self, source, variables):
        super(UriFragmentUtility, self).changeVariables(source, variables)
        self._fragment = variables.get('fragment')
        self.fireEvent(FragmentChangedEvent(self))

    def getFragment(self):
        """Gets currently set URI fragment.

        To listen changes in fragment, hook a L{IFragmentChangedListener}.

        Note that initial URI fragment that user used to enter the application
        will be read after application init. It fires FragmentChangedEvent
        only if it is not the same as on server side.

        @return: the current fragment in browser uri or null if not known
        """
        return self._fragment

    def setFragment(self, newFragment, fireEvent=True):
        """Sets URI fragment. Optionally fires a L{FragmentChangedEvent}

        @param newFragment:
                   id of the new fragment
        @param fireEvent:
                   true to fire event
        @see: L{FragmentChangedEvent}
        @see: L{IFragmentChangedListener}
        """
        if newFragment is None and self._fragment is not None or newFragment is not None and newFragment != self._fragment:
            self._fragment = newFragment
            if fireEvent:
                fireEvent(FragmentChangedEvent(self))
            self.requestRepaint()
        return


class FragmentChangedEvent(ComponentEvent):
    """Event fired when uri fragment changes."""

    def __init__(self, source):
        """Creates a new instance of UriFragmentReader change event.

        @param source:
                   the Source of the event.
        """
        super(FragmentChangedEvent, self).__init__(source)

    def getUriFragmentUtility(self):
        """Gets the UriFragmentReader where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()