# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/widgets/proportional.py
# Compiled at: 2009-02-25 04:20:27
from bezel.graphics.containers import BaseContainer

class ProportionalContainer(BaseContainer):

    def __init__(self, width, height):
        """TODO: Detail that width and height are relative."""
        super(ProportionalContainer, self).__init__()
        self.relative_size = (
         width, height)

    def paint(self):
        super(ProportionalContainer, self).paint()
        (width, height) = map(float, self.rect.size)
        (rwidth, rheight) = map(float, self.relative_size)
        adjust_x = self.rect.x
        adjust_y = self.rect.y
        scaling = None
        hscale = width / rwidth
        vscale = height / rheight
        if hscale < vscale:
            scaling = hscale
            adjust_y += (height - width / (rwidth / rheight)) / 2.0
        else:
            scaling = vscale
            adjust_x += (width - height / (rheight / rwidth)) / 2.0
        for child in self.children:
            (child_x, child_y) = child.position
            child_x *= scaling
            child_y *= scaling
            (child_w, child_h) = child.size
            child_w *= scaling
            child_h *= scaling
            previous = tuple(child.rect.size)
            child.rect.topleft = (adjust_x + child_x, adjust_y + child_y)
            child.rect.size = (child_w, child_h)
            if previous != (child_w, child_h):
                child.paint()

        return