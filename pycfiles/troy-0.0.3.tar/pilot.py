# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/overlay/pilot.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class Pilot(tu.Properties, tu.Timed):
    """
    """
    _instance_cache = tu.InstanceCache()

    def __init__(self, session, param, _overlay=None, _instance_type=None):
        """
        Create a new pilot according to a description, or reconnect to with an ID.

        Each new pilot is assigned a new ID.
        """
        self.session = session
        self.overlay = _overlay
        if isinstance(param, basestring):
            self.id = param
            descr = troy.PilotDescription()
            reconnect = True
        elif isinstance(param, troy.PilotDescription):
            self.id = ru.generate_id('p.')
            descr = param
            reconnect = False
        else:
            raise TypeError("Pilot constructor accepts either a pid (string) or a description (troy.PilotDescription), not '%s'" % type(param))
        tu.Timed.__init__(self, 'troy.Pilot', self.id)
        self.session.timed_component(self, 'troy.Pilot', self.id)
        if self.overlay:
            self.overlay.timed_component(self, 'troy.Pilot', self.id)
        tu.Properties.__init__(self, descr)
        self.register_property('id')
        self.register_property('state')
        self.register_property('description')
        self.register_property('overlay')
        self.register_property('size')
        self.register_property('resource')
        self.register_property('units')
        self.register_property('native_id')
        self.register_property('native_description')
        self.register_property('start_time')
        self.register_property('last_contact')
        self.register_property('end_queue_time')
        self.register_property('processes_per_node')
        self.register_property('slots')
        self.register_property('working_directory')
        self.register_property('service_url')
        self.register_property('project')
        self.register_property('queue')
        self.register_property('walltime')
        self.register_property('affinity_datacenter_label')
        self.register_property('affinity_machine_label')
        self.state = DESCRIBED
        self.description = descr
        self.resource = None
        self._provisioner = None
        self._instance = None
        self._instance_type = None
        self._pilot_info = None
        self.register_property_updater(self._update_properties)
        if reconnect:
            self.id, self.native_id, self._provisioner, self._instance, self._instance_type, self._state, self.resource = self._instance_cache.get(instance_id=self.id, native_id=self.native_id)
            if not self._instance:
                troy._logger.warn('Could not reconnect to pilot %s (%s)' % (self.id, self.native_id))
            else:
                self._update_properties()
        else:
            self._instance_cache.put(instance_id=self.id, native_id=self.native_id, instance=[
             self.id,
             self.native_id,
             self._provisioner,
             self._instance,
             self._instance_type,
             self.state,
             self.resource])
        return

    def __del__(self):
        """
        Destructor -- cancels the pilot
        """
        self.cancel()

    def merge_description(self, source):
        """
        merge additional information into the pilot description -- such as
        resource information, or application specific data
        """
        if self.state not in [DESCRIBED, BOUND]:
            raise RuntimeError('pilot is not in DESCRIBED state (%s)' % self.state)
        pd_dict = self.description.as_dict()
        ru.dict_merge(pd_dict, source, policy='overwrite')
        ru.dict_stringexpand(pd_dict)
        ru.dict_stringexpand(pd_dict, self.session.cfg)
        self.description = troy.PilotDescription(pd_dict)

    def cancel(self):
        """
        cancel the pilot
        """
        if self.state in [PROVISIONED]:
            troy._logger.info('cancel pilot    %s' % self.id)
            if self._provisioner:
                self._provisioner.pilot_cancel(self)
            self.state = CANCELED

    def _bind(self, resource):
        if self.state not in [DESCRIBED]:
            raise RuntimeError('Can only bind pilots in DESCRIBED state (%s)' % self.state)
        self.resource = resource
        self.state = BOUND
        self._instance_cache.put(instance_id=self.id, native_id=self.native_id, instance=[
         self.id,
         self.native_id,
         self._provisioner,
         self._instance,
         self._instance_type,
         self.state,
         self.resource])

    def _set_instance(self, instance_type, provisioner, instance, native_id):
        if self.state not in [BOUND]:
            raise RuntimeError('Can only provision pilots in BOUND state (%s)' % self.state)
        self._provisioner = provisioner
        self._instance_type = instance_type
        self._instance = instance
        self.native_id = native_id
        self.state = PROVISIONED
        troy.OverlayManager.pilot_id_to_native_id(self.id, native_id)
        self._instance_cache.put(instance_id=self.id, native_id=self.native_id, instance=[
         self.id,
         self.native_id,
         self._provisioner,
         self._instance,
         self._instance_type,
         self.state,
         self.resource])

    def _get_instance(self, instance_type):
        if instance_type != self._instance_type:
            raise RuntimeError("pilot instance type is '%s', not '%s'" % (
             self._instance_type, instance_type))
        return self._instance

    def _update_properties(self, key=None):
        """
        This method is invoked whenever some attribute is asked for, to give us 
        a chance to update the respective attribute value.
        """
        if not key:
            if not self._provisioner:
                raise RuntimeError('pilot is in inconsistent state (no provisioner known)')
            self._pilot_info = self._provisioner.pilot_get_info(self)
            self._update_pilot_info()
            return
        if key not in ('state', 'resource', 'size', 'units', 'processes_per_node',
                       'working_directory', 'project', 'queue', 'walltime', 'affinity_datacenter_label',
                       'affinity_machine_label'):
            return self.get_property(key)
        if key == 'resource':
            return self.resource
        if key == 'instance':
            return self._instance
        if self.description and key in self.description:
            return self.description[key]
        if self._provisioner:
            if self.state not in [COMPLETED, CANCELED, FAILED]:
                if key not in ('state', ) and self._pilot_info:
                    if key in self._pilot_info:
                        return self._pilot_info[key]
                self._pilot_info = self._provisioner.pilot_get_info(self)
                self._update_pilot_info()
                if key in self._pilot_info:
                    return self._pilot_info[key]
        return self.get_property(key)

    def _update_pilot_info(self):
        keymap = {'description': 'native_description', 'bigjob_id': 'native_id', 
           'start_time': 'start_time', 
           'last_contact': 'last_contact', 
           'stopped': 'stopped', 
           'end_queue_time': 'end_queue_time', 
           'resource': 'native_resource', 
           'processes_per_node': 'processes_per_node', 
           'number_of_processes': 'slots', 
           'working_directory': 'working_directory', 
           'service_url': 'service_url'}
        for info_key in self._pilot_info:
            new_key = keymap.get(info_key, info_key)
            self.set_property(new_key, self._pilot_info[info_key])

        if 'description' in self._pilot_info:
            description = self._pilot_info['description']
            for descr_key in description:
                new_key = keymap.get(descr_key, descr_key)
                self.set_property(new_key, description[descr_key])