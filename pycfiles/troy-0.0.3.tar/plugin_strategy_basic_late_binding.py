# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/strategy/plugin_strategy_basic_late_binding.py
# Compiled at: 2014-02-27 11:31:04
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'strategy', 
   'name': 'basic_late_binding', 
   'version': '0.1', 
   'description': 'this is the basic troy strategy for executing workloads.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    The late binding strategy will execute a workload in very basic fasion: use
    planner, overlay_mgr and workload_mgr as configured, etc.  The interesting
    part is that it will schedule the units over the pilots *after* the pilots
    are scheduled over resources.  That scheduling will have more information
    then, but happens rather late in the game.
    
    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def execute(self, workload_id, planner, overlay_mgr, workload_mgr):
        """
        run the given workload, using the given managers, in late-binding mode.
        """
        workload = None
        overlay = None
        try:
            troy._logger.info('troy default strategy : strategize workload %s!' % workload_id)
            workload = workload_mgr.get_workload(workload_id)
            planner.expand_workload(workload.id)
            overlay_descr = planner.derive_overlay(workload.id)
            overlay = troy.Overlay(overlay_mgr.session, overlay_descr)
            overlay_mgr.translate_overlay(overlay.id)
            overlay_mgr.schedule_overlay(overlay.id)
            overlay_mgr.provision_overlay(overlay.id)
            workload_mgr.translate_workload(workload.id, overlay.id)
            for partition_id in workload.partitions:
                troy._logger.info('running workload partition %s' % partition_id)
                partition = troy.WorkloadManager.get_workload(partition_id)
                workload.state = partition.state
                workload_mgr.bind_workload(partition.id, overlay.id, bind_mode=troy.LATE)
                workload.state = partition.state
                workload_mgr.stage_in_workload(partition_id)
                workload_mgr.dispatch_workload(partition.id, overlay.id)
                workload.state = partition.state
                partition.wait()
                workload.state = partition.state
                if partition.state == troy.DONE:
                    troy._logger.info('partition %s done' % partition.id)
                else:
                    troy._logger.error('partition %s failed - abort' % partition.id)
                    raise RuntimeError('partition %s failed - abort' % partition.id)
                workload_mgr.stage_out_workload(partition_id)

            troy._logger.info('all partition done (%s)' % workload.state)
            overlay_mgr.cancel_overlay(overlay.id)
        except Exception as e:
            troy._logger.critical('strategy execution failed: %s' % e)
            if workload:
                troy._logger.warn('shutting down workload: %s' % workload.id)
                workload_mgr.cancel_workload(workload.id)
            if overlay:
                troy._logger.warn('shutting down overlay: %s' % overlay.id)
                overlay_mgr.cancel_overlay(overlay.id)

        return