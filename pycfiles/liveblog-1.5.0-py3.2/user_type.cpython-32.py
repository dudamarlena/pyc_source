# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/user/meta/user_type.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on May 27, 2013

@package: superdesk user
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Martin Saturka

Contains the SQL alchemy meta for user type API.
"""
from ..api.user_type import UserType
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from superdesk.meta.metadata_superdesk import Base

class UserTypeMapped(Base, UserType):
    """
    Provides the mapping for UserType.
    """
    __tablename__ = 'user_type'
    __table_args__ = dict(mysql_engine='InnoDB')
    Key = Column('key', String(255), nullable=False, unique=True)
    id = Column('id', INTEGER(unsigned=True), primary_key=True)