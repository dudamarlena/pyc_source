# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.iconpicker/medialog/iconpicker/widgets/widget.py
# Compiled at: 2019-03-04 06:48:35
import zope.component, zope.interface, zope.schema.interfaces
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text
from plone import api
from medialog.iconpicker.interfaces import IIconPickerSettings

class IIconPickerWidget(interfaces.IWidget):
    """Iconpicker widget."""
    pass


@zope.interface.implementer_only(IIconPickerWidget)
class IconPickerWidget(text.TextWidget):
    """Iconpicker Widget"""

    def family_css(self):
        iconset = self.iconset()
        if iconset == 'glyphicon':
            return 'glyphicon'
        if iconset == 'mapicon':
            return 'map-icons'
        if iconset == 'typicon':
            return 'typcn'
        if iconset == 'ionicon':
            return 'ionicons'
        if iconset == 'weathericon':
            return 'wi'
        if iconset == 'octicon':
            return 'octicon'
        if iconset == 'elusiveicon':
            return 'el-icon'
        if iconset == 'medialogfont':
            return 'medialogfont'
        if iconset == 'iconpickerfont':
            return 'iconpickerfont'
        if iconset == 'lineawsome':
            return 'linewsome'
        return 'fa'

    def plone5(self):
        try:
            from Products.CMFPlone.factory import _IMREALLYPLONE5
            return 1
        except ImportError:
            return 0

    def iconset(self):
        """Returns current iconset name This is also used for loading the resources below"""
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.iconset')

    def cols(self):
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.cols')

    def rows(self):
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.rows')

    def placement(self):
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.placement')

    def loadbootstrap(self):
        return api.portal.get_registry_record('medialog.iconpicker.interfaces.IIconPickerSettings.loadbootstrap')

    def medialogfont(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/medialogfont/css/medialogfont.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-medialogfont.js"></script>\n        '

    def iconpickerfont(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/iconpickerfont/style.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-iconpickerfont.js"></script>\n        '

    def glyphicon(self):
        return '\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-glyphicon.min.js"></script>\n        '

    def fontawesome(self):
        return '\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-fontawesome-4.2.0.js"></script>\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/font-awesome-4.2.0/css/font-awesome.min.css"/>\n        '

    def mapicon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/map-icons-2.1.0/css/map-icons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-mapicon-2.1.0.min.js"></script>\n        '

    def typicon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/typicons-2.0.6/css/typicons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-typicon-2.0.6.min.js"></script>\n        '

    def ionicon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/ionicons-1.5.2/css/ionicons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-ionicon-1.5.2.min.js"></script>\n       '

    def weathericon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/weather-icons-1.2.0/css/weather-icons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-weathericon-1.2.0.min.js"></script>\n        '

    def octicon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/octicons-2.1.2/css/octicons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-octicon-2.1.2.min.js"></script>\n        '

    def elusiveicon(self):
        return '\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/elusive-icons-2.0.0/css/elusive-icons.min.css"/>\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-elusiveicon-2.0.0.min.js"></script>\n        '

    def lineawesome(self):
        return '\n        <script type="text/javascript" src="++resource++medialog.iconpicker/bootstrap-iconpicker/js/iconset/iconset-line-awesome.js"></script>\n        <link rel="stylesheet" href="++resource++medialog.iconpicker/icon-fonts/line-awesome/css/line-awesome.css"/>\n        '

    def color(self):
        context = self.context
        color = getattr(context, 'color', None)
        if color:
            return '#' + color
        else:
            return 'inherit'


@zope.interface.implementer(interfaces.IFieldWidget)
def IconPickerFieldWidget(field, request):
    """IFieldWidget factory for IconPickerWidget."""
    return widget.FieldWidget(field, IconPickerWidget(request))


class IColorPickerWidget(interfaces.IWidget):
    """Colorpicker widget."""
    pass


@zope.interface.implementer_only(IColorPickerWidget)
class ColorPickerWidget(text.TextWidget):
    """Colorpicker Widget"""
    pass


@zope.interface.implementer(interfaces.IFieldWidget)
def ColorPickerFieldWidget(field, request):
    """IFieldWidget factory for ColorPickerWidget."""
    return widget.FieldWidget(field, ColorPickerWidget(request))