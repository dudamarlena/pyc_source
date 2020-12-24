# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./BiDirPolicy.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 2529 bytes
import omniORB
from omniORB import CORBA
try:
    property
except NameError:

    def property(*args):
        pass


NORMAL = 0
BOTH = 1
BIDIRECTIONAL_POLICY_TYPE = 37

class BidirectionalPolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omg.org/BiDirPolicy/BidirectionalPolicy:1.0'

    def __init__(self, value):
        if value not in (NORMAL, BOTH):
            raise CORBA.PolicyError(CORBA.BAD_POLICY_VALUE)
        self._value = value
        self._policy_type = BIDIRECTIONAL_POLICY_TYPE

    def _get_value(self):
        return self._value

    value = property(_get_value)


def _create_policy(ptype, val):
    if ptype == BIDIRECTIONAL_POLICY_TYPE:
        return BidirectionalPolicy(val)


omniORB.policyMakers.append(_create_policy)

class BidrectionalPolicyValue:
    _NP_RepositoryId = 'IDL:omg.org/BiDirPolicy/BidrectionalPolicyValue:1.0'

    def __init__(self, *args, **kw):
        raise RuntimeError('Cannot construct objects of this type.')


_d_BidrectionalPolicyValue = omniORB.tcInternal.tv_ushort
_ad_BidrectionalPolicyValue = (omniORB.tcInternal.tv_alias, BidrectionalPolicyValue._NP_RepositoryId, 'BidrectionalPolicyValue', omniORB.tcInternal.tv_ushort)
_tc_BidrectionalPolicyValue = omniORB.tcInternal.createTypeCode(_ad_BidrectionalPolicyValue)
omniORB.registerType(BidrectionalPolicyValue._NP_RepositoryId, _ad_BidrectionalPolicyValue, _tc_BidrectionalPolicyValue)