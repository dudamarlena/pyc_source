# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\port_v2\load_plugin.py
# Compiled at: 2015-08-04 11:44:30
from pysideuic.exceptions import WidgetPluginError

def load_plugin(plugin, plugin_globals, plugin_locals):
    """ Load the given plugin (which is an open file).  Return True if the
    plugin was loaded, or False if it wanted to be ignored.  Raise an exception
    if there was an error.
    """
    try:
        exec (
         plugin.read(), plugin_globals, plugin_locals)
    except ImportError:
        return False
    except Exception as e:
        raise WidgetPluginError('%s: %s' % (e.__class__, str(e)))

    return True