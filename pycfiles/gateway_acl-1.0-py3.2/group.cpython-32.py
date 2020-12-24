# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/meta/group.py
# Compiled at: 2013-11-05 07:07:00
"""
Created on Aug 19, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for ACL group.
"""
from ..api.group import Group
from .acl import WithAclAccess
from .compensate import WithCompensate
from .metadata_acl import Base
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Boolean

class GroupMapped(Base, Group):
    """
    Provides the ACL group mapping.
    """
    __tablename__ = 'acl_group'
    __table_args__ = dict(mysql_engine='InnoDB')
    Name = Column('name', String(255), nullable=False, unique=True)
    IsAnonymous = Column('is_anonymous', Boolean, nullable=False, default=False)
    Description = Column('description', String(255))
    id = Column('id', INTEGER(unsigned=True), primary_key=True)


class GroupAccess(Base, WithAclAccess):
    """
    Provides the Group to Access mapping.
    """
    __tablename__ = 'acl_group_access'
    aclId = Column('fk_group_id', ForeignKey(GroupMapped.id, ondelete='CASCADE'))


class GroupCompensate(Base, WithCompensate):
    """
    Provides the Group to Compensate mapping.
    """
    __tablename__ = 'acl_group_compensate'
    aclAccessId = Column('fk_group_access_id', ForeignKey(GroupAccess.id, ondelete='CASCADE'))