# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/logging.py
# Compiled at: 2019-03-17 15:16:50
# Size of source mod 2**32: 1227 bytes
"""Common logging functions"""
import os, logging
from logging.config import dictConfig
import yaml
LOGGING_CONF = 'logging.yaml'
LOGGING_DEFAULT = {'version':1, 
 'formatters':{'default': {'format': '%(asctime)s %(name)s %(levelname)s %(message)s'}}, 
 'handlers':{'default': {'class':'logging.StreamHandler', 
              'formatter':'default'}}, 
 'root':{'handlers':[
   'default'], 
  'level':'INFO'}}

def configure_logging(debug: bool=False, config: dict=None, filename: str=LOGGING_CONF) -> logging.Logger:
    """Configure logging"""
    if config is not None:
        config_dict = config
        config_source = 'dictionary'
    else:
        if filename is not None and os.path.exists(filename):
            with open(filename, 'rt') as (file):
                config_dict = yaml.load(file)
            config_source = 'file'
        else:
            config_dict = LOGGING_DEFAULT
            config_source = 'default'
    if debug:
        config_dict['root']['level'] = 'DEBUG'
    dictConfig(config_dict)
    logging.debug('Configured logging using %s', config_source)
    return logging.getLogger()