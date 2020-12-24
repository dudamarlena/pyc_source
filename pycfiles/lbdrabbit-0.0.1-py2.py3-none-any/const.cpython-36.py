# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/const.py
# Compiled at: 2019-10-01 15:26:56
# Size of source mod 2**32: 206 bytes
from .apigw import HttpMethod
DEFAULT_LBD_HANDLER_FUNC_NAME = 'handler'
VALID_LBD_HANDLER_FUNC_NAME_LIST = HttpMethod.get_all_valid_func_name() + [DEFAULT_LBD_HANDLER_FUNC_NAME]