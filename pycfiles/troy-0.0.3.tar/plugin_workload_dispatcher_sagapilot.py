# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/workload_dispatcher/plugin_workload_dispatcher_sagapilot.py
# Compiled at: 2014-02-27 11:31:04
import os, sagapilot as sp, radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'workload_dispatcher', 
   'name': 'sagapilot', 
   'version': '0.1', 
   'description': 'this is a dispatcher which submits to sagapilot pilots.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin dispatches workloads (and their compute units) to SAGA-Pilot pilots,
    uring SAGA-Pilot's pilot API.

    **Configuration Options:**

    * `coordination_url`: the redis URL to be used by SAGA-Pilot.  The environment
        variable COORDINATION_URL is used as fallback.
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def init(self):
        self._coord = None
        if 'coordination_url' in self.cfg:
            self._coord = self.cfg['coordination_url']
        elif 'COORDINATION_URL' in os.environ:
            self._coord = os.environ['COORDINATION_URL']
        else:
            troy._logger.error('No COORDINATION_URL set for sagapilot backend')
            troy._logger.info('example: export COORDINATION_URL=redis://<pass>@gw68.quarry.iu.teragrid.org:6379')
            troy._logger.info('Contact Radica@Ritgers for the redis password')
            raise RuntimeError('Cannot use sagapilot backend - no COORDINATION_URL -- see debug log for details')
        self._sp = sp.Session(database_url=self._coord)
        return

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
                pilot = troy.Pilot(self.session, pilot_id, _instance_type='sagapilot')
                troy._logger.info('workload dispatch : dispatch %-18s to %s' % (
                 uid, pilot._get_instance('sagapilot')[1]))
                keymap = {'tag': 'name', 
                   'executable': 'executable', 
                   'arguments': 'arguments', 
                   'environment': 'environment', 
                   'cores': 'cores', 
                   'working_directory': 'working_directory_priv'}
                sp_cu_descr = sp.ComputeUnitDescription()
                for key in unit_descr:
                    if key in keymap:
                        sp_cu_descr[keymap[key]] = unit_descr[key]

                sp_um, sp_pm, sp_pilot = pilot._get_instance('sagapilot')
                sp_cu = sp_um.submit_units(sp_cu_descr)
                unit._set_instance('sagapilot', self, instance=[
                 sp_um, sp_cu], native_id=[
                 sp_um.uid, sp_cu.uid])

    def unit_reconnect(self, native_id):
        """
        the unit lost the instance, and needs to reconnect...
        This is what is getting called on troy.Unit._get_instance, if that
        troy.Unit doesn't have that instance anymore...
        """
        troy._logger.debug('reconnect to sagapilot cu %s' % native_id)
        sp_um_id = native_id[0]
        sp_cu_id = native_id[1]
        sp_um = self._sp.get_unit_managers(sp_um_id)
        sp_cu = sp_um.get_units(sp_cu_id)
        return [
         sp_um, sp_cu]

    def unit_get_info(self, unit):
        """
        unit inspection: get all possible information for the unit, and return
        in a dict.  This dict SHOULD contain 'state' at the very least -- but
        check the pilot_inspection unit test for more recommended attributes.
        """
        sp_um, sp_cu = unit._get_instance('sagapilot')
        info = {'uid': sp_cu.uid, 'description': sp_cu.description, 
           'state': sp_cu.state, 
           'stdout': sp_cu.stdout, 
           'stderr': sp_cu.stderr, 
           'log': sp_cu.log, 
           'execution_details': sp_cu.execution_details, 
           'submission_time': sp_cu.submission_time, 
           'start_time': sp_cu.start_time, 
           'stop_time': sp_cu.stop_time}
        if 'state' in info:
            troy._logger.debug('sagalilot level cu state: %s' % info['state'])
            info['state'] = {sp.states.PENDING: PENDING, sp.states.PENDING_EXECUTION: PENDING, 
               sp.states.PENDING_INPUT_TRANSFER: RUNNING, 
               sp.states.TRANSFERRING_INPUT: RUNNING, 
               sp.states.RUNNING: RUNNING, 
               sp.states.PENDING_OUTPUT_TRANSFER: RUNNING, 
               sp.states.TRANSFERRING_OUTPUT: RUNNING, 
               sp.states.DONE: DONE, 
               sp.states.CANCELED: CANCELED, 
               sp.states.FAILED: FAILED, 
               sp.states.UNKNOWN: UNKNOWN}.get(info['state'], UNKNOWN)
        if 'submission_time' in info and info['submission_time']:
            unit.timed_event('submission', 'sagapilot', info['submission_time'])
        if 'start_time' in info and info['start_time']:
            unit.timed_event('start', 'sagapilot', info['start_time'])
        if 'stop_time' in info and info['stop_time']:
            unit.timed_event('stop', 'sagapilot', info['stop_time'])
        if info['state'] == FAILED:
            troy._logger.error('CU %s failed' % unit.id)
            troy._logger.info('log: \n----\n%s\n---\n' % info['log'])
            troy._logger.info('stderr: \n----\n%s\n---\n' % info['stderr'])
            troy._logger.info('stdout: \n----\n%s\n---\n' % info['stdout'])
        return info

    def unit_cancel(self, unit):
        """
        bye bye bye Junimond, es ist vorbei, bye bye...
        """
        sp_um, sp_cu = unit._get_instance('sagapilot')
        sp_cu.cancel()