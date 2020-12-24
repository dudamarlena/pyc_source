# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/fixture/elixir_model.py
# Compiled at: 2011-05-02 14:52:14
"""Mock Elixir-powered model definition."""
from hashlib import sha1
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
import elixir
from elixir import Entity, Field
from elixir import DateTime, Unicode
from elixir import using_options
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
metadata = elixir.metadata
elixir.session = DBSession

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)
    metadata.bind = engine


class User(Entity):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    using_options(tablename='user', auto_primarykey='user_id')
    user_name = Field(Unicode(16), required=True, unique=True)
    _password = Field(Unicode(40), colname='password', required=True)

    def _set_password(self, password):
        """encrypts password on the fly"""
        self._password = self.__encrypt_password(password)

    def _get_password(self):
        """returns password"""
        return self._password

    password = descriptor = property(_get_password, _set_password)

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