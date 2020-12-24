# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/models.py
# Compiled at: 2013-03-11 22:09:01
import time
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from zope.sqlalchemy import ZopeTransactionExtension
from .generators import gen_token
from .generators import gen_client_id
from .generators import gen_client_secret
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Oauth2Client(Base):
    __tablename__ = 'oauth2_provider_clients'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(64), unique=True, nullable=False)
    client_secret = Column(String(64), unique=True, nullable=False)
    revoked = Column(Boolean, default=False)
    revocation_date = Column(DateTime)

    def __init__(self):
        self.client_id = gen_client_id()
        self.client_secret = gen_client_secret()

    def revoke(self):
        self.revoked = True
        self.revocation_date = datetime.utcnow()

    def isRevoked(self):
        return self.revoked


class Oauth2RedirectUri(Base):
    __tablename__ = 'oauth2_provider_redirect_uris'
    id = Column(Integer, primary_key=True)
    uri = Column(String(256), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey(Oauth2Client.id))
    client = relationship(Oauth2Client, backref=backref('redirect_uris'))

    def __init__(self, client, uri):
        self.client = client
        self.uri = uri


class Oauth2Code(Base):
    __tablename__ = 'oauth2_provider_codes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    authcode = Column(String(64), unique=True, nullable=False)
    expires_in = Column(Integer, nullable=False, default=600)
    revoked = Column(Boolean, default=False)
    revocation_date = Column(DateTime)
    creation_date = Column(DateTime, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey(Oauth2Client.id))
    client = relationship(Oauth2Client, backref=backref('authcode'))

    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id
        self.authcode = gen_token(self.client)

    def revoke(self):
        self.revoked = True
        self.revocation_date = datetime.utcnow()

    def isRevoked(self):
        expiry = time.mktime(self.create_date.timetuple()) + self.expires_in
        if datetime.frometimestamp(expiry) < datetime.utcnow():
            self.revoke()
        return self.revoked


class Oauth2Token(Base):
    __tablename__ = 'oauth2_provider_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(64), unique=True, nullable=False)
    refresh_token = Column(String(64), unique=True, nullable=False)
    expires_in = Column(Integer, nullable=False, default=3600)
    revoked = Column(Boolean, default=False)
    revocation_date = Column(DateTime)
    creation_date = Column(DateTime, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey(Oauth2Client.id))
    client = relationship(Oauth2Client, backref=backref('tokens'))

    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id
        self.access_token = gen_token(self.client)
        self.refresh_token = gen_token(self.client)

    def revoke(self):
        self.revoked = True
        self.revocation_date = datetime.utcnow()

    def isRevoked(self):
        expiry = time.mktime(self.creation_date.timetuple()) + self.expires_in
        if datetime.fromtimestamp(expiry) < datetime.utcnow():
            self.revoke()
        return self.revoked

    def refresh(self):
        """
        Generate a new token for this client.
        """
        cls = self.__class__
        self.revoke()
        return cls(self.client, self.user_id)

    def asJSON(self, **kwargs):
        token = {'access_token': self.access_token, 
           'refresh_token': self.refresh_token, 
           'user_id': self.user_id, 
           'expires_in': self.expires_in}
        kwargs.update(token)
        return kwargs


def initialize_sql(engine, settings):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)