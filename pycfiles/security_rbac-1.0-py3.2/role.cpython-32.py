# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/meta/role.py
# Compiled at: 2013-11-05 07:07:00
"""
Created on Dec 21, 2012

@package: security - role based access control
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Contains the SQL alchemy meta for rbac APIs.
"""
from ..api.role import Role
from .rbac import WithRbac
from .rbac_intern import Rbac
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String

class RoleMapped(Rbac, WithRbac, Role):
    """
    Provides the mapping for Role rbac.
    """
    __tablename__ = 'rbac_role'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Name = Column('name', String(255), nullable=False, unique=True)
    Description = Column('description', String(255))
    rbacId = Column('fk_rbac_id', ForeignKey(Rbac.id), nullable=True, primary_key=True)