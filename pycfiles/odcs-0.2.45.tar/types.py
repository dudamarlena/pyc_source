# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/types.py
# Compiled at: 2017-08-31 11:17:14


class PungiSourceType:
    KOJI_TAG = 1
    MODULE = 2
    REPO = 3


PUNGI_SOURCE_TYPE_NAMES = {'tag': PungiSourceType.KOJI_TAG, 
   'module': PungiSourceType.MODULE, 
   'repo': PungiSourceType.REPO}
COMPOSE_STATES = {'wait': 0, 
   'generating': 1, 
   'done': 2, 
   'removed': 3, 
   'failed': 4}
INVERSE_COMPOSE_STATES = {v:k for k, v in COMPOSE_STATES.items()}
COMPOSE_RESULTS = {'repository': 1, 
   'iso': 2, 
   'ostree': 4}
COMPOSE_FLAGS = {'no_flags': 0, 
   'no_deps': 1}
INVERSE_COMPOSE_FLAGS = {v:k for k, v in COMPOSE_FLAGS.items()}