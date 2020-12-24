# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/overlay_scheduler/plugin_overlay_scheduler_local.py
# Compiled at: 2014-02-27 11:31:04
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'overlay_scheduler', 
   'name': 'local', 
   'version': '0.1', 
   'description': 'this is a scheduler which assigns al pilots to localhost.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin schedules all pilots on `localhost`.

    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def schedule(self, overlay):
        """
        we simply assign all pilots to localhost
        """
        for pid in overlay.pilots.keys():
            pilot = overlay.pilots[pid]
            pilot._bind('fork://localhost')
            troy._logger.info('overlay  schedule : schedule pilot %s to localhost' % pilot.id)