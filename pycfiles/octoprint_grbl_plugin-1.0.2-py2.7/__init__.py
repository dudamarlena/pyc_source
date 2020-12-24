# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/octoprint_grbl_plugin/__init__.py
# Compiled at: 2017-10-20 09:32:44
from octoprint_grbl_plugin.plugin import unsupported_commands, translate_ok
__plugin_name__ = 'Grbl support'
__plugin_hooks__ = {'octoprint.comm.protocol.gcode.sending': unsupported_commands, 
   'octoprint.comm.protocol.gcode.received': translate_ok}