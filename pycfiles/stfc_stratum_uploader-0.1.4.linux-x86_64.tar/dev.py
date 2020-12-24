# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/settings/dev.py
# Compiled at: 2013-08-08 10:52:33
from archer.settings.common import Common

class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS = Common.INSTALLED_APPS + ('debug_toolbar', 'gunicorn')
    DEBUG_TOOLBAR_PANELS = ('debug_toolbar.panels.version.VersionDebugPanel', 'debug_toolbar.panels.timer.TimerDebugPanel',
                            'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
                            'debug_toolbar.panels.headers.HeaderDebugPanel', 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
                            'debug_toolbar.panels.template.TemplateDebugPanel', 'debug_toolbar.panels.sql.SQLDebugPanel',
                            'debug_toolbar.panels.signals.SignalDebugPanel', 'debug_toolbar.panels.logger.LoggingPanel')
    INTERNAL_IPS = ('127.0.0.1', )
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, 
       'HIDE_DJANGO_SQL': False, 
       'TAG': 'body', 
       'ENABLE_STACKTRACES': True}