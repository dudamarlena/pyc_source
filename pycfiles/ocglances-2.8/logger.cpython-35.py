# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Downloads\ocglances\ocglances\logger.py
# Compiled at: 2017-02-13 10:46:28
# Size of source mod 2**32: 3318 bytes
"""Custom logger class."""
import os, json, getpass, tempfile, logging, logging.config
LOG_FILENAME = os.path.join(tempfile.gettempdir(), 'glances-{}.log'.format(getpass.getuser()))
LOGGING_CFG = {'version': 1, 
 'disable_existing_loggers': 'False', 
 'root': {'level': 'INFO', 
          'handlers': ['file', 'console']}, 
 
 'formatters': {'standard': {'format': '%(asctime)s -- %(levelname)s -- %(message)s'}, 
                
                'short': {'format': '%(levelname)s: %(message)s'}, 
                
                'free': {'format': '%(message)s'}}, 
 
 'handlers': {'file': {'level': 'DEBUG', 
                       'class': 'logging.handlers.RotatingFileHandler', 
                       'formatter': 'standard', 
                       'filename': LOG_FILENAME}, 
              
              'console': {'level': 'CRITICAL', 
                          'class': 'logging.StreamHandler', 
                          'formatter': 'free'}}, 
 
 'loggers': {'debug': {'handlers': ['file', 'console'], 
                       'level': 'DEBUG'}, 
             
             'verbose': {'handlers': ['file', 'console'], 
                         'level': 'INFO'}, 
             
             'standard': {'handlers': ['file'], 
                          'level': 'INFO'}, 
             
             'requests': {'handlers': ['file', 'console'], 
                          'level': 'ERROR'}, 
             
             'elasticsearch': {'handlers': ['file', 'console'], 
                               'level': 'ERROR'}, 
             
             'elasticsearch.trace': {'handlers': ['file', 'console'], 
                                     'level': 'ERROR'}}}

def glances_logger(env_key='LOG_CFG'):
    """Build and return the logger.

    env_key define the env var where a path to a specific JSON logger
            could be defined

    :return: logger -- Logger instance
    """
    _logger = logging.getLogger()
    config = LOGGING_CFG
    user_file = os.getenv(env_key, None)
    if user_file and os.path.exists(user_file):
        with open(user_file, 'rt') as (f):
            config = json.load(f)
    logging.config.dictConfig(config)
    return _logger


logger = glances_logger()