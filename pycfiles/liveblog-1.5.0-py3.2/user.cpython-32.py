# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/user/meta/user.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Aug 23, 2011

@package: superdesk user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Contains the SQL alchemy meta for user API.
"""
from ..api.user import User
from ..meta.user_type import UserTypeMapped
from ally.container.binder_op import validateManaged, validateRequired
from ally.support.sqlalchemy.mapper import validate
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from superdesk.person.meta.person import PersonMapped

@validate(exclude=('Password', 'CreatedOn', 'Active', 'Type'))
class UserMapped(PersonMapped, User):
    """
    Provides the mapping for User entity.
    """
    __tablename__ = 'user'
    __table_args__ = (UniqueConstraint('name', name='uix_user_name'),
     dict(mysql_engine='InnoDB', mysql_charset='utf8'))
    Name = Column('name', String(150), nullable=False, unique=True)
    CreatedOn = Column('created_on', DateTime, nullable=False)
    Active = Column('active', Boolean, nullable=False, default=True)
    Type = association_proxy('type', 'Key')
    userId = Column('fk_person_id', ForeignKey(PersonMapped.Id, ondelete='CASCADE'), primary_key=True)
    password = Column('password', String(255), nullable=False)
    typeId = Column('fk_type_id', ForeignKey(UserTypeMapped.id, ondelete='RESTRICT'), nullable=False)
    type = relationship(UserTypeMapped, uselist=False, lazy='joined')


validateRequired(UserMapped.Password)
validateManaged(UserMapped.CreatedOn)
validateManaged(UserMapped.Active)