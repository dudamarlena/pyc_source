# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/masking.py
# Compiled at: 2012-08-15 03:48:07
from svgwrite.base import BaseElement
from svgwrite.mixins import Transform

class ClipPath(BaseElement, Transform):
    """
    The clipping path restricts the region to which paint can be applied.
    Conceptually, any parts of the drawing that lie outside of the region
    bounded by the currently active clipping path are not drawn. A clipping
    path can be thought of as a mask wherein those pixels outside the clipping
    path are black with an alpha value of zero and those pixels inside the
    clipping path are white with an alpha value of one (with the possible
    exception of anti-aliasing along the edge of the silhouette).

    A **clipPath** element can contain **path** elements, **text** elements,
    basic shapes (such as **circle**) or a **use** element. If a **use**
    element is a child of a **clipPath** element, it must directly reference
    **path**, **text** or basic shape elements. Indirect references are an
    error.
    """
    elementname = 'clipPath'


class Mask(BaseElement):
    """
    In SVG, you can specify that any other graphics object or **g** element
    can be used as an alpha mask for compositing the current object into the
    background.

    A **mask** can contain any graphical elements or container elements such
    as a **g**.
    """
    elementname = 'mask'

    def __init__(self, start=None, size=None, **extra):
        super(Mask, self).__init__(**extra)
        if start is not None:
            self['x'] = start[0]
            self['y'] = start[1]
        if size is not None:
            self['width'] = size[0]
            self['height'] = size[1]
        return