# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/Endpoint.py
# Compiled at: 2020-03-16 18:59:53
# Size of source mod 2**32: 22169 bytes
from abc import ABCMeta
import cruisecontrolclient.client.CCParameter as CCParameter
from typing import Callable, ClassVar, Dict, List, Tuple, Union

class AbstractEndpoint(metaclass=ABCMeta):
    __doc__ = '\n    An abstract representation of a cruise-control endpoint.\n\n    Note that this class also provides methods for returning a correctly-\n    concatenated endpoint with parameters.\n    '
    name: ClassVar[str]
    description: ClassVar[str]
    http_method: ClassVar[str]
    can_execute_proposal: ClassVar[bool]
    available_Parameters: ClassVar[Tuple[CCParameter.AbstractParameter]]
    argparse_properties = {'args':(), 
     'kwargs':{}}
    argparse_properties: ClassVar[Dict[(str, Union[(Tuple[str], Dict[(str, str)])])]]

    def __init__(self):
        self.parameter_name_to_available_Parameters = {ap.name:ap for ap in self.available_Parameters}
        self.parameter_name_to_instantiated_Parameters = {}
        self.parameter_name_to_value = {}

    def add_param(self, parameter_name: str, value: Union[(str, int, bool)]) -> None:
        """
        Adds this parameter to this Endpoint, overriding any previous value-definition
        for this parameter.

        If the supplied 'parameter' matches one of the known Parameters for this
        Endpoint, that Parameter will be instantiated and its value validated.
        If the supplied value is not valid, Parameter will raise a ValueError.

        If the supplied 'parameter' does not match one of the known Parameters
        for this Endpoint, that 'parameter': 'value' mapping will be added to
        self.parameter_name_to_value without validation.

        :param parameter_name:
        :param value:
        :return:
        """
        if parameter_name in self.parameter_name_to_available_Parameters:
            Parameter_to_instantiate = self.parameter_name_to_available_Parameters[parameter_name]
            self.parameter_name_to_instantiated_Parameters[parameter_name] = Parameter_to_instantiate(value)
        else:
            self.parameter_name_to_value[parameter_name] = value

    def get_value(self, parameter_name: str) -> Union[(str, None)]:
        """
        Returns value if this parameter exists in this endpoint.

        Returns None otherwise

        :param parameter_name:
        :return:
        """
        if parameter_name in self.parameter_name_to_instantiated_Parameters:
            return self.parameter_name_to_instantiated_Parameters[parameter_name].value
        if parameter_name in self.parameter_name_to_value:
            return self.parameter_name_to_value[parameter_name]
        return

    def has_param(self, parameter_name: str) -> bool:
        """
        Returns True if this endpoint already has this parameter, False otherwise.

        :param parameter_name:
        :return:
        """
        return parameter_name in self.parameter_name_to_instantiated_Parameters or parameter_name in self.parameter_name_to_value

    def remove_param(self, parameter_name: str) -> None:
        """
        Remove this parameter from this Endpoint.

        If the supplied 'parameter' matches one of the known Parameters for this
        Endpoint, that Parameter will be removed from self.parameter_name_to_instantiated_Parameters.

        If the supplied 'parameter' does not match one of the known Parameters
        for this Endpoint, that 'parameter': 'value' mapping will be removed from
        self.parameter_name_to_value, if present.

        :param parameter_name:
        :return:
        """
        if parameter_name in self.parameter_name_to_instantiated_Parameters:
            self.parameter_name_to_instantiated_Parameters.pop(parameter_name)
        else:
            if parameter_name in self.parameter_name_to_value:
                self.parameter_name_to_value.pop(parameter_name)

    def get_composed_params(self) -> Dict[(str, Union[(bool, int, str)])]:
        """
        Returns a requests-compatible dictionary of this Endpoint's current parameters.

        :return: A dict like:
            {'json': True,
             'allow_capacity_estimation': False}
        """
        combined_parameter_to_value = {}
        if self.parameter_name_to_instantiated_Parameters:
            combined_parameter_to_value.update({name:ip.value for name, ip in self.parameter_name_to_instantiated_Parameters.items()})
        if self.parameter_name_to_value:
            combined_parameter_to_value.update(self.parameter_name_to_value)
        return combined_parameter_to_value


class AddBrokerEndpoint(AbstractEndpoint):
    name = 'add_broker'
    description = 'Move partitions to the specified brokers, according to the specified goals'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.BrokerIdParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.ExcludedTopicsParameter,
     CCParameter.GoalsParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.SkipHardGoalCheckParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.ThrottleRemovedBrokerParameter,
     CCParameter.UseReadyDefaultGoalsParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=['add_brokers', 'add-broker', 'add-brokers'], help=description)}

    def __init__(self, broker_ids: Union[(str, List[str])]):
        AbstractEndpoint.__init__(self)
        self.add_param('brokerid', broker_ids)


class AdminEndpoint(AbstractEndpoint):
    name = 'admin'
    description = 'Used to change runtime configurations on the cruise-control server itself'
    http_method = 'POST'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DisableSelfHealingForParameter,
     CCParameter.DropRecentlyDemotedBrokersParameter,
     CCParameter.DropRecentlyRemovedBrokersParameter,
     CCParameter.EnableSelfHealingForParameter,
     CCParameter.JSONParameter,
     CCParameter.ReviewIDParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}


class BootstrapEndpoint(AbstractEndpoint):
    name = 'bootstrap'
    description = 'Bootstrap the load monitor'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.ClearMetricsParameter,
     CCParameter.EndParameter,
     CCParameter.JSONParameter,
     CCParameter.StartParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}


class DemoteBrokerEndpoint(AbstractEndpoint):
    name = 'demote_broker'
    description = 'Remove leadership and preferred leadership from the specified brokers'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.BrokerIdParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeFollowerDemotionParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.SkipURPDemotionParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=['demote_brokers', 'demote-broker', 'demote-brokers'], help=description)}

    def __init__(self, broker_ids: Union[(str, List[str])]):
        AbstractEndpoint.__init__(self)
        self.add_param('brokerid', broker_ids)


class FixOfflineReplicasEndpoint(AbstractEndpoint):
    name = 'fix_offline_replicas'
    description = 'Fixes the offline replicas in the cluster (kafka 1.1+ only)'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.ExcludedTopicsParameter,
     CCParameter.GoalsParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.SkipHardGoalCheckParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.UseReadyDefaultGoalsParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class KafkaClusterStateEndpoint(AbstractEndpoint):
    name = 'kafka_cluster_state'
    description = 'Get under-replicated and offline partitions (and under MinISR partitions in kafka 2.0+)'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.JSONParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class LoadEndpoint(AbstractEndpoint):
    name = 'load'
    description = 'Get the load on each kafka broker'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.JSONParameter,
     CCParameter.TimeParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}

    def __init__(self):
        AbstractEndpoint.__init__(self)


class PartitionLoadEndpoint(AbstractEndpoint):
    name = 'partition_load'
    description = 'Get the resource load for each partition'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.EndParameter,
     CCParameter.EntriesParameter,
     CCParameter.JSONParameter,
     CCParameter.MaxLoadParameter,
     CCParameter.MinValidPartitionRatioParameter,
     CCParameter.PartitionParameter,
     CCParameter.ResourceParameter,
     CCParameter.StartParameter,
     CCParameter.TopicParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class PauseSamplingEndpoint(AbstractEndpoint):
    name = 'pause_sampling'
    description = 'Pause metrics load sampling'
    http_method = 'POST'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReviewIDParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class ProposalsEndpoint(AbstractEndpoint):
    name = 'proposals'
    description = 'Get current proposals'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.DataFromParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.ExcludedTopicsParameter,
     CCParameter.GoalsParameter,
     CCParameter.IgnoreProposalCacheParameter,
     CCParameter.JSONParameter,
     CCParameter.UseReadyDefaultGoalsParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}


class RebalanceEndpoint(AbstractEndpoint):
    name = 'rebalance'
    description = 'Rebalance the partition distribution in the kafka cluster, according to the specified goals'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DestinationBrokerIdsParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.ExcludedTopicsParameter,
     CCParameter.GoalsParameter,
     CCParameter.IgnoreProposalCacheParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.SkipHardGoalCheckParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.UseReadyDefaultGoalsParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}

    def __init__(self):
        AbstractEndpoint.__init__(self)


class RemoveBrokerEndpoint(AbstractEndpoint):
    name = 'remove_broker'
    description = 'Remove all partitions from the specified brokers, according to the specified goals'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.BrokerIdParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DestinationBrokerIdsParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.ExcludedTopicsParameter,
     CCParameter.GoalsParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.SkipHardGoalCheckParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.ThrottleRemovedBrokerParameter,
     CCParameter.UseReadyDefaultGoalsParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=['remove_brokers', 'remove-broker', 'remove-brokers'], help=description)}

    def __init__(self, broker_ids: Union[(str, List[str])]):
        AbstractEndpoint.__init__(self)
        self.add_param('brokerid', broker_ids)


class ResumeSamplingEndpoint(AbstractEndpoint):
    name = 'resume_sampling'
    description = 'Resume metrics load sampling'
    http_method = 'POST'
    can_execute_proposal = False
    available_Parameters = {
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReviewIDParameter}
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class ReviewEndpoint(AbstractEndpoint):
    name = 'review'
    description = 'Create, approve, or discard reviews'
    http_method = 'POST'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.ApproveParameter,
     CCParameter.DiscardParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}


class ReviewBoardEndpoint(AbstractEndpoint):
    name = 'review_board'
    description = 'View already-created reviews'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.JSONParameter,
     CCParameter.ReviewIDsParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class StateEndpoint(AbstractEndpoint):
    name = 'state'
    description = 'Get the state of cruise control'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.JSONParameter,
     CCParameter.SubstatesParameter,
     CCParameter.SuperVerboseParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}

    def __init__(self):
        AbstractEndpoint.__init__(self)
        self.add_param('substates', 'executor')


class StopProposalExecutionEndpoint(AbstractEndpoint):
    name = 'stop_proposal_execution'
    description = 'Stop the currently-executing proposal'
    http_method = 'POST'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.JSONParameter,
     CCParameter.ReviewIDParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-'), 'stop'], help=description)}


class TopicConfigurationEndpoint(AbstractEndpoint):
    name = 'topic_configuration'
    description = 'Update the configuration of the specified topics'
    http_method = 'POST'
    can_execute_proposal = True
    available_Parameters = (
     CCParameter.AllowCapacityEstimationParameter,
     CCParameter.ConcurrentLeaderMovementsParameter,
     CCParameter.ConcurrentPartitionMovementsPerBrokerParameter,
     CCParameter.DryRunParameter,
     CCParameter.ExcludeRecentlyDemotedBrokersParameter,
     CCParameter.ExcludeRecentlyRemovedBrokersParameter,
     CCParameter.GoalsParameter,
     CCParameter.JSONParameter,
     CCParameter.ReasonParameter,
     CCParameter.ReplicaMovementStrategiesParameter,
     CCParameter.ReplicationFactorParameter,
     CCParameter.ReviewIDParameter,
     CCParameter.SkipHardGoalCheckParameter,
     CCParameter.SkipRackAwarenessCheckParameter,
     CCParameter.StopOngoingExecutionParameter,
     CCParameter.TopicParameter,
     CCParameter.VerboseParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=[name.replace('_', '-')], help=description)}


class TrainEndpoint(AbstractEndpoint):
    name = 'train'
    description = 'Train the linear regression model'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.EndParameter,
     CCParameter.JSONParameter,
     CCParameter.StartParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(help=description)}


class UserTasksEndpoint(AbstractEndpoint):
    name = 'user_tasks'
    description = 'Get the recent user tasks from cruise control'
    http_method = 'GET'
    can_execute_proposal = False
    available_Parameters = (
     CCParameter.ClientIdsParameter,
     CCParameter.EndpointsParameter,
     CCParameter.EntriesParameter,
     CCParameter.JSONParameter,
     CCParameter.TypesParameter,
     CCParameter.UserTaskIdsParameter)
    argparse_properties = {'args':(
      name,), 
     'kwargs':dict(aliases=['user_task', 'user-tasks', 'user-task'], help=description)}