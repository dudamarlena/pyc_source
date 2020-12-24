# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/ExecutionContext.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 6258 bytes
import cruisecontrolclient.client.Endpoint as Endpoint
from typing import Dict, Tuple, Type

class ExecutionContext:
    available_endpoints = (
     Endpoint.AddBrokerEndpoint,
     Endpoint.AdminEndpoint,
     Endpoint.BootstrapEndpoint,
     Endpoint.DemoteBrokerEndpoint,
     Endpoint.FixOfflineReplicasEndpoint,
     Endpoint.KafkaClusterStateEndpoint,
     Endpoint.LoadEndpoint,
     Endpoint.PartitionLoadEndpoint,
     Endpoint.PauseSamplingEndpoint,
     Endpoint.ProposalsEndpoint,
     Endpoint.RebalanceEndpoint,
     Endpoint.RemoveBrokerEndpoint,
     Endpoint.ResumeSamplingEndpoint,
     Endpoint.ReviewBoardEndpoint,
     Endpoint.ReviewEndpoint,
     Endpoint.StateEndpoint,
     Endpoint.StopProposalExecutionEndpoint,
     Endpoint.TrainEndpoint,
     Endpoint.TopicConfigurationEndpoint,
     Endpoint.UserTasksEndpoint)
    available_endpoints: Tuple[Type[Endpoint.AbstractEndpoint]]
    dest_to_Endpoint = {}
    dest_to_Endpoint: Dict[(str, Type[Endpoint.AbstractEndpoint])]
    available_parameter_set = set()
    for endpoint in available_endpoints:
        dest_to_Endpoint[endpoint.name] = endpoint
        if 'aliases' in endpoint.argparse_properties['kwargs']:
            endpoint_aliases = endpoint.argparse_properties['kwargs']['aliases']
            for alias in endpoint_aliases:
                dest_to_Endpoint[alias] = endpoint

        for parameter in endpoint.available_Parameters:
            available_parameter_set.add(parameter)

    flag_to_parameter_name = {}
    flag_to_parameter_name: Dict[(str, str)]
    for parameter in available_parameter_set:
        argparse_parameter_name = None
        for possible_argparse_name in parameter.argparse_properties['args']:
            if not possible_argparse_name.startswith('-'):
                argparse_parameter_name = possible_argparse_name.replace('-', '_')
            elif not possible_argparse_name.startswith('--'):
                continue
            else:
                argparse_parameter_name = possible_argparse_name.lstrip('-').replace('-', '_')
                break

        if argparse_parameter_name and argparse_parameter_name in flag_to_parameter_name:
            raise ValueError(f"Colliding parameter flags: {argparse_parameter_name}")
        else:
            flag_to_parameter_name[argparse_parameter_name] = parameter.name

    def __init__(self):
        self.non_parameter_flags = set()