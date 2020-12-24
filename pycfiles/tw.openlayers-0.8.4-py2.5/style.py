# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/openlayers/style.py
# Compiled at: 2008-07-12 11:31:37
from tw.api import Widget, JSLink
__all__ = [
 'Style', 'StyleMap']

class StyleBase(Widget):
    """ Base class for Style Widgets. """
    params = []
    config = None

    def __init__(self, id=None, parent=None, children=[], **kw):
        super(Widget, self).__init__(id, parent, children, **kw)
        self.config = kw
        self.config['_style_type'] = self.__class__.__name__

    @property
    def all_params(self):
        d = {}
        for param in self.params:
            d[param] = getattr(self, param)

        return d

    def update_params(self, d):
        super(StyleBase, self).update_params(d)


class Style(StyleBase):
    """ An OpenLayers Style widget.

    This widget can be used ti create a style object for OpenLayers.
    This style is created based on use defined SDL (Styled Layer
    Descriptor) Document. The style is then applied to a Vector layer
    or its subclasses.

    For detailed documentation on the OpenLayers API, visit the OpenLayers
    homepage: http://www.openlayers.org/
    """
    template = '\n    '
    params = []

    def update_params(self, d):
        super(Style, self).update_params(d)


class StyleMap(StyleBase):
    """The StyleMap Widget creates a style map object from either a set
    of style options or an OGC Styled Layer Descriptor (SLD) document.
    """
    params = []

    def update_params(self, d):
        super(StyleMap, self).update_params(d)