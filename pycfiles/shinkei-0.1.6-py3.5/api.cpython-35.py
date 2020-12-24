# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/api.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 2727 bytes
import logging, aiohttp
from .exceptions import ShinkeiHTTPException
from .objects import Version
try:
    import ujson as json
except ImportError:
    import json

log = logging.getLogger(__name__)

class APIClient:
    BODY_METHODS = {
     'POST', 'PATCH', 'PUT', 'DELETE', 'MOVE'}
    METHODS = BODY_METHODS | {'GET', 'HEAD'}

    def __init__(self):
        self.headers = {}

    @classmethod
    async def create(cls, url, *, session, auth, loop):
        self = cls()
        self.session = session or aiohttp.ClientSession(json_serialize=json.dumps, loop=loop)
        self.url = url / 'api'
        self.auth = auth
        if self.auth:
            self.headers['Authorization'] = auth
        self.version = Version(await self._fetch_version())
        self.url = self.url / self.version.api
        return self

    async def request(self, method, url, **kwargs):
        async with self.session.request(method, url, headers=self.headers, **kwargs) as response:
            log.debug('%s %s with %s returned %d status code', method, url.human_repr(), kwargs.get('data'), response.status)
            data = await response.json(loads=json.loads)
            if not response.status == 200:
                raise ShinkeiHTTPException(response, response.status, '{0.status} {0.reason} {1}'.format(response, data.get('error')))
            return data

    async def _fetch_version(self):
        return await self.request('GET', self.url / 'version')

    async def discovery_tags(self, tags):
        if not isinstance(tags, list):
            raise TypeError('Expected type list, got {0}'.format(tags.__class__.__name__))
        tags = json.dumps(tags)
        url = (self.url / 'discovery' / 'tags').with_query('q={0}'.format(tags))
        return await self.request('GET', url)

    async def proxy(self, method, route, *, target, body=None, headers=None):
        actual = method.upper()
        if actual not in self.METHODS:
            raise ValueError('{0} is not a supported HTTP method. (Valid methods are {1.METHODS})'.format(actual, self))
        payload = {'method': actual, 
         'route': route, 
         'query': target.to_json()}
        can_have_body = actual in self.BODY_METHODS
        if body is None and can_have_body:
            payload['body'] = ''
        elif body is not None and can_have_body:
            payload['body'] = body
        if headers is None:
            payload['headers'] = {}
        return await self.request('POST', self.url / 'proxy', data=payload)