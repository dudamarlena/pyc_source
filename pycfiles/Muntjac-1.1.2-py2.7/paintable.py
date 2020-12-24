# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/paintable.py
# Compiled at: 2013-04-04 15:36:36
"""Defines an interface implemented by all classes that can be painted."""
from muntjac.util import IEventListener, EventObject

class IPaintable(IEventListener):
    """Interface implemented by all classes that can be painted. Classes
    implementing this interface know how to output themselves to a UIDL
    stream and that way describing to the terminal how it should be displayed
    in the UI.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def paint(self, target):
        """Paints the IPaintable into a UIDL stream. This method creates the
        UIDL sequence describing it and outputs it to the given UIDL stream.

        It is called when the contents of the component should be painted in
        response to the component first being shown or having been altered so
        that its visual representation is changed.

        @param target:
                   the target UIDL stream where the component should paint
                   itself to.
        @raise PaintException:
                    if the paint operation failed.
        """
        raise NotImplementedError

    def requestRepaint(self):
        """Requests that the paintable should be repainted as soon as
        possible."""
        raise NotImplementedError

    def setDebugId(self, idd):
        """Adds an unique id for component that get's transferred to terminal
        for testing purposes. Keeping identifiers unique throughout the
        Application instance is on programmers responsibility.

        Note, that with the current terminal implementation the identifier
        cannot be changed while the component is visible. This means that the
        identifier should be set before the component is painted for the first
        time and kept the same while visible in the client.

        @param idd:
                   A short (< 20 chars) alphanumeric id
        """
        raise NotImplementedError

    def getDebugId(self):
        """Get's currently set debug identifier

        @return: current debug id, null if not set
        """
        raise NotImplementedError

    def addListener(self, listener, iface=None):
        """Adds repaint request listener. In order to assure that no repaint
        requests are missed, the new repaint listener should paint the
        paintable right after adding itself as listener.

        @param listener:
                   the listener to be added.
        """
        if isinstance(listener, IRepaintRequestListener) and (iface is None or iface == IRepaintRequestListener):
            raise NotImplementedError
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if eventType == RepaintRequestEvent:
            raise NotImplementedError
        return

    def removeListener(self, listener, iface):
        """Removes repaint request listener.

        @param listener:
                   the listener to be removed.
        """
        if iface == IRepaintRequestListener:
            raise NotImplementedError
        else:
            super(IPaintable, self).removeListener(listener, iface)

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if eventType == RepaintRequestEvent:
            raise NotImplementedError
        return

    def requestRepaintRequests(self):
        """Request sending of repaint events on any further visible changes.
        Normally the paintable only send up to one repaint request for
        listeners after paint as the paintable as the paintable assumes that
        the listeners already know about the repaint need. This method resets
        the assumtion. Paint implicitly does the assumtion reset functionality
        implemented by this method.

        This method is normally used only by the terminals to note paintables
        about implicit repaints (painting the component without actually
        invoking paint method).
        """
        raise NotImplementedError


class RepaintRequestEvent(EventObject):
    """Repaint request event is thrown when the paintable needs to be
    repainted. This is typically done when the C{paint} method
    would return dissimilar UIDL from the previous call of the method.
    """

    def __init__(self, source):
        """Constructs a new event.

        @param source:
                   the paintable needing repaint.
        """
        super(RepaintRequestEvent, self).__init__(source)

    def getPaintable(self):
        """Gets the paintable needing repainting.

        @return: IPaintable for which the C{paint} method will return
                dissimilar UIDL from the previous call of the method.
        """
        return self.getSource()


class IRepaintRequestListener(object):
    """Listens repaint requests. The C{repaintRequested} method is
    called when the paintable needs to be repainted. This is typically done
    when the C{paint} method would return dissimilar UIDL from the
    previous call of the method.
    """

    def repaintRequested(self, event):
        """Receives repaint request events.

        @param event:
                   the repaint request event specifying the paintable source.
        """
        raise NotImplementedError