# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/TimeStampParameter.py
# Compiled at: 2019-06-18 20:07:56
# Size of source mod 2**32: 1914 bytes
from typing import Union
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractTimestampParameter(AbstractParameter):
    __doc__ = '\n    For parameters that accept timestamps in milliseconds since the Epoch.\n    '

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

        else:
            if type(self.value) != int:
                raise ValueError(f"{self.value} must be either a string or an integer")


class EndParameter(AbstractTimestampParameter):
    __doc__ = 'start=[END_TIMESTAMP]'
    name = 'end'
    description = 'The timestamp in milliseconds since the Epoch to use as the end'
    argparse_properties = {'args':('--end-timestamp', ), 
     'kwargs':dict(help=description, metavar='END_TIMESTAMP')}


class StartParameter(AbstractTimestampParameter):
    __doc__ = 'start=[START_TIMESTAMP]'
    name = 'start'
    description = 'The timestamp in milliseconds since the Epoch to use as the start'
    argparse_properties = {'args':('--start-timestamp', ), 
     'kwargs':dict(help=description, metavar='START_TIMESTAMP')}


class TimeParameter(AbstractTimestampParameter):
    __doc__ = 'time=[TIMESTAMP]'
    name = 'time'
    description = 'The timestamp in milliseconds since the Epoch to use'
    argparse_properties = {'args':('--timestamp', ), 
     'kwargs':dict(help=description, metavar='TIMESTAMP')}