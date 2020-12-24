# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/CCParameter/NonNegativeIntegerParameter.py
# Compiled at: 2019-07-09 13:29:06
# Size of source mod 2**32: 763 bytes
from cruisecontrolclient.client.CCParameter.Parameter import AbstractParameter

class AbstractNonNegativeIntegerParameter(AbstractParameter):

    def __init__(self, value: int):
        AbstractParameter.__init__(self, value)

    def validate_value(self):
        if type(self.value) != int:
            raise ValueError(f"{self.value} is not an integer value")
        elif self.value < 0:
            raise ValueError(f"{self.value} must be a non-negative integer")


class ReviewIDParameter(AbstractNonNegativeIntegerParameter):
    """ReviewIDParameter"""
    name = 'review_id'
    description = 'The id of the approved review'
    argparse_properties = {'args':('--review-id', ), 
     'kwargs':dict(metavar='K', help=description, type=int)}