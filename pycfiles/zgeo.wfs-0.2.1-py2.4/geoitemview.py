# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/browser/geoitemview.py
# Compiled at: 2008-10-27 05:35:22
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import event
from Products.Archetypes.event import ObjectEditedEvent
from zgeo.geographer.interfaces import IWriteGeoreferenced
import logging
logger = logging.getLogger('WFSView')

class GeoItemView(BrowserView):
    """ View on a georeferenced object
        """
    __module__ = __name__
    editgeometry_screen = ViewPageTemplateFile('editGeometry.pt')

    def __call__(self):
        """
                """
        logger.info('EDIT GEOM')
        action = self.request.get('ACTION')
        if action == 'STORE_GEOMETRY':
            logger.info('STORE GEOM')
            self.manage_storeGeometry()
        return self.editgeometry_screen()

    def getGeoInterface(self):
        """
                """
        adapted = IWriteGeoreferenced(self.context)
        return adapted.geo

    def manage_storeGeometry(self):
        """
                """
        type = self.request.get('geo_type')
        str_coords = self.request.get('geo_coords')
        IWriteGeoreferenced(self.context).setGeoInterface(type, eval(str_coords), crs='EPSG:4326')
        event.notify(ObjectEditedEvent(self.context))