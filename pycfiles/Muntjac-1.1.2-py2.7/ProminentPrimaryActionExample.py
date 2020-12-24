# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/blueprints/ProminentPrimaryActionExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, HorizontalLayout, Button, Alignment
from muntjac.ui.themes import BaseTheme
from muntjac.ui.button import IClickListener

class ProminentPrimaryActionExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(ProminentPrimaryActionExample, self).__init__()
        self.setSpacing(True)
        horiz = HorizontalLayout()
        horiz.setCaption('Save/cancel example:')
        horiz.setSpacing(True)
        horiz.setMargin(True)
        self.addComponent(horiz)
        secondary = Button('Cancel', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        horiz.addComponent(secondary)
        primary = Button('Save', self)
        horiz.addComponent(primary)
        horiz = HorizontalLayout()
        horiz.setCaption('Sign up example:')
        horiz.setSpacing(True)
        horiz.setMargin(True)
        self.addComponent(horiz)
        primary = Button('Sign up', self)
        primary.addStyleName('primary')
        horiz.addComponent(primary)
        secondary = Button('or Sign in', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        horiz.addComponent(secondary)
        horiz.setComponentAlignment(secondary, Alignment.MIDDLE_LEFT)
        vert = VerticalLayout()
        vert.setCaption('Login example:')
        vert.setSizeUndefined()
        vert.setSpacing(True)
        vert.setMargin(True)
        self.addComponent(vert)
        primary = Button('Login', self)
        vert.addComponent(primary)
        vert.setComponentAlignment(primary, Alignment.BOTTOM_RIGHT)
        secondary = Button('Forgot your password?', self)
        secondary.setStyleName(BaseTheme.BUTTON_LINK)
        vert.addComponent(secondary)
        vert.setComponentAlignment(secondary, Alignment.BOTTOM_RIGHT)

    def buttonClick(self, event):
        self.getWindow().showNotification('"' + event.getButton().getCaption() + '" clicked')