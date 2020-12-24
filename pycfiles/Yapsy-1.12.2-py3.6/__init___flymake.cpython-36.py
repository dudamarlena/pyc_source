# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/__init___flymake.py
# Compiled at: 2019-07-27 13:47:40
# Size of source mod 2**32: 2981 bytes
"""

Overview
========

Yapsy's main purpose is to offer a way to easily design a plugin
system in Python, and motivated by the fact that many other Python
plugin system are either too complicated for a basic use or depend on
a lot of libraries. Yapsy only depends on Python's standard library.

|yapsy| basically defines two core classes:

- a fully functional though very simple ``PluginManager`` class

- an interface ``IPlugin`` which defines the interface of plugin
  instances handled by the ``PluginManager``

Getting started
===============

The basic classes defined by |yapsy| should work "as is" and enable
you to load and activate your plugins. So that the following code
should get you a fully working plugin management system::

   from yapsy.PluginManager import PluginManager
   
   # Build the manager
   simplePluginManager = PluginManager()
   # Tell it the default place(s) where to find plugins
   simplePluginManager.setPluginPlaces(["path/to/myplugins"])
   # Load all plugins
   simplePluginManager.collectPlugins()

   # Activate all loaded plugins
   for pluginInfo in simplePluginManager.getAllPlugins():
      simplePluginManager.activatePluginByName(pluginInfo.name)

.. note:: The ``plugin_info`` object (typically an instance of
          ``IPlugin``) plays as *the entry point of each
          plugin*. That's also where |yapsy| ceases to guide you: it's
          up to you to define what your plugins can do and how you
          want to talk to them ! Talking to your plugin will then look
          very much like the following::

             # Trigger 'some action' from the loaded plugins
             for pluginInfo in simplePluginManager.getAllPlugins():
                pluginInfo.plugin_object.doSomething(...)

"""
__version__ = '1.12.2'
__docformat__ = 'restructuredtext en'
import logging
log = logging.getLogger('yapsy')
PLUGIN_NAME_FORBIDEN_STRING = ';;'
import re
from yapsy.compat import is_py2, str
if is_py2:
    RE_NON_ALPHANUM = re.compile('\\W', re.U)
else:
    RE_NON_ALPHANUM = re.compile('\\W')

def NormalizePluginNameForModuleName(pluginName):
    """
        Normalize a plugin name into a safer name for a module name.
        
        .. note:: may do a little more modifications than strictly
                  necessary and is not optimized for speed.
        """
    if is_py2:
        pluginName = str(pluginName, 'utf-8')
    if len(pluginName) == 0:
        return '_'
    else:
        if pluginName[0].isdigit():
            pluginName = '_' + pluginName
        ret = RE_NON_ALPHANUM.sub('_', pluginName)
        if is_py2:
            ret = ret.encode('utf-8')
        return ret