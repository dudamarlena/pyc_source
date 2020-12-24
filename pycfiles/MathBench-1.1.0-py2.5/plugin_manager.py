# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/basement/plugin_manager.py
# Compiled at: 2008-04-06 13:50:04
"""
Create a PluginManager.

Create it as a Singleton with yapsy.
"""
import os, yapsy
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.AutoInstallPluginManager import AutoInstallPluginManager
from yapsy.IPlugin import IPlugin
LabPluginManager = PluginManagerSingleton
LabPluginManager.setBehaviour([
 ConfigurablePluginManager,
 AutoInstallPluginManager])