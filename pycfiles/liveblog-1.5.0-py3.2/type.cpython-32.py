# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/source/meta/type.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on May 2, 2012

@package: superdesk source
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy meta for source type API.
"""
from ..api.type import SourceType
from ally.internationalization import _
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.orm.mapper import reconstructor
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from superdesk.meta.metadata_superdesk import Base

class SourceTypeMapped(Base, SourceType):
    """
    Provides the mapping for SourceType.
    """
    __tablename__ = 'source_type'
    __table_args__ = dict(mysql_engine='InnoDB')
    Key = Column('key', String(100), nullable=False, unique=True)
    id = Column('id', INTEGER(unsigned=True), primary_key=True)

    @reconstructor
    def init_on_load(self):
        self.Name = _(self.Key)