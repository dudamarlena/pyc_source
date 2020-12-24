# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./ZIOP.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 3064 bytes
import omniORB.ziop_idl, _omniZIOP
from omniORB import CORBA
import omniORB
omniORB.updateModule('omniORB.ZIOP')

class CompressionEnablingPolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omg.org/ZIOP/CompressionEnablingPolicy:1.0'

    def __init__(self, value):
        self._value = value
        self._policy_type = COMPRESSION_ENABLING_POLICY_ID

    def _get_compression_enabled(self):
        return self._value

    compression_enabled = property(_get_compression_enabled)


class CompressionIdLevelListPolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omg.org/ZIOP/CompressionIdLevelListPolicy:1.0'

    def __init__(self, value):
        self._value = value
        self._policy_type = COMPRESSOR_ID_LEVEL_LIST_POLICY_ID

    def _get_compressor_ids(self):
        return self._value

    compressor_ids = property(_get_compressor_ids)


class CompressionLowValuePolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omg.org/ZIOP/CompressionLowValuePolicy:1.0'

    def __init__(self, value):
        self._value = value
        self._policy_type = COMPRESSION_LOW_VALUE_POLICY_ID

    def _get_low_value(self):
        return self._value

    low_value = property(_get_low_value)


class CompressionMinRatioPolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omg.org/ZIOP/CompressionMinRatioPolicy:1.0'

    def __init__(self, value):
        self._value = value
        self._policy_type = COMPRESSION_MIN_RATIO_POLICY_ID

    def _get_ratio(self):
        return self._value

    ratio = property(_get_ratio)


def _create_policy(ptype, val):
    if ptype == COMPRESSION_ENABLING_POLICY_ID:
        return CompressionEnablingPolicy(val)
    else:
        if ptype == COMPRESSOR_ID_LEVEL_LIST_POLICY_ID:
            return CompressionIdLevelListPolicy(val)
        if ptype == COMPRESSION_LOW_VALUE_POLICY_ID:
            return CompressionLowValuePolicy(val)
        if ptype == COMPRESSION_MIN_RATIO_POLICY_ID:
            return CompressionMinRatioPolicy(val)


omniORB.policyMakers.append(_create_policy)