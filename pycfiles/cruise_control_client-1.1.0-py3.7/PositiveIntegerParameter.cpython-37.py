# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/PositiveIntegerParameter.py
# Compiled at: 2019-07-09 13:29:06
# Size of source mod 2**32: 2525 bytes
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractPositiveIntegerParameter(AbstractParameter):

    def __init__(self, value: int):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != int:
            raise ValueError(f"{self.value} is not an integer value")
        else:
            if self.value < 1:
                raise ValueError(f"{self.value} must be a positive integer")


class ConcurrentLeaderMovementsParameter(AbstractPositiveIntegerParameter):
    __doc__ = 'concurrent_leader_movements=[POSITIVE-INTEGER]'
    name = 'concurrent_leader_movements'
    description = 'The maximum number of concurrent leadership movements across the entire cluster'
    argparse_properties = {'args':('--leader-concurrency', '--leadership-concurrency', '--concurrent-leader-movements'), 
     'kwargs':dict(metavar='K', help=description, type=int)}


class ConcurrentPartitionMovementsPerBrokerParameter(AbstractPositiveIntegerParameter):
    __doc__ = 'concurrent_partition_movements_per_broker=[POSITIVE-INTEGER]'
    name = 'concurrent_partition_movements_per_broker'
    description = 'The maximum number of concurrent partition movements per broker'
    argparse_properties = {'args':('--concurrency', '--concurrent-partition-movements-per-broker'), 
     'kwargs':dict(metavar='K', help=description, type=int)}


class DataFromParameter(AbstractPositiveIntegerParameter):
    __doc__ = 'data_from=[valid_windows/valid_partitions]'
    name = 'data_from'
    description = 'The number of valid [windows, partitions] from which to use data'
    argparse_properties = {'args':('--data-from', ), 
     'kwargs':dict(metavar='K', help=description, type=int)}


class EntriesParameter(AbstractPositiveIntegerParameter):
    __doc__ = 'entries=[number-of-entries-to-show]'
    name = 'entries'
    description = 'The number of entries to show in the response'
    argparse_properties = {'args':('--number-of-entries-to-show', '--num-entries'), 
     'kwargs':dict(metavar='K', help=description, type=int)}


class ReplicationFactorParameter(AbstractPositiveIntegerParameter):
    __doc__ = 'replication_factor=[target_replication_factor]'
    name = 'replication_factor'
    description = 'The target replication factor to which the specified topics should be set'
    argparse_properties = {'args':('--replication-factor', ), 
     'kwargs':dict(metavar='K', help=description, type=int)}