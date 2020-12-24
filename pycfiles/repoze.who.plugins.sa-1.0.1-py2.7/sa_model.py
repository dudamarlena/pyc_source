# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/fixture/sa_model.py
# Compiled at: 2011-11-23 17:56:16
"""Mock SQLAlchemy-powered model definition."""
from hashlib import sha1
from datetime import datetime
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Unicode, UnicodeText, Integer, DateTime, Boolean, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relation, backref, synonym
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata

class DummyValidateException(BaseException):
    """Dummy error used for dummy_validate."""
    pass


def dummy_validate(password):
    """Dummy validation function that will only raise a dummy error to know
    that we reached this execution path."""
    raise DummyValidateException()


def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)


class User(DeclarativeBase):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    __tablename__ = 'user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True)
    _password = Column('password', Unicode(40))

    def _set_password(self, password):
        """encrypts password on the fly."""
        self._password = self.__encrypt_password(password)

    def _get_password(self):
        """returns password"""
        return self._password

    password = synonym('password', descriptor=property(_get_password, _set_password))

    def __encrypt_password(self, password):
        """Hash the given password with SHA1."""
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        hashed_password = sha1()
        hashed_password.update(password_8bit)
        hashed_password = hashed_password.hexdigest()
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')
        return hashed_password

    def validate_password(self, password):
        """Check the password against existing credentials.
        this method _MUST_ return a boolean.

        @param password: the password that was provided by the user to
        try and authenticate. This is the clear text version that we will
        need to match against the (possibly) encrypted one in the database.
        @type password: unicode object
        """
        return self.password == self.__encrypt_password(password)


class Member(DeclarativeBase):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    
    It uses non-default attributes, so it'll have to be translated.
    
    """
    __tablename__ = 'member'
    member_id = Column(Integer, autoincrement=True, primary_key=True)
    member_name = Column(Unicode(16), unique=True)
    _password = Column('password', Unicode(40))

    def _set_password(self, password):
        """encrypts password on the fly."""
        self._password = self.__encrypt_password(password)

    def _get_password(self):
        """returns password"""
        return self._password

    password = synonym('password', descriptor=property(_get_password, _set_password))

    def __encrypt_password(self, password):
        """Hash the given password with SHA1."""
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        hashed_password = sha1()
        hashed_password.update(password_8bit)
        hashed_password = hashed_password.hexdigest()
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')
        return hashed_password

    def verify_pass(self, password):
        """Check the password against existing credentials.
        this method _MUST_ return a boolean.
        """
        return self.password == self.__encrypt_password(password)