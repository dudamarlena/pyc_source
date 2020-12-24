# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/interfaces.py
# Compiled at: 2015-09-10 10:38:05
from zope.interface import Interface, Attribute
from zope.schema import TextLine, BytesLine, Bool, Int
from ztfy.alchemy import _
REQUEST_SESSION_KEY = 'ztfy.alchemy.session'

class IAlchemyEngineUtility(Interface):
    """SQLAlchemy engine utility interface"""
    name = TextLine(title=_('Name'), required=False)
    dsn = TextLine(title=_('DSN'), required=True, default='sqlite://')
    echo = Bool(title=_('Echo SQL'), required=True, default=False)
    pool_size = Int(title=_('Pool size'), required=True, default=25)
    pool_recycle = Int(title=_('Pool recycle time'), required=True, default=-1)
    register_geotypes = Bool(title=_('Register GEOTypes'), required=True, default=False)
    register_opengis = Bool(title=_('Register OpenGIS'), required=True, default=False)
    encoding = BytesLine(title=_('Encoding'), required=True, default='utf-8')
    convert_unicode = Bool(title=_('Convert Unicode'), required=True, default=False)


class IAlchemyBaseObject(Interface):
    """SQLAlchemy object base interface"""
    _sa_instance_state = Attribute(_('SQLAlchemy instance state'))