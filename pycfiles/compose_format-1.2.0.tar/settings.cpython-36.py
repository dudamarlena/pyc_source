# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/settings.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 715 bytes
import os
APP_CONFIG_ROOT = os.environ.get('CF_APP_CONFIG_ROOT', os.path.expanduser('~/.compose'))
APP_ENVIRONMENTS_ROOT = os.path.join(APP_CONFIG_ROOT, 'environments')
LOGGING = {'version':1, 
 'disable_existing_loggers':False, 
 'handlers':{'console': {'level':'DEBUG',  'class':'logging.StreamHandler'}}, 
 'loggers':{'compose_flow': {'handlers':['console'],  'level':'INFO',  'propagate':False}}, 
 'root':{'handlers':[
   'console'], 
  'level':'WARNING',  'propagate':True}}
USER = os.environ.get('USER', 'nobody')
DEFAULT_CF_REMOTE_USER = os.environ.get('CF_REMOTE_USER', USER)
DOCKER_IMAGE_PREFIX = os.environ.get('CF_DOCKER_IMAGE_PREFIX', 'localhost.localdomain')