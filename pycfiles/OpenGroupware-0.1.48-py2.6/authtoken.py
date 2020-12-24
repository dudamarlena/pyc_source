# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/authtoken.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from uuid import uuid4
from sqlalchemy import *
from base import Base, KVC

class AuthenticationToken(Base, KVC):
    """ An OpenGroupware Authentication Token object """
    __tablename__ = 'login_token'
    __entityName__ = 'AuthenticationToken'
    __internalName__ = 'AuthenticationToken'
    token = Column('token', String(4096), primary_key=True)
    account_id = Column('account_id', Integer, ForeignKey('person.company_id'), nullable=False)
    created = Column('creation_date', DateTime())
    touched = Column('touch_date', DateTime())
    expiration = Column('expiration_date', DateTime())
    timeout = Column('timeout', Integer)

    def __init__(self):
        self.token = ('{0}-{1}-{2}').format(uuid4(), uuid4(), uuid4())
        self.created = datetime.now()
        self.touched = datetime.now()
        self.timeout = 120
        self.expiration = None
        return