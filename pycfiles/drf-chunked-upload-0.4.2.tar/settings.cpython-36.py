# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/phoetrymaster/Development/CSAR/drf-chunked-upload/drf_chunked_upload/settings.py
# Compiled at: 2017-02-26 16:17:08
# Size of source mod 2**32: 1264 bytes
from datetime import timedelta
from django.conf import settings
DEFAULT_EXPIRATION_DELTA = timedelta(days=1)
EXPIRATION_DELTA = getattr(settings, 'DRF_CHUNKED_UPLOAD_EXPIRATION_DELTA', DEFAULT_EXPIRATION_DELTA)
DEFAULT_UPLOAD_PATH = 'chunked_uploads/%Y/%m/%d'
UPLOAD_PATH = getattr(settings, 'DRF_CHUNKED_UPLOAD_PATH', DEFAULT_UPLOAD_PATH)
COMPLETE_EXT = getattr(settings, 'DRF_CHUNKED_UPLOAD_COMPLETE_EXT', '.done')
INCOMPLETE_EXT = getattr(settings, 'DRF_CHUNKED_UPLOAD_INCOMPLETE_EXT', '.part')
STORAGE = getattr(settings, 'DRF_CHUNKED_UPLOAD_STORAGE_CLASS', lambda : None)()
ABSTRACT_MODEL = getattr(settings, 'DRF_CHUNKED_UPLOAD_ABSTRACT_MODEL', True)
USER_RESTRICTED = getattr(settings, 'DRF_CHUNKED_UPLOAD_USER_RESTRICED', True)
DEFAULT_MAX_BYTES = None
MAX_BYTES = getattr(settings, 'DRF_CHUNKED_UPLOAD_MAX_BYTES', DEFAULT_MAX_BYTES)