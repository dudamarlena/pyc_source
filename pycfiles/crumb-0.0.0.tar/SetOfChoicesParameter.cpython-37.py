# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/SetOfChoicesParameter.py
# Compiled at: 2020-03-16 12:47:01
# Size of source mod 2**32: 2915 bytes
from typing import Set, Union, Collection
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractSetOfChoicesParameter(AbstractParameter):
    lowercase_set_of_choices = set()
    lowercase_set_of_choices: Set[str]

    def __init__(self, value: Union[(str, Collection[str])]):
        if isinstance(value, Collection):
            if type(value) != str:
                value = ','.join(value)
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != str:
            if type(self.value) != Collection:
                raise ValueError(f"{self.value} must be either a string or a Collection")


class DisableSelfHealingForParameter(AbstractSetOfChoicesParameter):
    """DisableSelfHealingForParameter"""
    lowercase_set_of_choices = {
     'goal_violation', 'metric_anomaly', 'broker_failure'}
    name = 'disable_self_healing_for'
    description = 'The anomaly detectors for which to disable self-healing'
    argparse_properties = {'args':('--disable-self-healing-for', '--disable-self-healing'), 
     'kwargs':dict(help=description, metavar='ANOMALY_DETECTOR', choices=lowercase_set_of_choices, nargs='+', type=str.lower)}


class EnableSelfHealingForParameter(AbstractSetOfChoicesParameter):
    """EnableSelfHealingForParameter"""
    lowercase_set_of_choices = {
     'goal_violation', 'metric_anomaly', 'broker_failure'}
    name = 'enable_self_healing_for'
    description = 'The anomaly detectors for which to enable self-healing'
    argparse_properties = {'args':('--enable-self-healing-for', '--enable-self-healing'), 
     'kwargs':dict(help=description, metavar='ANOMALY_DETECTOR', choices=lowercase_set_of_choices, nargs='+', type=str.lower)}


class ResourceParameter(AbstractSetOfChoicesParameter):
    """ResourceParameter"""
    lowercase_set_of_choices = {
     'cpu', 'nw_in', 'nw_out', 'disk'}
    name = 'resource'
    description = 'The host and broker-level resource by which to sort the cruise-control response'
    argparse_properties = {'args':('--resource', ), 
     'kwargs':dict(help=description, metavar='RESOURCE', choices=lowercase_set_of_choices, type=str.lower)}


class SubstatesParameter(AbstractSetOfChoicesParameter):
    """SubstatesParameter"""
    lowercase_set_of_choices = {
     'executor', 'analyzer', 'monitor', 'anomaly_detector'}
    name = 'substates'
    description = 'The substates for which to retrieve state from cruise-control'
    argparse_properties = {'args':('--substate', '--substates'), 
     'kwargs':dict(help=description, metavar='SUBSTATE', choices=lowercase_set_of_choices, nargs='+', type=str.lower)}