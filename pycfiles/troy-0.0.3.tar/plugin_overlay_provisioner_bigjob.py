# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/overlay_provisioner/plugin_overlay_provisioner_bigjob.py
# Compiled at: 2014-02-27 11:31:04
import os, saga, getpass, pilot as pilot_module, radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'overlay_provisioner', 
   'name': 'bigjob', 
   'version': '0.1', 
   'description': 'this is a scheduler which provisions bigjob pilots.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin creates pilots via the BigJob Pilot API.

    **Configuration Options:**

    * `coordination_url`: the redis URL to be used by BigJob.  The environment
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
            troy._logger.error('No COORDINATION_URL set for bigjob backend')
            troy._logger.info('example: export COORDINATION_URL=redis://<pass>@gw68.quarry.iu.teragrid.org:6379')
            troy._logger.info('Contact Radica@Ritgers for the redis password')
            raise RuntimeError('Cannot use bigjob backend - no COORDINATION_URL -- see debug log for details')
        troy._logger.debug('using bj coordination url %s' % self._coord)
        self.cp_service = pilot_module.PilotComputeService(self._coord)
        return

    def provision(self, overlay):
        """
        provision the pilots of the overlay -- inspect that overlay, dig out the pilots
        and their description, check state, and instantiate them via the backend
        system.
        """
        for pid in overlay.pilots.keys():
            troy_pilot = overlay.pilots[pid]
            if troy_pilot.state not in [BOUND]:
                raise RuntimeError('Can only provision pilots in BOUND state (%s)' % troy_pilot.state)
            pilot_descr = pilot_module.PilotComputeDescription()
            pilot_descr.resource_url = troy_pilot.resource
            pilot_descr.number_of_processes = troy_pilot.description['size']
            pilot_descr.walltime = troy_pilot.description['walltime']
            pilot_descr.queue = troy_pilot.description['queue']
            pilot_descr.working_directory = '%s/troy_agents/' % troy_pilot.description['home']
            bj_pilot = self.cp_service.create_pilot(pilot_descr)
            troy_pilot._set_instance(instance_type='bigjob', provisioner=self, instance=bj_pilot, native_id=bj_pilot.get_url())
            troy._logger.info('overlay  provision: provision pilot  %s : %s ' % (
             troy_pilot, troy_pilot._get_instance('bigjob')))

    def pilot_reconnect(self, native_id):
        """
        the pilot lost the instance, and needs to reconnect...
        This is what is getting called on troy.Pilot._get_instance, if that
        troy.Pilot doesn't have that instance anymore...
        """
        bj_pilot = pilot_module.PilotCompute(pilot_url=native_id)
        return bj_pilot

    def pilot_get_info(self, pilot):
        """
        pilot inspection: get all possible information for the pilot, and return
        in a dict.  This dict SHOULD contain 'state' at the very least -- but
        check the pilot_inspection unit test for more recommended attributes.
        """
        bj_pilot = pilot._get_instance('bigjob')
        info = dict()
        bj_units = bj_pilot.list_compute_units()
        info['units'] = dict()
        for bj_unit in bj_units:
            unit = troy.ComputeUnit(pilot.session, _native_id=bj_unit.get_url(), _pilot_id=pilot.id)
            info['units'][unit.id] = unit

        if 'description' in info:
            info['description'] = eval(info['description'])
        details = bj_pilot.get_details()
        if 'start_time' in details and details['start_time']:
            pilot.timed_event('submission', 'bigjob', details['start_time'])
        if 'end_queue_time' in details and details['end_queue_time']:
            pilot.timed_event('start', 'bigjob', details['end_queue_time'])
        if 'end_time' in details and details['end_time']:
            pilot.timed_event('stop', 'bigjob', details['end_time'])
        if 'last_contact' in details and details['last_contact']:
            pilot.timed_event('heartbeat', 'bigjob', details['last_contact'])
        if 'start_staging_time' in details and details['start_staging_time']:
            pilot.timed_event('start_staging', 'bigjob', details['start_staging_time'])
        info['state'] = {'New': DESCRIBED, 'Running': PROVISIONED, 
           'Failed': FAILED, 
           'Done': DONE, 
           'Unknown': UNKNOWN}.get(bj_pilot.get_state(), UNKNOWN)
        return info

    def pilot_cancel(self, pilot):
        """
        bye bye bye Junimond, es ist vorbei, bye bye...
        """
        bj_pilot = pilot._get_instance('bigjob')
        bj_pilot.cancel()