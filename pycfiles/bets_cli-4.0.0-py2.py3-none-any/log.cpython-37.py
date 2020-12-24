# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\utils\log.py
# Compiled at: 2019-05-04 21:48:57
# Size of source mod 2**32: 360 bytes
import logging
FORMAT = '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
_log = logging.getLogger('bets-cli')
debug = _log.debug
info = _log.info
warning = _log.warning
exception = _log.exception
error = _log.error

def init(level=logging.DEBUG):
    logging.basicConfig(format=FORMAT, level=level)
    debug('log initialized!')