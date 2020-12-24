# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/knownevent.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1893 bytes
from airflow.models.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from airflow.utils.sqlalchemy import UtcDateTime
from sqlalchemy.orm import relationship

class KnownEventType(Base):
    __tablename__ = 'known_event_type'
    id = Column(Integer, primary_key=True)
    know_event_type = Column(String(200))

    def __repr__(self):
        return self.know_event_type


class KnownEvent(Base):
    __tablename__ = 'known_event'
    id = Column(Integer, primary_key=True)
    label = Column(String(200))
    start_date = Column(UtcDateTime)
    end_date = Column(UtcDateTime)
    user_id = Column(Integer(), ForeignKey('users.id'))
    known_event_type_id = Column(Integer(), ForeignKey('known_event_type.id'))
    reported_by = relationship('User',
      cascade=False, cascade_backrefs=False, backref='known_events')
    event_type = relationship('KnownEventType',
      cascade=False,
      cascade_backrefs=False,
      backref='known_events')
    description = Column(Text)

    def __repr__(self):
        return self.label