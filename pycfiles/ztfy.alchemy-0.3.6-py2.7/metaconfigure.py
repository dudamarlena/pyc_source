# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/metaconfigure.py
# Compiled at: 2015-09-10 10:38:05
from ztfy.alchemy.interfaces import IAlchemyEngineUtility
from zope.component.security import PublicPermission
from zope.component.zcml import utility
from ztfy.alchemy.engine import AlchemyEngineUtility, assignTable, assignClass

def engine(context, dsn, name='', echo=False, pool_size=25, pool_recycle=-1, register_geotypes=False, register_opengis=False, **kw):
    engine = AlchemyEngineUtility(name, dsn, echo=echo, pool_size=pool_size, pool_recycle=pool_recycle, register_geotypes=register_geotypes, register_opengis=register_opengis, **kw)
    utility(context, IAlchemyEngineUtility, engine, permission=PublicPermission, name=name)


def connectTable(context, table, engine):
    context.action(discriminator=('ztfy.alchemy.table', table), callable=assignTable, args=(
     table, engine, False))


def connectClass(context, class_, engine):
    context.action(discriminator=('ztfy.alchemy.class', class_), callable=assignClass, args=(
     class_, engine, False))