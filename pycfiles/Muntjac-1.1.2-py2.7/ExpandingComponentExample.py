# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/ExpandingComponentExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, HorizontalLayout, Button

class ExpandingComponentExample(VerticalLayout):

    def __init__(self):
        super(ExpandingComponentExample, self).__init__()
        self.setSpacing(True)
        layout = HorizontalLayout()
        layout.setWidth('100%')
        self.addComponent(layout)
        naturalButton = Button('Natural')
        naturalButton.setDescription("This button does not have an explicit size - instead, its size depends on it's content - a.k.a <i>natural size.</i>")
        layout.addComponent(naturalButton)
        expandedButton = Button('Expanded')
        expandedButton.setWidth('100%')
        expandedButton.setDescription('The width of this button is set to 100% and expanded, and will thus occupy the space left over by the other components.')
        layout.addComponent(expandedButton)
        layout.setExpandRatio(expandedButton, 1.0)
        sizedButton = Button('Explicit')
        sizedButton.setWidth('150px')
        sizedButton.setDescription('This button is explicitly set to be 150 pixels wide.')
        layout.addComponent(sizedButton)
        layout = HorizontalLayout()
        layout.setWidth('100%')
        self.addComponent(layout)
        naturalButton = Button('Natural')
        naturalButton.setDescription("This button does not have an explicit size - instead, its size depends on it's content - a.k.a <i>natural size.</i>")
        layout.addComponent(naturalButton)
        expandedButton1 = Button('Ratio 1.0')
        expandedButton1.setWidth('100%')
        expandedButton1.setDescription('The width of this button is set to 100% and expanded with a ratio of 1.0, and will in this example occupy 1:3 of the leftover space.')
        layout.addComponent(expandedButton1)
        layout.setExpandRatio(expandedButton1, 1.0)
        expandedButton2 = Button('Ratio 2.0')
        expandedButton2.setWidth('100%')
        expandedButton2.setDescription('The width of this button is set to 100% and expanded with a ratio of 2.0, and will in this example occupy 2:3 of the leftover space.')
        layout.addComponent(expandedButton2)
        layout.setExpandRatio(expandedButton2, 2.0)