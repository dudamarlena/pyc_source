# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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