# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/CssLayoutsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Panel, Label, CssLayout

class CssLayoutsExample(VerticalLayout):

    def __init__(self):
        super(CssLayoutsExample, self).__init__()
        self.setMargin(True)
        panel = Panel('Panel')
        panel.setStyleName('floatedpanel')
        panel.setWidth('30%')
        panel.setHeight('370px')
        panel.addComponent(Label('This panel is 30% wide ' + 'and 370px high (defined on the server side) ' + 'and floated right (with custom css). ' + 'Try resizing the browser window to see ' + 'how the black boxes (floated left) ' + 'behave. Every third of them has colored text ' + 'to demonstrate the dynamic css injection.'))
        bottomCenter = Label("I'm a 3 inches wide footer at the bottom of the layout")
        bottomCenter.setSizeUndefined()
        bottomCenter.setStyleName('footer')
        cssLayout = MyCssLayout()
        cssLayout.setWidth('100%')
        cssLayout.addComponent(panel)
        for _ in range(15):
            cssLayout.addComponent(Brick())

        cssLayout.addComponent(bottomCenter)
        self.addComponent(cssLayout)


class MyCssLayout(CssLayout):

    def __init__(self):
        super(MyCssLayout, self).__init__()
        self._brickCounter = 0

    def getCss(self, c):
        if isinstance(c, Brick):
            self._brickCounter += 1
            if self._brickCounter % 3 == 0:
                return 'color: #ff6611; font-style: italic;'
        return


class Brick(Label):
    """A simple label containing text "Brick" and themed black square."""

    def __init__(self):
        super(Brick, self).__init__('Brick')
        self.setSizeUndefined()
        self.setStyleName('brick')