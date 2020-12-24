# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/logging.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1319 bytes
"""
Logging settings with base formatters and handlers.
"""
SERVER_EMAIL = 'django_cms_qe@localhost'
ADMINS = (('Root', 'root@localhost'), )
MANAGERS = ADMINS
LOGGING = {'version':1, 
 'disable_existing_loggers':False, 
 'formatters':{'short':{'format':'%(levelname)s [%(filename)s:%(lineno)s] %(message)s', 
   'datefmt':'%d/%b/%Y %H:%M:%S'}, 
  'long':{'format':'[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s', 
   'datefmt':'%d/%b/%Y %H:%M:%S'}}, 
 'handlers':{'console':{'level':'DEBUG', 
   'class':'logging.StreamHandler', 
   'formatter':'short'}, 
  'mailadmins':{'level':'WARNING', 
   'class':'django.utils.log.AdminEmailHandler'}}, 
 'loggers':{'django':{'level':'ERROR', 
   'handlers':[
    'mailadmins'], 
   'propagate':True}, 
  'cms_qe*':{'level':'WARNING', 
   'handlers':[
    'mailadmins'], 
   'propagate':True}, 
  '':{'level':'INFO', 
   'handlers':[
    'console']}}}