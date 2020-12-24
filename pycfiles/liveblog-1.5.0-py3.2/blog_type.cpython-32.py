# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/livedesk/meta/blog_type.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Aug 30, 2012

@package: livedesk
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Contains the SQL alchemy meta for blog type API.
"""
from ally.support.sqlalchemy.mapper import validate
from superdesk.meta.metadata_superdesk import Base
from livedesk.api.blog_type import BlogType
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String

@validate
class BlogTypeMapped(Base, BlogType):
    """
    Provides the mapping for Blog.
    """
    __tablename__ = 'livedesk_blog_type'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Name = Column('name', String(255), nullable=False)