# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/planner_derive/plugin_planner_derive_maxcores.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'derive', 
   'name': 'maxcores', 
   'version': '0.1', 
   'description': 'This plugin derives an overlay size by counting cores'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin determines the overlay size by simply adding the sizes of all
    workload tasks.
    
    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def derive_overlay(self, workload):
        """
        Counts the cores needed to run the workload, assuming that all tasks are
        to be running concurrently.
        """
        cores = 0
        for task_id in workload.tasks:
            cores += workload.tasks[task_id].cores

        ovl_descr = troy.OverlayDescription({'cores': cores})
        troy._logger.info('planner  derive ol: derive overlay for workload: %s' % ovl_descr)
        return ovl_descr