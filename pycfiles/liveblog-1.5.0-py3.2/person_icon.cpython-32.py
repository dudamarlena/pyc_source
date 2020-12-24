# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/person_icon/meta/person_icon.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Nov 22, 2012

@package: superdesk person icon
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Contains the SQL alchemy meta for person icon API.
"""
from sqlalchemy.schema import Column, ForeignKey
from superdesk.person.meta.person import PersonMapped
from superdesk.person_icon.api.person_icon import PersonIcon
from superdesk.meta.metadata_superdesk import Base
from superdesk.media_archive.meta.meta_data import MetaDataMapped
from sqlalchemy.ext.hybrid import hybrid_property

class PersonIconMapped(Base, PersonIcon):
    """
    Provides the mapping for PersonIcon entity.
    """
    __tablename__ = 'person_icon'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    Id = Column('fk_person_id', ForeignKey(PersonMapped.Id, ondelete='CASCADE'), primary_key=True)
    MetaData = Column('fk_metadata_id', ForeignKey(MetaDataMapped.Id, ondelete='CASCADE'))

    @hybrid_property
    def Person(self):
        return self.Id

    Person.expression(lambda cls: cls.Id)