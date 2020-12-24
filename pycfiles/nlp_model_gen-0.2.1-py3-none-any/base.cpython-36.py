# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/base.py
# Compiled at: 2019-07-04 20:26:34
# Size of source mod 2**32: 510 bytes
import os
from .packages.logger.assets.logTexts import TYPE_ERR, TYPE_WRN
CURRENT_BASE_PATH = os.path.dirname(os.path.realpath(__file__))
EXPORT_FORMAT = 'zip'
FILE_JOIN_OPERATOR = 'cat'
REMOTE_MODEL_SOURCE = {'path':'https://github.com/galias11',  'remote':True}
SPLIT_FILE_OPERATOR = 'split -a 1 -b'
DEBUG_MODE = False
LOG_LEVEL = [TYPE_WRN, TYPE_ERR]
LOG_PATH = CURRENT_BASE_PATH + '/logs/operation_log.log'
MAX_CONCURRENT_TASKS = 16