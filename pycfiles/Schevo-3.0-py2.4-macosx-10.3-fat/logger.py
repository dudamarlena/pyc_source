# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/store/logger.py
# Compiled at: 2007-03-21 14:34:41
"""$URL: svn+ssh://svn.mems-exchange.org/repos/trunk/durus/logger.py $
$Id: logger.py 1475 2005-12-01 17:36:40Z mscott $
"""
import sys
from logging import getLogger, StreamHandler, Formatter, INFO
logger = getLogger('durus')
log = logger.log

def direct_output(file):
    logger.handlers[:] = []
    handler = StreamHandler(file)
    handler.setFormatter(Formatter('%(message)s'))
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(INFO)
    if file is sys.__stderr__:
        return
    if sys.stdout is sys.__stdout__:
        sys.stdout = file
    if sys.stderr is sys.__stderr__:
        sys.stderr = file


if not logger.handlers:
    direct_output(sys.stderr)

def is_logging(level):
    return logger.getEffectiveLevel() <= level