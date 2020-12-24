# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/abstract_layout.py
# Compiled at: 2013-04-04 15:36:35
"""Defines the default implementation of the ILayout interface."""
from muntjac.ui.layout import ILayout, IMarginHandler, MarginInfo
from muntjac.ui.abstract_component_container import AbstractComponentContainer
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.event.layout_events import ILayoutClickNotifier, LayoutClickEvent

class AbstractLayout(AbstractComponentContainer, ILayout, IMarginHandler):
    """An abstract class that defines default implementation for the
    L{ILayout} interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.margins = MarginInfo(False)

    def setMargin(self, *args):
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], MarginInfo):
                marginInfo, = args
                self.margins.setMargins(marginInfo)
                self.requestRepaint()
            else:
                enabled, = args
                self.margins.setMargins(enabled)
                self.requestRepaint()
        elif nargs == 4:
            topEnabled, rightEnabled, bottomEnabled, leftEnabled = args
            self.margins.setMargins(topEnabled, rightEnabled, bottomEnabled, leftEnabled)
            self.requestRepaint()
        else:
            raise ValueError, 'invalid number of arguments'

    def getMargin(self):
        return self.margins

    def paintContent(self, target):
        target.addAttribute('margins', int(self.margins.getBitMask()))

    def changeVariables(self, source, variables):
        super(AbstractLayout, self).changeVariables(source, variables)
        if isinstance(self, ILayoutClickNotifier) and self._CLICK_EVENT in variables:
            self.fireClick(variables.get(self._CLICK_EVENT))

    def fireClick(self, parameters):
        """Fire a layout click event.

        Note that this method is only used by the subclasses that
        implement L{LayoutClickNotifier}, and can be overridden
        for custom click event firing.

        @param parameters:
                   The parameters received from the client side
                   implementation
        """
        mouseDetails = MouseEventDetails.deSerialize(parameters.get('mouseDetails'))
        clickedComponent = parameters.get('component')
        childComponent = clickedComponent
        while childComponent is not None and childComponent.getParent() != self:
            childComponent = childComponent.getParent()

        self.fireEvent(LayoutClickEvent(self, mouseDetails, clickedComponent, childComponent))
        return