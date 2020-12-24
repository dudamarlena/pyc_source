# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/meta/meta_data.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Apr 19, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for media meta data API.
"""
from ..api.meta_data import MetaData
from .meta_type import MetaTypeMapped
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.orm.mapper import reconstructor
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Integer
from superdesk.meta.metadata_superdesk import Base
from ally.support.sqlalchemy.session import openSession
from superdesk.user.meta.user import UserMapped
from ally.internationalization import N_
META_TYPE_KEY = N_('other')

class ThumbnailFormat(Base):
    """
    Provides the mapping for thumbnails.
    This is not a REST model.
    """
    __tablename__ = 'archive_thumbnail'
    __table_args__ = dict(mysql_engine='InnoDB')
    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    format = Column('format', String(190), unique=True, nullable=False, doc='\n    The format for the reference of the thumbnail images in the media archive\n    id = the meta data database id; name = the name of the content file; size = the key of the thumbnail size\n    ')


class MetaDataMapped(Base, MetaData):
    """
    Provides the mapping for MetaData.
    """
    __tablename__ = 'archive_meta_data'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Name = Column('name', String(255), nullable=False)
    SizeInBytes = Column('size_in_bytes', Integer)
    CreatedOn = Column('created_on', DateTime, nullable=False)
    Creator = Column('fk_creator_id', ForeignKey(UserMapped.Id), nullable=False)
    typeId = Column('fk_type_id', ForeignKey(MetaTypeMapped.Id, ondelete='RESTRICT'), nullable=False)
    thumbnailFormatId = Column('fk_thumbnail_format_id', ForeignKey(ThumbnailFormat.id, ondelete='RESTRICT'), nullable=False)
    content = Column('content', String(255))
    _cache_types = {}

    @reconstructor
    def init_on_load(self):
        typeId = self._cache_types.get(self.typeId)
        if typeId is None:
            metaType = openSession().query(MetaTypeMapped).get(self.typeId)
            assert isinstance(metaType, MetaTypeMapped), 'Invalid type id %s' % metaType
            typeId = self._cache_types[metaType.Id] = metaType.Type
        self.Type = typeId
        return