# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/workload_dispatcher/plugin_workload_dispatcher_bigjob.py
# Compiled at: 2014-02-27 11:31:04
import os, saga, pilot as pilot_module, radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'workload_dispatcher', 
   'name': 'bigjob', 
   'version': '0.1', 
   'description': 'this is a dispatcher which submits to bigjob pilots.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin dispatches workloads (and their compute units) to BigJob pilots,
    uring BigJob's pilot API.

    **Configuration Options:**

    * `coordination_url`: the redis URL to be used by BigJob.  The environment
        variable COORDINATION_URL is used as fallback.
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)
        self._dir_cache = dict()

    def dispatch(self, workload, overlay):
        """
        Dispatch a given workload: examine all tasks in the WL to find the
        defined CUs, and dispatch them to the pilot system.  
        """
        for tid in workload.tasks.keys():
            task = workload.tasks[tid]
            for uid in task.units.keys():
                unit = task.units[uid]
                if unit.state not in [BOUND]:
                    raise RuntimeError('Can only dispatch units in BOUND state (%s)' % unit.state)
                unit_descr = unit.as_dict()
                pilot_id = unit['pilot_id']
                pilot = troy.Pilot(overlay.session, pilot_id, _instance_type='bigjob')
                troy._logger.info('workload dispatch : dispatch %-18s to %s' % (
                 uid, pilot._get_instance('bigjob')))
                bj_cu_descr = pilot_module.ComputeUnitDescription()
                for key in unit_descr:
                    if key in ('tag', ):
                        continue
                    bj_cu_descr[key] = unit_descr[key]

                bj_pilot = pilot._get_instance('bigjob')
                bj_cu = bj_pilot.submit_compute_unit(bj_cu_descr)
                bj_cu_url = bj_cu.get_url()
                unit._set_instance('bigjob', self, bj_cu, bj_cu_url)

    def unit_reconnect(self, native_id):
        """
        the unit lost the instance, and needs to reconnect...
        This is what is getting called on troy.Unit._get_instance, if that
        troy.Unit doesn't have that instance anymore...
        """
        troy._logger.debug('reconnect to bigjob subjob %s' % native_id)
        bj_cu = pilot_module.ComputeUnit(cu_url=native_id)
        return bj_cu

    def unit_get_info(self, unit):
        """
        unit inspection: get all possible information for the unit, and return
        in a dict.  This dict SHOULD contain 'state' at the very least -- but
        check the pilot_inspection unit test for more recommended attributes.
        """
        bj_cu = unit._get_instance('bigjob')
        info = bj_cu.get_details()
        if 'state' in info:
            info['state'] = {'New': DISPATCHED, 'Running': RUNNING, 
               'Staging': RUNNING, 
               'Failed': FAILED, 
               'Done': DONE, 
               'Unknown': UNKNOWN}.get(info['state'], UNKNOWN)
        return info

    def unit_cancel(self, unit):
        """
        bye bye bye Junimond, es ist vorbei, bye bye...
        """
        sj = unit._get_instance('bigjob')
        sj.cancel()