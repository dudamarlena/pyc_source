# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/config.py
# Compiled at: 2019-09-28 14:40:45
# Size of source mod 2**32: 373 bytes
DEBUG = False
TESTING = False
SECRET_KEY = 'not so secret'
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
REDIS_URL = 'redis://localhost:6379/0'
ALLOWED_EXTENSIONS = {'md', 'txt'}
UPLOAD_DIRECTORY = None
MAX_CONTENT_LENGTH = 8388608
LIST_SIZE = 20