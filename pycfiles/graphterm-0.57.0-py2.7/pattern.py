# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/pattern.py
# Compiled at: 2012-08-15 03:48:07
from svgwrite.base import BaseElement
from svgwrite.mixins import XLink, ViewBox, Transform, Presentation
from svgwrite.utils import is_string

class Pattern(BaseElement, XLink, ViewBox, Transform, Presentation):
    """
    A pattern is used to fill or stroke an object using a pre-defined graphic
    object which can be replicated ("tiled") at fixed intervals in x and y to
    cover the areas to be painted. Patterns are defined using a `pattern` element
    and then referenced by properties `fill` and `stroke` on a given graphics
    element to indicate that the given element shall be filled or stroked with
    the referenced pattern.
    """
    elementname = 'pattern'
    transformname = 'patternTransform'

    def __init__(self, insert=None, size=None, inherit=None, **extra):
        """
        :param 2-tuple insert: base point of the pattern (**x**, **y**)
        :param 2-tuple size: size of the pattern (**width**, **height**)
        :param inherit: pattern inherits properties from `inherit` see: **xlink:href**

        """
        super(Pattern, self).__init__(**extra)
        if insert is not None:
            self['x'] = insert[0]
            self['y'] = insert[1]
        if size is not None:
            self['width'] = size[0]
            self['height'] = size[1]
        if inherit is not None:
            if is_string(inherit):
                self.set_href(inherit)
            else:
                self.set_href(inherit.get_iri())
        if self.debug:
            self.validator.check_all_svg_attribute_values(self.elementname, self.attribs)
        return

    def get_paint_server(self, default='none'):
        """ Returns the <FuncIRI> of the gradient. """
        return '%s %s' % (self.get_funciri(), default)