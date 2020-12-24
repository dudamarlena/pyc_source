# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rect/packer.py
# Compiled at: 2007-07-27 06:30:19
from rect import Rect

class PackNode(object):
    """
    Creates an area which can recursively pack smaller areas into itself.
    """

    def __init__(self, xywh):
        self.rect = Rect(xywh)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.rect)

    def insert(self, xywh):
        """
        Insert an rect into the current rect. Returns a new Node representing
        the new rect.
        Returns None if no space is available for the new rect.
        """
        if hasattr(self, 'children'):
            for child in self.children:
                r = child.insert(xywh)
                if r is not None:
                    return r

            return
        rect = Rect(xywh)
        if self.rect.fits(rect):
            a = PackNode((self.rect.left + rect.width, self.rect.bottom, self.rect.width - rect.width, rect.height))
            b = PackNode((self.rect.left, self.rect.bottom + rect.height, self.rect.width, self.rect.height - rect.height))
            self.children = [a, b]
            return PackNode((self.rect.left, self.rect.bottom, rect.width, rect.height))
        return


def pack(big_rect, rects, padding=1):
    """
    Packs a list of rects (or w,h pairs) into a larger containing rect,
    with optional padding. Returns list of new rects.
    Raises ValueError if big_rect is too small.
    """
    input_order = []
    rects = [ Rect(i) for i in rects ]
    for r in rects:
        input_order.append((-r.height, -r.width, r))

    input_order.sort()
    map = {}
    tree = PackNode(big_rect)
    for (h, w, rect) in input_order:
        uv = tree.insert((rect.width + padding, rect.height + padding))
        if uv is None:
            raise ValueError('Pack size too small.')
        uv.rect.width -= padding
        uv.rect.height -= padding
        map[rect] = uv.rect

    coords = []
    for r in rects:
        coords.append(map[r])

    return coords