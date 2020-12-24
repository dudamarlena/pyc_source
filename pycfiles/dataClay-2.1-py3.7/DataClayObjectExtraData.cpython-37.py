# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/DataClayObjectExtraData.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 2441 bytes
"""Custom container for holding extra information on classes.

The dataClay friendly classed (either before registration or stub-generated
ones) will contain their extra information --like the full_name, the class_id
or the namespace-- in DataClayExtraData instances.
"""
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class DataClayCommonExtraData(object):
    __doc__ = 'ExtraData commonlib base class.\n\n    ExtraData behaves as a dictionary, with some optional extras.\n    '
    __slots__ = list()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        for s in self.__slots__:
            try:
                _ = getattr(self, s)
            except AttributeError:
                setattr(self, s, None)

    def __str__(self):
        ret = [
         '{%s contents:' % self.__class__.__name__]
        for s in self.__slots__:
            ret.append('  %s: %s' % (s, getattr(self, s)))

        ret.append('}')
        return '\n'.join(ret)


class DataClayClassExtraData(DataClayCommonExtraData):
    __doc__ = 'Container for ExtraData related to a certain dataClay Class\n\n    Instances for this class are typically associated to DataClayObject\n    derived classes (and automatically populated by the ExecutionGateway).\n    '
    __slots__ = ('full_name', 'namespace', 'classname', 'class_id', 'properties', 'imports',
                 'stub_info', 'metaclass_container')


class DataClayInstanceExtraData(DataClayCommonExtraData):
    __doc__ = 'Container for ExtraData related to a certain dataClay Object instance.\n\n    Instances for this class are typically created and assigned to a certain\n    DataClayObject instance when creating them. The ExecutionGateway populates\n    its data.\n    '
    __slots__ = ('persistent_flag', 'object_id', 'master_location', 'dataset_id', 'execenv_id',
                 'loaded_flag', 'pending_to_register_flag', 'owner_session_id', 'dirty_flag',
                 'memory_pinned')