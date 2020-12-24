# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/link/LinkNoDecorationsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Link
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource

class LinkNoDecorationsExample(VerticalLayout):
    _CAPTION = 'Open Google in new window'
    _TOOLTIP = 'http://www.google.com (opens in new window)'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')

    def __init__(self):
        super(LinkNoDecorationsExample, self).__init__()
        self.setSpacing(True)
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        self.addComponent(l)
        l = Link(self._CAPTION, ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)
        l = Link()
        l.setResource(ExternalResource('http://www.google.com'))
        l.setTargetName('_blank')
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)