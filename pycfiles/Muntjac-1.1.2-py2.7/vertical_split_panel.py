# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/vertical_split_panel.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a panel that contains two components and lays them out
vertically."""
from muntjac.ui.abstract_split_panel import AbstractSplitPanel

class VerticalSplitPanel(AbstractSplitPanel):
    """A vertical split panel contains two components and lays them
    vertically. The first component is above the second component::

         +--------------------------+
         |                          |
         |  The first component     |
         |                          |
         +==========================+  <-- splitter
         |                          |
         |  The second component    |
         |                          |
         +--------------------------+
    """
    CLIENT_WIDGET = None

    def __init__(self):
        super(VerticalSplitPanel, self).__init__()
        self.setSizeFull()