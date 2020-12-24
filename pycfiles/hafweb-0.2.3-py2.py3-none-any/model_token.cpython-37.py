# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\model\model_token.py
# Compiled at: 2019-04-16 02:17:35
# Size of source mod 2**32: 513 bytes
from hafweb.config import Base
from sqlalchemy import *
import json

class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    user_id = Column(Integer)
    token = Column(String)

    def __repr__(self):
        attr_list = [
         'id', 'username', 'password', 'user_id', 'token']
        rev = {}
        for attr in attr_list:
            rev[attr] = getattr(self, attr)

        return json.dumps(rev)