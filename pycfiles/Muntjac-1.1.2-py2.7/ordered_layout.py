# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/ordered_layout.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a component container, which shows the subcomponents in the order
of their addition in specified orientation."""
from warnings import warn
from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout

class OrderedLayout(AbstractOrderedLayout):
    """Ordered layout.

    C{OrderedLayout} is a component container, which shows the
    subcomponents in the order of their addition in specified orientation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @deprecated: Replaced by VerticalLayout/HorizontalLayout. For type checking
                 please not that VerticalLayout/HorizontalLayout do not extend
                 OrderedLayout but AbstractOrderedLayout (which also
                 OrderedLayout extends).
    """
    CLIENT_WIDGET = None
    ORIENTATION_VERTICAL = 0
    ORIENTATION_HORIZONTAL = 1

    def __init__(self, orientation=None):
        """Creates a new ordered layout. The order of the layout defaults to
        C{ORIENTATION_VERTICAL}.

        @param orientation: the Orientation of the layout.
        @deprecated: Use VerticalLayout/HorizontalLayout instead.
        """
        warn('use VerticalLayout/HorizontalLayout instead', DeprecationWarning)
        super(OrderedLayout, self).__init__()
        self._orientation = None
        if orientation is None:
            orientation = self.ORIENTATION_VERTICAL
        self._orientation = orientation
        if orientation == self.ORIENTATION_VERTICAL:
            self.setWidth(100, self.UNITS_PERCENTAGE)
        return

    def getOrientation(self):
        """Gets the orientation of the container.

        @return: the Value of property orientation.
        """
        return self._orientation

    def setOrientation(self, orientation, needsRepaint=True):
        """Sets the orientation of this OrderedLayout. This method should only
        be used before initial paint.

        @param orientation:
                   the New value of property orientation.
        @deprecated: Use VerticalLayout/HorizontalLayout or define orientation
                     in constructor instead
        """
        if orientation < self.ORIENTATION_VERTICAL or orientation > self.ORIENTATION_HORIZONTAL:
            raise ValueError()
        self._orientation = orientation
        if needsRepaint:
            self.requestRepaint()

    def paintContent(self, target):
        super(OrderedLayout, self).paintContent(target)
        if self._orientation == self.ORIENTATION_HORIZONTAL:
            target.addAttribute('orientation', 'horizontal')