# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/workload_scheduler/plugin_workload_scheduler_first.py
# Compiled at: 2014-02-27 11:31:04
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'workload_scheduler', 
   'name': 'first', 
   'version': '0.1', 
   'description': 'this is an empty scheduler which basically does nothing.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This simple workload scheduler plugin will place all compute units on the
    first pilot in the given overlay -- all other pilots will remain idle.  This
    is close to be the worst possible (while still functional) scheduler
    imaginable.

    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def schedule(self, workload, overlay):
        """
        Assign all units to pilot nu. 0
        """
        if not overlay.pilots.keys():
            troy._logger.warn('no pilots in overlay')
            return
        pilot_id = overlay.pilots.keys()[0]
        for tid in workload.tasks.keys():
            task = workload.tasks[tid]
            for unit_id in task.units:
                troy._logger.info('workload schedule : assign unit %-18s to %s' % (unit_id, pilot_id))
                unit = task.units[unit_id]
                unit._bind(pilot_id)