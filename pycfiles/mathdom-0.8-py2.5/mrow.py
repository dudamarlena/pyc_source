# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/mrow.py
# Compiled at: 2003-10-27 09:54:48
from element import *
import mtoken

class MRow(Element):

    class Strategy:

        def layout(self, elements):
            """Set positions of elements in a row;
            Returns (width, height, axis) of row"""
            global_axis = 0
            max_height_non_stretchy = 0
            max_height_stretchy = 0
            max_depth_non_stretchy = 0
            max_depth_stretchy = 0
            for elem in elements:
                if elem.axis is None:
                    elem.axis = elem.height / 2
                if elem is elem.embellished_container and elem.embellished_core.getAttribute('stretchy', recursive=0, default=0).bool:
                    max_height_stretchy = max(max_height_stretchy, elem.height - elem.axis)
                    max_depth_stretchy = max(max_depth_stretchy, elem.axis)
                else:
                    max_height_non_stretchy = max(max_height_non_stretchy, elem.height - elem.axis)
                    max_depth_non_stretchy = max(max_depth_non_stretchy, elem.axis)
                global_axis = max(global_axis, elem.axis)

            if max_height_non_stretchy == 0:
                height = max_height_stretchy
                depth = max_depth_stretchy
            else:
                height = max_height_non_stretchy
                depth = max_depth_non_stretchy
            for elem in elements:
                if elem is not elem.embellished_container:
                    continue
                core = elem.embellished_core
                if core.getAttribute('stretchy', recursive=0, default=0).bool:
                    if core.getAttribute('symmetric', recursive=0, default=True).bool:
                        core.setVStretch(max(height, depth), max(height, depth))
                    else:
                        core.setVStretch(height, depth)
                    elem.update()
                    global_axis = max(global_axis, elem.axis)

            x = 0
            height = 0
            for elem in elements:
                if isinstance(elem, mtoken.MOperator):
                    lspace = elem.getAttribute('lspace', recursive=False, default=0.0).asLength()
                    rspace = elem.getAttribute('rspace', recursive=False, default=0.0).asLength()
                else:
                    lspace = 0
                    rspace = 0
                x += lspace
                elem.x0 = x
                x += rspace
                x += elem.width
                elem.y0 = global_axis - elem.axis
                height = max(height, elem.y0 + elem.height)

            return (
             x, height, global_axis)

        def modify_children(self, elements):
            last_nonspace_index = -1
            first_nonspace_index = -1
            i = 0
            for child in elements:
                if not child.isSpaceLike:
                    last_nonspace_index = i
                    if first_nonspace_index == -1:
                        first_nonspace_index = i
                i += 1

            i = 0
            for child in elements:
                if child.isSpaceLike:
                    i += 1
                    continue
                if not isinstance(child, mtoken.MOperator):
                    i += 1
                    continue
                if i == first_nonspace_index:
                    form = 'prefix'
                elif i == last_nonspace_index:
                    form = 'postfix'
                else:
                    form = 'infix'
                child.setAttributeWeak('form', form)
                i += 1

        def embellished_p(self, children):
            eopnum = 0
            for elem in children:
                if elem.isSpaceLike:
                    continue
                eopnum += 1
                if eopnum > 1:
                    return
                core = elem.embellished_p()

            return core

    def __init__(self, plotter, children):
        Element.__init__(self, plotter)
        for child in children:
            self.addChild(child)

        self.strategy = self.Strategy()

    def update(self):
        if not self.needs_update:
            return
        self.needs_update = 0
        self.strategy.modify_children(self.children)
        for child in self:
            child.update()

        (self.width, self.height, self.axis) = self.strategy.layout(self.children)

    def embellished_p(self):
        return self.strategy.embellished_p(self.children)


class MStyle(MRow):
    pass


xml_mapping['mrow'] = MRow
xml_mapping['mstyle'] = MStyle