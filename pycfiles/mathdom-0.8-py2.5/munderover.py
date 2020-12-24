# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/munderover.py
# Compiled at: 2003-10-27 11:16:29
from element import *
import warnings, msubsup
_ACCENT_SPACING = 0.05
_LIMIT_SPACING = 0.2

class MOver(Element):

    class Strategy:

        def modify_children(elem, base, over):
            if base.embellished_core is not None:
                elem.setAttributeWeak('accent', base.embellished_core.getAttribute('accent', recursive=False, default=False).bool)
            else:
                elem.setAttributeWeak('accent', False)
            if not elem.getAttribute('accent', recursive=False).bool:
                over.setAttributeWeak('scriptlevel', '+1')
            over.setAttributeWeak('displaystyle', 'false')
            return

        modify_children = staticmethod(modify_children)

        def layout(elem, base, over):
            if elem.getAttribute('accent', recursive=False, default=False).bool:
                spacing = base.font_size * _ACCENT_SPACING
            else:
                spacing = base.font_size * _LIMIT_SPACING
            base.x0 = 0
            base.y0 = 0
            if over is over.embellished_container:
                core = over.embellished_core
                if core.getAttribute('stretchy', recursive=0, default=False).bool:
                    core.setHStretch(base.width)
                    over.update()
            over.x0 = base.width / 2 - over.width / 2
            over.y0 = base.height + spacing
            if over.x0 < 0:
                base.x0 -= over.x0
                over.x0 = 0
            elem.height = over.y0 + over.height
            elem.width = max(base.x0 + base.width, over.x0 + over.width)
            elem.axis = base.y0 + base.axis

        layout = staticmethod(layout)

    def __init__(self, plotter, children):
        assert len(children) == 2
        Element.__init__(self, plotter)
        for child in children:
            self.addChild(child)

    def update(self):
        assert len(self.children) == 2
        (base, over) = self.children
        base.update()
        if base.embellished_core is not None and base.embellished_core.getAttribute('movablelimits', recursive=False, default=False) and not self.getAttribute('displaystyle').bool:
            strategy = msubsup.MSup.Strategy
        else:
            strategy = self.Strategy
        strategy.modify_children(self, base, over)
        over.update()
        strategy.layout(self, base, over)
        return

    def embellished_p(self):
        try:
            return self.children[0].embellished_p()
        except IndexError:
            return

        return


class MUnder(Element):

    class Strategy:

        def modify_children(elem, base, under):
            if base.embellished_core is not None:
                elem.setAttributeWeak('accentunder', base.embellished_core.getAttribute('accent', recursive=False, default=False).bool)
            else:
                elem.setAttributeWeak('accentunder', False)
            if not elem.getAttribute('accentunder', recursive=False).bool:
                under.setAttributeWeak('scriptlevel', '+1')
            under.setAttributeWeak('displaystyle', 'false')
            return

        modify_children = staticmethod(modify_children)

        def layout(elem, base, under):
            if elem.getAttribute('accentunder', recursive=False, default=False).bool:
                spacing = base.font_size * _ACCENT_SPACING
            else:
                spacing = base.font_size * _LIMIT_SPACING
            base.x0 = 0
            base.y0 = under.height + spacing
            under.x0 = base.width / 2 - under.width / 2
            under.y0 = 0
            if under.x0 < 0:
                base.x0 -= under.x0
                under.x0 = 0
            elem.height = base.y0 + base.height
            elem.width = max(base.x0 + base.width, under.x0 + under.width)
            elem.axis = base.y0 + base.axis

        layout = staticmethod(layout)

    def __init__(self, plotter, children):
        assert len(children) == 2
        Element.__init__(self, plotter)
        for child in children:
            self.addChild(child)

    def update(self):
        assert len(self.children) == 2
        (base, under) = self.children
        base.update()
        if base.embellished_core is not None and base.embellished_core.getAttribute('movablelimits', recursive=False, default=False) and not self.getAttribute('displaystyle').bool:
            strategy = msubsup.MSub.Strategy
        else:
            strategy = self.Strategy
        strategy.modify_children(self, base, under)
        under.update()
        strategy.layout(self, base, under)
        return

    def embellished_p(self):
        try:
            return self.children[0].embellished_p()
        except IndexError:
            return

        return


class MUnderOver(Element):

    class Strategy:

        def modify_children(elem, base, under, over):
            if base.embellished_core is not None:
                elem.setAttributeWeak('accentunder', base.embellished_core.getAttribute('accent', recursive=False, default=False).bool)
                elem.setAttributeWeak('accent', base.embellished_core.getAttribute('accent', recursive=False, default=False).bool)
            else:
                elem.setAttributeWeak('accentunder', False)
                elem.setAttributeWeak('accent', False)
            if not elem.getAttribute('accentunder', recursive=False).bool:
                under.setAttributeWeak('scriptlevel', '+1')
            under.setAttributeWeak('displaystyle', 'false')
            if not elem.getAttribute('accent', recursive=False).bool:
                over.setAttributeWeak('scriptlevel', '+1')
            over.setAttributeWeak('displaystyle', 'false')
            return

        modify_children = staticmethod(modify_children)

        def layout(elem, base, under, over):
            if elem.getAttribute('accentunder', recursive=False, default=False).bool:
                spacing = base.font_size * _ACCENT_SPACING
            else:
                spacing = base.font_size * _LIMIT_SPACING
            if elem.getAttribute('accent', recursive=False, default=False).bool:
                spacing_over = base.font_size * _ACCENT_SPACING
            else:
                spacing_over = base.font_size * _LIMIT_SPACING
            base.x0 = 0
            base.y0 = under.height + spacing
            under.x0 = base.width / 2 - under.width / 2
            under.y0 = 0
            if under.x0 < 0:
                base.x0 -= under.x0
                under.x0 = 0
            over.x0 = base.x0 + base.width / 2 - over.width / 2
            over.y0 = base.y0 + base.height + spacing_over
            if over.x0 < 0:
                base.x0 -= over.x0
                under.x0 -= over.x0
                over.x0 = 0
            elem.height = over.y0 + over.height
            elem.width = max(base.x0 + base.width, under.x0 + under.width, over.x0 + over.width)
            elem.axis = base.y0 + base.axis

        layout = staticmethod(layout)

    def __init__(self, plotter, children):
        assert len(children) == 3
        Element.__init__(self, plotter)
        for child in children:
            self.addChild(child)

    def update(self):
        (base, under, over) = self.children
        base.update()
        if base.embellished_core is not None and base.embellished_core.getAttribute('movablelimits', recursive=False, default=False) and not self.getAttribute('displaystyle').bool:
            strategy = msubsup.MSubSup.Strategy
        else:
            strategy = self.Strategy
        strategy.modify_children(self, base, under, over)
        under.update()
        over.update()
        strategy.layout(self, base, under, over)
        return

    def embellished_p(self):
        try:
            return self.children[0].embellished_p()
        except IndexError:
            return

        return


xml_mapping['mover'] = MOver
xml_mapping['munder'] = MUnder
xml_mapping['munderover'] = MUnderOver