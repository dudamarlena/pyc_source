# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/RegularExpressionParameter.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 1815 bytes
import re
from typing import Union, Pattern
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractRegularExpressionParameter(AbstractParameter):

    def __init__(self, value: Union[(str, Pattern)]):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if isinstance(self.value, Pattern):
            self.value = self.value.pattern
        elif type(self.value) == str:
            try:
                re.compile(self.value)
            except re.error as e:
                try:
                    raise ValueError(f"{self.value} is not a valid regular expression", e)
                finally:
                    e = None
                    del e

        else:
            raise ValueError(f"{self.value} must be either a string or a re.Pattern")


class ExcludedTopicsParameter(AbstractRegularExpressionParameter):
    """ExcludedTopicsParameter"""
    name = 'excluded_topics'
    description = "A regular expression matching which topics to exclude from this endpoint's action"
    argparse_properties = {'args':('--excluded-topics', '--exclude-topics', '--exclude-topic'), 
     'kwargs':dict(help=description, metavar='REGEX')}


class TopicParameter(AbstractRegularExpressionParameter):
    """TopicParameter"""
    name = 'topic'
    description = 'A regular expression matching the desired topics'
    argparse_properties = {'args':('--topic', ), 
     'kwargs':dict(help=description, metavar='REGEX')}