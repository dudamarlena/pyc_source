# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/vista/services/orm.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import ORMEntity, UniversalTimeZone, UTCDateTime
from sqlalchemy import types, Column, String, Integer, func, BOOLEAN
from sqlalchemy.dialects.postgresql import ARRAY
from edition import INDEXER_EDITION

class TextSearchVector(types.UserDefinedType):

    def get_col_spec(self):
        return 'plainto_tsvector'


class SearchVector(ORMEntity):
    __tablename__ = 'vista_vector'
    object_id = Column('object_id', Integer, primary_key=True)
    entity = Column('entity', String)
    version = Column('version', Integer)
    edition = Column('edition', Integer)
    archived = Column('archived', BOOLEAN, default=False)
    event_date = Column('event_date', UTCDateTime)
    keywords = Column('keywords', ARRAY(String))
    vector = Column('vector', TextSearchVector, nullable=False)

    def __init__(self, object_id, entity, version, edition):
        self.object_id = object_id
        self.entity = entity.lower()
        self.version = version
        self.edition = INDEXER_EDITION