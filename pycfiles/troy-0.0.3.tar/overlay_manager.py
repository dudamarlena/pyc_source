# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/overlay/overlay_manager.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class OverlayManager(tu.Timed):
    """
    Generates and instantiates an overlay. An overlay consists of pilot
    descriptions and instances.

    Capabilities provided:

    * Get information about resources [from ResourceInformation(Bundle)]:
      - Queues:
        . Name;
        . allowed walltime;
        . prediction on queuing time depending on the job size.
    * Get general information about workload: 
      - Total time required for its execution [from Planner];
      - total space required for its execution [from Planner]:
        . # of cores.
    * Get information about compute unit [from WorkloadManager]:
      - Time required;
      - Space required:
        . # of cores.
      - Grouping with other Units.
    * describe pilots.
    * Schedule pilots on resources.
    * Provision pilots on resources [by means of Provisioner].

    """
    _pilot_id_map = dict()

    def __init__(self, session, translator=AUTOMATIC, scheduler=AUTOMATIC, provisioner=AUTOMATIC):
        """
        Create a new overlay manager instance.

        Use default plugins if not otherwise indicated.  Note that the
        provisioner plugin is actually not owned by the OverlayManager, but by
        the pilots of the Overlay managed by the OverlayManager.
        """
        self.session = session
        self.id = ru.generate_id('olm.')
        tu.Timed.__init__(self, 'troy.OverlayManager', self.id)
        self.session.timed_component(self, 'troy.OverlayManager', self.id)
        self._plugin_mgr = None
        self.plugins = dict()
        self.plugins['translator'] = translator
        self.plugins['scheduler'] = scheduler
        self.plugins['provisioner'] = provisioner
        cfg = session.get_config('overlay_manager')
        if 'plugin_overlay_translator' in cfg:
            self.plugins['translator'] = cfg['plugin_overlay_translator']
        if 'plugin_overlay_scheduler' in cfg:
            self.plugins['scheduler'] = cfg['plugin_overlay_scheduler']
        if 'plugin_overlay_provisioner' in cfg:
            self.plugins['provisioner'] = cfg['plugin_overlay_provisioner']
        return

    def _init_plugins(self, workload_mgr=None):
        if self._plugin_mgr:
            if workload_mgr:
                troy._logger.warning('Ignore overlay_mgr re-initialization')
            return
        if self.plugins['translator'] == AUTOMATIC:
            self.plugins['translator'] = 'max_pilot_size'
        if self.plugins['scheduler'] == AUTOMATIC:
            self.plugins['scheduler'] = 'local'
        if self.plugins['provisioner'] == AUTOMATIC:
            if workload_mgr:
                self.plugins['provisioner'] = workload_mgr.plugins['dispatcher']
        if self.plugins['provisioner'] == AUTOMATIC:
            self.plugins['provisioner'] = 'local'
        self._plugin_mgr = ru.PluginManager('troy')
        self._translator = self._plugin_mgr.load('overlay_translator', self.plugins['translator'])
        self._scheduler = self._plugin_mgr.load('overlay_scheduler', self.plugins['scheduler'])
        self._provisioner = self._plugin_mgr.load('overlay_provisioner', self.plugins['provisioner'])
        if not self._translator:
            raise RuntimeError('Could not load translator  plugin')
        if not self._scheduler:
            raise RuntimeError('Could not load scheduler   plugin')
        if not self._provisioner:
            raise RuntimeError('Could not load provisioner plugin')
        self._translator.init_plugin(self.session, 'overlay_manager')
        self._scheduler.init_plugin(self.session, 'overlay_manager')
        self._provisioner.init_plugin(self.session, 'overlay_manager')
        troy._logger.info('initialized  overlay manager (%s)' % self.plugins)

    @classmethod
    def register_overlay(cls, overlay):
        ru.Registry.register(overlay)

    @classmethod
    def unregister_overlay(cls, overlay_id):
        ru.Registry.unregister(overlay_id)

    @classmethod
    def native_id_to_pilot_id(cls, native_id):
        for troy_id in cls._pilot_id_map:
            if native_id == cls._pilot_id_map[troy_id]:
                return troy_id

        return

    @classmethod
    def pilot_id_to_native_id(cls, pilot_id, native_id=None):
        if native_id:
            if pilot_id in cls._pilot_id_map:
                raise ValueError('Cannot register that pilot id -- already known')
            cls._pilot_id_map[pilot_id] = native_id
        else:
            if pilot_id not in cls._pilot_id_map:
                raise ValueError("no such pilot known '%s'" % pilot_id)
            return cls._pilot_id_map[pilot_id]

    @classmethod
    def get_overlay(cls, overlay_id, _manager=None):
        """
        We don't care about locking at this point -- so we simply release the
        overlay immediately...
        """
        if not overlay_id:
            return None
        else:
            if not overlay_id.startswith('ol.'):
                raise ValueError("'%s' does not represent a overlay" % overlay_id)
            overlay = ru.Registry.acquire(overlay_id, ru.READONLY)
            ru.Registry.release(overlay_id)
            if _manager:
                _manager.timed_component(overlay, 'troy.Overlay', overlay_id)
            return overlay

    def translate_overlay(self, overlay_id):
        """
        Inspect backend resources, and select suitable resources for the
        overlay.

        See the documentation of the :class:`Overlay` class on how exactly the
        scheduler changes and/or annotates the given overlay.
        """
        overlay = self.get_overlay(overlay_id)
        self.timed_component(overlay, 'troy.Overlay', overlay.id)
        if overlay.state != DESCRIBED:
            raise ValueError("overlay '%s' not in DESCRIBED state" % overlay.id)
        self._init_plugins()
        overlay.timed_method('translate', [], self._translator.translate, [overlay])
        overlay.state = TRANSLATED

    def schedule_overlay(self, overlay_id):
        """
        Inspect backend resources, and select suitable resources for the
        overlay.

        See the documentation of the :class:`Overlay` class on how exactly the
        scheduler changes and/or annotates the given overlay.
        """
        overlay = self.get_overlay(overlay_id)
        self.timed_component(overlay, 'troy.Overlay', overlay.id)
        if overlay.state != TRANSLATED:
            raise ValueError("overlay '%s' not in TRANSLATED state" % overlay.id)
        self._init_plugins()
        overlay.timed_method('schedule', [], self._scheduler.schedule, [overlay])
        overlay.state = SCHEDULED

    def provision_overlay(self, overlay_id):
        """
        Create pilot instances for each pilot described in the overlay.

        See the documentation of the :class:`Overlay` class on how exactly the
        scheduler changes and/or annotates the given overlay.
        """
        overlay = self.get_overlay(overlay_id)
        self.timed_component(overlay, 'troy.Overlay', overlay.id)
        if overlay.state != SCHEDULED:
            raise ValueError("overlay '%s' not in SCHEDULED state" % overlay.id)
        self._init_plugins()
        for pilot_id, pilot in overlay.pilots.iteritems():
            resource_cfg = self.session.get_resource_config(pilot.resource)
            pilot.merge_description(resource_cfg)

        overlay.timed_method('provision', [], self._provisioner.provision, [overlay])
        overlay.state = PROVISIONED

    def cancel_overlay(self, overlay_id):
        """
        cancel the referenced overlay, i.e. all its pilots
        """
        overlay = self.get_overlay(overlay_id)
        self.timed_component(overlay, 'troy.Overlay', overlay.id)
        overlay.timed_method('cancel', [], overlay.cancel)
        overlay.cancel()