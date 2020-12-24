# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/planner_expand/plugin_planner_expand_cardinal.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import copy, radical.utils as ru
from troy.constants import *
import troy
PLUGIN_DESCRIPTION = {'type': 'expand', 
   'name': 'cardinal', 
   'version': '0.1', 
   'description': "This workload expander can multiplies tasks according to their 'cardinality' property."}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This plugin expands a workload by inspecting all tasks, and multiplying them
    according to their `cardinality` property.  If that property is not set, no
    additional tasks will be created.  The new tasks will have a new property,
    `cardinal`, which is set to their index respecitive to their sibling tasks.
    That property can also be used for expansion in other task properties.
    workload tasks.
    
    **Configuration Options:** None
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def expand_workload(self, workload):
        """
        Inspect all workload tasks, check if cardinality is set and larger than
        1.  If so, created that many identical tasks, assign them an `cardinal`
        index, and have that set replace the original task.  All new tasks
        will have a cardinality of 1.
        """
        task_descriptions = list()
        for task_id in workload.tasks:
            task = workload.tasks[task_id]
            task_dict = task.as_dict()
            ru.dict_stringexpand(task_dict, self.session.cfg)
            if 'cardinality' in task_dict:
                cardinality = int(task_dict['cardinality'])
                for c in range(cardinality):
                    new_task_dict = copy.deepcopy(task_dict)
                    new_task_dict['cardinality'] = 1
                    new_task_dict['cardinal'] = c
                    task_descriptions.append(troy.TaskDescription(new_task_dict))

            else:
                task_descriptions.append(task.as_dict())

        workload.tasks = dict()
        workload.add_task(task_descriptions)
        troy._logger.info('planner  expand wl cardinality: %s' % workload)