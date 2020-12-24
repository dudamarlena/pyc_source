# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/meta/right.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Dec 21, 2012\n\n@package: security\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Ioan v. Pocol\n\nContains the SQL alchemy meta for right API.\n'
from ..api.right import Right
from .metadata_security import Base
from .right_type import RightTypeMapped
from ally.support.sqlalchemy.mapper import validate
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String

@validate
class RightMapped(Base, Right):
    """
    Provides the mapping for Right.
    """
    __tablename__ = 'security_right'
    __table_args__ = (UniqueConstraint('fk_right_type_id', 'name', name='uix_type_name'),
     dict(mysql_engine='InnoDB', mysql_charset='utf8'))
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    Type = Column('fk_right_type_id', ForeignKey(RightTypeMapped.Id), nullable=False)
    Name = Column('name', String(150), nullable=False)
    Description = Column('description', String(255))