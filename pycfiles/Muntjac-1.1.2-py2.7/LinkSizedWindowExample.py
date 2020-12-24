# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/link/LinkSizedWindowExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.external_resource import ExternalResource
from muntjac.ui.link import Link

class LinkSizedWindowExample(VerticalLayout):
    _CAPTION = 'Open Google in small window'
    _TOOLTIP = 'http://www.google.com (opens in small window)'
    _ICON = ThemeResource('../sampler/icons/icon_world.gif')
    _TARGET = ExternalResource('http://www.google.com/m')

    def __init__(self):
        super(LinkSizedWindowExample, self).__init__()
        self.setSpacing(True)
        l = Link(self._CAPTION, self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        self.addComponent(l)
        l = Link(self._CAPTION, self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)
        l = Link()
        l.setResource(self._TARGET)
        l.setTargetName('_blank')
        l.setTargetWidth(300)
        l.setTargetHeight(300)
        l.setTargetBorder(Link.TARGET_BORDER_NONE)
        l.setDescription(self._TOOLTIP)
        l.setIcon(self._ICON)
        self.addComponent(l)