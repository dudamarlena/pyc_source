# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/exceptions.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 961 bytes
"""
"""
from builtins import str

class BadSearchSpace(Exception):
    __doc__ = 'Something is wrong in the description of the search space'


class DuplicateLabel(BadSearchSpace):
    __doc__ = 'A search space included a duplicate label '


class InvalidTrial(ValueError):
    __doc__ = 'Non trial-like object used as Trial'

    def __init__(self, msg, obj):
        ValueError.__init__(self, msg + ' ' + str(obj))
        self.obj = obj


class InvalidResultStatus(ValueError):
    __doc__ = 'Status of fmin evaluation was not in base.STATUS_STRINGS'

    def __init__(self, result):
        ValueError.__init__(self)
        self.result = result


class InvalidLoss(ValueError):
    __doc__ = 'fmin evaluation returned invalid loss value'

    def __init__(self, result):
        ValueError.__init__(self)
        self.result = result


class AllTrialsFailed(Exception):
    __doc__ = 'All optimization steps have finished with status base.STATUS_FAIL'