# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/workload/task_description.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu

class TaskDescription(tu.Properties):
    """
    The `TaskDescription` class is a simple container for properties which
    describe a :class:`Task`, i.e. a workload element.  `TaskDescription`s are
    submitted to :class:`WorkloadManager` instances on `add_task`, and are
    internally used to create :class:`Task` instances.

    FIXME: description of supported properties goes here
    """

    def __init__(self, descr={}):
        self.tag = None
        self.cardinality = 1
        self.executable = None
        self.arguments = list()
        self.stdin = None
        self.stdout = None
        self.cores = 1
        self.inputs = list()
        self.outputs = list()
        tu.Properties.__init__(self, descr)
        return

    def expand_description(self, session):
        td_dict = self.as_dict()
        print td_dict
        ru.dict_stringexpand(td_dict, session.cfg)
        print td_dict
        tu.Properties.__init__(self, td_dict)