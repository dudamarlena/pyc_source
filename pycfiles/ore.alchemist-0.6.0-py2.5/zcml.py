# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/zcml.py
# Compiled at: 2008-09-11 20:29:53
from zope import interface, schema
from zope.configuration.fields import GlobalObject
from zope import component
from zope.app.component.metaconfigure import utility, PublicPermission
import sqlalchemy, interfaces

class IEngineDirective(interface.Interface):
    """ Creates A Database Engine. Database Engines are named utilities.
    """
    url = schema.URI(title='Database URL', description='SQLAlchemy Database URL', required=True)
    name = schema.Text(title='Engine Name', description='Empty if this engine is the default engine.', required=False, default='')
    echo = schema.Bool(title='Echo SQL statements', description='Debugging Echo Log for Engine', required=False, default=False)
    pool_recycle = schema.Int(title='Connection Recycle', description='Time Given in Seconds', required=False, default=-1)


IEngineDirective.setTaggedValue('keyword_arguments', True)

def engine(_context, url, name='', echo=False, pool_recycle=-1, **kwargs):
    component = sqlalchemy.create_engine(url, echo=echo, pool_recycle=pool_recycle, **kwargs)
    utility(_context, provides=interfaces.IDatabaseEngine, component=component, permission=PublicPermission, name=name)


class IBindDirective(interface.Interface):
    """ Binds a MetaData to a database engine.
    """
    engine = schema.Text(title='Engine Name')
    metadata = GlobalObject(title='Metadata Instance', description='Metadata Instance to be bound')


def bind(_context, engine, metadata):

    def _bind(engine_name, metadata):
        metadata.bind = component.getUtility(interfaces.IDatabaseEngine, engine)

    _context.action(discriminator=(
     'alchemist.bind', metadata), callable=_bind, args=(
     engine, metadata))