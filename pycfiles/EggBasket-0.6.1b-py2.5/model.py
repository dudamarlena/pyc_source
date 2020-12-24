# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/model.py
# Compiled at: 2008-07-13 16:55:56
import os, re
from datetime import datetime
from os.path import basename, isdir, join, getmtime, getsize
import pkg_resources
pkg_resources.require('SQLAlchemy>=0.3.10')
import turbogears as tg
from turbogears.database import metadata, mapper
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy import String, Unicode, Integer, DateTime
from sqlalchemy.exceptions import InvalidRequestError
from eggbasket.util import is_package_file
from eggbasket.pkginfo import read_pkg_info

class Package(object):
    """A simple container class for holding information about package releases.
    """
    _version_rx = re.compile('-(\\d*.\\d*(.\\d)?)')

    def __str__(self):
        return '<PackageInfo name=%s>' % self.name

    def __init__(self, path, name=None):
        self.path = path
        if name:
            self.name = name
        else:
            self.name = basename(path)
        self.modified = datetime.fromtimestamp(getmtime(path))
        self._releases = None
        self._files = None
        return

    def _get_stats(self):
        return (len(self.releases), sum([ len(l) for l in self.files.values() ]))

    stats = property(_get_stats)

    def _get_releases(self):
        if self._releases is None:
            self._find_releases()
        return self._releases

    releases = property(_get_releases)

    def _get_files(self):
        if self._files is None:
            self._find_releases()
        return self._files

    files = property(_get_files)

    def _find_releases(self):
        self._releases = list()
        self._files = dict()
        known_extensions = tg.config.get('eggbasket.package_extensions', [])
        for filename in os.listdir(self.path):
            filepath = join(self.path, filename)
            if isdir(filepath) or not is_package_file(filepath):
                continue
            if 'dev_' in filename:
                version = 'dev'
            else:
                version = None
                mo = self._version_rx.search(filename)
                if mo:
                    version = mo.group(1)
                else:
                    version = 'unknown'
            if version not in self._releases:
                self._releases.append(version)
                self._files[version] = list()
            self._files[version].append(dict(name=filename, size=getsize(filepath), modified=datetime.fromtimestamp(getmtime(filepath))))

        self._releases.sort(reverse=True)
        self._files.get('dev', []).sort(reverse=True)
        return

    @staticmethod
    def package_info(filename):
        return read_pkg_info(filename)


visits_table = Table('visit', metadata, Column('visit_key', String(40), primary_key=True), Column('created', DateTime, nullable=False, default=datetime.now), Column('expiry', DateTime))
visit_identity_table = Table('visit_identity', metadata, Column('visit_key', String(40), primary_key=True), Column('user_id', Integer, ForeignKey('tg_user.user_id'), index=True))
groups_table = Table('tg_group', metadata, Column('group_id', Integer, primary_key=True), Column('group_name', Unicode(16), unique=True), Column('display_name', Unicode(255)), Column('created', DateTime, default=datetime.now))
users_table = Table('tg_user', metadata, Column('user_id', Integer, primary_key=True), Column('user_name', Unicode(16), unique=True), Column('email_address', Unicode(255), unique=True), Column('display_name', Unicode(255)), Column('password', Unicode(40)), Column('created', DateTime, default=datetime.now))
permissions_table = Table('permission', metadata, Column('permission_id', Integer, primary_key=True), Column('permission_name', Unicode(16), unique=True), Column('description', Unicode(255)))
user_group_table = Table('user_group', metadata, Column('user_id', Integer, ForeignKey('tg_user.user_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True), Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))
group_permission_table = Table('group_permission', metadata, Column('group_id', Integer, ForeignKey('tg_group.group_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True), Column('permission_id', Integer, ForeignKey('permission.permission_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True))

class Visit(object):
    """A visit to your site."""

    @classmethod
    def lookup_visit(cls, visit_key):
        return cls.query.get(visit_key)


class VisitIdentity(object):
    """A Visit that is link to a User object"""
    pass


class Group(object):
    """An ultra-simple group definition."""
    pass


class User(object):
    """Reasonably basic User definition.

    Probably would want additional attributes.
    """

    @property
    def permissions(self):
        p = set()
        for g in self.groups:
            p |= set(g.permissions)

        return p

    @classmethod
    def by_email_address(cls, email):
        """Returns User object with given 'email_address' attribute value.

        A class method that can be used to search users
        based on their email addresses since it is unique.

        """
        return cls.query.filter_by(email_address=email).first()

    @classmethod
    def by_user_name(cls, username):
        """Returns User object with given 'user_name' attribute value."""
        return cls.query.filter_by(user_name=username).first()

    def _set_password(self, password):
        """Encrypts password on the fly using the encryption
        algo defined in the configuration.

        """
        password = tg.identity.encrypt_password(password)
        try:
            password = password.decode('utf-8')
        except:
            pass

        self._password = password

    def _get_password(self):
        """Returns password."""
        return self._password

    password = property(_get_password, _set_password)


class Permission(object):
    """A relationship that determines what each Group can do."""
    pass


mapper(Visit, visits_table)
mapper(VisitIdentity, visit_identity_table, properties=dict(users=relation(User, backref='visit_identity')))
mapper(User, users_table, properties=dict(_password=users_table.c.password))
mapper(Group, groups_table, properties=dict(users=relation(User, secondary=user_group_table, backref='groups')))
mapper(Permission, permissions_table, properties=dict(groups=relation(Group, secondary=group_permission_table, backref='permissions')))