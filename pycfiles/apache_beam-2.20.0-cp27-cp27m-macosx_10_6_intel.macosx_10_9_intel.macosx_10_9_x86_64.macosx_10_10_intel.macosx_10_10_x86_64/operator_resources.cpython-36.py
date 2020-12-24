# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/operator_resources.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 3770 bytes
from airflow import configuration
from airflow.exceptions import AirflowException
MB = 1
GB = 1024 * MB
TB = 1024 * GB
PB = 1024 * TB
EB = 1024 * PB

class Resource(object):
    """Resource"""

    def __init__(self, name, units_str, qty):
        if qty < 0:
            raise AirflowException('Received resource quantity {} for resource {} but resource quantity must be non-negative.'.format(qty, name))
        self._name = name
        self._units_str = units_str
        self._qty = qty

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @property
    def name(self):
        return self._name

    @property
    def units_str(self):
        return self._units_str

    @property
    def qty(self):
        return self._qty


class CpuResource(Resource):

    def __init__(self, qty):
        super(CpuResource, self).__init__('CPU', 'core(s)', qty)


class RamResource(Resource):

    def __init__(self, qty):
        super(RamResource, self).__init__('RAM', 'MB', qty)


class DiskResource(Resource):

    def __init__(self, qty):
        super(DiskResource, self).__init__('Disk', 'MB', qty)


class GpuResource(Resource):

    def __init__(self, qty):
        super(GpuResource, self).__init__('GPU', 'gpu(s)', qty)


class Resources(object):
    """Resources"""

    def __init__(self, cpus=configuration.conf.getint('operators', 'default_cpus'), ram=configuration.conf.getint('operators', 'default_ram'), disk=configuration.conf.getint('operators', 'default_disk'), gpus=configuration.conf.getint('operators', 'default_gpus')):
        self.cpus = CpuResource(cpus)
        self.ram = RamResource(ram)
        self.disk = DiskResource(disk)
        self.gpus = GpuResource(gpus)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)