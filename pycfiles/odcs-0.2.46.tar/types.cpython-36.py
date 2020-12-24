# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/common/odcs/common/types.py
# Compiled at: 2017-12-08 06:56:10
# Size of source mod 2**32: 2623 bytes


class PungiSourceType:
    KOJI_TAG = 1
    MODULE = 2
    REPO = 3
    PULP = 4
    RAW_CONFIG = 5


PUNGI_SOURCE_TYPE_NAMES = {'tag':PungiSourceType.KOJI_TAG, 
 'module':PungiSourceType.MODULE, 
 'repo':PungiSourceType.REPO, 
 'pulp':PungiSourceType.PULP, 
 'raw_config':PungiSourceType.RAW_CONFIG}
INVERSE_PUNGI_SOURCE_TYPE_NAMES = {v:k for k, v in PUNGI_SOURCE_TYPE_NAMES.items()}
COMPOSE_STATES = {'wait':0, 
 'generating':1, 
 'done':2, 
 'removed':3, 
 'failed':4}
INVERSE_COMPOSE_STATES = {v:k for k, v in COMPOSE_STATES.items()}
COMPOSE_RESULTS = {'repository':1, 
 'iso':2, 
 'ostree':4, 
 'boot.iso':8}
COMPOSE_FLAGS = {'no_flags':0, 
 'no_deps':1, 
 'no_inheritance':2}
INVERSE_COMPOSE_FLAGS = {v:k for k, v in COMPOSE_FLAGS.items()}