# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/BooleanParameter.py
# Compiled at: 2020-03-16 18:59:53
# Size of source mod 2**32: 8623 bytes
from typing import Union
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter
set_of_choices = {
 'true', 'false'}

class AbstractBooleanParameter(AbstractParameter):

    def __init__(self, value: Union[(bool, str)]):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != bool:
            if type(self.value) != str:
                raise ValueError(f"{self.value} is neither a boolean nor a string")


class AllowCapacityEstimationParameter(AbstractBooleanParameter):
    __doc__ = 'allow_capacity_estimation=[true/false]'
    name = 'allow_capacity_estimation'
    description = 'Whether to allow capacity estimation when cruise-control is unable to obtain all per-broker capacity information'
    argparse_properties = {'args':('--allow-capacity-estimation', ), 
     'kwargs':dict(help=description, action='store_true')}


class ClearMetricsParameter(AbstractBooleanParameter):
    __doc__ = 'clearmetrics=[true/false]'
    name = 'clearmetrics'
    description = 'Clear the existing metric samples'
    argparse_properties = {'args':('--clearmetrics', '--clear-metrics'), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class DryRunParameter(AbstractBooleanParameter):
    __doc__ = 'dryRun=[true/false]'
    name = 'dryrun'
    description = 'Calculate, but do not execute, the cruise-control proposal'
    argparse_properties = {'args':('-n', '--dry-run', '--dryrun'), 
     'kwargs':dict(help=description, action='store_true')}


class ExcludeFollowerDemotionParameter(AbstractBooleanParameter):
    __doc__ = 'exclude_follower_demotion=[true/false]'
    name = 'exclude_follower_demotion'
    description = 'Whether to operate on partitions which only have follower replicas on the specified broker(s)'
    argparse_properties = {'args':('--exclude-follower-demotion', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class ExcludeRecentlyDemotedBrokersParameter(AbstractBooleanParameter):
    __doc__ = 'exclude_recently_demoted_brokers=[true/false]'
    name = 'exclude_recently_demoted_brokers'
    description = "Whether to exclude all recently-demoted brokers from this endpoint's action"
    argparse_properties = {'args':('--exclude-recently-demoted-brokers', '--exclude-recently-demoted', '--exclude-demoted'), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class ExcludeRecentlyRemovedBrokersParameter(AbstractBooleanParameter):
    __doc__ = 'exclude_recently_removed_brokers=[true/false]'
    name = 'exclude_recently_removed_brokers'
    description = "Whether to exclude all recently-removed brokers from this endpoint's action"
    argparse_properties = {'args':('--exclude-recently-removed-brokers', '--exclude-recently-removed', '--exclude-removed'), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class IgnoreProposalCacheParameter(AbstractBooleanParameter):
    __doc__ = 'ignore_proposal_cache=[true/false]'
    name = 'ignore_proposal_cache'
    description = 'Whether to ignore the proposal cache'
    argparse_properties = {'args':('--ignore-proposal-cache', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class JSONParameter(AbstractBooleanParameter):
    __doc__ = 'json=[true/false]'
    name = 'json'
    description = "Whether cruise-control's response should be in JSON format"
    argparse_properties = {'args':('--json', '--json-response'), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class MaxLoadParameter(AbstractBooleanParameter):
    __doc__ = 'max_load=[true/false]'
    name = 'max_load'
    description = 'Whether to return the peak load (max load) or the average load'
    argparse_properties = {'args':('--max-load', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class SkipHardGoalCheckParameter(AbstractBooleanParameter):
    __doc__ = 'skip_hard_goal_check=[true/false]'
    name = 'skip_hard_goal_check'
    description = 'Whether cruise-control should skip all hard goal checks'
    argparse_properties = {'args':('--skip-hard-goal-check', '--skip-hard-goal-checks'), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class SkipRackAwarenessCheckParameter(AbstractBooleanParameter):
    __doc__ = 'skip_rack_awareness_check=[true/false]'
    name = 'skip_rack_awareness_check'
    description = 'Whether to skip the rack-awareness check when performing this action'
    argparse_properties = {'args':('--skip-rack-awareness-check', ), 
     'kwargs':dict(help=description, action='store_true')}


class SkipURPDemotionParameter(AbstractBooleanParameter):
    __doc__ = 'skip_urp_demotion=[true/false]'
    name = 'skip_urp_demotion'
    description = 'Whether to operate on partitions which are currently under-replicated'
    argparse_properties = {'args':('--skip-urp-demotion', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class StopOngoingExecutionParameter(AbstractBooleanParameter):
    __doc__ = 'stop_ongoing_execution=[true/false]'
    name = 'stop_ongoing_execution'
    description = 'Whether to stop the ongoing execution (if any) and start executing the given request'
    argparse_properties = {'args':('--stop-ongoing-execution', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class SuperVerboseParameter(AbstractBooleanParameter):
    __doc__ = 'super_verbose=[true/false]'
    name = 'super_verbose'
    description = "Whether cruise-control's response should return super-verbose information"
    argparse_properties = {'args':('--super-verbose', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class ThrottleRemovedBrokerParameter(AbstractBooleanParameter):
    __doc__ = 'throttle_removed_broker=[true/false]'
    name = 'throttle_removed_broker'
    description = 'Whether to apply the concurrent_partition_movements_per_broker limitation to the removed broker'
    argparse_properties = {'args':('--throttle-removed-broker', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class UseReadyDefaultGoalsParameter(AbstractBooleanParameter):
    __doc__ = 'use_ready_default_goals=[true/false]'
    name = 'use_ready_default_goals'
    description = 'Whether cruise-control should use its ready default goals'
    argparse_properties = {'args':('--use-ready-default-goals', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}


class VerboseParameter(AbstractBooleanParameter):
    __doc__ = 'verbose=[true/false]'
    name = 'verbose'
    description = "Whether cruise-control's response should return verbose information"
    argparse_properties = {'args':('--verbose', ), 
     'kwargs':dict(help=description, choices=set_of_choices, metavar='BOOL', type=str.lower)}