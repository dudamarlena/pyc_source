# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/base/persistent_store.py
# Compiled at: 2015-01-11 00:13:45
"""
********************************************************************************
* Name: persistent store
* Author: Nathan Swain
* Created On: September 22, 2014
* Copyright: (c) Brigham Young University 2014
* License: BSD 2-Clause
********************************************************************************
"""
import sys
from django.conf import settings
from sqlalchemy import create_engine

class PersistentStore(object):
    """
    An object that stores the registration data for a Tethys Persistent Store.

    Args:
      name(string): The name of the persistent store.
      initializer(string): Path to the initialization function for the persistent store. Use dot-notation with a colon delineating the function (e.g.: "foo.bar:function").
      spatial(bool, optional): PostGIS spatial extension will be enabled on the persistent store if True. Defaults to False.
      postgis(bool, deprecated): PostGIS spatial extension will be enabled on the persistent store if True. Defaults to False. Deprecated, use spatial instead.

    """

    def __init__(self, name, initializer, spatial=False, postgis=False):
        """
        Constructor
        """
        self.name = name
        self.initializer = initializer
        self.postgis = postgis
        self.spatial = spatial

    def __repr__(self):
        """
        String representation
        """
        if hasattr(self, 'spatial'):
            return ('<Persistent Store: name={0}, initializer={1}, spatial={2}>').format(self.name, self.initializer, self.spatial)
        else:
            return ('<Persistent Store: name={0}, initializer={1}, spatial={2}>').format(self.name, self.initializer, self.postgis)


def get_persistent_store_engine(app_name, persistent_store_name):
    """
    Creates an SQLAlchemy engine object for the app and persistent store given.

    Args:
      app_name(string): Name of the app to which the persistent store belongs. More specifically, the app package name.
      persistent_store_name(string): Name of the persistent store for which to retrieve the engine.

    Returns:
      object: An SQLAlchemy engine object for the persistent store requested.
    """
    unique_store_name = ('_').join([app_name, persistent_store_name])
    database_manager_db = settings.TETHYS_DATABASES['tethys_db_manager']
    database_manager_url = ('postgresql://{0}:{1}@{2}:{3}/{4}').format(database_manager_db['USER'] if 'USER' in database_manager_db else 'tethys_db_manager', database_manager_db['PASSWORD'] if 'PASSWORD' in database_manager_db else 'pass', database_manager_db['HOST'] if 'HOST' in database_manager_db else '127.0.0.1', database_manager_db['PORT'] if 'PORT' in database_manager_db else '5435', database_manager_db['NAME'] if 'NAME' in database_manager_db else 'tethys_db_manager')
    engine = create_engine(database_manager_url)
    connection = engine.connect()
    existing_dbs_statement = '\n                             SELECT d.datname as name\n                             FROM pg_catalog.pg_database d\n                             LEFT JOIN pg_catalog.pg_user u ON d.datdba = u.usesysid\n                             ORDER BY 1;\n                             '
    existing_dbs = connection.execute(existing_dbs_statement)
    existing_db_names = []
    for existing_db in existing_dbs:
        existing_db_names.append(existing_db.name)

    if unique_store_name in existing_db_names:
        database_manager_db = settings.TETHYS_DATABASES['tethys_db_manager']
        persistent_store_url = ('postgresql://{0}:{1}@{2}:{3}/{4}').format(database_manager_db['USER'] if 'USER' in database_manager_db else 'tethys_db_manager', database_manager_db['PASSWORD'] if 'PASSWORD' in database_manager_db else 'pass', database_manager_db['HOST'] if 'HOST' in database_manager_db else '127.0.0.1', database_manager_db['PORT'] if 'PORT' in database_manager_db else '5435', unique_store_name)
        return create_engine(persistent_store_url)
    print ('ERROR: No persistent store "{0}" for app "{1}". Make sure you register the persistent store in app.py and reinstall app.').format(persistent_store_name, app_name)
    sys.exit()