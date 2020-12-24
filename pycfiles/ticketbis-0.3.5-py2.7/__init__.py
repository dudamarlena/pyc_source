# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/ticketbis/__init__.py
# Compiled at: 2019-05-02 11:55:14
import logging
log = logging.getLogger(__name__)
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import inspect, math, time, sys
from copy import copy
try:
    import requests
    from six.moves.urllib import parse
    from six.moves import xrange
    import six
    requests.models.json = json
except ImportError:
    pass

NETWORK_DEBUG = False
if NETWORK_DEBUG:
    import httplib
    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
API_VERSION = 1
__version__ = '0.3.5'
__author__ = 'Jose Gargallo'
API_ENDPOINT = 'https://api.ticketbis.com/'
AUTH_ENDPOINT = 'oauth/authorize/'
TOKEN_ENDPOINT = 'oauth/token/'
NUM_REQUEST_RETRIES = 1
MAX_MULTI_REQUESTS = 5
VERIFY_SSL = True
AUTH_CODE_GRANT_TYPE = 'authorization_code'
CLIENT_CRED_GRANT_TYPE = 'client_credentials'

class TicketbisException(RuntimeError):
    pass


class InvalidAuth(TicketbisException):
    pass


class ParamError(TicketbisException):
    pass


class EndpointError(TicketbisException):
    pass


class NotAuthorized(TicketbisException):
    pass


class RateLimitExceeded(TicketbisException):
    pass


class Deprecated(TicketbisException):
    pass


class ServerError(TicketbisException):
    pass


class FailedGeocode(TicketbisException):
    pass


class PreconditionFailed(TicketbisException):
    pass


class Other(TicketbisException):
    pass


error_types = {'invalid_auth': InvalidAuth, 
   'param_error': ParamError, 
   'endpoint_error': EndpointError, 
   'not_authorized': NotAuthorized, 
   'rate_limit_exceeded': RateLimitExceeded, 
   'deprecated': Deprecated, 
   'server_error': ServerError, 
   'failed_geocode': FailedGeocode, 
   'other': Other}

class Ticketbis(object):
    """Ticketbis API wrapper"""

    def __init__(self, client_id=None, client_secret=None, access_token=None, redirect_uri=None, version=None, site=None, lang='en-gb', grant_type=AUTH_CODE_GRANT_TYPE, api_endpoint=API_ENDPOINT, auth=None):
        """Sets up the api object"""
        self.oauth = self.OAuth(api_endpoint, client_id, client_secret, redirect_uri, grant_type)
        self.base_requester = self.Requester(api_endpoint, client_id, client_secret, access_token, version, site, lang, auth)
        self._attach_endpoints()
        if not site and access_token:
            self.sites(params={'max': 1})

    def _attach_endpoints(self):
        """Dynamically attach endpoint callables to this client"""
        for name, endpoint in inspect.getmembers(self):
            if inspect.isclass(endpoint) and issubclass(endpoint, self._Endpoint) and endpoint is not self._Endpoint:
                endpoint_instance = endpoint(self.base_requester)
                setattr(self, endpoint_instance.endpoint, endpoint_instance)

    def set_access_token(self, access_token):
        """Update the access token to use"""
        self.base_requester.set_token(access_token)

    @property
    def rate_limit(self):
        """Returns the maximum rate limit for the last API call"""
        return self.base_requester.rate_limit

    @property
    def total_count(self):
        """Returns the total count of items when listing"""
        return self.base_requester.total_count

    @property
    def page_offset(self):
        """Returns current offset when listing"""
        return self.base_requester.page_offset

    @property
    def page_max(self):
        """Returns the max items per page when listing"""
        return self.base_requester.page_max

    @property
    def site(self):
        """Returns site name"""
        return self.base_requester.site

    @property
    def rate_remaining(self):
        """
        Returns the remaining rate limit for the last API call
        i.e. X-RateLimit-Remaining
        """
        return self.base_requester.rate_remaining

    class OAuth(object):
        """Handles OAuth authentication procedures and helps retrieve tokens"""

        def __init__(self, api_endpoint, client_id, client_secret, redirect_uri, grant_type):
            self.api_endpoint = api_endpoint
            self.client_id = client_id
            self.client_secret = client_secret
            self.redirect_uri = redirect_uri
            self.grant_type = grant_type

        def auth_url(self):
            """Gets the url a user needs to access to give up a user token"""
            params = {'client_id': self.client_id, 
               'response_type': 'code', 
               'redirect_uri': self.redirect_uri}
            return ('{API_ENDPOINT}{AUTH_ENDPOINT}?{params}').format(API_ENDPOINT=self.api_endpoint, AUTH_ENDPOINT=AUTH_ENDPOINT, params=parse.urlencode(params))

        def get_token(self, code=None, scope='read write'):
            """Gets the auth token from a user's response"""
            params = {'client_id': self.client_id, 
               'client_secret': self.client_secret, 
               'grant_type': self.grant_type}
            if self.grant_type == AUTH_CODE_GRANT_TYPE:
                params['redirect_uri'] = self.redirect_uri
                if not code:
                    log.error('Code not provided')
                    return None
                params['code'] = six.u(code)
            elif self.grant_type == CLIENT_CRED_GRANT_TYPE:
                params['scope'] = scope
            token_endpoint = ('{0}{1}').format(self.api_endpoint, TOKEN_ENDPOINT)
            res = _post(token_endpoint, data=params)
            return res['data']['access_token']

    class Requester(object):
        """Api requesting object"""

        def __init__(self, api_endpoint, client_id=None, client_secret=None, access_token=None, version=None, site=None, lang=None, auth=None):
            """Sets up the api object"""
            self.client_id = client_id
            self.client_secret = client_secret
            self.set_token(access_token)
            self.version = version or API_VERSION
            self.site = site
            self.lang = lang
            self.multi_requests = list()
            self.rate_limit = None
            self.rate_remaining = None
            self.rate_remaining = None
            self.api_endpoint = api_endpoint
            self.auth = auth
            self.total_count = None
            self.page_offset = None
            self.page_max = None
            api_v = ('application/vnd.ticketbis.v{0}+json').format(self.version)
            self.base_headers = {'Accept': ('{0}, application/json').format(api_v), 
               'Content-Type': 'application/json'}
            return

        def set_token(self, access_token):
            """Set the OAuth token for this requester"""
            self.oauth_token = access_token
            self.userless = not bool(access_token)

        def GET(self, path, params={}, **kwargs):
            """GET request that returns processed data"""
            params = params.copy()
            if kwargs.get('multi') is True:
                return self.add_multi_request(path, params)
            headers = self._create_headers()
            params = self._enrich_params(params)
            url = self._get_url(path)
            result = _get(url, headers=headers, params=params, auth=self.auth)
            self._set_header_properties(result)
            return result['data']

        def GET_PAGINATED(self, path, params={}, **kwargs):
            """GET request that returns data iterating over pagination"""
            params = params.copy()
            headers = self._create_headers()
            params = self._enrich_params(params)
            url = self._get_url(path)
            pending_pages = True
            while pending_pages:
                result = _get(url, headers=headers, params=params, auth=self.auth)
                self._set_header_properties(result)
                pending_pages = self.page_offset + len(result['data']) < self.total_count
                params['offset'] = self.page_offset + self.page_max
                for r in result['data']:
                    yield r

        def _set_header_properties(self, result):
            self.site = result['headers']['X-ticketbis-site']
            self.rate_limit = result['headers'].get('X-RateLimit-Limit', None)
            self.rate_remaining = result['headers'].get('X-RateLimit-Remaining', None)
            if 'X-ticketbis-totalCount' in result['headers']:
                self.total_count = int(result['headers']['X-ticketbis-totalCount'])
                self.page_offset = int(result['headers']['X-ticketbis-pageOffset'])
                self.page_max = int(result['headers']['X-ticketbis-pageMaxSize'])
            else:
                self.total_count = None
                self.page_offset = None
                self.page_max = None
            return

        def add_multi_request(self, path, params={}):
            """Add multi request to list and return number of requests added"""
            url = path
            if params:
                url += ('?{0}').format(parse.quote_plus(parse.urlencode(params)))
            self.multi_requests.append(url)
            return len(self.multi_requests)

        def POST(self, path, data={}, files=None):
            """POST request that returns processed data"""
            if data is not None:
                data = data.copy()
            if files is not None:
                files = files.copy()
            headers = self._create_headers()
            data = self._enrich_params(data)
            url = self._get_url(path)
            result = _post(url, headers=headers, data=json.dumps(data), files=files, auth=self.auth)
            self.rate_limit = result['headers'].get('X-RateLimit-Limit', None)
            self.rate_remaining = result['headers'].get('X-RateLimit-Remaining', None)
            return result['data']

        def PUT(self, path, data={}, files=None):
            """PUT request that returns processed data"""
            if data is not None:
                data = data.copy()
            if files is not None:
                files = files.copy()
            headers = self._create_headers()
            data = self._enrich_params(data)
            url = self._get_url(path)
            result = _put(url, headers=headers, data=json.dumps(data), files=files, auth=self.auth)
            self.rate_limit = result['headers'].get('X-RateLimit-Limit', None)
            self.rate_remaining = result['headers'].get('X-RateLimit-Remaining', None)
            return result['data']

        def _get_url(self, path):
            return ('{API_ENDPOINT}{path}').format(API_ENDPOINT=self.api_endpoint, path=path)

        def _enrich_params(self, params):
            """Enrich the params dict"""
            if self.userless:
                params['client_id'] = self.client_id
                params['client_secret'] = self.client_secret
            return params

        def _create_headers(self):
            """Get the headers we need"""
            headers = self.base_headers.copy()
            if not self.userless:
                headers['Authorization'] = ('Bearer {0}').format(self.oauth_token)
            if self.site:
                headers['X-ticketbis-site'] = self.site
            elif self.lang:
                headers['Accept-Language'] = self.lang
            return headers

    class _Endpoint(object):
        """Generic endpoint class"""

        def __init__(self, requester):
            """Stores the request function for retrieving data"""
            self.requester = requester

        def copy(self):
            """Generates a new copy of endpoint"""
            return self.__class__(copy(self.requester))

        def _expanded_path(self, path=None):
            """Gets the expanded path, given this endpoint"""
            return ('{expanded_path}').format(expanded_path=('/').join(p for p in (self.endpoint, path) if p))

        def create(self, params={}):
            return self.POST('', params)

        def update(self, params={}):
            return self.PUT(('{0}').format(params['id']), params)

        def GET(self, path=None, auto_pagination=False, *args, **kwargs):
            """Use the requester to get the data"""
            if not auto_pagination:
                return self.requester.GET(self._expanded_path(path), *args, **kwargs)
            else:
                return self.requester.GET_PAGINATED(self._expanded_path(path), *args, **kwargs)

        def POST(self, path=None, *args, **kwargs):
            """Use the requester to post the data"""
            return self.requester.POST(self._expanded_path(path), *args, **kwargs)

        def PUT(self, path=None, *args, **kwargs):
            """Use the requester to put the data"""
            return self.requester.PUT(self._expanded_path(path), *args, **kwargs)

    class Events(_Endpoint):
        endpoint = 'events'

        def __call__(self, event_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(event_id), auto_pagination, params=params, multi=multi)

        def section_groups(self, event_id, auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}/section_groups').format(event_id), auto_pagination, params=params, multi=multi)

    class Categories(_Endpoint):
        endpoint = 'categories'

        def __call__(self, category_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(category_id), auto_pagination, params=params, multi=multi)

        def events(self, category_id, auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}/events').format(category_id), auto_pagination, params=params, multi=multi)

    class Sites(_Endpoint):
        endpoint = 'sites'

        def __call__(self, site_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(site_id), auto_pagination, params=params, multi=multi)

    class Cities(_Endpoint):
        endpoint = 'cities'

        def __call__(self, site_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(site_id), auto_pagination, params=params, multi=multi)

    class Venues(_Endpoint):
        endpoint = 'venues'

        def __call__(self, venue_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(venue_id), auto_pagination, params=params, multi=multi)

        def schemas(self, venue_id, auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}/schemas').format(venue_id), auto_pagination, params=params, multi=multi)

    class Schemas(_Endpoint):
        endpoint = 'schemas'

        def __call__(self, schema_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(schema_id), auto_pagination, params=params, multi=multi)

    class SectionGroups(_Endpoint):
        endpoint = 'section_groups'

        def __call__(self, schema_id='', auto_pagination=False, params={}, multi=False):
            return self.GET(('{0}').format(schema_id), auto_pagination, params=params, multi=multi)

    class Multi(_Endpoint):
        """Multi request endpoint handler"""
        endpoint = 'multi'

        def __len__(self):
            return len(self.requester.multi_requests)

        def __call__(self):
            """
            Generator to process the current queue of multi's

            note: This generator will yield both data and TicketbisException's
            Code processing this sequence must check the yields for their type.
            The exceptions should be handled by the calling code, or raised.
            """
            while self.requester.multi_requests:
                requests = self.requester.multi_requests[:MAX_MULTI_REQUESTS]
                del self.requester.multi_requests[:MAX_MULTI_REQUESTS]
                params = {'requests': (',').join(requests)}
                responses = self.GET(params=params)['responses']
                for response in responses:
                    try:
                        _raise_error_from_response(response)
                        yield response['response']
                    except TicketbisException as e:
                        yield e

        @property
        def num_required_api_calls(self):
            """Returns the expected number of API calls to process"""
            return int(math.ceil(len(self.requester.multi_requests) / float(MAX_MULTI_REQUESTS)))


def _log_and_raise_exception(msg, data, cls=TicketbisException):
    """Calls log.error() then raises an exception of class cls"""
    data = ('{0}').format(data)
    log.error(('{0}: %s').format(msg), data)
    raise cls(('{0}: {1}').format(msg, data))


def _get(url, headers={}, params=None, auth=None):
    """Tries to GET data from an endpoint using retries"""
    param_string = _ticketbis_urlencode(params)
    for i in xrange(NUM_REQUEST_RETRIES):
        try:
            try:
                response = requests.get(url, headers=headers, params=param_string, verify=VERIFY_SSL, auth=auth)
                return _process_response(response)
            except requests.exceptions.RequestException as e:
                _log_and_raise_exception('Error connecting with ticketbis API', e)

        except TicketbisException as e:
            if e.__class__ in [InvalidAuth, ParamError, EndpointError,
             NotAuthorized, Deprecated]:
                raise
            if i + 1 == NUM_REQUEST_RETRIES:
                raise

        time.sleep(1)


def _post(url, headers={}, data=None, files=None, auth=None):
    """Tries to POST data to an endpoint"""
    try:
        response = requests.post(url, headers=headers, data=data, files=files, verify=VERIFY_SSL, auth=auth)
        return _process_response(response)
    except requests.exceptions.RequestException as e:
        _log_and_raise_exception('Error connecting with ticketbis API', e)


def _put(url, headers={}, data=None, files=None, auth=None):
    """Tries to PUT data to an endpoint"""
    try:
        response = requests.put(url, headers=headers, data=data, files=files, verify=VERIFY_SSL, auth=auth)
        return _process_response(response)
    except requests.exceptions.RequestException as e:
        _log_and_raise_exception('Error connecting with ticketbis API', e)


def _process_response(response):
    """Make the request and handle exception processing"""
    try:
        if response.status_code in (200, 201):
            data = response.json()
            return {'headers': response.headers, 'data': data}
        else:
            if response.status_code == 412:
                _log_and_raise_exception('Precondition failed', response.text, cls=PreconditionFailed)
            data = response.json()
            return _raise_error_from_response(data)

    except ValueError:
        _log_and_raise_exception('Invalid response', response.text)


def _raise_error_from_response(data):
    """Processes the response data"""
    meta = data.get('meta')
    if meta:
        if meta.get('code') in (200, 409):
            return data
        exc = error_types.get(meta.get('errorType'))
        if exc:
            raise exc(meta.get('errorDetail'))
        else:
            _log_and_raise_exception('Unknown error. meta', meta)
    else:
        _log_and_raise_exception('Invalid format, missing meta property. data', data)


def _as_utf8(s):
    try:
        return str(s)
    except UnicodeEncodeError:
        return unicode(s).encode('utf8')


def _ticketbis_urlencode(query, doseq=0, safe_chars='&/,+'):
    if hasattr(query, 'items'):
        query = query.items()
    else:
        try:
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
        except TypeError:
            ty, va, tb = sys.exc_info()
            raise TypeError('not valid non-string sequence').with_traceback(tb)

        l = []
        if not doseq:
            for k, v in query:
                k = parse.quote(_as_utf8(k), safe=safe_chars)
                v = parse.quote(_as_utf8(v), safe=safe_chars)
                l.append(k + '=' + v)

        else:
            for k, v in query:
                k = parse.quote(_as_utf8(k), safe=safe_chars)
                if isinstance(v, six.string_types):
                    v = parse.quote(_as_utf8(v), safe=safe_chars)
                    l.append(k + '=' + v)
                else:
                    try:
                        len(v)
                    except TypeError:
                        v = parse.quote(_as_utf8(v), safe=safe_chars)
                        l.append(k + '=' + v)

                    for elt in v:
                        l.append(k + '=' + parse.quote(_as_utf8(elt)))

    return ('&').join(l)