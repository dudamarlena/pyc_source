# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\common.py
# Compiled at: 2019-06-15 04:32:14
# Size of source mod 2**32: 223 bytes
import logging
FORMAT = '[%(levelname)s]: %(message)s'
MAX_LOG_LEVEL = 3
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
levels = {0:40, 
 1:30, 
 2:20, 
 3:10}