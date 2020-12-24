# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\ATGoogleMaps\widget.py
# Compiled at: 2010-10-23 04:05:06
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.Registry import registerWidget

class LatLngWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({'macro': 'latlng_widget'})
    security = ClassSecurityInfo()


registerWidget(LatLngWidget, title='LatLng', description='Renders latitude and longitude fields.', used_for=('Products.ATGoogleMaps.field.LatLngField', ))

class PolylineWidget(LinesWidget):
    _properties = LinesWidget._properties.copy()
    _properties.update({'macro': 'polyline_widget'})
    security = ClassSecurityInfo()


registerWidget(PolylineWidget, title='Polyline', description='Renders polyline fields.', used_for=('Products.Archetypes.Field.LinesField', ))