# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/_utils.py
# Compiled at: 2020-05-04 13:31:17
# Size of source mod 2**32: 1496 bytes
import logging.config, requests
log = logging.getLogger()

def init_logger():
    LOGLEVEL = logging.DEBUG
    logging.config.dictConfig({'version':1, 
     'disable_existing_loggers':False, 
     'formatters':{'default': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}}, 
     'handlers':{'console': {'class':'logging.StreamHandler', 
                  'formatter':'default'}}, 
     'loggers':{'':{'level':'DEBUG', 
       'handlers':[
        'console']}, 
      'wcm':{'level':LOGLEVEL, 
       'handlers':[
        'console'], 
       'propagate':False}, 
      'noisy_module':{'level':'ERROR', 
       'handlers':[
        'console'], 
       'propagate':False}}})
    logger = logging.getLogger(__package__)


def get_latest_version():
    return requests.get('https://pypi.org/pypi/dame-cli/json').json()['info']['version']