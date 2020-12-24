# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/css_layout.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a layout component that can be used in browser environment
only."""
from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.event.layout_events import ILayoutClickNotifier, LayoutClickEvent, ILayoutClickListener

class CssLayout(AbstractLayout, ILayoutClickNotifier):
    """CssLayout is a layout component that can be used in browser environment
    only. It simply renders components and their captions into a same div
    element. Component layout can then be adjusted with css.

    In comparison to L{HorizontalLayout} and L{VerticalLayout}

      - rather similar server side api
      - no spacing, alignment or expand ratios
      - much simpler DOM that can be styled by skilled web developer
      - no abstraction of browser differences (developer must ensure that
        the result works properly on each browser)
      - different kind of handling for relative sizes (that are set from
        server side) (*)
      - noticeably faster rendering time in some situations as we rely more
        on the browser's rendering engine.

    With L{CustomLayout} one can often achieve similar results (good
    looking layouts with web technologies), but with CustomLayout developer
    needs to work with fixed templates.

    By extending CssLayout one can also inject some css rules straight to
    child components using L{getCss}.

    (*) Relative sizes (set from server side) are treated bit differently than
    in other layouts in Muntjac. In cssLayout the size is calculated relatively
    to CSS layouts content area which is pretty much as in html and css. In
    other layouts the size of component is calculated relatively to the "slot"
    given by layout.

    Also note that client side framework in Muntjac modifies inline style
    properties width and height. This happens on each update to component. If
    one wants to set component sizes with CSS, component must have undefined
    size on server side (which is not the default for all components) and the
    size must be defined with class styles - not by directly injecting width
    and height.
    """
    CLIENT_WIDGET = None
    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self):
        super(CssLayout, self).__init__()
        self.components = list()

    def addComponent(self, c, index=None):
        """Add a component into this container. The component is added to
        the right/under the previous component or into indexed position in
        this container.

        @param c:
                   the component to be added.
        @param index:
                   the Index of the component position. The components
                   currently in and after the position are shifted forwards.
        """
        if index is None:
            self.components.append(c)
            try:
                super(CssLayout, self).addComponent(c)
                self.requestRepaint()
            except ValueError as e:
                self.components.remove(c)
                raise e

        else:
            self.components.insert(index, c)
            try:
                super(CssLayout, self).addComponent(c)
                self.requestRepaint()
            except ValueError as e:
                self.components.remove(c)
                raise e

        return

    def addComponentAsFirst(self, c):
        """Adds a component into this container. The component is added to
        the left or on top of the other components.

        @param c:
                   the component to be added.
        """
        self.components.insert(0, c)
        try:
            super(CssLayout, self).addComponent(c)
            self.requestRepaint()
        except ValueError as e:
            self.components.remove(c)
            raise e

    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: the component to be removed.
        """
        if c in self.components:
            self.components.remove(c)
        super(CssLayout, self).removeComponent(c)
        self.requestRepaint()

    def getComponentIterator(self):
        """Gets the component container iterator for going trough all the
        components in the container.

        @return: the iterator of the components inside the container.
        """
        return iter(self.components)

    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the
        iterator returned by L{getComponentIterator}.

        @return: the number of contained components
        """
        return len(self.components)

    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(CssLayout, self).paintContent(target)
        componentCss = None
        for c in self.components:
            c.paint(target)
            componentCssString = self.getCss(c)
            if componentCssString is not None:
                if componentCss is None:
                    componentCss = dict()
                componentCss[c] = componentCssString

        if componentCss is not None:
            target.addAttribute('css', componentCss)
        return

    def getCss(self, c):
        """Returns styles to be applied to given component. Override this
        method to inject custom style rules to components.

        Note that styles are injected over previous styles before actual
        child rendering. Previous styles are not cleared, but overridden.

        Note that one most often achieves better code style, by separating
        styling to theme (with custom theme and L{addStyleName}.
        With own custom styles it is also very easy to break browser
        compatibility.

        @param c: the component
        @return: css rules to be applied to component
        """
        return

    def replaceComponent(self, oldComponent, newComponent):
        oldLocation = -1
        newLocation = -1
        location = 0
        for component in self.components:
            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location
            location += 1

        if oldLocation == -1:
            self.addComponent(newComponent)
        elif newLocation == -1:
            self.removeComponent(oldComponent)
            self.addComponent(newComponent, oldLocation)
        else:
            if oldLocation > newLocation:
                self.components.remove(oldComponent)
                self.components.append(newLocation, oldComponent)
                self.components.remove(newComponent)
                self.components.append(oldLocation, newComponent)
            else:
                self.components.remove(newComponent)
                self.components.append(oldLocation, newComponent)
                self.components.remove(oldComponent)
                self.components.append(newLocation, oldComponent)
            self.requestRepaint()

    def addListener(self, listener, iface=None):
        if isinstance(listener, ILayoutClickListener) and (iface is None or issubclass(iface, ILayoutClickListener)):
            self.registerListener(self._CLICK_EVENT, LayoutClickEvent, listener, ILayoutClickListener.clickMethod)
        super(CssLayout, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, LayoutClickEvent):
            self.registerCallback(LayoutClickEvent, callback, None, *args)
        else:
            super(CssLayout, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, ILayoutClickListener) and (iface is None or issubclass(iface, ILayoutClickListener)):
            self.withdrawListener(self._CLICK_EVENT, LayoutClickEvent, listener)
        super(CssLayout, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, LayoutClickEvent):
            self.withdrawCallback(LayoutClickEvent, callback, self._CLICK_EVENT)
        else:
            super(CssLayout, self).removeCallback(callback, eventType)
        return