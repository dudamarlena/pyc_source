# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/GridLayoutBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, GridLayout, Button, Alignment
from muntjac.terminal.sizeable import ISizeable

class GridLayoutBasicExample(VerticalLayout):

    def __init__(self):
        super(GridLayoutBasicExample, self).__init__()
        grid = GridLayout(3, 3)
        grid.setSpacing(True)
        grid.addStyleName('gridexample')
        grid.setWidth(400, ISizeable.UNITS_PIXELS)
        grid.setHeight(400, ISizeable.UNITS_PIXELS)
        topleft = Button('Top Left')
        grid.addComponent(topleft, 0, 0)
        grid.setComponentAlignment(topleft, Alignment.MIDDLE_CENTER)
        topcenter = Button('Top Center')
        grid.addComponent(topcenter, 1, 0)
        grid.setComponentAlignment(topcenter, Alignment.MIDDLE_CENTER)
        bottomleft = Button('Bottom Left')
        grid.addComponent(bottomleft, 0, 2)
        grid.setComponentAlignment(bottomleft, Alignment.MIDDLE_CENTER)
        bottomcenter = Button('Bottom Center')
        grid.addComponent(bottomcenter, 1, 2)
        grid.setComponentAlignment(bottomcenter, Alignment.MIDDLE_CENTER)
        topright = Button('Extra height')
        grid.addComponent(topright, 2, 0, 2, 2)
        grid.setComponentAlignment(topright, Alignment.MIDDLE_CENTER)
        middleleft = Button('This is a wide cell in GridLayout')
        grid.addComponent(middleleft, 0, 1, 1, 1)
        grid.setComponentAlignment(middleleft, Alignment.MIDDLE_CENTER)
        self.addComponent(grid)
        self.setComponentAlignment(grid, Alignment.MIDDLE_CENTER)