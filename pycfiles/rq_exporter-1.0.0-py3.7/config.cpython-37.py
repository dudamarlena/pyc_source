# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rq_exporter/config.py
# Compiled at: 2020-04-23 10:04:39
# Size of source mod 2**32: 538 bytes
"""
RQ exporter configuration.

"""
import os
REDIS_URL = os.environ.get('RQ_REDIS_URL')
REDIS_HOST = os.environ.get('RQ_REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('RQ_REDIS_PORT', '6379')
REDIS_DB = os.environ.get('RQ_REDIS_DB', '0')
REDIS_PASS = os.environ.get('RQ_REDIS_PASS')
REDIS_PASS_FILE = os.environ.get('RQ_REDIS_PASS_FILE')
LOG_LEVEL = os.environ.get('RQ_EXPORTER_LOG_LEVEL', 'INFO').upper()