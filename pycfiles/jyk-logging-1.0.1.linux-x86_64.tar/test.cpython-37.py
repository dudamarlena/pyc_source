# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyongkang/anaconda3/lib/python3.7/site-packages/jyk/logging/test.py
# Compiled at: 2020-03-28 09:38:02
# Size of source mod 2**32: 286 bytes
import logging
log = logging.getLogger(__name__)

def makeLogs():
    for i in range(3):
        log.info('test log info {}'.format(i))

    for i in range(3):
        log.warning('test log warning {}'.format(i))

    for i in range(3):
        log.error('test log error {}'.format(i))