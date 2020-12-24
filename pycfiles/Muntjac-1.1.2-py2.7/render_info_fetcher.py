# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/csstools/render_info_fetcher.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.window import Window
from muntjac.addon.csstools.client.v_render_info_fetcher import VRenderInfoFetcher
from muntjac.addon.csstools.render_info import RenderInfo

class RenderInfoFetcher(Window):
    CLIENT_WIDGET = None
    TYPE_MAPPING = 'org.vaadin.csstools.RenderInfoFetcher'

    def __init__(self, c, cb, *props):
        self._c = c
        self._cb = cb
        self._props = props
        super(RenderInfoFetcher, self).__init__()

    def paintContent(self, target):
        super(RenderInfoFetcher, self).paintContent(target)
        target.addAttribute(VRenderInfoFetcher.ATTR_TARGET_COMPONENT, self._c)
        if self._props is not None and len(self._props) > 0:
            target.addAttribute(VRenderInfoFetcher.ATTR_PROPERTIES, self._props)
        return

    def changeVariables(self, source, variables):
        super(RenderInfoFetcher, self).changeVariables(source, variables)
        if VRenderInfoFetcher.ATTR_RENDER_INFO in variables:
            ri = RenderInfo(variables[VRenderInfoFetcher.ATTR_RENDER_INFO])
            self._cb.infoReceived(ri)
            self.getParent().removeWindow(self)