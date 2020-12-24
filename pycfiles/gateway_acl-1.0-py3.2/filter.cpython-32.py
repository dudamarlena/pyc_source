# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/meta/filter.py
# Compiled at: 2013-11-05 07:07:00
"""
Created on Aug 19, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for ACL filter.
"""
from ..api.filter import Filter
from .acl_intern import WithPath, WithSignature
from .metadata_acl import Base
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column
from sqlalchemy.types import String

class FilterMapped(Base, WithPath, WithSignature, Filter):
    """
    Provides the ACL filter mapping.
    """
    __tablename__ = 'acl_filter'
    __table_args__ = dict(mysql_engine='InnoDB')
    Name = Column('name', String(255), nullable=False, unique=True)
    Signature = WithSignature.createSignature()
    id = Column('id', INTEGER(unsigned=True), primary_key=True)