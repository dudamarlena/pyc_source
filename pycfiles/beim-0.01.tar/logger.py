# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/logger.py
# Compiled at: 2013-12-08 21:45:16
import logging
filename = 'debug.log'
logging.basicConfig(filename=filename, level=logging.DEBUG)
debug = logging.debug