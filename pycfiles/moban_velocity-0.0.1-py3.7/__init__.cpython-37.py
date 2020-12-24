# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/moban_velocity/__init__.py
# Compiled at: 2019-02-02 03:37:53
# Size of source mod 2**32: 399 bytes
from lml.plugin import PluginInfo, PluginInfoChain
import moban.constants as constants
from moban_velocity._version import __version__
from moban_velocity._version import __author__
PluginInfoChain(__name__).add_a_plugin_instance(PluginInfo((constants.TEMPLATE_ENGINE_EXTENSION),
  ('%s.engine.EngineVelocity' % __name__),
  tags=[
 'velocity', 'vtl']))