# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/uniconnect/auth.py
# Compiled at: 2019-08-27 00:58:10
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc, os
from six import with_metaclass
from typing import Any, Optional, Text

class Authentication(with_metaclass(abc.ABCMeta)):

    @abc.abstractmethod
    def set_http_session(self, http_session):
        pass

    @abc.abstractmethod
    def set_client_session(self, client_session):
        pass

    @abc.abstractmethod
    def setup(self):
        pass

    def get_exceptions(self):
        return tuple()

    def handle_err(self, error):
        pass


class KerberosAuthentication(Authentication):

    def __init__(self, config=None, service_name=None, mutual_authentication=False, force_preemptive=False, hostname_override=None, sanitize_mutual_error_response=True, principal=None, delegate=False, ca_bundle=None):
        self._config = config
        self._service_name = service_name
        self._mutual_authentication = mutual_authentication
        self._force_preemptive = force_preemptive
        self._hostname_override = hostname_override
        self._sanitize_mutual_error_response = sanitize_mutual_error_response
        self._principal = principal
        self._delegate = delegate
        self._ca_bundle = ca_bundle

    def set_client_session(self, client_session):
        pass

    def set_http_session(self, http_session):
        try:
            import requests_kerberos
        except ImportError:
            raise RuntimeError('unable to import requests_kerberos')

        if self._config:
            os.environ['KRB5_CONFIG'] = self._config
        http_session.trust_env = False
        http_session.auth = requests_kerberos.HTTPKerberosAuth(mutual_authentication=self._mutual_authentication, force_preemptive=self._force_preemptive, hostname_override=self._hostname_override, sanitize_mutual_error_response=self._sanitize_mutual_error_response, principal=self._principal, delegate=self._delegate, service=self._service_name)
        if self._ca_bundle:
            http_session.verify = self._ca_bundle
        return http_session

    def setup(self, uniconnect_client):
        self.set_client_session(uniconnect_client.client_session)
        self.set_http_session(uniconnect_client.http_session)

    def get_exceptions(self):
        try:
            from requests_kerberos.exceptions import KerberosExchangeError
            return (
             KerberosExchangeError,)
        except ImportError:
            raise RuntimeError('unable to import requests_kerberos')

    def handle_error(self, handle_error):
        pass


class BasicAuthentication(Authentication):

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def set_client_session(self, client_session):
        pass

    def set_http_session(self, http_session):
        try:
            import requests.auth
        except ImportError:
            raise RuntimeError('unable to import requests.auth')

        http_session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)
        return http_session

    def setup(self, uniconnect_client):
        self.set_client_session(uniconnect_client.client_session)
        self.set_http_session(uniconnect_client.http_session)

    def get_exceptions(self):
        return ()

    def handle_error(self, handle_error):
        pass