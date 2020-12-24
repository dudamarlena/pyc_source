# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/settings/local_settings.py
# Compiled at: 2015-02-18 13:07:40
# Size of source mod 2**32: 1248 bytes
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine', 
             'URL': 'https://bofur-us-east-1.searchly.com:80/', 
             'INDEX_NAME': 'goldwater', 
             'TIMEOUT': 300, 
             'INCLUDE_SPELLING': True, 
             'BATCH_SIZE': 100, 
             'KWARGS': {'http_auth': 'site:49970ebb2fda35c0ed81e481a07477ef'}}}