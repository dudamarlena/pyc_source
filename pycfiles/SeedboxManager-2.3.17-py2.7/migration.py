# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/sqlalchemy/migration.py
# Compiled at: 2015-06-14 13:30:57
"""Provides ability to manage versions of database models"""
import os
from migrate import exceptions as versioning_exceptions
from migrate.versioning import api as versioning_api
from migrate.versioning.repository import Repository
from seedbox.db import exception
INIT_VERSION = 0
_REPO = None

def db_sync(engine, version=None, init_version=INIT_VERSION):
    """Upgrade or downgrade a database.

    Function runs the upgrade() or downgrade() functions in change scripts.

    :param engine:       SQLAlchemy engine instance for a given database
    :param version:      Database will upgrade/downgrade until this version.
                         If None - database will update to the latest
                         available version.
    :param init_version: Initial database version
    """
    if version is not None:
        try:
            version = int(version)
        except ValueError:
            raise exception.DbMigrationError(message='version should be an integer')

    current_version = db_version(engine, init_version)
    repository = _find_migrate_repo()
    if version is None or version > current_version:
        return versioning_api.upgrade(engine, repository, version)
    else:
        return versioning_api.downgrade(engine, repository, version)
        return


def db_version(engine, init_version=INIT_VERSION):
    """Show the current version of the repository.

    :param engine:  SQLAlchemy engine instance for a given database
    :param init_version:  Initial database version
    """
    repository = _find_migrate_repo()
    try:
        return versioning_api.db_version(engine, repository)
    except versioning_exceptions.DatabaseNotControlledError:
        db_version_control(engine, init_version)
        return versioning_api.db_version(engine, repository)


def db_version_control(engine, version=None):
    """Mark a database as under this repository's version control.

    Once a database is under version control, schema changes should
    only be done via change scripts in this repository.

    :param engine:  SQLAlchemy engine instance for a given database
    :param version:  Initial database version
    """
    versioning_api.version_control(engine, _find_migrate_repo(), version)


def _find_migrate_repo():
    """Get the project's change script repository"""
    global _REPO
    if _REPO is None:
        abspath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'migrate_repo')
        _REPO = Repository(abspath)
    return _REPO