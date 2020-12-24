# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/split_panel.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a component container, that can contain two components which are
split by divider element."""
from muntjac.ui.abstract_split_panel import AbstractSplitPanel

class SplitPanel(AbstractSplitPanel):
    """SplitPanel.

    C{SplitPanel} is a component container, that can contain two
    components (possibly containers) which are split by divider element.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @deprecated: Use L{HorizontalSplitPanel} or L{VerticalSplitPanel} instead.
    """
    CLIENT_WIDGET = None
    ORIENTATION_VERTICAL = 0
    ORIENTATION_HORIZONTAL = 1

    def __init__(self, orientation=None):
        """Creates a new split panel. The orientation of the panels is
        C{ORIENTATION_VERTICAL} by default.

        @param orientation:
                   the orientation of the layout.
        """
        super(SplitPanel, self).__init__()
        if orientation is None:
            self._orientation = self.ORIENTATION_VERTICAL
        else:
            self.setOrientation(orientation)
        self.setSizeFull()
        return

    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(SplitPanel, self).paintContent(target)
        if self._orientation == self.ORIENTATION_VERTICAL:
            target.addAttribute('vertical', True)

    def getOrientation(self):
        """Gets the orientation of the split panel.

        @return: the Value of property orientation.
        """
        return self._orientation

    def setOrientation(self, orientation):
        """Sets the orientation of the split panel.

        @param orientation:
                   the New value of property orientation.
        """
        if orientation < self.ORIENTATION_VERTICAL or orientation > self.ORIENTATION_HORIZONTAL:
            raise ValueError
        self._orientation = orientation
        self.requestRepaint()