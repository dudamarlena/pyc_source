# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/huey/examples/django_ex/djangoex/settings.py
# Compiled at: 2019-08-25 16:10:18
# Size of source mod 2**32: 606 bytes
import logging
INSTALLED_APPS = [
 'huey.contrib.djhuey',
 'djangoex.test_app']
HUEY = {'name':'test-django', 
 'consumer':{'blocking':True, 
  'loglevel':logging.DEBUG, 
  'workers':4, 
  'scheduler_interval':1, 
  'simple_log':True}}
LOGGING = {'handlers':{'console': {'class': 'logging.StreamHandler'}}, 
 'loggers':{'huey': {'handlers':[
            'console'], 
           'level':logging.ERROR}}, 
 'version':1}
SECRET_KEY = 'foo'