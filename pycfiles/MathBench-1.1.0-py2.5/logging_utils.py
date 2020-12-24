# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/basement/logging_utils.py
# Compiled at: 2008-03-15 12:41:21
"""
Defines a logger based on Python's logger module.
"""
import logging, logging.handlers, configuration
MB_LOGLEVEL_MAPPING = {'DEBUG': logging.DEBUG, 
   'INFO': logging.INFO, 
   'ERROR': logging.ERROR, 
   'CRITICAL': logging.CRITICAL}
MB_LOGGER_NAME = 'mathbench'

def CreateLogger(handler):
    """
        Create a logger object with a default verbosity corresponding to a
        given loglevel.
        """
    __config = configuration.getConfig()
    __loglevel_str = __config.get('Development', 'Verbosity_Level')
    loglevel = MB_LOGLEVEL_MAPPING[__loglevel_str]
    logger = logging.getLogger(MB_LOGGER_NAME)
    logger.setLevel(loglevel)
    handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger