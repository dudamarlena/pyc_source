# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/log.py
# Compiled at: 2019-10-10 14:09:17
# Size of source mod 2**32: 416 bytes
import sys, logging
format = '%(message)s'
formatter = logging.Formatter(fmt=format)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.propagate = False
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

def set_verbose():
    logger.setLevel(logging.INFO)


def set_quiet():
    logger.setLevel(logging.ERROR)