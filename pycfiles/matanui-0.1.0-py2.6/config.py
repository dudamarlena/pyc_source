# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/matanui/config.py
# Compiled at: 2011-01-12 20:19:00
"""
Configuration of MataNui server.

TODO: Should this be replaced by ConfigObj?
"""
__author__ = 'Guy K. Kloss <Guy.Kloss@aut.ac.nz>'
STORAGE_BACKEND = 'matanui.mongogridfs.MongoGridFS'
GRIDFS_HOST = 'localhost'
GRIDFS_PORT = 27017
GRIDFS_DB_NAME = 'test'
GRIDFS_BUCKET = 'fs'
GRIDFS_USER = None
GRIDFS_PASSWORD = None
UMASK = 73
DEFAULT_PERMISSIONS = 420
VERBOSE_INFO = True