# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/vertical_layout.py
# Compiled at: 2013-04-04 15:36:35
from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout

class VerticalLayout(AbstractOrderedLayout):
    """Vertical layout.

    C{VerticalLayout} is a component container, which shows the
    subcomponents in the order of their addition (vertically). A vertical
    layout is by default 100% wide.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None

    def __init__(self):
        super(VerticalLayout, self).__init__()
        self.setWidth('100%')