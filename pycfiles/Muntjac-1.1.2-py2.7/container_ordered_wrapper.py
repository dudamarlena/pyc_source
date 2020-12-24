# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/container_ordered_wrapper.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.data.container import IOrdered, IItemSetChangeNotifier, IPropertySetChangeNotifier, IItemSetChangeListener, IPropertySetChangeListener, IItemSetChangeEvent, IPropertySetChangeEvent

class ContainerOrderedWrapper(IOrdered, IItemSetChangeNotifier, IPropertySetChangeNotifier):
    """A wrapper class for adding external ordering to containers not
    implementing the L{IOrdered} interface.

    If the wrapped container is changed directly (that is, not through the
    wrapper), and does not implement Container.ItemSetChangeNotifier and/or
    PropertySetChangeNotifier the hierarchy information must be updated with
    the L{updateOrderWrapper} method.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, toBeWrapped):
        """Constructs a new ordered wrapper for an existing Container. Works even if
        the to-be-wrapped container already implements the Container.Ordered
        interface.

        @param toBeWrapped
                   the container whose contents need to be ordered.
        """
        self._container = toBeWrapped
        self._next = None
        self._prev = None
        self._first = None
        self._last = None
        self._ordered = False
        self._lastKnownSize = -1
        self._ordered = isinstance(self._container, IOrdered)
        if self._container is None:
            raise ValueError, 'Null can not be wrapped'
        self.updateOrderWrapper()
        return

    def removeFromOrderWrapper(self, idd):
        """Removes the specified Item from the wrapper's internal hierarchy
        structure.

        Note : The Item is not removed from the underlying Container.

        @param idd:
                   the ID of the Item to be removed from the ordering.
        """
        if idd is not None:
            pid = self._prev.get(idd)
            nid = self._next.get(idd)
            if self._first == idd:
                self._first = nid
            if self._last == idd:
                self._first = pid
            if nid is not None:
                self._prev[nid] = pid
            if pid is not None:
                self._next[pid] = nid
            del self._next[idd]
            del self._prev[idd]
        return

    def addToOrderWrapper(self, idd, previousItemId=None):
        """Registers the specified Item to the last position in the wrapper's
        internal ordering. The underlying container is not modified.

        @param idd
                   the ID of the Item to be added to the ordering.
        ---
        Registers the specified Item after the specified itemId in the wrapper's
        internal ordering. The underlying container is not modified. Given item
        idd must be in the container, or must be null.

        @param idd
                   the ID of the Item to be added to the ordering.
        @param previousItemId
                   the Id of the previous item.
        """
        if previousItemId == None:
            if self._last is not None:
                self._next[self._last] = idd
                self._prev[idd] = self._last
                self._last = idd
            else:
                self._first = self._last = idd
        elif self._last == previousItemId or self._last is None:
            self.addToOrderWrapper(idd)
        elif previousItemId is None:
            self._next[idd] = self._first
            self._prev[self._first] = idd
            self._first = idd
        else:
            self._prev[idd] = previousItemId
            self._next[idd] = self._next[previousItemId]
            self._prev[self._next.get(previousItemId)] = idd
            self._next[previousItemId] = idd
        return

    def updateOrderWrapper(self):
        """Updates the wrapper's internal ordering information to include all
        Items in the underlying container.

        Note: If the contents of the wrapped container change without the
        wrapper's knowledge, this method needs to be called to update the
        ordering information of the Items.
        """
        if not self._ordered:
            ids = self._container.getItemIds()
            if self._next is None or self._first is None or self._last is None or self._prev is not None:
                self._first = None
                self._last = None
                self._next = dict()
                self._prev = dict()
            for idd in self._next:
                if not self._container.containsId(idd):
                    self.removeFromOrderWrapper(idd)

            for idd in ids:
                if idd not in self._next:
                    self.addToOrderWrapper(idd)

        return

    def firstItemId(self):
        if self._ordered:
            return self._container.firstItemId()
        return self._first

    def isFirstId(self, itemId):
        if self._ordered:
            return self._container.isFirstId(itemId)
        else:
            return self._first is not None and self._first == itemId

    def isLastId(self, itemId):
        if self._ordered:
            return self._container.isLastId(itemId)
        else:
            return self._last is not None and self._last == itemId

    def lastItemId(self):
        if self._ordered:
            return self._container.lastItemId()
        return self._last

    def nextItemId(self, itemId):
        if self._ordered:
            return self._container.nextItemId(itemId)
        else:
            if itemId is None:
                return
            return self._next.get(itemId)

    def prevItemId(self, itemId):
        if self._ordered:
            return self._container.prevItemId(itemId)
        else:
            if itemId is None:
                return
            return self._prev.get(itemId)

    def addContainerProperty(self, propertyId, typ, defaultValue):
        """Registers a new Property to all Items in the Container.

        @param propertyId:
                   the ID of the new Property.
        @param typ:
                   the Data type of the new Property.
        @param defaultValue:
                   the value all created Properties are initialized to.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        return self._container.addContainerProperty(propertyId, typ, defaultValue)

    def addItem(self, itemId=None):
        """Creates a new Item into the Container, assigns it an automatic ID,
        and adds it to the ordering. Alternatively, registers a new Item by
        its ID to the underlying container and to the ordering.

        @param itemId:
                   the ID of the Item to be created.
        @return:
                   C{None} if the operation failed
        @raise NotImplementedError:
                   if the addItem is not supported.
        """
        if itemId is None:
            idd = self._container.addItem()
            if not self._ordered and idd is not None:
                self.addToOrderWrapper(idd)
            return idd
        item = self._container.addItem(itemId)
        if not self._ordered and item is not None:
            self.addToOrderWrapper(itemId)
        return item
        return

    def removeAllItems(self):
        """Removes all items from the underlying container and from the
        ordering.

        @return: C{True} if the operation succeeded, otherwise C{False}
        @raise NotImplementedError:
                    if the removeAllItems is not supported.
        """
        success = self._container.removeAllItems()
        if not self._ordered and success:
            self._first = self._last = None
            self._next.clear()
            self._prev.clear()
        return success

    def removeItem(self, itemId):
        """Removes an Item specified by the itemId from the underlying
        container and from the ordering.

        @param itemId:
                   the ID of the Item to be removed.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                   if the removeItem is not supported.
        """
        success = self._container.removeItem(itemId)
        if not self._ordered and success:
            self.removeFromOrderWrapper(itemId)
        return success

    def removeContainerProperty(self, propertyId):
        """Removes the specified Property from the underlying container and
        from the ordering.

        Note: The Property will be removed from all the Items in the Container.

        @param propertyId:
                   the ID of the Property to remove.
        @return: C{True} if the operation succeeded, C{False} if not
        @raise NotImplementedError:
                   if the removeContainerProperty is not supported.
        """
        return self._container.removeContainerProperty(propertyId)

    def containsId(self, itemId):
        return self._container.containsId(itemId)

    def getItem(self, itemId):
        return self._container.getItem(itemId)

    def getItemIds(self):
        return self._container.getItemIds()

    def getContainerProperty(self, itemId, propertyId):
        return self._container.getContainerProperty(itemId, propertyId)

    def getContainerPropertyIds(self):
        return self._container.getContainerPropertyIds()

    def getType(self, propertyId):
        return self._container.getType(propertyId)

    def size(self):
        newSize = len(self._container)
        if self._lastKnownSize != -1 and newSize != self._lastKnownSize and not isinstance(self._container, IItemSetChangeNotifier):
            self.updateOrderWrapper()
        self._lastKnownSize = newSize
        return newSize

    def __len__(self):
        return self.size()

    def addListener(self, listener, iface=None):
        if isinstance(listener, IItemSetChangeListener) and (iface is None or issubclass(iface, IItemSetChangeListener)):
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.addListener(pl, IItemSetChangeListener)
        if isinstance(listener, IPropertySetChangeListener) and (iface is None or issubclass(iface, IPropertySetChangeListener)):
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.addListener(pl, IPropertySetChangeListener)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, IItemSetChangeEvent):
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(callback, self, *args)
                self._container.addListener(pl, IItemSetChangeListener)
        elif issubclass(eventType, IPropertySetChangeEvent):
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(callback, self, *args)
                self._container.addListener(pl, IPropertySetChangeListener)
        else:
            super(ContainerOrderedWrapper, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IItemSetChangeListener) and (iface is None or issubclass(iface, IItemSetChangeListener)):
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.removeListener(pl, IItemSetChangeListener)
        if isinstance(listener, IPropertySetChangeListener) and (iface is None or issubclass(iface, IPropertySetChangeListener)):
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(listener, self)
                self._container.removeListener(pl, IPropertySetChangeListener)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, IItemSetChangeEvent):
            if isinstance(self._container, IItemSetChangeNotifier):
                pl = PiggybackListener(callback, self)
                self._container.removeListener(pl, IItemSetChangeListener)
        elif issubclass(eventType, IPropertySetChangeEvent):
            if isinstance(self._container, IPropertySetChangeNotifier):
                pl = PiggybackListener(callback, self)
                self._container.removeListener(pl, IPropertySetChangeListener)
        else:
            super(ContainerOrderedWrapper, self).removeCallback(callback, eventType)
        return

    def addItemAfter(self, previousItemId, newItemId=None):
        if newItemId == None:
            if previousItemId is not None and not self.containsId(previousItemId):
                return
            idd = self._container.addItem()
            if not self._ordered and idd is not None:
                self.addToOrderWrapper(idd, previousItemId)
            return idd
        if previousItemId is not None and not self.containsId(previousItemId):
            return
        else:
            item = self._container.addItem(newItemId)
            if not self._ordered and item is not None:
                self.addToOrderWrapper(newItemId, previousItemId)
            return item
            return


class PiggybackListener(IPropertySetChangeListener, IItemSetChangeListener):
    """This listener 'piggybacks' on the real listener in order to update the
    wrapper when needed. It proxies __eq__() and __hash__() to the real
    listener so that the correct listener gets removed.
    """

    def __init__(self, realListener, wrapper, *args):
        self._listener = realListener
        self._wrapper = wrapper
        self._args = args

    def containerItemSetChange(self, event):
        self._wrapper.updateOrderWrapper()
        if isinstance(self._listener, IItemSetChangeListener):
            self._listener.containerItemSetChange(event)
        else:
            self._listener(event, *self._args)

    def containerPropertySetChange(self, event):
        self._wrapper.updateOrderWrapper()
        if isinstance(self._listener, IPropertySetChangeListener):
            self._listener.containerPropertySetChange(event)
        else:
            self._listener(event, *self._args)

    def __eq__(self, obj):
        return obj == self._listener or obj is not None and obj == self._listener

    def __hash__(self):
        return hash(self._listener)