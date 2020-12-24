# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/expand_layout.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a layout that will give one of it's components as much space as
possible, while still showing the other components in the layout."""
from warnings import warn
from muntjac.ui.ordered_layout import OrderedLayout

class ExpandLayout(OrderedLayout):
    """A layout that will give one of it's components as much space as
    possible, while still showing the other components in the layout. The
    other components will in effect be given a fixed sized space, while the
    space given to the expanded component will grow/shrink to fill the rest
    of the space available - for instance when re-sizing the window.

    Note that this layout is 100% in both directions by default
    (L{setSizeFull}). Remember to set the units if you want to
    specify a fixed size. If the layout fails to show up, check that the
    parent layout is actually giving some space.

    @deprecated: Deprecated in favor of the new OrderedLayout
    """

    def __init__(self, orientation=None):
        warn('use OrderedLayout', DeprecationWarning)
        self._expanded = None
        if orientation is None:
            self.ORIENTATION_VERTICAL
        super(ExpandLayout, self).__init__(orientation)
        self.setSizeFull()
        return

    def expand(self, c):
        """@param c: Component which container will be maximized
        """
        if self._expanded is not None:
            try:
                self.setExpandRatio(self._expanded, 0.0)
            except ValueError:
                pass

        self._expanded = c
        if self._expanded is not None:
            self.setExpandRatio(self._expanded, 1.0)
        self.requestRepaint()
        return

    def addComponent(self, c, index=None):
        if index is None:
            super(ExpandLayout, self).addComponent(c)
        else:
            super(ExpandLayout, self).addComponent(c, index)
        if self._expanded is None:
            self.expand(c)
        return

    def addComponentAsFirst(self, c):
        super(ExpandLayout, self).addComponentAsFirst(c)
        if self._expanded is None:
            self.expand(c)
        return

    def removeComponent(self, c):
        super(ExpandLayout, self).removeComponent(c)
        if c == self._expanded:
            try:
                self.expand(self.getComponentIterator().next())
            except StopIteration:
                self.expand(None)

        return

    def replaceComponent(self, oldComponent, newComponent):
        super(ExpandLayout, self).replaceComponent(oldComponent, newComponent)
        if oldComponent == self._expanded:
            self.expand(newComponent)