# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtp/log.py
# Compiled at: 2012-10-05 17:37:25
"""Log routines for LDTP"""
from os import environ as env
import logging
AREA = 'ldtp.client'
ENV_LOG_LEVEL = 'LDTP_LOG_LEVEL'
ENV_LOG_OUT = 'LDTP_LOG_OUT'
log_level = getattr(logging, env.get(ENV_LOG_LEVEL, 'NOTSET'), logging.NOTSET)
logger = logging.getLogger(AREA)
if ENV_LOG_OUT not in env:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(name)-11s %(levelname)-8s %(message)s'))
else:
    handler = logging.FileHandler(env[ENV_LOG_OUT])
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
logger.addHandler(handler)
logger.setLevel(log_level)