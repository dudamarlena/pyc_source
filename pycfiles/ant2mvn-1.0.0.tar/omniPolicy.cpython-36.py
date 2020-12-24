# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./omniPolicy.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 1839 bytes
import omniORB
from omniORB import CORBA
ENDPOINT_PUBLISH_POLICY_TYPE = 1096045570

class EndPointPublishPolicy(CORBA.Policy):
    _NP_RepositoryId = 'IDL:omniorb.net/omniPolicy/EndPointPublishPolicy:1.0'

    def __init__(self, value):
        if not isinstance(value, list):
            raise CORBA.PolicyError(CORBA.BAD_POLICY_VALUE)
        for item in value:
            if not isinstance(item, str):
                raise CORBA.PolicyError(CORBA.BAD_POLICY_VALUE)

        self._value = value
        self._policy_type = ENDPOINT_PUBLISH_POLICY_TYPE

    def _get_value(self):
        return self._value

    value = property(_get_value)


def _create_policy(ptype, val):
    if ptype == 1096045570:
        return EndPointPublishPolicy(val)


omniORB.policyMakers.append(_create_policy)