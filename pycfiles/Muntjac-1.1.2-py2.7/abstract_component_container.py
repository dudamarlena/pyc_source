# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/abstract_component_container.py
# Compiled at: 2013-04-04 15:36:35
"""Defines the default implementation for the methods in IComponentContainer.
"""
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component_container import ComponentAttachEvent, IComponentAttachListener, IComponentContainer, ComponentDetachEvent, IComponentDetachListener
_COMPONENT_ATTACHED_METHOD = getattr(IComponentAttachListener, 'componentAttachedToContainer')
_COMPONENT_DETACHED_METHOD = getattr(IComponentDetachListener, 'componentDetachedFromContainer')

class AbstractComponentContainer(AbstractComponent, IComponentContainer):
    """Extension to L{AbstractComponent} that defines the default
    implementation for the methods in L{IComponentContainer}. Basic
    UI components that need to contain other components inherit this class
    to easily qualify as a component container.

    @author: Vaadin Ltd.
    @version: 1.1.2
    """

    def __init__(self):
        """Constructs a new component container."""
        super(AbstractComponentContainer, self).__init__()

    def removeAllComponents(self):
        """Removes all components from the container. This should probably
        be re-implemented in extending classes for a more powerful
        implementation.
        """
        l = list()
        for c in self.getComponentIterator():
            l.append(c)

        for c in l:
            self.removeComponent(c)

    def moveComponentsFrom(self, source):
        components = list()
        for c in self.getComponentIterator():
            components.append(c)

        for c in components:
            source.removeComponent(c)
            self.addComponent(c)

    def attach(self):
        """Notifies all contained components that the container is attached
        to a window.

        @see: L{IComponent.attach}
        """
        super(AbstractComponentContainer, self).attach()
        for c in self.getComponentIterator():
            c.attach()

    def detach(self):
        """Notifies all contained components that the container is detached
        from a window.

        @see: L{IComponent.detach}
        """
        super(AbstractComponentContainer, self).detach()
        for c in self.getComponentIterator():
            c.detach()

    def addListener(self, listener, iface=None):
        if isinstance(listener, IComponentAttachListener) and (iface is None or issubclass(iface, IComponentAttachListener)):
            self.registerListener(ComponentAttachEvent, listener, _COMPONENT_ATTACHED_METHOD)
        if isinstance(listener, IComponentDetachListener) and (iface is None or issubclass(iface, IComponentDetachListener)):
            self.registerListener(ComponentDetachEvent, listener, _COMPONENT_DETACHED_METHOD)
        super(AbstractComponentContainer, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ComponentAttachEvent):
            self.registerCallback(ComponentAttachEvent, callback, None, *args)
        elif issubclass(eventType, ComponentDetachEvent):
            self.registerCallback(ComponentDetachEvent, callback, None, *args)
        else:
            super(AbstractComponentContainer, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IComponentAttachListener) and (iface is None or issubclass(iface, IComponentAttachListener)):
            self.withdrawListener(ComponentAttachEvent, listener, _COMPONENT_ATTACHED_METHOD)
        if isinstance(listener, IComponentDetachListener) and (iface is None or issubclass(iface, IComponentDetachListener)):
            self.withdrawListener(ComponentDetachEvent, listener, _COMPONENT_DETACHED_METHOD)
        super(AbstractComponentContainer, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ComponentAttachEvent):
            self.withdrawCallback(ComponentAttachEvent, callback)
        elif issubclass(eventType, ComponentDetachEvent):
            self.withdrawCallback(ComponentDetachEvent, callback)
        else:
            super(AbstractComponentContainer, self).removeCallback(callback, eventType)
        return

    def fireComponentAttachEvent(self, component):
        """Fires the component attached event. This should be called by
        the addComponent methods after the component have been added to
        this container.

        @param component:
                   the component that has been added to this container.
        """
        event = ComponentAttachEvent(self, component)
        self.fireEvent(event)

    def fireComponentDetachEvent(self, component):
        """Fires the component detached event. This should be called by
        the removeComponent methods after the component have been removed
        from this container.

        @param component:
                   the component that has been removed from this container.
        """
        event = ComponentDetachEvent(self, component)
        self.fireEvent(event)

    def addComponent(self, c):
        """This only implements the events and component parent calls. The
        extending classes must implement component list maintenance and call
        this method after component list maintenance.

        @see: L{IComponentContainer.addComponent}
        """
        if isinstance(c, IComponentContainer):
            parent = self
            while parent is not None:
                parent = parent.getParent()
                if parent == c:
                    msg = "Component cannot be added inside it's own content"
                    raise ValueError, msg

        if c.getParent() is not None:
            oldParent = c.getParent()
            oldParent.removeComponent(c)
        c.setParent(self)
        self.fireComponentAttachEvent(c)
        return

    def removeComponent(self, c):
        """This only implements the events and component parent calls. The
        extending classes must implement component list maintenance and call
        this method before component list maintenance.

        @see: L{IComponentContainer.removeComponent}
        """
        if c.getParent() == self:
            c.setParent(None)
            self.fireComponentDetachEvent(c)
        return

    def setEnabled(self, enabled):
        super(AbstractComponentContainer, self).setEnabled(enabled)
        if self.getParent() is not None and not self.getParent().isEnabled():
            return
        else:
            self.requestRepaintAll()
            return

    def setWidth(self, width, unit=None):
        if unit is not None:
            from muntjac.terminal.gwt.server.component_size_validator import ComponentSizeValidator
            dirtyChildren = None
            childrenMayBecomeUndefined = False
            if self.getWidth() == self.SIZE_UNDEFINED and width != self.SIZE_UNDEFINED:
                dirtyChildren = self.getInvalidSizedChildren(False)
            elif width == self.SIZE_UNDEFINED and self.getWidth() != self.SIZE_UNDEFINED or unit == self.UNITS_PERCENTAGE and self.getWidthUnits() != self.UNITS_PERCENTAGE and not ComponentSizeValidator.parentCanDefineWidth(self):
                childrenMayBecomeUndefined = True
                dirtyChildren = self.getInvalidSizedChildren(False)
            super(AbstractComponentContainer, self).setWidth(width, unit)
            self.repaintChangedChildTrees(dirtyChildren, childrenMayBecomeUndefined, False)
        else:
            super(AbstractComponentContainer, self).setWidth(width)
        return

    def repaintChangedChildTrees(self, invalidChildren, childrenMayBecomeUndefined, vertical):
        if childrenMayBecomeUndefined:
            previouslyInvalidComponents = invalidChildren
            invalidChildren = self.getInvalidSizedChildren(vertical)
            if previouslyInvalidComponents is not None and invalidChildren is not None:
                for component in invalidChildren:
                    if component in previouslyInvalidComponents:
                        previouslyInvalidComponents.remove(component)

        elif invalidChildren is not None:
            stillInvalidChildren = self.getInvalidSizedChildren(vertical)
            if stillInvalidChildren is not None:
                for component in stillInvalidChildren:
                    invalidChildren.remove(component)

        if invalidChildren is not None:
            self.repaintChildTrees(invalidChildren)
        return

    def getInvalidSizedChildren(self, vertical):
        components = None
        from muntjac.ui.panel import Panel
        from muntjac.terminal.gwt.server.component_size_validator import ComponentSizeValidator
        if isinstance(self, Panel):
            p = self
            content = p.getContent()
            if vertical:
                valid = ComponentSizeValidator.checkHeights(content)
            else:
                valid = ComponentSizeValidator.checkWidths(content)
            if not valid:
                components = set()
                components.add(content)
        else:
            for component in self.getComponentIterator():
                if vertical:
                    valid = ComponentSizeValidator.checkHeights(component)
                else:
                    valid = ComponentSizeValidator.checkWidths(component)
                if not valid:
                    if components is None:
                        components = set()
                    components.add(component)

        return components

    def repaintChildTrees(self, dirtyChildren):
        for c in dirtyChildren:
            if isinstance(c, IComponentContainer):
                c.requestRepaintAll()
            else:
                c.requestRepaint()

    def setHeight(self, height, unit=None):
        if unit is not None:
            from muntjac.terminal.gwt.server.component_size_validator import ComponentSizeValidator
            dirtyChildren = None
            childrenMayBecomeUndefined = False
            if self.getHeight() == self.SIZE_UNDEFINED and height != self.SIZE_UNDEFINED:
                dirtyChildren = self.getInvalidSizedChildren(True)
            elif height == self.SIZE_UNDEFINED and self.getHeight() != self.SIZE_UNDEFINED or unit == self.UNITS_PERCENTAGE and self.getHeightUnits() != self.UNITS_PERCENTAGE and not ComponentSizeValidator.parentCanDefineHeight(self):
                childrenMayBecomeUndefined = True
                dirtyChildren = self.getInvalidSizedChildren(True)
            super(AbstractComponentContainer, self).setHeight(height, unit)
            self.repaintChangedChildTrees(dirtyChildren, childrenMayBecomeUndefined, True)
        else:
            super(AbstractComponentContainer, self).setHeight(height)
        return

    def requestRepaintAll(self):
        self.requestRepaint()
        from muntjac.ui.form import Form
        from muntjac.ui.table import Table
        for c in self.getComponentIterator():
            if isinstance(c, Form):
                c.requestRepaint()
                c.getLayout().requestRepaintAll()
            elif isinstance(c, Table):
                c.requestRepaintAll()
            elif isinstance(c, IComponentContainer):
                c.requestRepaintAll()
            else:
                c.requestRepaint()