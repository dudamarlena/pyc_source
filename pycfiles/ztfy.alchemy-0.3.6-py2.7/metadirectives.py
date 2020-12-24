# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/metadirectives.py
# Compiled at: 2015-09-10 10:38:05
from zope.interface import Interface
from zope.schema import TextLine, Bool, Int
from zope.configuration.fields import GlobalObject
from ztfy.alchemy import _

class IEngineDirective(Interface):
    """Define a new SQLAlchemy engine"""
    dsn = TextLine(title=_('Database URL'), description=_('RFC-1738 compliant URL for the database connection'), required=True)
    name = TextLine(title=_('Engine name'), description=_('Empty if this engine is the default engine.'), required=False, default='')
    echo = Bool(title=_('Echo SQL statements'), required=False, default=False)
    pool_size = Int(title=_('Pool size'), description=_('SQLAlchemy connections pool size'), required=False, default=25)
    pool_recycle = Int(title=_('Pool recycle time'), description=_('SQLAlchemy connection recycle time (-1 for none)'), required=False, default=-1)
    register_geotypes = Bool(title=_('Register GeoTypes'), description=_('Should engine register PostGis GeoTypes'), default=False)
    register_opengis = Bool(title=_('Register OpenGIS'), description=_('Should engine register OpenGIS types'), default=False)


class ITableAssignDirective(Interface):
    """Assign a table to a given engine"""
    table = TextLine(title=_('Table name'), description=_('Name of the table to assign'), required=True)
    engine = TextLine(title=_('SQLAlchemy engine'), description=_('Name of the engine to connect the table to'), required=True)


class IClassAssignDirective(Interface):
    """Assign a table to a given engine"""
    class_ = GlobalObject(title=_('Class name'), description=_('Name of the class to assign'), required=True)
    engine = TextLine(title=_('SQLAlchemy engine'), description=_('Name of the engine to connect the table to'), required=True)