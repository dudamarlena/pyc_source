# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/heytitle/projects/attacut-project/attacut/artifacts/__init__.py
# Compiled at: 2019-09-08 07:59:58
# Size of source mod 2**32: 367 bytes
import os
from attacut import logger
log = logger.get_logger(__name__)
artifact_dir = os.path.dirname(__file__)

def get_path(name: str) -> str:
    if name in ('attacut-c', 'attacut-sc'):
        return f"{artifact_dir}/{name}"
    log.info('model_path: %s' % name)
    return name