# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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