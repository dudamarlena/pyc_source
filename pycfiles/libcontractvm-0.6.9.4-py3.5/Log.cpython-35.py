# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libcontractvm/Log.py
# Compiled at: 2015-09-12 08:31:58
# Size of source mod 2**32: 853 bytes
import logging
from colorlog import ColoredFormatter
formatter = ColoredFormatter('%(log_color)s[%(asctime)s] %(module)s: %(message_log_color)s%(message)s', datefmt=None, reset=True, log_colors={'DEBUG': 'blue', 
 'INFO': 'green', 
 'WARNING': 'yellow', 
 'ERROR': 'red', 
 'CRITICAL': 'red'}, secondary_log_colors={'message': {'DEBUG': 'purple', 
             'INFO': 'yellow', 
             'WARNING': 'green', 
             'ERROR': 'yellow', 
             'CRITICAL': 'red'}}, style='%')
stream = logging.StreamHandler()
stream.setFormatter(formatter)
logger = logging.getLogger('libcontractvm')
logger.addHandler(stream)
logger.setLevel(10)
logger.propagate = False