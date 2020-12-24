# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/case.py
# Compiled at: 2019-02-06 12:21:52
import urlparse, uuid, requests, api_account.run, api_account.views, api_compute.run, api_compute.views, api_metadata.views, httmock
from ocs.api.app import Application
from ocs.api.unittest import FlaskAPITestCase
from ocs.conf import Configuration
from ocs.object_store import cp_backend, world_backend
from ocs.object_store.cp_backend.unittest import ComputeDatabaseTestCase
from ocs.object_store.world_backend.unittest import sources as world_sources
from ocs.object_store.world_backend.unittest import WorldDatabaseTestCase
from scaleway.apis import AccountAPI, ComputeAPI

class APIMixin(object):

    def __init__(self, app):
        app.testing = True
        self.client = app.flask_app.test_client()

    def proxy_requests(self, api_url, client, url, request):
        """ Proxies `request` to `client` if `url` is a part of `api_url`.
        """
        request_url = urlparse.urlunsplit(url)
        if not request_url.startswith(api_url):
            return
        else:
            if request.method == 'GET':
                response = self.client.get(request.path_url, headers=dict(request.headers))
                return httmock.response(response.status_code, response.data, headers=dict(response.headers))
            if request.method in ('DELETE', 'PATCH', 'PUT'):
                response = getattr(self.client, request.method.lower())(request.path_url, data=request.body, headers=dict(request.headers))
                return httmock.response(response.status_code, response.data, headers=dict(response.headers))
            raise NotImplementedError('HTTP verb %s not implemented in proxy' % request.method)
            return

    def create_token(self, secret, service, name, resource):
        """ Creates a token and associates permissions to it.
        """
        user = world_sources.UserFactory()
        service = world_sources.ServiceFactory(name=service)
        permission = world_sources.PermissionFactory(service=service, name=name, resource=resource)
        world_sources.UsersPermissionsFactory(user=user, permission=permission)
        token = world_sources.TokenFactory(secret=secret, user=user, use_user_roles=True)
        world_backend.ConfiguredEngine.scoped_session().commit()
        return token


class FakeComputeAPI(APIMixin):
    PRIVILEGED_TOKEN = str(uuid.uuid4())

    def __init__(self):
        app = Application(api_compute.run.APPLICATION_INFO)
        app.register_views(api_compute.views)
        app.setup_dbsession(world_backend.ConfiguredEngine.scoped_session)
        app.setup_dbsession(cp_backend.ConfiguredEngine.scoped_session)
        self.load_data()
        super(FakeComputeAPI, self).__init__(app)
        Configuration.load_from_dict({'api-compute': {'api-account': {'token': FakeAccountAPI.PRIVILEGED_TOKEN}, 
                           'api-task': {'token': 'token-api-task-TBD', 
                                        'url': 'http://url-api-task.tbd/'}}}, api_compute.views.CONFIGURATION_NAME)

    def load_data(self):
        """ Instanciates models needed to make the API working.
        """
        self.create_token(self.PRIVILEGED_TOKEN, 'compute', '*', '*')

    def proxy_requests(self, url, request):
        return super(FakeComputeAPI, self).proxy_requests(ComputeAPI().get_api_url(), self.client, url, request)


class FakeAccountAPI(APIMixin):
    PRIVILEGED_TOKEN = str(uuid.uuid4())

    def __init__(self):
        app = Application(api_account.run.APPLICATION_INFO)
        app.register_views(api_account.views)
        app.setup_dbsession(world_backend.ConfiguredEngine.scoped_session)
        self.load_data()
        super(FakeAccountAPI, self).__init__(app)

    def load_data(self):
        self.create_token(self.PRIVILEGED_TOKEN, 'account', '*', '*')

    def proxy_requests(self, url, request):
        return super(FakeAccountAPI, self).proxy_requests(AccountAPI().get_api_url(), self.client, url, request)


class APITestCase(FlaskAPITestCase, WorldDatabaseTestCase, ComputeDatabaseTestCase):
    CLIENT_IP_ADDRESS = '10.0.0.100'

    def setUp(self):
        super(APITestCase, self).setUp()
        self.fake_compute_api = FakeComputeAPI()
        self.fake_account_api = FakeAccountAPI()
        self.app.register_views(api_metadata.views)
        Configuration.load_from_dict({'api-metadata': {'api-compute': {'token': FakeComputeAPI.PRIVILEGED_TOKEN}, 
                            'api-account': {'token': FakeAccountAPI.PRIVILEGED_TOKEN}}}, api_metadata.views.CONFIGURATION_NAME)
        Configuration.load_from_dict({}, 'ocs')

    def get_environ(self, environ):
        environ = super(APITestCase, self).get_environ(environ)
        environ['REMOTE_ADDR'] = self.CLIENT_IP_ADDRESS
        return environ

    def default_requests_send(self, mock, request):
        """ Escapes from the HTTMock context to really make the HTTP request.
        """
        patched_send = requests.Session.send
        requests.Session.send = mock._real_session_send
        try:
            try:
                session = requests.Session()
                res = session.send(request)
            except:
                raise

        finally:
            requests.Session.send = patched_send

        return res

    def run(self, *args, **kwargs):
        """ Forwards HTTP requests to FakeComputeAPI, or to FakeAccountAPI, or
        fallback to a real request.
        """
        with httmock.HTTMock(lambda url, request: self.fake_compute_api.proxy_requests(url, request) or self.fake_account_api.proxy_requests(url, request) or self.default_requests_send(mock, request)) as (mock):
            return super(APITestCase, self).run(*args, **kwargs)