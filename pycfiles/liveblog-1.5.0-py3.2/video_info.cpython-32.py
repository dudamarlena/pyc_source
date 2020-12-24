# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/meta/video_info.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Aug 23, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Contains the SQL alchemy meta for media video info API.
"""
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String
from superdesk.media_archive.meta.meta_info import MetaInfoMapped
from sqlalchemy.ext.declarative import declared_attr
from superdesk.meta.metadata_superdesk import Base
from superdesk.media_archive.api.video_info import VideoInfo

class VideoInfoDefinition:
    """
    Provides the mapping for VideoInfo.
    """
    __tablename__ = 'archive_video_info'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = declared_attr(lambda cls: Column('fk_metainfo_id', ForeignKey(MetaInfoMapped.Id, ondelete='CASCADE'), primary_key=True))
    Caption = declared_attr(lambda cls: Column('caption', String(255), nullable=True, key='Caption'))


class VideoInfoEntry(Base, VideoInfoDefinition):
    """
    Provides the mapping for VideoInfo table.
    """
    pass


class VideoInfoMapped(VideoInfoDefinition, MetaInfoMapped, VideoInfo):
    """
    Provides the mapping for VideoInfo when extending MetaInfo.
    """
    __table_args__ = dict(VideoInfoDefinition.__table_args__, extend_existing=True)