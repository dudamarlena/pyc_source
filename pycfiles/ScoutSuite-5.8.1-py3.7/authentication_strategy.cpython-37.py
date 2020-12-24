# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/authentication_strategy.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1128 bytes
import logging
from oci.config import from_file
from oci.identity import IdentityClient
from ScoutSuite.providers.base.authentication_strategy import AuthenticationStrategy, AuthenticationException

class OracleCredentials:

    def __init__(self, config):
        self.config = config

    def get_scope(self):
        if 'compartment-id' in self.config:
            return self.config['compartment-id']
        return self.config['tenancy']


class OracleAuthenticationStrategy(AuthenticationStrategy):
    __doc__ = '\n    Implements authentication for the AWS provider\n    '

    def authenticate(self, profile=None, **kwargs):
        try:
            logging.getLogger('oci').setLevel(logging.ERROR)
            config = from_file(profile_name=profile)
            identity = IdentityClient(config)
            identity.get_user(config['user']).data
            return OracleCredentials(config)
        except Exception as e:
            try:
                raise AuthenticationException(e)
            finally:
                e = None
                del e