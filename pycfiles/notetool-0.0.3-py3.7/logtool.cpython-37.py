# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notetool/logtool.py
# Compiled at: 2019-12-09 07:59:50
# Size of source mod 2**32: 233 bytes
import logging
logging.basicConfig(format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')

def log(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger