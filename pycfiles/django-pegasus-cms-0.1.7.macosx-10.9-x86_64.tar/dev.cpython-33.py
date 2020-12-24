# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/settings/dev.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 770 bytes
from __future__ import absolute_import, division
from .base import *
DEBUG = False
TEMPLATE_DEBUG = False
INSTALLED_APPS += ('storages', )
AWS_ACCESS_KEY_ID = 'AKIAJSWBP2Y3VOSVNGBQ'
AWS_SECRET_ACCESS_KEY = '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'
CELERITY_STATICFILES_BUCKET = 'dev-static.pegasus.org'
CELERITY_MEDIAFILES_BUCKET = 'dev-media.pegasus.org'
AWS_S3_URL_PROTOCOL = ''
DEFAULT_FILE_STORAGE = 'pegasus.storage.CelerityMediaFilesStorage'
STATICFILES_STORAGE = 'pegasus.storage.CelerityStaticFilesStorage'
STATIC_URL = '{s3_protocol}//s3.amazonaws.com/{s3_bucket}/'.format(s3_protocol=AWS_S3_URL_PROTOCOL, s3_bucket=CELERITY_STATICFILES_BUCKET)
try:
    from local_settings import *
except:
    pass