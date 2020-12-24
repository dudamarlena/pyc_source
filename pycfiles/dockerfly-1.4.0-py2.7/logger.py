# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/logger.py
# Compiled at: 2015-03-05 02:24:14
import os, logging
from dockerfly.settings import LOG_ROOT
_fh = logging.FileHandler(os.path.join(LOG_ROOT, 'dockerflyd.log'))

def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _fh.setFormatter(formatter)
    logger.addHandler(_fh)
    return logger


def getFh():
    return _fh