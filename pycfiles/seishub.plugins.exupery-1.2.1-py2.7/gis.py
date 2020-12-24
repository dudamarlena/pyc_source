# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\plugins\exupery\gis.py
# Compiled at: 2010-12-23 17:42:41
"""
Exupery - GIS resources.
"""
from obspy.core import UTCDateTime
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex
from seishub.core.packages.interfaces import IMapper, IResourceType
from sqlalchemy import sql
METADATA_RESOURCE_LINK = '\n    <item title="XML Resource">\n      <link href="%s/xml%s" text="%s" />\n    </item>\n  </metadata>\n'
METADATA_AL_LINK = '\n    <item title="XML Resource">\n      <link href="%s/xml%s" text="%s" />\n    </item>\n    <item title="XDSL Resource">\n      <link href="%s/xml%s?format=smile" text="%s" />\n    </item>\n  </metadata>\n'
METADATA_ALLOWED_VIEWS = {'gis_seismic-station': 0, 
   'gis_gps-data': 0, 
   'gis_gps-station': 0, 
   'gis_infrared-hotspot': 0, 
   'gis_seismic-event': 1, 
   'gis_minidoas-station': 0}
METADATA_EMPTY_XML = '\n  <metadata>\n  </metadata>\n'
SQL_QUERY_0 = '\n    SELECT document_id\n    FROM "%s"\n    WHERE Distance(GeomFromText(\'POINT(:x :y)\', 4326), geom) <= :d\n    AND start_datetime <= :now\n    AND (end_datetime >= :now OR end_datetime IS NULL)\n    ORDER BY \n        Distance(GeomFromText(\'POINT(:x :y)\', 4326), geom),\n        start_datetime DESC\n    LIMIT 1\n'
SQL_QUERY_1 = '\n    SELECT document_id\n    FROM "%s"\n    WHERE Distance(GeomFromText(\'POINT(:x :y)\', 4326), geom) <= :d\n    AND datetime >= :start\n    AND datetime <= :end\n    ORDER BY \n        Distance(GeomFromText(\'POINT(:x :y)\', 4326), geom),\n        datetime DESC\n    LIMIT 1\n'

class GISSessionResourceType(Component):
    """
    GIS Session resource type.
    """
    implements(IResourceType)
    package_id = 'exupery'
    resourcetype_id = 'gis-session'
    registerIndex('global', '/save/@global', 'boolean')
    registerIndex('project_id', '/save/@project_id', 'text')
    registerIndex('user_id', '/save/@user', 'text')


class GISMetadataMapper(Component):
    """
    Returns GIS Metadata for various GIS layers.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/gis/metadata'

    def process_GET(self, request):
        xslt_type = request.args0.get('xslt', '')
        if xslt_type:
            xslt_type = '.' + xslt_type
        try:
            document_id = int(request.args0.get('document_id'))
        except:
            try:
                document_id = self._getDocumentId(request)
            except:
                return '<metadata />'

        res = self.env.catalog.getResource(document_id=document_id)
        data = res.document.data
        reg = request.env.registry
        xslt = reg.stylesheets.get(package_id=res.package.package_id, resourcetype_id=res.resourcetype.resourcetype_id, type='metadata' + xslt_type)
        if not xslt or not len(xslt):
            xmldoc = METADATA_EMPTY_XML
        else:
            xslt = xslt[0]
            xmldoc = xslt.transform(data)
        if data[:70].find('alert_level') != -1:
            res_link = METADATA_AL_LINK % (self.env.getRestUrl(), str(res),
             res.name, self.env.getRestUrl(),
             str(res), res.name)
        else:
            res_link = METADATA_RESOURCE_LINK % (self.env.getRestUrl(), str(res),
             res.name)
        xmldoc = xmldoc.replace('</metadata>', str(res_link))
        return str(xmldoc)

    def _getDocumentId(self, request):
        args = {}
        args['x'] = float(request.args0.get('longitude', 0))
        args['y'] = float(request.args0.get('latitude', 0))
        args['d'] = float(request.args0.get('delta', 0))
        view_id = request.args0.get('view', 'gis_seismic-station')
        try:
            temp = request.args0.get('start_datetime')
            args['start'] = str(UTCDateTime(temp))
        except:
            args['start'] = str(UTCDateTime())

        try:
            temp = request.args0.get('end_datetime')
            args['end'] = str(UTCDateTime(temp))
        except:
            args['end'] = str(UTCDateTime())

        if args['end'] == args['start']:
            args['now'] = args['start']
        if view_id not in METADATA_ALLOWED_VIEWS.keys():
            raise
        type = METADATA_ALLOWED_VIEWS.get(view_id)
        if type == 0:
            query = sql.text(SQL_QUERY_0 % view_id)
        else:
            query = sql.text(SQL_QUERY_1 % view_id)
        try:
            result = self.env.db.query(query, **args).fetchone()
        except:
            raise

        if not result or len(result) != 1:
            raise
        return int(result[0])


class GISKMLMapper(Component):
    """
    Returns a KML document from a given document_id.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/gis/kml'

    def process_GET(self, request):
        try:
            document_id = int(request.args0.get('document_id', 0))
        except:
            return ''

        if not document_id:
            return '<kml />'
        res = self.env.catalog.getResource(document_id=document_id)
        data = res.document.data
        reg = request.env.registry
        xslt = reg.stylesheets.get(package_id=res.package.package_id, resourcetype_id=res.resourcetype.resourcetype_id, type='kml')
        if not xslt or not len(xslt):
            return '<kml />'
        xslt = xslt[0]
        xmldoc = xslt.transform(data)
        return str(xmldoc)


class GISSessionMapper(Component):
    """
    Returns a list of current GIS Session objects.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/gis/session'

    def process_GET(self, request):
        request.setHeader('content-type', 'text/plain; charset=UTF-8')
        uid = request.args0.get('user', '')
        gid = request.args0.get('global', 'true')
        pid = request.args0.get('project_id', '')
        if gid == 'true':
            gid = True
            uid = ''
        else:
            gid = False
            if not uid:
                return ''
        SQL_QUERY = '\n            SELECT document_id \n            FROM "/exupery/gis-session"\n            WHERE global = :gid \n            AND project_id = :pid\n        '
        if uid:
            SQL_QUERY += ' AND user_id = :uid'
        query = sql.text(SQL_QUERY)
        try:
            result = self.env.db.query(query, gid=gid, pid=pid, uid=uid).fetchall()
        except:
            return ''

        out = ''
        for res in result:
            res = self.env.catalog.getResource(document_id=res[0])
            data = res.document.data
            data = data.split('>', 1)[0]
            out += data + ' />\n'

        return out


class GISUserAuthMapper(Component):
    """
    Checks if given user and encoded password are correct.
    """
    implements(IMapper)
    package_id = 'exupery'
    mapping_url = '/exupery/gis/auth'
    public = True

    def process_GET(self, request):
        request.setHeader('content-type', 'text/plain; charset=UTF-8')
        user = request.args0.get('user', '')
        hash = request.args0.get('hash', '')
        try:
            if self.env.auth.checkPasswordHash(user, hash):
                return 'True'
            else:
                return 'WRONG PASSWORD'

        except:
            return 'WRONG USER'