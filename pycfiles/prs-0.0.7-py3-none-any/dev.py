# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/settings/dev.py
# Compiled at: 2015-08-31 13:52:46
__doc__ = '\nDev-specific Django settings.\n'
from .base import *
INSTALLED_APPS += ('django_pdb', 'debug_toolbar', 'debug_panel')
MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware', 'debug_panel.middleware.DebugPanelMiddleware')
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ('127.0.0.1', )
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'handlers': {'apps_info': {'level': 'INFO', 
                              'class': 'logging.FileHandler', 
                              'filename': 'logs/apps_info.log', 
                              'formatter': 'simple'}, 
                'apps_debug': {'level': 'DEBUG', 
                               'class': 'logging.FileHandler', 
                               'filename': 'logs/apps_debug.log', 
                               'formatter': 'simple'}, 
                'trace': {'level': 'DEBUG', 
                          'class': 'logging.handlers.RotatingFileHandler', 
                          'filename': 'logs/trace.log', 
                          'formatter': 'simple', 
                          'maxBytes': 1000000, 
                          'backupCount': 2}, 
                'events': {'level': 'INFO', 
                           'class': 'logging.FileHandler', 
                           'filename': 'logs/events.log', 
                           'formatter': 'simple'}, 
                'errors': {'level': 'ERROR', 
                           'class': 'logging.FileHandler', 
                           'filename': 'logs/errors.log', 
                           'formatter': 'simple'}}, 
   'formatters': {'simple': {'format': '%(asctime)s %(name)s [%(levelname)s] %(message)s'}}, 
   'loggers': {'': {'handlers': [
                               'trace', 'errors'], 
                    'propagate': True}, 
               'openassessment': {'handlers': [
                                             'apps_debug', 'apps_info'], 
                                  'propagate': True}, 
               'submissions': {'handlers': [
                                          'apps_debug', 'apps_info'], 
                               'propagate': True}, 
               'workbench.runtime': {'handlers': [
                                                'apps_debug', 'apps_info', 'events'], 
                                     'propogate': True}}}
MEDIA_ROOT = os.path.join(BASE_DIR, 'storage/dev')