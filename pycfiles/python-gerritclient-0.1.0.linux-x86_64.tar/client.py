# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/client.py
# Compiled at: 2017-08-20 02:34:52
import json, os, requests, gerritclient
from requests import auth
from gerritclient.common import utils
from gerritclient import error

class APIClient(object):
    """This class handles API requests."""

    def __init__(self, url, auth_type=None, username=None, password=None):
        """Creates APIClient.

        :param url: URL path to the Gerrit server
        :type url: str
        :param auth_type: Authentication method preferred ('basic'|'digest'),
                          if None then anonymous access is assumed
        :type auth_type: str
        :param username: username
        :type username: str
        :param password: password
        :type password: str
        """
        self.root = url
        self._username = username
        self._password = password
        self._session = None
        self._auth = None
        if auth_type:
            if not all((self._username, self._password)):
                raise ValueError('Username and password must be specified.')
            auth_types = {'basic': auth.HTTPBasicAuth, 'digest': auth.HTTPDigestAuth}
            if auth_type not in auth_types:
                raise ValueError(('Unsupported auth_type {}').format(auth_type))
            self._auth = auth_types[auth_type](self._username, self._password)
        if self.is_authed:
            self.api_root = utils.urljoin(self.root, 'a')
        else:
            self.api_root = utils.urljoin(self.root)
        return

    @property
    def is_authed(self):
        """Checks whether credentials were passed."""
        if self._auth:
            return True
        return False

    @staticmethod
    def _make_common_headers():
        """Returns a dict of HTTP headers common for all requests."""
        return {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def _make_session(self):
        """Initializes a HTTP session."""
        session = requests.Session()
        session.auth = self._auth
        session.headers.update(self._make_common_headers())
        return session

    @property
    def session(self):
        """Lazy initialization of a session."""
        if self._session is None:
            self._session = self._make_session()
        return self._session

    def delete_request(self, api, data=None):
        """Make DELETE request to specific API with some data.

        :param api: API endpoint(path)
        :param data: Data send in request, will be serialized to JSON
        """
        url = self.api_root + api
        resp = self.session.delete(url, json=data)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    def put_request(self, api, data=None, json_data=None, **kwargs):
        """Make PUT request to specific API with some data.

        :param api: API endpoint (path)
        :param data: Dictionary, bytes, or file-like object to send in the body
        :param json_data: Data in JSON to send in the body
        :param kwargs: Optional arguments that ``request`` takes
        """
        url = self.api_root + api
        resp = self.session.put(url, json=json_data, data=data, **kwargs)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    def get_request_raw(self, api, params=None):
        """Make a GET request to specific API and return raw response.

        :param api: API endpoint (path)
        :param params: params passed to GET request
        """
        url = self.api_root + api
        return self.session.get(url, params=params)

    def get_request(self, api, params=None):
        """Make GET request to specific API."""
        params = params or {}
        resp = self.get_request_raw(api, params)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    def post_request_raw(self, api, data=None, json_data=None, content_type=None):
        """Make a POST request to specific API and return raw response.

        :param api: API endpoint (path)
        :param data: Dictionary, bytes, or file-like object to send in the body
        :param json_data: Data in JSON to send in the body
        :param content_type: Content-Type value, if not specified (None) than
                             'application/json' is used by default
        """
        url = self.api_root + api
        if content_type is not None:
            self.session.headers.update({'Content-Type': content_type})
        return self.session.post(url, data=data, json=json_data)

    def post_request(self, api, data=None, json_data=None, content_type=None):
        """Make POST request to specific API with some data."""
        resp = self.post_request_raw(api, data, json_data, content_type)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    @staticmethod
    def _raise_for_status_with_info(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise error.HTTPError(error.get_full_error_message(e))

    @staticmethod
    def _decode_content(response):
        if response.status_code == 204:
            return {}
        if 'text/plain' in response.headers.get('Content-Type'):
            return response.text
        return json.loads(response.text.strip(")]}'"))


def get_settings(file_path=None):
    """Gets gerritclient configuration from 'settings.yaml' file.

    If path to configuration 'settings.yaml' file not specified (None), then
    first try to get it from local directory and then from user .config one

    :param str file_path: string that contains path to configuration file
    :raises: error.ConfigNotFoundException if configuration not specified
    """
    config = None
    user_config = os.path.join(os.path.expanduser('~'), '.config', 'gerritclient', 'settings.yaml')
    local_config = os.path.join(os.path.dirname(__file__), 'settings.yaml')
    if file_path is not None:
        config = file_path
    else:
        if os.path.isfile(local_config):
            config = local_config
        elif os.path.isfile(user_config):
            config = user_config
        if config is None:
            raise error.ConfigNotFoundException('Configuration not found.')
        try:
            config_data = utils.read_from_file(config)
        except (OSError, IOError):
            msg = ('Could not read settings from {0}').format(file_path)
            raise error.InvalidFileException(msg)

    return config_data


def connect(url, auth_type=None, username=None, password=None):
    """Creates API connection."""
    return APIClient(url, auth_type=auth_type, username=username, password=password)


def get_client(resource, version='v1', connection=None):
    """Gets an API client for a resource

    python-gerritclient provides access to Gerrit Code Review's API
    through a set of per-resource facades. In order to get a proper facade
    it's necessary to specify the name and the version of the API.

    :param resource: Name of the resource to get a facade for
    :type resource:  str
    :param version:  Version of the API
    :type version:   str,
                     Available: v1. Default: v1.
    :param connection: API connection
    :type connection: gerritclient.client.APIClient
    :return:         Facade to the specified resource that wraps
                     calls to the specified version of the API.
    """
    version_map = {'v1': {'account': gerritclient.v1.account, 
              'change': gerritclient.v1.change, 
              'group': gerritclient.v1.group, 
              'plugin': gerritclient.v1.plugin, 
              'project': gerritclient.v1.project, 
              'server': gerritclient.v1.server}}
    try:
        return version_map[version][resource].get_client(connection)
    except KeyError:
        msg = 'Cannot load API client for "{r}" in the API version "{v}".'
        raise ValueError(msg.format(r=resource, v=version))