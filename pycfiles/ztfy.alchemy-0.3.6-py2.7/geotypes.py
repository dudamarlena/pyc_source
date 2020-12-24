# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/geotypes.py
# Compiled at: 2015-09-10 10:38:05
import sqlalchemy
from GeoTypes import OGGeoTypeFactory, WKBParser

class PostGisWKBFactory(object):

    def __init__(self):
        pass

    def __call__(self, s=None):
        factory = OGGeoTypeFactory()
        parser = WKBParser(factory)
        parser.parseGeometry(s)
        return factory.getGeometry()


class GeometryType(sqlalchemy.types.TypeEngine):

    def __init__(self, SRID, typeName, dimension):
        super(GeometryType, self).__init__()
        self.mSrid = SRID
        self.mType = typeName.upper()
        self.mDim = dimension
        self.bfact = PostGisWKBFactory()

    def __repr__(self):
        return '%s:%s-%s(%s)' % (self.__class__.__name__, self.mType, self.mDim, self.mSrid)

    def get_col_spec(self):
        return 'GEOMETRY'


class GeometryPOINT(GeometryType):

    def __init__(self, srid):
        super(GeometryPOINT, self).__init__(srid, 'POINT', 2)


class GeometryLINESTRING(GeometryType):

    def __init__(self, srid):
        super(GeometryLINESTRING, self).__init__(srid, 'LINESTRING', 2)