# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/workload/compute_unit_description.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class ComputeUnitDescription(tu.Properties):
    """
    The `ComputeUnitDescription` class is a simple container for properties
    which describe a :class:`ComputeUnit`, i.e. a workload element.
    `ComputeUnitDescription`s are submitted to :class:`WorkloadManager`
    instances on `add_task`, and are internally used to create
    :class:`ComputeUnit` instances.

    FIXME: description of supported properties goes here
    """

    def __init__(self, descr={}):
        tu.Properties.__init__(self, descr)
        self.register_property('executable')
        self.register_property('arguments')
        self.register_property('working_directory')

    def __str__(self):
        return str(self.as_dict())

    def __repr__(self):
        return self.as_dict()