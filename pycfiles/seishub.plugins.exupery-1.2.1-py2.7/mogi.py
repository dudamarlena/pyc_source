# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\plugins\exupery\mogi.py
# Compiled at: 2010-12-23 17:42:41
"""
Exupery - WP5 - MOGI resources.

Deformation model simulation and stress field results

Contact:
 * Manoochehr Shirzaei (shirzaei@gfz-potsdam.de)
"""
from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql

class MogiResourceType(Component):
    """
    Mogi resource type.
    """
    implements(IResourceType)
    package_id = 'exupery'
    resourcetype_id = 'mogi'
    registerIndex('project_id', '/mogi/@project_id', 'text')
    registerIndex('volcano_id', '/mogi/@volcano_id', 'text')
    registerIndex('datetime', '/mogi/datetime/value', 'date')
    registerIndex('upperleft_latitude', '/mogi/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude', '/mogi/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude', '/mogi/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude', '/mogi/range_lowerright/longitude/value', 'float')
    registerIndex('local_path_image_pressure', '/mogi/files/file/local_path[../@id="mogi_pressure"]', 'text')
    registerIndex('local_path_image_s1', '/mogi/files/file/local_path[../@id="mogi_s1"]', 'text')
    registerIndex('local_path_image_s2', '/mogi/files/file/local_path[../@id="mogi_s2"]', 'text')
    registerIndex('local_path_image_s3', '/mogi/files/file/local_path[../@id="mogi_s3"]', 'text')


class MogiGeoTIFFMapper(Component):
    """
    Returns a list of filtered Mogi GeoTiff files.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/wp5/mogi/geotiff'

    def process_GET(self, request):
        pid = request.args0.get('project_id', '')
        xml = Element('query')
        query = sql.text('\n           SELECT \n               document_id, \n               datetime, \n               local_path_image_pressure,\n               local_path_image_s1,\n               local_path_image_s2,\n               local_path_image_s3\n           FROM "/exupery/mogi"\n           WHERE project_id = :pid \n        ')
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        image_types = {'pressure': 'local_path_image_pressure', 
           'sigma1': 'local_path_image_s1', 
           'sigma2': 'local_path_image_s2', 
           'sigma3': 'local_path_image_s3'}
        for i in result:
            for type, image_id in image_types.iteritems():
                s = Sub(xml, 'resource', document_id=str(i.document_id))
                Sub(s, 'type').text = type
                Sub(s, 'datetime').text = i.datetime.isoformat()
                Sub(s, 'url').text = 'local://' + i[image_id]

        return toString(xml)