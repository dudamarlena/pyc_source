# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/log/bin/release/sudosh/config.py
# Compiled at: 2014-06-03 11:14:08
import os
CRSF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'
SUDOSHPATH = '/var/log/sudosh/'
PAGE_SIZE = 5
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')