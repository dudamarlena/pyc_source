# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/conf/defaults.py
# Compiled at: 2012-12-12 10:05:53
from django.conf import settings
THUMBNAIL_DEBUG = False
THUMBNAIL_BACKEND = 'sorl.thumbnail.base.ThumbnailBackend'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
THUMBNAIL_KEY_DBCOLUMN = 'key'
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'
THUMBNAIL_CONVERT = 'convert'
THUMBNAIL_IDENTIFY = 'identify'
THUMBNAIL_STORAGE = settings.DEFAULT_FILE_STORAGE
THUMBNAIL_REDIS_DB = 0
THUMBNAIL_REDIS_PASSWORD = ''
THUMBNAIL_REDIS_HOST = 'localhost'
THUMBNAIL_REDIS_PORT = 6379
THUMBNAIL_REDIS_UNIX_SOCKET_PATH = None
THUMBNAIL_CACHE_TIMEOUT = 315360000
THUMBNAIL_KEY_PREFIX = 'sorl-thumbnail'
THUMBNAIL_PREFIX = 'cache/'
THUMBNAIL_FORMAT = 'JPEG'
THUMBNAIL_PRESERVE_FORMAT = False
THUMBNAIL_COLORSPACE = 'RGB'
THUMBNAIL_UPSCALE = True
THUMBNAIL_QUALITY = 95
THUMBNAIL_PROGRESSIVE = True
THUMBNAIL_ORIENTATION = True
THUMBNAIL_DUMMY = False
THUMBNAIL_DUMMY_SOURCE = 'http://dummyimage.com/%(width)sx%(height)s'
THUMBNAIL_DUMMY_RATIO = 1.5