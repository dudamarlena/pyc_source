# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/logger.py
# Compiled at: 2017-06-06 22:44:39
# Size of source mod 2**32: 278 bytes
import logging, sys
console_handler = logging.StreamHandler(stream=sys.stdout)
console_formatter = logging.Formatter('%(asctime)s [%(levelname)s]:%(message)s ', '%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_formatter)
__all__ = 'console_handler'