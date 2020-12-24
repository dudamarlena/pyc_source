# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/user.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1302 bytes
from sqlalchemy import Column, String, Integer, Boolean
from airflow.models.base import Base, ID_LEN

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column((String(ID_LEN)), unique=True)
    email = Column(String(500))
    superuser = Column((Boolean()), default=False)

    def __repr__(self):
        return self.username

    def get_id(self):
        return str(self.id)

    def is_superuser(self):
        return self.superuser