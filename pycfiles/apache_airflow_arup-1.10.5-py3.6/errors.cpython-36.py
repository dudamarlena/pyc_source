# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/errors.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1159 bytes
from sqlalchemy import Integer, Column, String, Text
from airflow.models.base import Base
from airflow.utils.sqlalchemy import UtcDateTime

class ImportError(Base):
    __tablename__ = 'import_error'
    id = Column(Integer, primary_key=True)
    timestamp = Column(UtcDateTime)
    filename = Column(String(1024))
    stacktrace = Column(Text)