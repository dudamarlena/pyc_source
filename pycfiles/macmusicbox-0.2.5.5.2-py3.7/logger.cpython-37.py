# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/logger.py
# Compiled at: 2020-03-16 06:20:25
# Size of source mod 2**32: 705 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import logging
from future.builtins import open
from . import const
FILE_NAME = const.Constant.log_path
with open(FILE_NAME, 'a+') as (f):
    f.write('################################################################################')
    f.write('\n')

def getLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(FILE_NAME)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(lineno)s: %(message)s'))
    log.addHandler(fh)
    return log