# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/meta/image_data.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Apr 19, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for media image data API.
"""
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
from superdesk.meta.metadata_superdesk import Base
from ally.internationalization import N_
from superdesk.media_archive.meta.meta_data import MetaDataMapped
from superdesk.media_archive.api.image_data import ImageData
META_TYPE_KEY = N_('image')

class ImageDataDefinition:
    """
    Provides the mapping for ImageData definition.
    """
    __tablename__ = 'archive_image_data'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = declared_attr(lambda cls: Column('fk_metadata_id', ForeignKey(MetaDataMapped.Id, ondelete='CASCADE'), primary_key=True))
    Width = declared_attr(lambda cls: Column('width', Integer))
    Height = declared_attr(lambda cls: Column('height', Integer))
    CreationDate = declared_attr(lambda cls: Column('creation_date', DateTime))
    CameraMake = declared_attr(lambda cls: Column('camera_make', String(255)))
    CameraModel = declared_attr(lambda cls: Column('camera_model', String(255)))


class ImageDataEntry(Base, ImageDataDefinition):
    """
    Provides the mapping for ImageData table.
    """
    pass


class ImageDataMapped(ImageDataDefinition, MetaDataMapped, ImageData):
    """
    Provides the mapping for ImageData when extending MetaData.
    """
    __table_args__ = dict(ImageDataDefinition.__table_args__, extend_existing=True)