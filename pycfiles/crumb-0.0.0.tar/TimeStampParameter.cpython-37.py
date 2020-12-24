# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/TimeStampParameter.py
# Compiled at: 2019-06-18 20:07:56
# Size of source mod 2**32: 1914 bytes
from typing import Union
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractTimestampParameter(AbstractParameter):
    """AbstractTimestampParameter"""

    def __init__(self, value: Union[(str, int)]):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        """
        Although there are many possible validations against a timestamp, none
        are satisfactorily one-size-fits-all.

        Accordingly, only type checking will be performed against the given value.
        :return:
        """
        if type(self.value) == str:
            try:
                int(self.value)
            except ValueError as e:
                try:
                    raise ValueError(f"{self.value} cannot be cast to integer timestamp", e)
                finally:
                    e = None
                    del e

        elif type(self.value) != int:
            raise ValueError(f"{self.value} must be either a string or an integer")


class EndParameter(AbstractTimestampParameter):
    """EndParameter"""
    name = 'end'
    description = 'The timestamp in milliseconds since the Epoch to use as the end'
    argparse_properties = {'args':('--end-timestamp', ), 
     'kwargs':dict(help=description, metavar='END_TIMESTAMP')}


class StartParameter(AbstractTimestampParameter):
    """StartParameter"""
    name = 'start'
    description = 'The timestamp in milliseconds since the Epoch to use as the start'
    argparse_properties = {'args':('--start-timestamp', ), 
     'kwargs':dict(help=description, metavar='START_TIMESTAMP')}


class TimeParameter(AbstractTimestampParameter):
    """TimeParameter"""
    name = 'time'
    description = 'The timestamp in milliseconds since the Epoch to use'
    argparse_properties = {'args':('--timestamp', ), 
     'kwargs':dict(help=description, metavar='TIMESTAMP')}