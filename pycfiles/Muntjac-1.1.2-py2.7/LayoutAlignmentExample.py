# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/LayoutAlignmentExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, GridLayout, Button, Alignment
from muntjac.terminal.gwt.client.ui.alignment_info import Bits

class LayoutAlignmentExample(VerticalLayout):

    def __init__(self):
        super(LayoutAlignmentExample, self).__init__()
        grid = GridLayout(1, 9)
        grid.setSpacing(True)
        grid.addStyleName('gridexample')
        grid.setWidth('300px')
        grid.setHeight('500px')
        topleft = Button('Top Left')
        grid.addComponent(topleft)
        grid.setComponentAlignment(topleft, Alignment.TOP_LEFT)
        topcenter = Button('Top Center')
        grid.addComponent(topcenter)
        grid.setComponentAlignment(topcenter, Alignment.TOP_CENTER)
        topright = Button('Top Right')
        grid.addComponent(topright)
        grid.setComponentAlignment(topright, Alignment.TOP_RIGHT)
        middleleft = Button('Middle Left')
        grid.addComponent(middleleft)
        grid.setComponentAlignment(middleleft, Alignment(Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_LEFT))
        middlecenter = Button('Middle Center')
        grid.addComponent(middlecenter)
        grid.setComponentAlignment(middlecenter, Alignment(Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_HORIZONTAL_CENTER))
        middleright = Button('Middle Right')
        grid.addComponent(middleright)
        grid.setComponentAlignment(middleright, Alignment(Bits.ALIGNMENT_VERTICAL_CENTER | Bits.ALIGNMENT_RIGHT))
        bottomleft = Button('Bottom Left')
        grid.addComponent(bottomleft)
        grid.setComponentAlignment(bottomleft, Alignment.BOTTOM_LEFT)
        bottomcenter = Button('Bottom Center')
        grid.addComponent(bottomcenter)
        grid.setComponentAlignment(bottomcenter, Alignment.BOTTOM_CENTER)
        bottomright = Button('Bottom Right')
        grid.addComponent(bottomright)
        grid.setComponentAlignment(bottomright, Alignment.BOTTOM_RIGHT)
        self.addComponent(grid)
        self.setComponentAlignment(grid, Alignment.MIDDLE_CENTER)