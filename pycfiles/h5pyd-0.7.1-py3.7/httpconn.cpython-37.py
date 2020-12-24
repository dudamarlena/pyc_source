# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/httpconn.py
# Compiled at: 2019-10-25 15:25:54
# Size of source mod 2**32: 16885 bytes
from __future__ import absolute_import
import os, base64, requests
from requests import ConnectionError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json, logging
MAX_CACHE_ITEM_SIZE = 10000

class CacheResponse(object):
    __doc__ = " Wrap a json response in a Requests.Response looking class.\n        Note: we don't want to keep a proper requests obj in the cache since it\n        would contain refernces to other objects\n    "

    def __init__(self, rsp):
        self._text = rsp.text
        self._status_code = rsp.status_code
        self._headers = rsp.headers

    @property
    def text(self):
        return self._text

    @property
    def status_code(self):
        return self._status_code

    @property
    def headers(self):
        return self._headers


class HttpConn:
    __doc__ = '\n    Some utility methods based on equivalents in base class.\n    TBD: Should refactor these to a common base class\n    '

    def __init__(self, domain_name, endpoint=None, username=None, password=None, bucket=None, api_key=None, mode='a', use_session=True, use_cache=True, logger=None, retries=3, **kwds):
        self._domain = domain_name
        self._mode = mode
        self._domain_json = None
        self._use_session = use_session
        self._retries = retries
        if use_cache:
            self._cache = {}
            self._objdb = {}
        else:
            self._cache = None
            self._objdb = None
        self._logger = logger
        if logger is None:
            self.log = logging
        else:
            self.log = logging.getLogger(logger)
        self.log.debug('HttpCon.init(omaion: {} use_session: {} use_cache: {} retries: {})'.format(domain_name, use_session, use_cache, retries))
        if endpoint is None:
            if 'HS_ENDPOINT' in os.environ:
                endpoint = os.environ['HS_ENDPOINT']
            else:
                if 'H5SERV_ENDPOINT' in os.environ:
                    endpoint = os.environ['H5SERV_ENDPOINT']
                else:
                    endpoint = 'http://127.0.0.1:5000'
        else:
            self._endpoint = endpoint
            if username is None:
                if 'HS_USERNAME' in os.environ:
                    username = os.environ['HS_USERNAME']
                else:
                    if 'H5SERV_USERNAME' in os.environ:
                        username = os.environ['H5SERV_USERNAME']
        if isinstance(username, str):
            if not username or username.upper() == 'NONE':
                username = None
        self._username = username
        if password is None:
            if 'HS_PASSWORD' in os.environ:
                password = os.environ['HS_PASSWORD']
            else:
                if 'H5SERV_PASSWORD' in os.environ:
                    password = os.environ['H5SERV_PASSWORD']
        if isinstance(password, str):
            if not password or password.upper() == 'NONE':
                password = None
        self._password = password
        if bucket is None:
            if 'HS_BUCKET' in os.environ:
                bucket = os.environ['HS_BUCKET']
            if isinstance(bucket, str):
                if not bucket or bucket.upper() == 'NONE':
                    bucket = None
        self._bucket = bucket
        if api_key is None:
            if 'HS_API_KEY' in os.environ:
                api_key = os.environ['HS_API_KEY']
        if isinstance(api_key, str):
            if not api_key or api_key.upper() == 'NONE':
                api_key = None
        self._api_key = api_key
        self._s = None

    def getHeaders(self, username=None, password=None, headers=None):
        if headers is None:
            headers = {}
        else:
            if username is None:
                username = self._username
            if password is None:
                password = self._password
            if username is not None and password is not None:
                auth_string = username + ':' + password
                auth_string = auth_string.encode('utf-8')
                auth_string = base64.b64encode(auth_string)
                auth_string = b'Basic ' + auth_string
                headers['Authorization'] = auth_string
        return headers

    def verifyCert(self):
        if 'H5PYD_VERIFY_CERT' in os.environ:
            verify_cert = os.environ['H5PYD_VERIFY_CERT'].upper()
            if verify_cert.startswith('F'):
                return False
        return True

    def getObjDb(self):
        return self._objdb

    def GET(self, req, format='json', params=None, headers=None, use_cache=True):
        if self._endpoint is None:
            raise IOError('object not initialized')
        else:
            if self._objdb:
                pass
            rsp = None
            if not headers:
                headers = self.getHeaders()
            if params is None:
                params = {}
            if 'domain' not in params:
                params['domain'] = self._domain
            if 'bucket' not in params:
                if self._bucket:
                    params['bucket'] = self._bucket
            if self._api_key:
                params['api_key'] = self._api_key
            if format == 'binary':
                headers['accept'] = 'application/octet-stream'
            if self._cache is not None:
                if use_cache:
                    if format == 'json':
                        if params['domain'] == self._domain:
                            self.log.debug('httpcon - checking cache')
                            if req in self._cache:
                                self.log.debug('httpcon - returning cache result')
                                rsp = self._cache[req]
                                return rsp
            self.log.info('GET: {} [{}]'.format(self._endpoint + req, params['domain']))
            if self._username and self._password:
                auth = (
                 self._username, self._password)
            else:
                auth = None
            try:
                s = self.session
                rsp = s.get((self._endpoint + req), params=params, headers=headers, auth=auth, verify=(self.verifyCert()))
                self.log.info('status: {}'.format(rsp.status_code))
            except ConnectionError as ce:
                try:
                    self.log.error('connection error: {}'.format(ce))
                    raise IOError('Connection Error')
                finally:
                    ce = None
                    del ce

            if rsp.status_code == 200:
                if self._cache is not None:
                    rsp_headers = rsp.headers
                    content_length = 0
                    self.log.debug('conent_length: {}'.format(content_length))
                    if 'Content-Length' in rsp_headers:
                        try:
                            content_length = int(rsp_headers['Content-Length'])
                        except ValueError:
                            content_length = MAX_CACHE_ITEM_SIZE + 1

                    content_type = None
                    if 'Content-Type' in rsp_headers:
                        content_type = rsp_headers['Content-Type']
                    self.log.debug('content_type: {}'.format(content_type))
                    if content_type.startswith('application/json'):
                        if content_length < MAX_CACHE_ITEM_SIZE:
                            cache_rsp = CacheResponse(rsp)
                            self.log.debug('adding {} to cache'.format(req))
                            self._cache[req] = cache_rsp
                    if rsp.status_code == 200:
                        if req == '/':
                            self._domain_json = json.loads(rsp.text)
                            self.log.info('got domain json: {}'.format(self._domain_json))
        return rsp

    def PUT(self, req, body=None, format='json', params=None, headers=None):
        if self._endpoint is None:
            raise IOError('object not initialized')
        else:
            if self._domain is None:
                raise IOError('no domain defined')
            elif self._cache is not None:
                self._cache = {}
            else:
                if params:
                    self.log.info('PUT params: {}'.format(params))
                else:
                    params = {}
                if 'domain' not in params:
                    params['domain'] = self._domain
                if 'bucket' not in params:
                    if self._bucket:
                        params['bucket'] = self._bucket
                if self._api_key:
                    params['api_key'] = self._api_key
                if self._mode == 'r':
                    raise IOError('Unable to create group (No write intent on file)')
                else:
                    if not headers:
                        headers = self.getHeaders()
                    if format == 'binary':
                        headers['Content-Type'] = 'application/octet-stream'
                        data = body
                    else:
                        data = json.dumps(body)
                self.log.info('PUT: {} format: {} [{} bytes]'.format(req, format, len(data)))
                if self._username and self._password:
                    auth = (
                     self._username, self._password)
                else:
                    auth = None
                try:
                    s = self.session
                    rsp = s.put((self._endpoint + req), data=data, headers=headers, params=params, auth=auth, verify=(self.verifyCert()))
                    self.log.info('status: {}'.format(rsp.status_code))
                except ConnectionError as ce:
                    try:
                        self.log.error('connection error: {}'.format(ce))
                        raise IOError('Connection Error')
                    finally:
                        ce = None
                        del ce

            if rsp.status_code == 201 and req == '/':
                self.log.info('clearning domain_json cache')
                self._domain_json = None
        return rsp

    def POST(self, req, body=None, format='json', params=None, headers=None):
        if self._endpoint is None:
            raise IOError('object not initialized')
        elif self._domain is None:
            raise IOError('no domain defined')
        else:
            if self._cache is not None:
                self._cache = {}
            else:
                if params is None:
                    params = {}
                else:
                    if 'domain' not in params:
                        params['domain'] = self._domain
                    if 'bucket' not in params:
                        if self._bucket:
                            params['bucket'] = self._bucket
                    if self._api_key:
                        params['api_key'] = self._api_key
                    if req.startswith('/datasets/') and req.endswith('/value'):
                        point_sel = True
                    else:
                        point_sel = False
                if self._mode == 'r':
                    if not point_sel:
                        raise IOError('Unable perform request (No write intent on file)')
                    else:
                        if not headers:
                            headers = self.getHeaders()
                        if format == 'binary':
                            headers['Content-Type'] = 'application/octet-stream'
                            headers['accept'] = 'application/octet-stream'
                            data = body
                        else:
                            data = json.dumps(body)
                    self.log.info('POST: ' + req)
                    if self._username and self._password:
                        auth = (
                         self._username, self._password)
                else:
                    auth = None
            try:
                s = self.session
                rsp = s.post((self._endpoint + req), data=data, headers=headers, params=params, auth=auth, verify=(self.verifyCert()))
            except ConnectionError as ce:
                try:
                    self.log.warn('connection error: ', ce)
                    raise IOError(str(ce))
                finally:
                    ce = None
                    del ce

        return rsp

    def DELETE(self, req, params=None, headers=None):
        if self._endpoint is None:
            raise IOError('object not initialized')
        else:
            if self._domain is None:
                raise IOError('no domain defined')
            elif self._cache is not None:
                self._cache = {}
            else:
                if params is None:
                    params = {}
                else:
                    if 'domain' not in params:
                        params['domain'] = self._domain
                    if 'bucket' not in params:
                        if self._bucket:
                            params['bucket'] = self._bucket
                        else:
                            if self._api_key:
                                params['api_key'] = self._api_key
                            if self._mode == 'r':
                                raise IOError('Unable perform request (No write intent on file)')
                            headers = headers or self.getHeaders()
                        self.log.info('DEL: ' + req)
                        if self._username and self._password:
                            auth = (
                             self._username, self._password)
                    else:
                        auth = None
                try:
                    s = self.session
                    rsp = s.delete((self._endpoint + req), headers=headers, params=params, auth=auth, verify=(self.verifyCert()))
                    self.log.info('status: {}'.format(rsp.status_code))
                except ConnectionError as ce:
                    try:
                        self.log.error('connection error: {}'.format(ce))
                        raise IOError('Connection Error')
                    finally:
                        ce = None
                        del ce

            if rsp.status_code == 200 and req == '/':
                self.log.info('clearning domain_json cache')
                self._domain_json = None
        return rsp

    @property
    def session(self):
        s = requests
        retries = self._retries
        backoff_factor = 0.1
        status_forcelist = (500, 502, 503, 504)
        if self._use_session:
            if self._s is None:
                s = requests.Session()
                retry = Retry(total=retries,
                  read=retries,
                  connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
                adapter = HTTPAdapter(max_retries=retry)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                self._s = s
            else:
                s = self._s
        return s

    def close(self):
        if self._s:
            self._s.close()
            self._s = None

    @property
    def domain(self):
        return self._domain

    @property
    def username(self):
        return self._username

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def password(self):
        return self._password

    @property
    def mode(self):
        return self._mode

    @property
    def domain_json(self):
        if self._domain_json is None:
            rsp = self.GET('/')
            if rsp.status_code != 200:
                raise IOError(rsp.reason)
            self._domain_json = json.loads(rsp.text)
        return self._domain_json

    @property
    def root_uuid(self):
        domain_json = self.domain_json
        if 'root' not in domain_json:
            raise IOError('Unexpected response')
        root_uuid = domain_json['root']
        return root_uuid

    @property
    def modified(self):
        """Last modified time of the domain as a datetime object."""
        domain_json = self.domain_json
        if 'lastModified' not in domain_json:
            raise IOError('Unexpected response')
        last_modified = domain_json['lastModified']
        return last_modified

    @property
    def created(self):
        """Creation time of the domain"""
        domain_json = self.domain_json
        if 'created' not in domain_json:
            raise IOError('Unexpected response')
        created = domain_json['created']
        return created

    @property
    def owner(self):
        """ username of creator of domain"""
        domain_json = self.domain_json
        username = None
        if 'owner' in domain_json:
            username = domain_json['owner']
        return username

    @property
    def logging(self):
        """ return name of logging handler"""
        return self.log