# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/workload_translator/plugin_workload_translator_direct.py
# Compiled at: 2014-02-27 11:31:04
import radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'workload_translator', 
   'name': 'direct', 
   'version': '0.1', 
   'description': 'this is a sime translator which defines one CU per task.'}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This is a simple workload translator, which will create exactly one CU per
    task.  This is not a clever plugin.
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def translate(self, workload, overlay=None):
        """
        Iterate over tasks, and essentially cast the task's description into
        a CU description.  Et voila!
        """
        for tid in workload.tasks.keys():
            task = workload.tasks[tid]
            cu_descr = troy.ComputeUnitDescription(task.as_dict())
            cu_id = task._add_unit(cu_descr)
            troy._logger.info('workload translate: derive unit %-18s for %s' % (cu_id, task.id))