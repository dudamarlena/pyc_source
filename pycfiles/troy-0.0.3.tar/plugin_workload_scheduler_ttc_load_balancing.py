# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/workload_scheduler/plugin_workload_scheduler_ttc_load_balancing.py
# Compiled at: 2014-02-27 11:31:04
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'workload_scheduler', 
   'name': 'ttc_load_balancing', 
   'version': '0.01', 
   'description': 'debug scheduler, throws out tons of info'}
_idx = 0

class PLUGIN_CLASS(troy.PluginBase):
    """
    This workload scheduler will evenly distribute tasks over the set of known
    pilots.  It does not take pilot sizes into account, nor pilot state, nor
    does it care about task relationships or data dependencies.  It is not
    a clever plugin.

    **Configuration Options:** None
    This assumes that one of the earlier Troy plugins, or the user, is abvle to
    determine reasonably TTC estimates -- otherwise the plugin will behave like
    round-robin.  This plugin does not take the number of cores into account,
    neither for the pilots, nor for the CUs, nor does the plugin look at the
    *actual* pilot load (i.e. does not check if CUs have finished meanwhile).

    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def schedule(self, workload, overlay):
        """
        Iterate over the workload's CUs, and give them to the pilot which at
        this point accumulated the least load.  Add the CUs TTC to the pilots
        load property.
        """
        for t_id in workload.tasks.keys():
            task = workload.tasks[t_id]
            for u_id in task.units.keys():
                unit = task.units[u_id]
                try:
                    unit._ttc = int(unit.as_dict().get('walltime', 1))
                except:
                    pass

        for p_id in overlay.pilots.keys():
            pilot = overlay.pilots[p_id]
            if pilot.units:
                import pprint
                pprint.pprint(pilot)
                pprint.pprint(pilot.units)
                for u_id in pilot.units.keys():
                    unit = pilot.units[u_id]

        for p_id in overlay.pilots:
            if not hasattr(overlay.pilots[p_id], 'est_begin'):
                overlay.pilots[p_id].est_begin = 0

        pilot = overlay.pilots[p_id]
        if not len(overlay.pilots.keys()):
            raise ValueError('no pilots on overlay')
        for t_id in workload.tasks:
            task = workload.tasks[t_id]
            for u_id in task.units:
                unit = task.units[u_id]
                est_optimal = 999999
                p_optimal = 'invalid'
                for p_id in overlay.pilots.keys():
                    if overlay.pilots[p_id].est_begin < est_optimal:
                        p_optimal = p_id
                        est_optimal = overlay.pilots[p_id].est_begin

                unit._bind(p_optimal)
                overlay.pilots[p_optimal].est_begin += int(unit._ttc)
                troy.logger.debug('assigning unit %s to pilot %s' % (u_id, p_optimal))