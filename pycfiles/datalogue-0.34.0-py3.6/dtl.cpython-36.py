# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/dtl.py
# Compiled at: 2020-04-24 18:45:43
# Size of source mod 2**32: 6196 bytes
from datalogue.clients.http import _HttpClient, Union, Optional, HttpMethod
from datalogue.clients.jobs import _JobsClient
from datalogue.clients.datastore_collections import _DatastoreCollectionClient
from datalogue.clients.credentials import _CredentialsClient
from datalogue.clients.datastore import _DatastoreClient
from datalogue.clients.organization import _OrganizationClient
from datalogue.clients.group import _GroupClient
from datalogue.clients.tag import _TagClient
from datalogue.clients.user import _UserClient
from datalogue.clients.ontology import _OntologyClient
from datalogue.clients.ml import _MLClient
from datalogue.clients.classifier import _ClassifierClient
from datalogue.clients.regex import _RegexClient
from datalogue.clients.pipeline import _PipelineClient
from datalogue.errors import DtlError
from urllib.parse import urlparse
import os
from datalogue.models.organization import User
from datalogue.models.version import Version

def _get_ssl_verify_env() -> bool:
    verify_certificate = os.environ.get('DTL_SSL_VERIFY_CERT')
    return verify_certificate is None or verify_certificate.lower() != 'false'


class DtlCredentials:
    __doc__ = '\n    Information to be able to connect to the platform\n\n    if verify_certificate is set, this variable will be used\n    otherwise we look at the environment variable `DTL_SSL_VERIFY_CERT`\n    if none is set then we use True as a default\n\n    :param username: username to be used to login on the platform\n    :param password: password to be used to login on the platform\n    :param uri: root url where the system lives ie: https://test.datalogue.io/api\n    :param verify_certificate: (Optional) verify the certificate when connecting to remote, no value means true.\n    '

    def __init__(self, username: str, password: str, uri: str, verify_certificate: Optional[bool]=None):
        self.username = username.strip()
        self.password = password.strip()
        if verify_certificate is None:
            verify_certificate = _get_ssl_verify_env()
        self.verify_certificate = verify_certificate
        uri = uri.strip()
        if self.validate_url(uri) is not True:
            raise DtlError('The URL you provided is invalid')
        if not uri.endswith('/api'):
            raise DtlError("The URL you provided doesn't end with '/api' it is most likely invalid")
        self.uri = uri

    def validate_url(self, uri: str) -> bool:
        parsed_url = urlparse(uri)
        return all([parsed_url.scheme, parsed_url.netloc])

    def __repr__(self):
        res = f"{self.__class__.__name__}(username: {self.username!r}, password: ****, uri: {self.uri!r})"
        if self.verify_certificate is None:
            return res
        else:
            return res[:-1] + f", verify_certificate: {self.verify_certificate!r})"


class Dtl:
    __doc__ = '\n    Root class to be built to interact with all the services\n\n    :param credentials: contains the information to connect\n    '

    def __init__(self, credentials: DtlCredentials):
        self.uri = credentials.uri
        self.username = credentials.username
        self.http_client = _HttpClient(credentials.uri, credentials.verify_certificate)
        login_res = self.http_client.login(credentials.username, credentials.password)
        if isinstance(login_res, DtlError):
            raise login_res
        self.group = _GroupClient(self.http_client)
        self.user = _UserClient(self.http_client)
        self.organization = _OrganizationClient(self.http_client)
        self.jobs = _JobsClient(self.http_client)
        self.datastore_collection = _DatastoreCollectionClient(self.http_client)
        self.datastore = _DatastoreClient(self.http_client)
        self.credentials = _CredentialsClient(self.http_client)
        self.ontology = _OntologyClient(self.http_client)
        self.ml = _MLClient(self.http_client)
        self.classifier = _ClassifierClient(self.http_client, self.ontology)
        self.regex = _RegexClient(self.http_client)
        self.tag = _TagClient(self.http_client)
        self.pipeline = _PipelineClient(self.http_client)

    def __repr__(self):
        return f"Logged in {self.uri!r} with {self.username!r} account."

    @staticmethod
    def signup(uri='', first_name='', last_name='', email='', password='', accept_terms=True, verify_certificate: Optional[bool]=None) -> Union[(DtlError, User)]:
        """
        Perform signup of user
        :param uri: The target URI where the user data will be associated in
        :param accept_terms: Whether the user accept the following terms : https://www.datalogue.io/pages/terms-of-service
        :return: User object if successful, else return DtlError
        """
        if verify_certificate is None:
            verify_certificate = _get_ssl_verify_env()
        http_client = _HttpClient(uri, verify_certificate=verify_certificate)
        http_client.get_csrf()
        registered_user = http_client.signup(first_name, last_name, email, password, accept_terms)
        return registered_user

    def version(self) -> Union[(DtlError, Version)]:
        """
        Get version number of SDK, platform, and the platform's services'
        :return: Version object containing version number of SDK, platform, and the platform's services'
        """
        res = self.http_client.make_authed_request('/version', HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        else:
            return Version.from_payload(res)