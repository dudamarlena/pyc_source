# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/config.py
# Compiled at: 2015-07-19 15:10:44
# Size of source mod 2**32: 469 bytes
from pynhost import constants, engineio
settings = {'logging level': constants.LOGGING_LEVELS['on'], 
 'logging directory': constants.DEFAULT_LOGGING_DIRECTORY, 
 'engine': engineio.SharedDirectoryEngine(constants.DEFAULT_INPUT_SOURCE)}