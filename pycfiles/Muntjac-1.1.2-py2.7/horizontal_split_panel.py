# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/horizontal_split_panel.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a panel that contains two components and lays them out
horizontally."""
from muntjac.ui.abstract_split_panel import AbstractSplitPanel

class HorizontalSplitPanel(AbstractSplitPanel):
    """A horizontal split panel contains two components and lays them
    horizontally. The first component is on the left side::

         +---------------------++----------------------+
         |                     ||                      |
         | The first component || The second component |
         |                     ||                      |
         +---------------------++----------------------+

                               ^
                               |
                         the splitter

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None

    def __init__(self):
        super(HorizontalSplitPanel, self).__init__()
        self.setSizeFull()