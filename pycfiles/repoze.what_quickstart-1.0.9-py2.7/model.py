# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/fixture/model.py
# Compiled at: 2011-11-29 15:47:41
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

def dummy_validate_password(val):
    pass


def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)


group_permission_table = Table('tg_group_permission', metadata, Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE')), Column('permission_id', Integer, ForeignKey('tg_permission.permission_id', onupdate='CASCADE', ondelete='CASCADE')))
user_group_table = Table('tg_user_group', metadata, Column('user_id', Integer, ForeignKey('tg_user.user_id', onupdate='CASCADE', ondelete='CASCADE')), Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE')))

class Group(DeclarativeBase):
    """An ultra-simple group definition.
    """
    __tablename__ = 'tg_group'
    group_id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(Unicode(16), unique=True)
    users = relation('User', secondary=user_group_table, backref='groups')

    def __init__(self, group_name=None, display_name=''):
        if group_name is not None:
            self.group_name = group_name
        self.display_name = display_name
        return

    def __repr__(self):
        return '<Group: name=%s>' % self.group_name


class User(DeclarativeBase):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    __tablename__ = 'tg_user'
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


class Permission(DeclarativeBase):
    """A relationship that determines what each Group can do
    """
    __tablename__ = 'tg_permission'
    permission_id = Column(Integer, autoincrement=True, primary_key=True)
    permission_name = Column(Unicode(16), unique=True)
    groups = relation(Group, secondary=group_permission_table, backref='permissions')