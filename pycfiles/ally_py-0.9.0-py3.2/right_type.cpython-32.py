# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/meta/right_type.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Dec 21, 2012

@package: security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Contains the SQL alchemy meta for right API.
"""
from ..api.right_type import RightType
from .metadata_security import Base
from ally.support.sqlalchemy.mapper import validate
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String

@validate
class RightTypeMapped(Base, RightType):
    """
    Provides the mapping for RightType.
    """
    __tablename__ = 'security_right_type'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Name = Column('name', String(100), nullable=False, unique=True)
    Description = Column('description', String(255))