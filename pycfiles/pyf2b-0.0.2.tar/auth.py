# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/model/auth.py
# Compiled at: 2010-05-21 08:57:50
__doc__ = "\nAuth* related model.\n\nThis is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are\ndefined.\n\nIt's perfectly fine to re-use this definition in the pyf.services application,\nthough.\n\n"
import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\nIf you are on python2.4 this library is not part of python. Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym
from pyf.services.model import DeclarativeBase, metadata, DBSession
__all__ = [
 'User', 'Group', 'Permission']
group_permission_table = Table('tg_group_permission', metadata, Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE')), Column('permission_id', Integer, ForeignKey('tg_permission.permission_id', onupdate='CASCADE', ondelete='CASCADE')))
user_group_table = Table('tg_user_group', metadata, Column('user_id', Integer, ForeignKey('tg_user.user_id', onupdate='CASCADE', ondelete='CASCADE')), Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE')))

class Group(DeclarativeBase):
    """
    Group definition for :mod:`repoze.what`.
    
    Only the ``group_name`` column is required by :mod:`repoze.what`.
    
    """
    __tablename__ = 'tg_group'
    group_id = Column(Integer, autoincrement=True, primary_key=True)
    group_name = Column(Unicode(16), unique=True, nullable=False)
    display_name = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    users = relation('User', secondary=user_group_table, backref='groups')

    def __repr__(self):
        return '<Group: name=%s>' % self.group_name

    def __unicode__(self):
        return self.group_name

    @property
    def id(self):
        return self.group_id


class User(DeclarativeBase):
    """
    User definition.
    
    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.
    
    """
    __tablename__ = 'tg_user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True, nullable=False)
    email_address = Column(Unicode(255), unique=True, nullable=False, info={'rum': {'field': 'Email'}})
    display_name = Column(Unicode(255))
    _password = Column('password', Unicode(80), info={'rum': {'field': 'Password'}})
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<User: email="%s", display name="%s">' % (
         self.email_address, self.display_name)

    def __unicode__(self):
        return self.display_name or self.user_name

    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)

        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter(cls.email_address == email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter(cls.user_name == username).first()

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')
        self._password = hashed_password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password, _set_password))

    @property
    def id(self):
        return self.user_id

    def validate_password(self, password):
        """
        Check the password against existing credentials.
        
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

    primary_key = [
     user_id]


class Permission(DeclarativeBase):
    """
    Permission definition for :mod:`repoze.what`.
    
    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    
    """
    __tablename__ = 'tg_permission'
    permission_id = Column(Integer, autoincrement=True, primary_key=True)
    permission_name = Column(Unicode(16), unique=True, nullable=False)
    description = Column(Unicode(255))
    groups = relation(Group, secondary=group_permission_table, backref='permissions')

    def __repr__(self):
        return '<Permission: name=%s>' % self.permission_name

    def __unicode__(self):
        return self.permission_name

    @property
    def id(self):
        return self.permission_id