# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/constants.py
# Compiled at: 2013-04-04 15:36:36


class Constants(object):
    NOT_PRODUCTION_MODE_INFO = '\n=================================================================\nMuntjac is running in DEBUG MODE.\nAdd productionMode=true to INI to disable debug features.\nTo show debug window, add ?debug to your application URL.\n================================================================='
    WARNING_XSRF_PROTECTION_DISABLED = '\n===========================================================\nWARNING: Cross-site request forgery protection is disabled!\n==========================================================='
    WARNING_RESOURCE_CACHING_TIME_NOT_NUMERIC = '\n===========================================================\nWARNING: resourceCacheTime has been set to a non integer value in INI. The default of 1h will be used.\n==========================================================='
    WIDGETSET_MISMATCH_INFO = '\n=================================================================\nThe widgetset in use does not seem to be built for the Muntjac\nversion in use. This might cause strange problems - a\nrecompile/deploy is strongly recommended.\n Muntjac version: %s\n Widgetset version: %s\n================================================================='
    URL_PARAMETER_RESTART_APPLICATION = 'restartApplication'
    URL_PARAMETER_CLOSE_APPLICATION = 'closeApplication'
    URL_PARAMETER_REPAINT_ALL = 'repaintAll'
    URL_PARAMETER_THEME = 'theme'
    SERVLET_PARAMETER_DEBUG = 'Debug'
    SERVLET_PARAMETER_PRODUCTION_MODE = 'productionMode'
    SERVLET_PARAMETER_DISABLE_XSRF_PROTECTION = 'disable-xsrf-protection'
    SERVLET_PARAMETER_RESOURCE_CACHE_TIME = 'resourceCacheTime'
    PARAMETER_VAADIN_RESOURCES = 'Resources'
    DEFAULT_BUFFER_SIZE = 32768
    MAX_BUFFER_SIZE = 65536
    AJAX_UIDL_URI = '/UIDL'
    THEME_DIRECTORY_PATH = 'VAADIN/themes/'
    DEFAULT_THEME_CACHETIME = 86400000
    WIDGETSET_DIRECTORY_PATH = 'VAADIN/widgetsets/'
    DEFAULT_WIDGETSET = 'org.muntiacus.MuntjacWidgetSet'
    PARAMETER_WIDGETSET = 'widgetset'
    ERROR_NO_WINDOW_FOUND = 'No window found. Did you remember to setMainWindow()?'
    DEFAULT_THEME_NAME = 'reindeer'
    INVALID_SECURITY_KEY_MSG = 'Invalid security key.'
    PORTAL_PARAMETER_VAADIN_WIDGETSET = 'vaadin.widgetset'
    PORTAL_PARAMETER_VAADIN_RESOURCE_PATH = 'vaadin.resources.path'
    PORTAL_PARAMETER_VAADIN_THEME = 'vaadin.theme'