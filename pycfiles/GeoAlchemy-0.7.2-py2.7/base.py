# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geoalchemy/base.py
# Compiled at: 2012-06-01 14:24:10
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql import expression, not_
from sqlalchemy.sql.expression import ColumnClause, literal
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles
from utils import from_wkt
from functions import functions, _get_function, BaseFunction

class SpatialElement(object):
    """Represents a geometry value."""

    def __str__(self):
        if isinstance(self.desc, SpatialElement):
            return self.desc.desc
        return self.desc

    def __repr__(self):
        return '<%s at 0x%x; %r>' % (self.__class__.__name__, id(self), self.desc)

    def __getattr__(self, name):
        return getattr(functions, name)(self)

    def __get_wkt(self, session):
        """This method converts the object into a WKT geometry. It takes into
        account that WKTSpatialElement does not have to make a new query
        to retrieve the WKT geometry.
        
        """
        if isinstance(self, WKTSpatialElement):
            return self.desc
        else:
            if isinstance(self.desc, WKTSpatialElement):
                return self.desc.desc
            return session.scalar(self.wkt)

    def geom_type(self, session):
        wkt = self.__get_wkt(session)
        return from_wkt(wkt)['type']

    def coords(self, session):
        wkt = self.__get_wkt(session)
        return from_wkt(wkt)['coordinates']


class WKTSpatialElement(SpatialElement, expression.Function):
    """Represents a Geometry value expressed within application code; i.e. in
    the OGC Well Known Text (WKT) format.
    
    Extends expression.Function so that in a SQL expression context the value 
    is interpreted as 'GeomFromText(value)' or as the equivalent function in the 
    currently used database.
    
    """

    def __init__(self, desc, srid=4326, geometry_type='GEOMETRY'):
        assert isinstance(desc, basestring)
        self.desc = desc
        self.srid = srid
        self.geometry_type = geometry_type
        expression.Function.__init__(self, '')

    @property
    def geom_wkt(self):
        return self.desc


@compiles(WKTSpatialElement)
def __compile_wktspatialelement(element, compiler, **kw):
    function = _get_function(element, compiler, (element.desc, element.srid), kw.get('within_columns_clause', False))
    return compiler.process(function)


class WKBSpatialElement(SpatialElement, expression.Function):
    """Represents a Geometry value as expressed in the OGC Well
    Known Binary (WKB) format.
    
    Extends expression.Function so that in a SQL expression context the value 
    is interpreted as 'GeomFromWKB(value)' or as the equivalent function in the 
    currently used database .
    
    """

    def __init__(self, desc, srid=4326, geometry_type='GEOMETRY'):
        assert isinstance(desc, (basestring, buffer))
        self.desc = desc
        self.srid = srid
        self.geometry_type = geometry_type
        expression.Function.__init__(self, '')


@compiles(WKBSpatialElement)
def __compile_wkbspatialelement(element, compiler, **kw):
    from geoalchemy.dialect import DialectManager
    database_dialect = DialectManager.get_spatial_dialect(compiler.dialect)
    function = _get_function(element, compiler, (database_dialect.bind_wkb_value(element),
     element.srid), kw.get('within_columns_clause', False))
    return compiler.process(function)


class DBSpatialElement(SpatialElement, expression.Function):
    """This class can be used to wrap a geometry returned by a 
    spatial database operation.
    
    For example:: 
    
        element = DBSpatialElement(session.scalar(r.geom.buffer(10.0)))
        session.scalar(element.wkt)
    
    """

    def __init__(self, desc):
        self.desc = desc
        expression.Function.__init__(self, '', desc)


@compiles(DBSpatialElement)
def __compile_dbspatialelement(element, compiler, **kw):
    function = _get_function(element, compiler, [literal(element.desc)], kw.get('within_columns_clause', False))
    return compiler.process(function)


class PersistentSpatialElement(SpatialElement):
    """Represents a Geometry value loaded from the database."""

    def __init__(self, desc):
        self.desc = desc

    @property
    def geom_wkb(self):
        if self.desc is not None and isinstance(self.desc, WKBSpatialElement):
            return self.desc.desc
        else:
            return
            return

    @property
    def geom_wkt(self):
        if self.desc is not None and isinstance(self.desc, WKTSpatialElement):
            return self.desc.desc
        else:
            return
            return


class GeometryBase(UserDefinedType):
    """Base Geometry column type for all spatial databases.
    """
    name = 'GEOMETRY'

    def __init__(self, dimension=2, srid=4326, spatial_index=True, wkt_internal=False, **kwargs):
        self.dimension = dimension
        self.srid = srid
        self.spatial_index = spatial_index
        self.wkt_internal = wkt_internal
        self.kwargs = kwargs
        super(GeometryBase, self).__init__()

    def get_col_spec(self):
        return self.name

    def bind_processor(self, dialect):

        def process(value):
            if value is not None:
                if isinstance(value, SpatialElement):
                    if isinstance(value.desc, SpatialElement):
                        return value.desc.desc
                    return value.desc
                else:
                    return value

            else:
                return value
            return

        return process

    def result_processor(self, dialect, coltype=None):

        def process(value):
            if value is not None:
                return PersistentSpatialElement(value)
            else:
                return value
                return

        return process

    def adapt(self, cls, **kwargs):
        return cls(dimension=self.dimension, srid=self.srid, spatial_index=self.spatial_index, wkt_internal=self.wkt_internal, **self.kwargs)


def _to_gis(value, srid_db):
    """Interpret a value as a GIS-compatible construct."""
    if hasattr(value, '__clause_element__'):
        return value.__clause_element__()
    else:
        if isinstance(value, SpatialElement):
            if isinstance(value.desc, (WKBSpatialElement, WKTSpatialElement)):
                return _check_srid(value.desc, srid_db)
            return _check_srid(value, srid_db)
        if isinstance(value, basestring):
            return _check_srid(WKTSpatialElement(value), srid_db)
        if isinstance(value, expression.ClauseElement):
            return value
        if value is None:
            return
        raise Exception('Invalid type')
        return


def _check_srid(spatial_element, srid_db):
    """Check if the SRID of the spatial element which we are about to insert
    into the database equals the SRID used for the geometry column.
    If not, a transformation is added.
    """
    if srid_db is None or not hasattr(spatial_element, 'srid') or isinstance(spatial_element.srid, BaseFunction):
        return spatial_element
    if spatial_element.srid == srid_db:
        return spatial_element
    else:
        return functions.transform(spatial_element, srid_db)
        return


class RawColumn(ColumnClause):
    """This class is used to wrap a geometry column, so that
    no conversion to WKB is added, see SpatialComparator.RAW
    """

    def __init__(self, column):
        self.column = column
        ColumnClause.__init__(self, column.name, column.table)

    def _make_proxy(self, selectable, name=None):
        return self.column._make_proxy(selectable, name)


@compiles(RawColumn)
def __compile_rawcolumn(rawcolumn, compiler, **kw):
    return compiler.visit_column(rawcolumn.column)


class SpatialComparator(ColumnProperty.ColumnComparator):
    """Intercepts standard Column operators on mapped class attributes
        and overrides their behavior.
        
        A comparator class makes sure that queries like 
        "session.query(Lake).filter(Lake.lake_geom.gcontains(..)).all()" can be executed.
    """

    @property
    def RAW(self):
        """For queries like 'select extent(spots.spot_location) from spots' the 
        geometry column should not be surrounded by 'AsBinary(..)'. If 'RAW' is
        called on a geometry column, this column wont't be converted to WKB::
        
            session.query(func.extent(Spot.spot_location.RAW)).first() 
        
        """
        return RawColumn(self.__clause_element__())

    def __getattr__(self, name):
        return getattr(functions, name)(self)

    def __eq__(self, other):
        if other is None:
            return self.op('IS')(None)
        else:
            return functions.equals(self, other)

    def __ne__(self, other):
        if other is None:
            return self.op('IS NOT')(None)
        else:
            return not_(functions.equals(self, other))