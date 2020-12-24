# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/overlay_provisioner/plugin_overlay_provisioner_sagapilot.py
# Compiled at: 2014-02-27 11:31:04
import os, saga, getpass, sagapilot as sp, radical.utils as ru
from troy.constants import *
import troy
FGCONF = 'https://raw.github.com/saga-project/saga-pilot/master/configs/futuregrid.json'
XSEDECONF = 'https://raw.github.com/saga-project/saga-pilot/master/configs/xsede.json'
PLUGIN_DESCRIPTION = {'type': 'overlay_provisioner', 
   'name': 'sagapilot', 
   'version': '0.1', 
   'description': 'this is a plugin which provisions sagapilot pilots.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin creates pilots via the SAGA-Pilot Pilot API.

    **Configuration Options:**

    * `coordination_url`: the redis URL to be used by SAGA-Pilot.  The environment
        variable COORDINATION_URL is used as fallback.
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)
        self._credentials = list()
        self._coord = None
        return

    def init(self):
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

    def provision(self, overlay):
        """
        provision a given overlay -- inspect that overlay, dig out the pilots
        and their description, check state, and instantiate them via the backend
        system.

        For each pilot, we need to also keep the pilot manager and the unit
        manager -- otherwise we are not able to reconnec to to pilots and units.
        So whenever a pilot is created, we immediately also create a unit
        manager, ad pass it around with the PM and pilot instance.
        """
        for pid in overlay.pilots.keys():
            troy_pilot = overlay.pilots[pid]
            if troy_pilot.state not in [BOUND]:
                raise RuntimeError('Can only provision BOUND pilots (%s)' % troy_pilot.state)
            pilot_descr = sp.ComputePilotDescription()
            pilot_descr.resource = troy_pilot.description['hostname']
            pilot_descr.cores = troy_pilot.description['size']
            pilot_descr.runtime = troy_pilot.description['walltime']
            pilot_descr.queue = troy_pilot.description['queue']
            pilot_descr.sandbox = '%s/troy_agents/' % troy_pilot.description['home']
            troy._logger.info('overlay  provision: provision   pilot  %s : %s ' % (
             pid, troy_pilot.resource))
            if 'username' in troy_pilot.description:
                username = troy_pilot.description['username']
                if username not in self._credentials:
                    self._credentials.append(username)
                    cred = sp.SSHCredential()
                    cred.user_id = username
                    self._sp.add_credential(cred)
                    print 'added username %s @ %s' % (username, pilot_descr.resource)
            sp_um = sp.UnitManager(session=self._sp, scheduler='direct_submission')
            sp_pm = sp.PilotManager(session=self._sp, resource_configurations=[
             FGCONF, XSEDECONF])
            sp_pilot = sp_pm.submit_pilots(pilot_descr)
            sp_um.add_pilots(sp_pilot)
            troy_pilot._set_instance(instance_type='sagapilot', provisioner=self, instance=[
             sp_um, sp_pm, sp_pilot], native_id=[
             sp_um.uid, sp_pm.uid, sp_pilot.uid])
            troy._logger.info('overlay  provision: provisioned pilot  %s : %s (%s)' % (
             troy_pilot,
             troy_pilot._get_instance('sagapilot')[2],
             troy_pilot.resource))

    def pilot_reconnect(self, native_id):
        """
        the pilot lost the instance, and needs to reconnect...
        This is what is getting called on troy.Pilot._get_instance, if that
        troy.Pilot doesn't have that instance anymore...
        """
        sp_um_id = native_id[0]
        sp_pm_id = native_id[1]
        sp_pilot_id = native_id[2]
        sp_um = self._sp.get_unit_managers(sp_um_id)
        sp_pm = self._sp.get_pilot_managers(sp_pm_id)
        sp_pilot = sp_pm.get_pilots(sp_pilot_id)
        return [
         sp_um, sp_pm, sp_pilot]

    def pilot_get_info(self, pilot):
        """
        pilot inspection: get all possible information for the pilot, and return
        in a dict.  This dict SHOULD contain 'state' at the very least -- but
        check the pilot_inspection unit test for more recommended attributes.
        """
        sp_um, sp_pm, sp_pilot = pilot._get_instance('sagapilot')
        info = {'uid': sp_pilot.uid, 'description': sp_pilot.description, 
           'state': sp_pilot.state, 
           'log': sp_pilot.log, 
           'resource_detail': sp_pilot.resource_detail, 
           'cores_per_node': sp_pilot.resource_detail['cores_per_node'], 
           'nodes': sp_pilot.resource_detail['nodes'], 
           'unit_ids': list(), 
           'unit_managers': list(), 
           'pilot_manager': sp_pilot.pilot_manager, 
           'submission_time': sp_pilot.submission_time, 
           'start_time': sp_pilot.start_time, 
           'stop_time': sp_pilot.stop_time}
        info['state'] = {sp.states.PENDING: PROVISIONED, sp.states.RUNNING: PROVISIONED, 
           sp.states.DONE: COMPLETED, 
           sp.states.CANCELED: CANCELED, 
           sp.states.FAILED: FAILED, 
           sp.states.UNKNOWN: UNKNOWN}.get(sp_pilot.state, UNKNOWN)
        if 'submission_time' in info and info['submission_time']:
            pilot.timed_event('submission', 'sagapilot', info['submission_time'])
        if 'start_time' in info and info['start_time']:
            pilot.timed_event('start', 'sagapilot', info['start_time'])
        if 'stop_time' in info and info['stop_time']:
            pilot.timed_event('stop', 'sagapilot', info['stop_time'])
        if 'log' in info:
            for log in info['log']:
                pilot.timed_event('state_detail', ['sagapilot', log], -1)

        return info

    def pilot_cancel(self, pilot):
        sp_um, sp_pm, sp_pilot = pilot._get_instance('sagapilot')
        sp_pilot.cancel()