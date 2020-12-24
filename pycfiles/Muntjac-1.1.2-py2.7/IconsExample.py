# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/IconsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Button, Label, Panel, Link
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource

class IconsExample(VerticalLayout):

    def __init__(self):
        super(IconsExample, self).__init__()
        self.setSpacing(True)
        button = Button('Save')
        button.setIcon(ThemeResource('../sampler/icons/action_save.gif'))
        self.addComponent(button)
        l = Label('Icons are very handy')
        l.setCaption('Comment')
        l.setIcon(ThemeResource('../sampler/icons/comment_yellow.gif'))
        self.addComponent(l)
        p = Panel('Handy links')
        p.setIcon(ThemeResource('../sampler/icons/icon_info.gif'))
        self.addComponent(p)
        lnk = Link('http://vaadin.com', ExternalResource('http://www.vaadin.com'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://vaadin.com/learn', ExternalResource('http://www.vaadin.com/learn'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://dev.vaadin.com/', ExternalResource('http://dev.vaadin.com/'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)
        lnk = Link('http://vaadin.com/forum', ExternalResource('http://vaadin.com/forum'))
        lnk.setIcon(ThemeResource('../sampler/icons/icon_world.gif'))
        p.addComponent(lnk)