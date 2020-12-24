# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/meta/meta_type.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Apr 19, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for meta type API.
"""
from ..api.meta_type import MetaType
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from superdesk.meta.metadata_superdesk import Base

class MetaTypeMapped(Base, MetaType):
    """
    Provides the mapping for MetaType.
    """
    __tablename__ = 'archive_meta_type'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Type = Column('type', String(50), nullable=False, unique=True)