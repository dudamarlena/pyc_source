# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/credentials/credential_provider.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 6118 bytes
import abc, deprecated.sphinx
from .cred_data import SynapseCredentials
from . import cached_sessions

class SynapseCredentialsProvider(metaclass=abc.ABCMeta):
    __doc__ = '\n    A credential provider is responsible for retrieving synapse authentication information (e.g. username/password or\n    username/api key) from a source(e.g. login args, config file, cached credentials in keyring), and use them to return\n    a ``SynapseCredentials` instance.\n    '

    @abc.abstractmethod
    def _get_auth_info(self, syn, user_login_args):
        """
        Subclasses must implement this to decide how to obtain username, password, and api_key.
        For any of these 3 values, return None if it is not possible to get that value.

        Not all implementations will need to make use of the user_login_args parameter or syn.
        These parameters provide context about the Synapse client's configuration and login() arguments.

        :param ``synapseclient.client.Synapse`` syn:        Synapse client instance
        :param ``cred_data.UserLoginArgs`` user_login_args: subset of arguments passed during syn.login()
        :return: tuple of (username, password, api_key), any of these three values could None if it is not available.
        """
        return (None, None, None)

    def get_synapse_credentials(self, syn, user_login_args):
        """
        Returns `SynapseCredentials` if this provider is able to get valid credentials, returns None otherwise.
        :param ``synapseclient.client.Synapse`` syn:        Synapse client instance
        :param ``cred_data.UserLoginArgs`` user_login_args: subset of arguments passed during syn.login()
        :return: `SynapseCredentials` if valid credentials can be found by this provider, None otherwise
        """
        return (self._create_synapse_credential)(syn, *self._get_auth_info(syn, user_login_args))

    def _create_synapse_credential(self, syn, username, password, api_key):
        if username is not None:
            if password is not None:
                retrieved_session_token = syn._getSessionToken(email=username, password=password)
                return SynapseCredentials(username, syn._getAPIKey(retrieved_session_token))
            if api_key is not None:
                return SynapseCredentials(username, api_key)


class UserArgsCredentialsProvider(SynapseCredentialsProvider):
    __doc__ = '\n    Retrieves auth info from user_login_args\n    '

    def _get_auth_info(self, syn, user_login_args):
        return (user_login_args.username, user_login_args.password, user_login_args.api_key)


@deprecated.sphinx.deprecated(version='1.9.0', action='ignore', reason='This will be removed in 2.0. Please use username and password or apiKey instead.')
class UserArgsSessionTokenCredentialsProvider(SynapseCredentialsProvider):
    __doc__ = '\n    This is a special case where we are not given context as to what the username is. We are only given a session token\n    and must retrieve the username and api key from Synapse\n    '

    def _get_auth_info(self, syn, user_login_args):
        if user_login_args.session_token:
            return (syn.getUserProfile(sessionToken=(user_login_args.session_token))['userName'], None,
             syn._getAPIKey(user_login_args.session_token))
        else:
            return (None, None, None)


class ConfigFileCredentialsProvider(SynapseCredentialsProvider):
    __doc__ = '\n    Retrieves auth info from .synapseConfig file\n    '

    def _get_auth_info(self, syn, user_login_args):
        config_dict = syn._get_config_authentication()
        username = config_dict.get('username')
        if user_login_args.username is None or username == user_login_args.username:
            return (config_dict.get('username'), config_dict.get('password'), config_dict.get('apikey'))
        else:
            return (None, None, None)


class CachedCredentialsProvider(SynapseCredentialsProvider):
    __doc__ = '\n    Retrieves auth info from cached_sessions\n    '

    def _get_auth_info(self, syn, user_login_args):
        if not user_login_args.skip_cache:
            username = user_login_args.username or cached_sessions.get_most_recent_user()
            return (
             username, None, cached_sessions.get_api_key(username))
        else:
            return (None, None, None)


class SynapseCredentialsProviderChain(object):
    __doc__ = '\n    Class that has a list of ``SynapseCredentialsProvider`` from which this class attempts to retrieve\n    ``SynapseCredentials``.\n    '

    def __init__(self, cred_providers):
        """
        :param list[``SynapseCredentialsProvider``] cred_providers: list of credential providers
        """
        self.cred_providers = list(cred_providers)

    def get_credentials(self, syn, user_login_args):
        """
        Iterates its list of ``SynapseCredentialsProvider`` and returns the first non-None ``SynapseCredential``
        returned by a provider. If no provider is able to provide a ``SynapseCredential``, returns None.
        :param ``synapseclient.client.Synapse`` syn:        Synapse client instance
        :param ``cred_data.UserLoginArgs`` user_login_args: subset of arguments passed during syn.login()
        :return: `SynapseCredentials` returned by the first non-None provider in its list, None otherwise
        """
        for provider in self.cred_providers:
            creds = provider.get_synapse_credentials(syn, user_login_args)
            if creds is not None:
                return creds


DEFAULT_CREDENTIAL_PROVIDER_CHAIN = SynapseCredentialsProviderChain([
 UserArgsSessionTokenCredentialsProvider(),
 UserArgsCredentialsProvider(),
 ConfigFileCredentialsProvider(),
 CachedCredentialsProvider()])

def get_default_credential_chain():
    """
    :return: credential chain
    :rtype: ```SynapseCredentialsProviderChain``
    """
    return DEFAULT_CREDENTIAL_PROVIDER_CHAIN