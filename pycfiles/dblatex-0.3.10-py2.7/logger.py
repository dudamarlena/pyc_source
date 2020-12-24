# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/core/logger.py
# Compiled at: 2017-04-03 18:58:57
import logging
VERBOSE = 1
NORMAL = 0
LESS_VERBOSE = -1
QUIET = -2

def logger(logname, level):
    loglevels = {QUIET: logging.ERROR - 1, LESS_VERBOSE: logging.WARNING - 1, 
       NORMAL: logging.INFO - 1, 
       VERBOSE: logging.DEBUG - 1}
    log = logging.getLogger(logname)
    log.setLevel(loglevels[level])
    console = logging.StreamHandler()
    format = logging.Formatter('%(message)s')
    console.setFormatter(format)
    log.addHandler(console)
    return log