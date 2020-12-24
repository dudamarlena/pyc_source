# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/meta/security_intern.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Jan 21, 2013

@package: superdesk security
@copyright 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for rbac user internal mappings.
"""
from security.rbac.meta.rbac import RbacMapped
from sqlalchemy.schema import Column, ForeignKey
from superdesk.user.meta.user import UserMapped

class RbacUser(RbacMapped):
    """
    Provides the mapping for user Rbac.
    """
    __tablename__ = 'user_rbac'
    __table_args__ = dict(mysql_engine='InnoDB')
    userId = Column('fk_user_id', ForeignKey(UserMapped.Id), primary_key=True, unique=True)
    rbac = Column('fk_rbac_id', ForeignKey(RbacMapped.Id), primary_key=True, unique=True)