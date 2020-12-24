# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oldcai/programs/python/webproject/django-in-memory-models/in_memory/ssdb/utils.py
# Compiled at: 2017-10-12 11:05:41
# Size of source mod 2**32: 386 bytes
import ssdb
from django.conf import settings
SSDB_HOST = getattr(settings, 'SSDB_HOST', 'localhost')
SSDB_PORT = getattr(settings, 'SSDB_PORT', 8888)
SSDB_AUTH = getattr(settings, 'SSDB_AUTH', '')

def get_ssdb_client():
    ssdb_client = ssdb.Client(SSDB_HOST, SSDB_PORT)
    if SSDB_AUTH:
        ssdb_client.auth(SSDB_AUTH)
    return ssdb_client


ssdb_client = get_ssdb_client()