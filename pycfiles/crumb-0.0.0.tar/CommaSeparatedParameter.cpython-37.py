# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/CommaSeparatedParameter.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 5674 bytes
from typing import Union, List
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractCommaSeparatedParameter(AbstractParameter):

    def __init__(self, value: Union[(str, List[str])]):
        if type(value) == list:
            value = ','.join(value)
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != str:
            raise ValueError(f"{self.value} is not a string value")


class ApproveParameter(AbstractCommaSeparatedParameter):
    """ApproveParameter"""
    name = 'approve'
    description = 'The review IDs to approve'
    argparse_properties = {'args':('--approve', ), 
     'kwargs':dict(help=description, nargs='+')}


class BrokerIdParameter(AbstractCommaSeparatedParameter):
    """BrokerIdParameter"""
    name = 'brokerid'
    description = 'Comma-separated and/or space-separated list of broker IDs'
    argparse_properties = {'args':('brokers', ), 
     'kwargs':dict(help=description, nargs='+')}


class ClientIdsParameter(AbstractCommaSeparatedParameter):
    """ClientIdsParameter"""
    name = 'client_ids'
    description = 'The set of Client IDs by which to filter the user_tasks response'
    argparse_properties = {'args':('--client-id', '--client-ids'), 
     'kwargs':dict(help=description, nargs='+')}


class DestinationBrokerIdsParameter(AbstractCommaSeparatedParameter):
    """DestinationBrokerIdsParameter"""
    name = 'destination_broker_ids'
    description = 'Comma-separated and/or space-separated list of broker IDs'
    argparse_properties = {'args':('--destination-broker', '--destination-brokers', '--destination-broker-id', '--destination-broker-ids'), 
     'kwargs':dict(help=description, nargs='+')}


class DiscardParameter(AbstractCommaSeparatedParameter):
    """DiscardParameter"""
    name = 'discard'
    description = 'The review IDs to discard'
    argparse_properties = {'args':('--discard', ), 
     'kwargs':dict(help=description, nargs='+')}


class DropRecentlyDemotedBrokersParameter(AbstractCommaSeparatedParameter):
    """DropRecentlyDemotedBrokersParameter"""
    name = 'drop_recently_demoted_brokers'
    description = 'Comma-separated and/or space-separated list of broker IDs'
    argparse_properties = {'args':('--drop-recently-demoted-broker', '--drop-recently-demoted-brokers', '--drop-recently-demoted-broker-id',
 '--drop-recently-demoted-brokers-ids'), 
     'kwargs':dict(help=description, nargs='+')}


class DropRecentlyRemovedBrokersParameter(AbstractCommaSeparatedParameter):
    """DropRecentlyRemovedBrokersParameter"""
    name = 'drop_recently_removed_brokers'
    description = 'Comma-separated and/or space-separated list of broker IDs'
    argparse_properties = {'args':('--drop-recently-removed-broker', '--drop-recently-removed-brokers', '--drop-recently-removed-broker-id',
 '--drop-recently-removed-brokers-ids'), 
     'kwargs':dict(help=description, nargs='+')}


class EndpointsParameter(AbstractCommaSeparatedParameter):
    """EndpointsParameter"""
    name = 'endpoints'
    description = 'The set of Endpoint by which to filter the user_tasks response'
    argparse_properties = {'args':('--endpoint', '--endpoints'), 
     'kwargs':dict(help=description, nargs='+')}


class GoalsParameter(AbstractCommaSeparatedParameter):
    """GoalsParameter"""
    name = 'goals'
    description = 'Comma-separated and/or space-separated ordered list of goals'
    argparse_properties = {'args':('--goals', ), 
     'kwargs':dict(help=description, nargs='+')}


class ReplicaMovementStrategiesParameter(AbstractCommaSeparatedParameter):
    """ReplicaMovementStrategiesParameter"""
    name = 'replica_movement_strategies'
    description = 'Comma-separated and/or space-separated list of replica movement strategies'
    argparse_properties = {'args':('--strategies', ), 
     'kwargs':dict(help=description, nargs='+')}


class ReviewIDsParameter(AbstractCommaSeparatedParameter):
    """ReviewIDsParameter"""
    name = 'review_ids'
    description = 'The review IDs by which to filter the review_board response'
    argparse_properties = {'args':('--review-ids', '--review-id', '--reviews', '--review'), 
     'kwargs':dict(help=description, nargs='+')}


class TypesParameter(AbstractCommaSeparatedParameter):
    """TypesParameter"""
    name = 'types'
    description = 'The set of TaskStates by which to filter the user_tasks response'
    argparse_properties = {'args':('--types', '--type', '--task-states', '--task-state'), 
     'kwargs':dict(help=description, nargs='+')}


class UserTaskIdsParameter(AbstractCommaSeparatedParameter):
    """UserTaskIdsParameter"""
    name = 'user_task_ids'
    description = 'The set of UserTaskIDs by which to filter the user_tasks response'
    argparse_properties = {'args':('--user-task-ids', '--user-task-id'), 
     'kwargs':dict(help=description, nargs='+')}