# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
        else:
            if self.value < 0:
                raise ValueError(f"{self.value} must be a non-negative integer")


class ReviewIDParameter(AbstractNonNegativeIntegerParameter):
    __doc__ = 'review_id=[id]'
    name = 'review_id'
    description = 'The id of the approved review'
    argparse_properties = {'args':('--review-id', ), 
     'kwargs':dict(metavar='K', help=description, type=int)}