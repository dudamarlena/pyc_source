# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/route.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from base import Base, KVC
from utcdatetime import UTCDateTime

class Route(Base, KVC):
    """ An OpenGroupare route object """
    __tablename__ = 'route'
    __entityName__ = 'Route'
    __internalName__ = 'Route'
    object_id = Column('route_id', ForeignKey('log.object_id'), ForeignKey('object_acl.object_id'), primary_key=True)
    name = Column('name', String(50))
    status = Column('db_status', String)
    comment = Column('comment', Text)
    created = Column('created', UTCDateTime)
    modified = Column('lastmodified', UTCDateTime)
    version = Column('object_version', Integer)
    owner_id = Column('owner_id', Integer, ForeignKey('person.company_id'), nullable=False)

    def __init__(self):
        self.status = 'inserted'

    def set_markup(self, text):
        self._markup = text

    def get_markup(self):
        if hasattr(self, '_markup'):
            return self._markup
        else:
            return

    def get_display_name(self):
        return self.name

    def __repr__(self):
        return ('<Route objectId={0} version={1} name="{2}" owner={3}>').format(self.object_id, self.version, self.name, self.owner_id)