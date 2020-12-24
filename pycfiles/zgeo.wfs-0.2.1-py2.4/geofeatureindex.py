# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/geocatalog/geofeatureindex.py
# Compiled at: 2008-10-27 05:35:22
from Products.PluginIndexes.common.UnIndex import UnIndex
from zgeo.wfs.interfaces import IWFSGeoItem
import logging
logger = logging.getLogger('WFSCatalog')

class GeoFeatureIndex(UnIndex):
    """Index for geofeature attribute provided by IWriteGeoreferenced adapter
        """
    __module__ = __name__
    __implements__ = UnIndex.__implements__
    meta_type = 'GeoFeatureIndex'
    query_options = [
     'query']

    def index_object(self, documentId, obj, threshold=None):
        """
                """
        geoitem = IWFSGeoItem(obj)
        fields = self.getIndexSourceNames()
        res = 0
        for attr in fields:
            if hasattr(obj, attr):
                res += self._index_object(documentId, obj, threshold, attr)
            else:
                res += self._index_object(documentId, geoitem, threshold, attr)

        return res > 0