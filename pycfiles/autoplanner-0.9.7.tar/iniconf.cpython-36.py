# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/iniconf.py
# Compiled at: 2017-07-26 13:19:11
# Size of source mod 2**32: 416 bytes
from djangofloor.iniconf import INI_MAPPING as DEFAULTS, OptionParser
__author__ = 'Matthieu Gallet'
INI_MAPPING = DEFAULTS + [OptionParser('REDIS_HOST', 'celery.redis_host'),
 OptionParser('REDIS_PORT', 'celery.redis_port'),
 OptionParser('BROKER_DB', 'celery.redis_db', int),
 OptionParser('REFRESH_DURATION', 'global.refresh_duration')]