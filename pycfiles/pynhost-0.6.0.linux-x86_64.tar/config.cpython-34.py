# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/config.py
# Compiled at: 2015-07-19 15:10:44
# Size of source mod 2**32: 469 bytes
from pynhost import constants, engineio
settings = {'logging level': constants.LOGGING_LEVELS['on'], 
 'logging directory': constants.DEFAULT_LOGGING_DIRECTORY, 
 'engine': engineio.SharedDirectoryEngine(constants.DEFAULT_INPUT_SOURCE)}