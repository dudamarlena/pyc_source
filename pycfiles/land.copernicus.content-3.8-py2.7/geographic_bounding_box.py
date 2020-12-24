# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/widgets/geographic_bounding_box.py
# Compiled at: 2017-09-19 09:07:49
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget
from AccessControl import ClassSecurityInfo

class GeographicBoundingBoxWidget(StringWidget):
    """ Based on StringWidget, saves the values from all 4 text inputs
        West    = -81.2549
        East    = -81.2549
        North   = -81.2549
        South   = -81.2549
    """
    _properties = StringWidget._properties.copy()
    _properties.update({'macro': 'geographic_bounding_box_widget'})
    security = ClassSecurityInfo()
    security.declarePublic('render_own_label')

    def render_own_label(self):
        return True


registerWidget(GeographicBoundingBoxWidget, title='Geographic Bounding Box Widget', description='GeographicBoundingBoxWidget uses 4 inputs (West, East, North, South)', used_for=('land.copernicus.content.fields.geographic_bounding_box.GeographicBoundingBoxWidget', ))