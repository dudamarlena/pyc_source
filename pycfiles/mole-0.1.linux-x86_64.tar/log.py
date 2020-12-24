# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/helper/log.py
# Compiled at: 2012-07-05 09:24:31
import sys, logging
LOG_FORMAT = '[%(asctime)s] %(message)s'
logging.basicConfig(format=LOG_FORMAT, stream=sys.stderr, level=logging.DEBUG)

def getLogger(ident='mole'):
    """Singleton to get an unique log object across any
    caller class or thread."""
    return logging.getLogger(ident)