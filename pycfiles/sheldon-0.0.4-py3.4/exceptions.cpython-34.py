# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/exceptions.py
# Compiled at: 2015-11-19 11:58:40
# Size of source mod 2**32: 647 bytes
"""
Tools for catching exceptions

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
from sheldon.utils import logger

def catch_module_errors(module_call_function):
    """
    Catch all module exceptions and log it

    :param module_call_function: function with calling user module
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            module_call_function(*args, **kwargs)
        except Exception as error:
            error_message = str(error)
            logger.error_message('Module error: \n' + error_message)

    return wrapper