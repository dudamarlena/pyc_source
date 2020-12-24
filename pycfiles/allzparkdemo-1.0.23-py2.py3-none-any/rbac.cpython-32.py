# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/meta/rbac.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Dec 21, 2012\n\n@package: security - role based access control\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Ioan v. Pocol\n\nContains the SQL alchemy meta for rbac APIs.\n'
from ..api.rbac import Rbac, Role
from security.meta.metadata_security import Base
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String
from ally.support.sqlalchemy.mapper import validate

class RbacMapped(Base, Rbac):
    """
    Provides the mapping for base Rbac.
    """
    __tablename__ = 'rbac'
    __table_args__ = dict(mysql_engine='InnoDB')
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)


@validate
class RoleMapped(RbacMapped, Role):
    """
    Provides the mapping for Role rbac.
    """
    __tablename__ = 'rbac_role'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Name = Column('name', String(100), nullable=False, unique=True)
    Description = Column('description', String(255))
    rbacId = Column('fk_rbac_id', ForeignKey(RbacMapped.Id, ondelete='CASCADE'), primary_key=True)