# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/planner_derive/plugin_planner_derive_bundles.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru
from troy.constants import *
import troy
from bundle import BundleManager
PLUGIN_DESCRIPTION = {'type': 'derive', 
   'name': 'bundles', 
   'version': '0.1', 
   'description': 'This plugin derives an overlay from bundles information.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin is not used at this point.

    **Configuration Options:**

    * `guard`: documentation for guard
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def init(self):
        troy._logger.debug('init plugin %s (bundles)' % self.name)
        self.guard = self.cfg.get('guard', None)
        self.init_bundles()
        return

    def init_bundles(self):
        troy._logger.info('Initializing Bundle Manager')
        self.bm = BundleManager()
        cg = self.session.get_config('troy:bundle')
        finished_job_trace = cg['finished_job_trace']
        for sect in self.session.get_config('troy:resources'):
            cs = self.session.cfg.get_config(sect)
            cred = {'port': int(cs['port'].get_value()), 'hostname': cs['endpoint'].get_value(), 
               'cluster_type': cs['type'].get_value(), 
               'username': cs['username'].get_value(), 
               'password': cs['password'].get_value(), 
               'key_filename': cs['ssh_key'].get_value(), 
               'h_flag': cs['h_flag'].get_value()}
            self.bm.add_cluster(cred, finished_job_trace)

        if 'pilot_size' in self.cfg:
            pilot_size = int(self.cfg['pilot_size'])
        self.cluster_list = self.bm.get_cluster_list()
        if not self.cluster_list:
            raise RuntimeError('No clusters available in Bundle Manager. You might want to check your config file.')

    def check_resource_availability(self, overlay_desc):
        resource_request = {'p_procs': overlay_desc.cores, 'est_runtime': overlay_desc.walltime}
        predictions = {}
        for cluster in self.cluster_list:
            predictions[cluster] = self.bm.resource_predict(cluster, resource_request)

        usable = filter(lambda x: x != -1, predictions.values())
        if not usable:
            raise RuntimeError('No resources available that can fulfill this request!')

    def derive_overlay(self, workload, guard=LOWER_LIMIT):
        """
        Based on obtained bundle information, derive a useful overlay
        description.  Guard is respected.
        """
        if self.guard == UPPER_LIMIT:
            cores = len(workload.tasks)
        elif self.guard == LOWER_LIMIT:
            cores = 1
        else:
            raise RuntimeError('Unknown guard: "%d') % self.guard
        ovl_descr = troy.OverlayDescription({'cores': cores})
        troy._logger.info('planner derive ol: derive overlay for workload: %s' % ovl_descr)
        self.check_resource_availability(ovl_descr)
        return ovl_descr