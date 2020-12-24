# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/Parameter.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 4812 bytes
from abc import ABCMeta, abstractmethod
from typing import ClassVar, Collection, Dict, Tuple, Union

class AbstractParameter(metaclass=ABCMeta):
    __doc__ = '\n    An abstract representation of a cruise-control parameter.\n\n    Parameters are the key=value mappings that follow the endpoint in a URL.\n    '
    name = None
    name: ClassVar[str]
    description = None
    description: ClassVar[str]
    argparse_properties = {'args':(), 
     'kwargs':{}}
    argparse_properties: ClassVar[Dict[(str, Union[(Tuple[str], Dict[(str, str)])])]]

    def __init__(self, value: Union[(bool, int, float, str)]=None):
        self.value = value
        self.validate_value()

    def __hash__(self):
        return hash((self.name, self.value))

    @abstractmethod
    def validate_value(self):
        """
        This method provides further validation on the supplied value.

        If the supplied value is invalid for this parameter, raises ValueError.
        """
        pass


class MinValidPartitionRatioParameter(AbstractParameter):
    __doc__ = 'min_valid_partition_ratio=[min_valid_partition_ratio]'
    name = 'min_valid_partition_ratio'
    description = 'The minimum required ratio of monitored topics [0-1]'
    argparse_properties = {'args':('--min-valid-partition-ratio', ), 
     'kwargs':dict(help=description, metavar='R', type=float)}

    def __init__(self, value: float):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != float:
            if type(self.value) != int:
                raise ValueError(f"{self.value} must be a float or an integer")
        if self.value < 0 or self.value > 1:
            raise ValueError(f"{self.value} must be between 0 and 1, inclusive")


class PartitionParameter(AbstractParameter):
    __doc__ = 'partition=[partition/start_partition-end_partition]'
    name = 'partition'
    description = 'The partition or [start]-[end] partitions to return'
    argparse_properties = {'args':('--partition', '--partitions'), 
     'kwargs':dict(help=description, metavar='PARTITION_OR_RANGE')}

    def __init__(self, value: Union[(int, Tuple[(int, int)], str)]):
        if isinstance(value, Collection):
            value = '-'.join(value)
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) == int:
            pass
        elif type(self.value) == str:
            if len(self.value.split('-')) > 2:
                raise ValueError(f"{self.value} must contain either 1 integer, or 2 '-'-separated integers")
        else:
            raise ValueError(f"{self.value} must either be a string, an integer, or a Collection of two integers")


class ReasonParameter(AbstractParameter):
    __doc__ = '\n    reason=[reason-for-pause]\n    reason=[reason-for-request]\n    reason=[reason-for-review]\n    '
    name = 'reason'
    description = 'The human-readable reason for this action'
    argparse_properties = {'args':('--reason', ), 
     'kwargs':dict(help=description, metavar='REASON', type=str)}

    def validate_value(self):
        """
        The validation strategy here is to avoid a Bobby Tables situation
        by ensuring that the provided reason does not contain any
        RFC-3986 "reserved" characters.

        See https://tools.ietf.org/html/rfc3986#section-2.2
        See also https://xkcd.com/327/
        :return:
        """
        gen_delims = set(':/?#[]@')
        sub_delims = set("!$&'()*+,;=")
        reserved_html_characters = gen_delims | sub_delims
        for character in self.value:
            if character in reserved_html_characters:
                raise ValueError(f'"{character}" is a reserved HTML character and cannot be transmitted correctly to cruise-control as part of the reason= parameter')