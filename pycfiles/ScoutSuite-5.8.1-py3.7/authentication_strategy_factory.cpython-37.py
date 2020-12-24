# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/base/authentication_strategy_factory.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 839 bytes
_strategies = {'aws':'AWSAuthenticationStrategy',  'gcp':'GCPAuthenticationStrategy', 
 'azure':'AzureAuthenticationStrategy', 
 'aliyun':'AliyunAuthenticationStrategy', 
 'oci':'OracleAuthenticationStrategy'}

def import_authentication_strategy(provider):
    strategy_class = _strategies[provider]
    module = __import__(('ScoutSuite.providers.{}.authentication_strategy'.format(provider)), fromlist=[strategy_class])
    authentication_strategy = getattr(module, strategy_class)
    return authentication_strategy


def get_authentication_strategy(provider: str):
    """
        Returns an authentication strategy implementation for a provider.
        :param provider: The authentication strategy 
    """
    authentication_strategy = import_authentication_strategy(provider)
    return authentication_strategy()