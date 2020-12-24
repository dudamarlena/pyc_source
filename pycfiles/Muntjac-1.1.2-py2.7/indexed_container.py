# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/indexed_container.py
# Compiled at: 2013-04-04 15:36:37
"""An implementation of the IIndexed interface with all important features."""
from muntjac.data import property as prop
from muntjac.data.item import IItem
from muntjac.data.util.abstract_in_memory_container import AbstractInMemoryContainer
from muntjac.data.util.filter.simple_string_filter import SimpleStringFilter
from muntjac.data.util.filter.unsupported_filter_exception import UnsupportedFilterException
from muntjac.data.util.abstract_container import BaseItemSetChangeEvent, AbstractContainer
from muntjac.data import container
from muntjac.util import EventObject
from muntjac.util import fullname

class IndexedContainer(AbstractInMemoryContainer, container.IPropertySetChangeNotifier, prop.IValueChangeNotifier, container.ISortable, container.IFilterable, container.ISimpleFilterable):
    """An implementation of the L{IContainer.Indexed} interface with all
    important features.

    Features:
      - L{IIndexed}
      - L{IOrdered}
      - L{ISortable}
      - L{IFilterable}
      - L{ICloneable} (deprecated, might be removed in the future)
      - Sends all needed events on content changes.

    @see: L{IContainer}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, itemIds=None):
        self._propertyIds = list()
        self._types = dict()
        self._items = dict()
        self._readOnlyProperties = set()
        self._propertyValueChangeListeners = list()
        self._propertyValueChangeCallbacks = dict()
        self._singlePropertyValueChangeListeners = dict()
        self._defaultPropertyValues = dict()
        self._nextGeneratedItemId = 1
        super(IndexedContainer, self).__init__()
        if itemIds is not None:
            for itemId in itemIds:
                self.internalAddItemAtEnd(itemId, IndexedContainerItem(itemId, self), False)

            self.filterAll()
        return

    def getUnfilteredItem(self, itemId):
        if itemId is not None and itemId in self._items:
            return IndexedContainerItem(itemId, self)
        else:
            return

    def getContainerPropertyIds(self):
        return list(self._propertyIds)

    def getType(self, propertyId):
        """Gets the type of a IProperty stored in the list.

        @param propertyId:
                   the ID of the IProperty.
        @return: Type of the requested IProperty
        """
        return self._types.get(propertyId)

    def getContainerProperty(self, itemId, propertyId):
        if not self.containsId(itemId):
            return None
        else:
            return IndexedContainerProperty(itemId, propertyId, self)

    def addContainerProperty(self, propertyId, typ, defaultValue):
        if propertyId is None or typ is None:
            return False
        if propertyId in self._propertyIds:
            return False
        else:
            self._propertyIds.append(propertyId)
            self._types[propertyId] = typ
            if defaultValue is not None:
                for item in self.getAllItemIds():
                    prop = self.getItem(item).getItemProperty(propertyId)
                    prop.setValue(defaultValue)

                if self._defaultPropertyValues is None:
                    self._defaultPropertyValues = dict()
                self._defaultPropertyValues[propertyId] = defaultValue
            self.fireContainerPropertySetChange()
            return True

    def removeAllItems(self):
        origSize = len(self)
        self.internalRemoveAllItems()
        self._items.clear()
        if origSize != 0:
            self.fireItemSetChange()
        return True

    def addItem(self, itemId=None):
        if itemId is None:
            idd = self.generateId()
            self.addItem(idd)
            return idd
        else:
            item = self.internalAddItemAtEnd(itemId, IndexedContainerItem(itemId, self), False)
            if not self.isFiltered():
                self.fireItemAdded(self.size() - 1, itemId, item)
            elif self.passesFilters(itemId) and not self.containsId(itemId):
                self.getFilteredItemIds().append(itemId)
                self.fireItemAdded(self.size() - 1, itemId, item)
            return item
            return

    def addDefaultValues(self, t):
        """Helper method to add default values for items if available

        @param t: data table of added item
        """
        if self._defaultPropertyValues is not None:
            for key in self._defaultPropertyValues.keys():
                t[key] = self._defaultPropertyValues.get(key)

        return

    def removeItem(self, itemId):
        if itemId is None or itemId not in self._items:
            return False
        del self._items[itemId]
        origSize = self.size()
        position = self.indexOfId(itemId)
        if self.internalRemoveItem(itemId):
            if self.size() != origSize:
                self.fireItemRemoved(position, itemId)
            return True
        return False
        return

    def removeContainerProperty(self, propertyId):
        if propertyId not in self._propertyIds:
            return False
        else:
            self._propertyIds.remove(propertyId)
            if propertyId in self._types:
                del self._types[propertyId]
            if self._defaultPropertyValues is not None:
                if propertyId in self._defaultPropertyValues:
                    del self._defaultPropertyValues[propertyId]
            for item in self.getAllItemIds():
                self._items.get(item).remove(propertyId)

            self.fireContainerPropertySetChange()
            return True

    def addItemAfter(self, previousItemId, newItemId=None):
        if newItemId is None:
            idd = self.generateId()
            if self.addItemAfter(previousItemId, idd) is not None:
                return idd
            return
        else:
            return self.internalAddItemAfter(previousItemId, newItemId, IndexedContainerItem(newItemId, self), True)
        return

    def addItemAt(self, index, newItemId=None):
        if newItemId is None:
            idd = self.generateId()
            self.addItemAt(index, idd)
            return idd
        else:
            return self.internalAddItemAt(index, newItemId, IndexedContainerItem(newItemId, self), True)
            return

    def generateId(self):
        """Generates an unique identifier for use as an item id. Guarantees
        that the generated id is not currently used as an id.
        """
        while True:
            idd = int(self._nextGeneratedItemId)
            self._nextGeneratedItemId += 1
            if idd not in self._items:
                break

        return idd

    def registerNewItem(self, index, newItemId, item):
        t = dict()
        self._items[newItemId] = t
        self.addDefaultValues(t)

    def addListener(self, listener, iface=None):
        if isinstance(listener, container.IPropertySetChangeListener) and (iface is None or issubclass(iface, container.IPropertySetChangeListener)):
            pass
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)):
            self._propertyValueChangeListeners.append(listener)
        super(IndexedContainer, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, container.IPropertySetChangeEvent):
            super(IndexedContainer, self).addCallback(callback, eventType, *args)
        elif issubclass(eventType, prop.ValueChangeEvent):
            self._propertyValueChangeCallbacks[callback] = args
        else:
            super(IndexedContainer, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, container.IPropertySetChangeListener):
            if iface is None or issubclass(iface, container.IPropertySetChangeListener):
                pass
            if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)) and listener in self._propertyValueChangeListeners:
                self._propertyValueChangeListeners.remove(listener)
        super(IndexedContainer, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, container.IPropertySetChangeEvent):
            super(IndexedContainer, self).removecallback(callback, eventType)
        elif issubclass(eventType, prop.ValueChangeEvent):
            if callback in self._propertyValueChangeCallbacks:
                del self._propertyValueChangeCallbacks[callback]
        else:
            super(IndexedContainer, self).removeCallback(callback, eventType)
        return

    def firePropertyValueChange(self, source):
        """Sends a IProperty value change event to all interested listeners.

        @param source:
                   the IndexedContainerProperty object.
        """
        event = PropertyValueChangeEvent(source)
        for listener in self._propertyValueChangeListeners:
            listener.valueChange(event)

        for callback, args in self._propertyValueChangeCallbacks.iteritems():
            callback(event, *args)

        propertySetToListenerListMap = self._singlePropertyValueChangeListeners.get(source._propertyId)
        if propertySetToListenerListMap is not None:
            listenerList = propertySetToListenerListMap.get(source._itemId)
            if listenerList is not None:
                event = PropertyValueChangeEvent(source)
                for l in listenerList:
                    l.valueChange(event)

        return

    def getListeners(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return list(self._propertyValueChangeListeners)
        return super(IndexedContainer, self).getListeners(eventType)

    def getCallbacks(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return dict(self._propertyValueChangeCallbacks)
        return super(IndexedContainer, self).getCallbacks(eventType)

    def fireItemAdded(self, position, itemId, item):
        if position >= 0:
            event = ItemSetChangeEvent(self, position)
            AbstractContainer.fireItemSetChange(self, event)

    def fireItemSetChange(self, event=None):
        if event is None:
            event = ItemSetChangeEvent(self, -1)
            super(IndexedContainer, self).fireItemSetChange(event)
        else:
            super(IndexedContainer, self).fireItemSetChange(event)
        return

    def addSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Adds new single IProperty change listener.

        @param propertyId:
                   the ID of the IProperty to add.
        @param itemId:
                   the ID of the IItem .
        @param listener:
                   the listener to be added.
        """
        if listener is not None:
            if self._singlePropertyValueChangeListeners is None:
                self._singlePropertyValueChangeListeners = dict()
            propertySetToListenerListMap = self._singlePropertyValueChangeListeners.get(propertyId)
            if propertySetToListenerListMap is None:
                propertySetToListenerListMap = dict()
                self._singlePropertyValueChangeListeners[propertyId] = propertySetToListenerListMap
            listenerList = propertySetToListenerListMap.get(itemId)
            if listenerList is None:
                listenerList = list()
                propertySetToListenerListMap[itemId] = listenerList
            listenerList.append(listener)
        return

    def removeSinglePropertyChangeListener(self, propertyId, itemId, listener):
        """Removes a previously registered single IProperty change listener.

        @param propertyId:
                   the ID of the IProperty to remove.
        @param itemId:
                   the ID of the IItem.
        @param listener:
                   the listener to be removed.
        """
        if listener is not None and self._singlePropertyValueChangeListeners is not None:
            propertySetToListenerListMap = self._singlePropertyValueChangeListeners.get(propertyId)
            if propertySetToListenerListMap is not None:
                listenerList = propertySetToListenerListMap.get(itemId)
                if listenerList is not None and listener in listenerList:
                    listenerList.remove(listener)
                    if len(listenerList) == 0:
                        if itemId in propertySetToListenerListMap:
                            del propertySetToListenerListMap[itemId]
                if len(propertySetToListenerListMap) == 0:
                    if propertyId in self._singlePropertyValueChangeListeners:
                        del self._singlePropertyValueChangeListeners[propertyId]
            if len(self._singlePropertyValueChangeListeners) == 0:
                self._singlePropertyValueChangeListeners = None
        return

    def sort(self, propertyId, ascending):
        self.sortContainer(propertyId, ascending)

    def getSortableContainerPropertyIds(self):
        return self.getSortablePropertyIds()

    def getItemSorter(self):
        return super(IndexedContainer, self).getItemSorter()

    def setItemSorter(self, itemSorter):
        super(IndexedContainer, self).setItemSorter(itemSorter)

    def clone(self):
        """Supports cloning of the IndexedContainer cleanly.

        @raise CloneNotSupportedException:
                    if an object cannot be cloned. .

        @deprecated: cloning support might be removed from IndexedContainer
                    in the future
        """
        nc = IndexedContainer()
        if self.getAllItemIds() is not None:
            nc.setAllItemIds(self.getAllItemIds().clone())
        else:
            nc.setAllItemIds(None)
        if self.getItemSetChangeListeners() is not None:
            nc.setItemSetChangeListeners(list(self.getItemSetChangeListeners()))
        else:
            nc.setItemSetChangeListeners(None)
        if self._propertyIds is not None:
            nc._propertyIds = self._propertyIds.clone()
        else:
            nc._propertyIds = None
        if self.getPropertySetChangeListeners() is not None:
            nc.setPropertySetChangeListeners(list(self.getPropertySetChangeListeners()))
        else:
            nc.setPropertySetChangeListeners(None)
        if self._propertyValueChangeListeners is not None:
            nc.propertyValueChangeListeners = self._propertyValueChangeListeners.clone()
        else:
            nc.propertyValueChangeListeners = None
        if self._readOnlyProperties is not None:
            nc.readOnlyProperties = self._readOnlyProperties.clone()
        else:
            nc.readOnlyProperties = None
        if self._singlePropertyValueChangeListeners is not None:
            nc.singlePropertyValueChangeListeners = self._singlePropertyValueChangeListeners.clone()
        else:
            nc.singlePropertyValueChangeListeners = None
        if self._types is not None:
            nc.types = self._types.clone()
        else:
            nc.types = None
        nc.setFilters(self.getFilters().clone())
        if self.getFilteredItemIds() is None:
            nc.setFilteredItemIds(None)
        else:
            nc.setFilteredItemIds(self.getFilteredItemIds().clone())
        if self._items is None:
            nc.items = None
        else:
            nc.items = dict()
            for idd in self._items.keys():
                it = self._items.get(idd)
                nc.items[idd] = it.clone()

        return nc

    def addContainerFilter(self, *args):
        nargs = len(args)
        if nargs == 1:
            fltr, = args
            self.addFilter(fltr)
        elif nargs == 4:
            propertyId, filterString, ignoreCase, onlyMatchPrefix = args
            try:
                self.addFilter(SimpleStringFilter(propertyId, filterString, ignoreCase, onlyMatchPrefix))
            except UnsupportedFilterException:
                pass

        else:
            raise ValueError, 'invalid number of elements'

    def removeAllContainerFilters(self):
        self.removeAllFilters()

    def removeContainerFilters(self, propertyId):
        self.removeFilters(propertyId)

    def removeContainerFilter(self, fltr):
        self.removeFilter(fltr)


class IndexedContainerItem(IItem):

    def __init__(self, itemId, container):
        """Constructs a new ListItem instance and connects it to a host
        container.

        @param itemId: the IItem ID of the new IItem.
        """
        if itemId is None:
            raise ValueError
        self._itemId = itemId
        self._container = container
        return

    def getItemProperty(self, idd):
        return IndexedContainerProperty(self._itemId, idd, self._container)

    def getItemPropertyIds(self):
        return list(self._container._propertyIds)

    def __str__(self):
        """Gets the string representation of the contents of the IItem. The
        format of the string is a space separated catenation of the string
        representations of the Properties contained by the IItem.

        @return: string representation of the IItem contents
        """
        retValue = ''
        for i, propertyId in enumerate(self._container._propertyIds):
            retValue += str(self.getItemProperty(propertyId))
            if i < len(self._container._propertyIds) - 1:
                retValue += ' '

        return retValue

    def __hash__(self):
        """Calculates a integer hash-code for the IItem that's unique inside
        the list. Two Items inside the same list have always different
        hash-codes, though Items in different lists may have identical
        hash-codes.

        @return: A locally unique hash-code as integer
        """
        return hash(self._itemId)

    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two Items
        got from a list container with the same ID are equal.

        @param obj:
                   an object to compare with this object
        @return: C{True} if the given object is the same as this
                object, C{False} if not
        """
        if obj is None or obj.__class__ != IndexedContainerItem:
            return False
        li = obj
        return self.getHost() == li.getHost() and self._itemId == li._itemId

    def getHost(self):
        return self._container

    def addItemProperty(self, idd, prop):
        """IndexedContainerItem does not support adding new properties. Add
        properties at container level. See
        L{IndexedContainer.addContainerProperty}

        @see: L{IItem.addProperty}
        """
        raise NotImplementedError, 'Indexed container item ' + 'does not support adding new properties'

    def removeItemProperty(self, idd):
        """Indexed container does not support removing properties. Remove
        properties at container level. See
        L{IndexedContainer.removeContainerProperty}

        @see: IItem.removeProperty
        """
        raise NotImplementedError, 'Indexed container item does not support property removal'


class IndexedContainerProperty(prop.IProperty, prop.IValueChangeNotifier):
    """A class implementing the L{IProperty} interface to be contained in
    the L{IndexedContainerItem} contained in the L{IndexedContainer}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, itemId, propertyId, container):
        """Constructs a new L{IndexedContainerProperty} object.

        @param itemId:
                   the ID of the IItem to connect the new IProperty to.
        @param propertyId:
                   the IProperty ID of the new IProperty.
        @param container:
                   the list that contains the IItem to contain the new
                   IProperty.
        """
        if itemId is None or propertyId is None:
            raise ValueError, 'IContainer item or property ids can not be null'
        self._propertyId = propertyId
        self._itemId = itemId
        self._container = container
        return

    def getType(self):
        return self._container._types.get(self._propertyId)

    def getValue(self):
        return self._container._items.get(self._itemId).get(self._propertyId)

    def isReadOnly(self):
        return self in self._container._readOnlyProperties

    def setReadOnly(self, newStatus):
        if newStatus:
            self._container._readOnlyProperties.add(self)
        else:
            self._container._readOnlyProperties.remove(self)

    def setValue(self, newValue):
        propertySet = self._container._items.get(self._itemId)
        if newValue is None:
            if self._propertyId in propertySet:
                del propertySet[self._propertyId]
        elif issubclass(newValue.__class__, self.getType()):
            propertySet[self._propertyId] = newValue
        else:
            try:
                constr = self.getType().__init__
                propertySet[self._propertyId] = constr(*[str(newValue)])
            except Exception:
                raise prop.ConversionException, "Conversion for value '" + newValue + "' of class " + fullname(newValue) + ' to ' + self.getType().__name__ + ' failed'

        if self._container.isPropertyFiltered(self._propertyId):
            self._container.filterAll()
        self._container.firePropertyValueChange(self)
        return

    def __str__(self):
        """Returns the value of the IProperty in human readable textual format.
        The return value should be assignable to the C{setValue} method if the
        IProperty is not in read-only mode.

        @return: String representation of the value stored in the IProperty
        """
        value = self.getValue()
        if value is None:
            return ''
        else:
            return str(value)

    def __hash__(self):
        """Calculates a integer hash-code for the IProperty that's unique inside
        the IItem containing the IProperty. Two different Properties inside the
        same IItem contained in the same list always have different
        hash-codes, though Properties in different Items may have identical
        hash-codes.

        @return: A locally unique hash-code as integer
        """
        return hash(self._itemId) ^ hash(self._propertyId)

    def __eq__(self, obj):
        """Tests if the given object is the same as the this object. Two
        Properties got from an IItem with the same ID are equal.

        @param obj:
                   an object to compare with this object
        @return: C{True} if the given object is the same as this
                object, C{False} if not
        """
        if obj is None or obj.__class__ != IndexedContainerProperty:
            return False
        lp = obj
        return lp.getHost() == self.getHost() and lp._propertyId == self._propertyId and lp._itemId == self._itemId

    def addListener(self, listener, iface=None):
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or iface == prop.IValueChangeListener):
            self._container.addSinglePropertyChangeListener(self._propertyId, self._itemId, listener)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if eventType == prop.ValueChangeEvent:
            self._container.addSinglePropertyChangeListener(self._propertyId, self._itemId, (callback, args))
        else:
            super(IndexedContainerProperty, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or iface == prop.IValueChangeListener):
            self._container.removeSinglePropertyChangeListener(self._propertyId, self._itemId, listener)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if eventType == prop.ValueChangeEvent:
            self._container.removeSinglePropertyChangeListener(self._propertyId, self._itemId, callback)
        else:
            super(IndexedContainer, self).removeCallback(callback, eventType)
        return

    def getHost(self):
        return self._container


class ItemSetChangeEvent(BaseItemSetChangeEvent):
    """An C{Event} object specifying the list whose IItem set has changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, source, addedItemIndex):
        super(ItemSetChangeEvent, self).__init__(source)
        self._addedItemIndex = addedItemIndex

    def getAddedItemIndex(self):
        """Iff one item is added, gives its index.

        @return: -1 if either multiple items are changed or some other change
                than add is done.
        """
        return self._addedItemIndex


class PropertyValueChangeEvent(EventObject, prop.ValueChangeEvent):
    """An C{Event} object specifying the IProperty in a list whose
    value has changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, source):
        super(PropertyValueChangeEvent, self).__init__(source)

    def getProperty(self):
        return self.getSource()