# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gardar/code/adagios/adagios/__init__.py
# Compiled at: 2020-01-05 16:55:12
import os.path
__version__ = '1.6.6'
notifications = {}
active_plugins = {}
tasks = []
misc_menubar_items = []
menubar_items = []

def add_plugin(name='myplugin', modulepath=None):
    """ Adds a new django application dynamically to adagios.

    """
    if name in active_plugins:
        return
    else:
        if not modulepath:
            modulepath = name
        plugin_module = __import__(modulepath, fromlist=modulepath.split()).__file__
        template_dir = os.path.dirname(plugin_module) + '/templates/'
        active_plugins[name] = modulepath
        import adagios.urls
        from django.conf.urls import patterns, include
        new_pattern = patterns('', (
         '^%s' % name, include('%s.urls' % modulepath)))
        adagios.urls.urlpatterns += new_pattern
        if os.path.isfile(template_dir + '%s_menubar_misc.html' % name):
            misc_menubar_items.append('%s_menubar_misc.html' % name)
        if os.path.isfile(template_dir + '%s_menubar.html' % name):
            menubar_items.append('%s_menubar.html' % name)
        return


try:
    from adagios import settings
    for k, v in settings.plugins.items():
        try:
            add_plugin(k, v)
        except Exception:
            pass

except Exception:
    pass

import adagios.profiling