# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/test_http.py
# Compiled at: 2010-09-03 02:22:19
try:
    import json
except ImportError:
    import simplejson as json

from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList, inlineCallbacks, returnValue
from twisted.trial.unittest import TestCase
from twisted.web import http
from twisted.web.resource import Resource
from pendrell import log
from pendrell.protocols import OKAY_CODES
from pendrell.error import WebError
from pendrell.cases.util import PendrellTestMixin
from pendrell.cases.http_server import Site, NOT_DONE_YET
_CONFUSION_IS_SEX = 'I maintain that chaos is the future\nAnd beyond it is freedom\nConfusion is next and next after that is the truth\nYou got to cultivate what you need to need\nSonic tooth\nSonic tooth\nSonic tooth\n\nStick your fingers in your mouth\nSqueeze your tongue and wrench it out\nFrom its ugly fucking cancer\nIts ugly fucking cancer root\nYou got to cultivate what you need to need\nSonic tooth\nSonic tooth\nSonic tooth\n\nChaos is the future and beyond it is freedom\nConfusion is next and next after that is the truth\nYou gotta cultivate what you need to need\nSonic tooth, sonic tooth\nSonic tooth, sonic tooth\nStick your fingers in your mouth\nSqueeze your tongue and wrench it out\nFrom its ugly fucking cancer\nIts ugly fucking cancer root\nYou got to cultivate what you need to need\nSonic tooth, sonic tooth\nSonic tooth, sonic tooth\n\nTell nothing but the truth. \n'

class _MethodSite(Site):

    def __init__(self):
        Site.__init__(self, _MethodRoot())


class _MethodRoot(Resource):
    isLeaf = False

    def __init__(self):
        Resource.__init__(self)
        self.putChild('', _RootResource())
        self.putChild('deleteme', _DeleteableResource(self))
        self.putChild('generator', _GeneratorRoot())
        self.putChild('aminal', _PuttableResource())

    def deleteYou(self):
        self.delEntity('deleteme')


class _OptionsResource(Resource):

    @property
    def allowedMethods(self):
        """Get the list of allowed methods from render_{METHOD} methods.
        """
        methods = []
        for attr in dir(self):
            if attr.startswith('render_'):
                (prefix, method) = attr.split('_', 1)
                if method.isupper():
                    methods.append(method)

        return methods

    def render_OPTIONS(self, request):
        request.setHeader('Allow', (', ').join(self.allowedMethods))
        return ''


class _GettableResource(_OptionsResource):
    isLeaf = True

    def render_GET(self, request):
        request.setResponseCode(http.NO_CONTENT)
        request.finish()
        return NOT_DONE_YET


class _DeleteableResource(_GettableResource):
    isLeaf = True

    def __init__(self, parent):
        _GettableResource.__init__(self)
        self.parent = parent

    def render_DELETE(self, request):
        self.parent.deleteYou()
        request.setResponseCode(http.NO_CONTENT)
        request.finish()
        return NOT_DONE_YET


class _PuttableResource(_OptionsResource):
    isLeaf = True
    animal = 'monkey'

    @property
    def json(self):
        return json.dumps({'animal': self.animal})

    def render_GET(self, request):
        request.setHeader('Content-type', 'application/json')
        return self.json

    def render_PUT(self, request):
        contentType = request.getHeader('Content-type')
        if contentType == 'application/json':
            rep = json.load(request.content)
            try:
                self.animal = rep['animal']
            except KeyError:
                request.setResponseCode(http.BAD_REQUEST)

        else:
            request.setResponseCode(http.BAD_REQUEST)
        request.setHeader('Content-type', 'application/json')
        return self.json


class _RootResource(_OptionsResource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader('Content-type', 'text/plain')
        return _CONFUSION_IS_SEX


class _GeneratorRoot(Resource):
    isLeaf = False

    def __init__(self):
        Resource.__init__(self)
        self.putChild('', _GeneratorResource(self))


class _GeneratorResource(_GettableResource):
    isLeaf = True

    def __init__(self, parent):
        Resource.__init__(self)
        self.parent = parent

    def buildUrl(self, request, resourceName):
        scheme = 'http'
        host = request.getRequestHostname()
        port = request.getHost().port
        portSpec = '' if port == 80 else ':%d' % port
        path = str().join([request.uri, resourceName])
        return str('%s://%s%s%s' % (scheme, host, portSpec, path))

    def render_POST(self, request):
        contentType = request.getHeader('Content-type')
        if contentType == 'application/json':
            content = json.load(request.content)
            resourceName = content['resource']
            if resourceName not in self.parent.children:
                url = self.buildUrl(request, resourceName)
                log.msg('%r: Creating resource: %s' % (request, url))
                resource = _GettableResource()
                self.parent.putChild(resourceName, resource)
                log.msg('%r: Created resource: %s' % (request, url))
                request.setResponseCode(http.CREATED)
                request.setHeader('Location', url)
            else:
                request.setResponseCode(http.CONFLICT)
        else:
            request.setResponseCode(http.BAD_REQUEST)
        return ''


class HTTPMethodTestMixin(object):
    _lo0 = '127.0.0.1'
    http_port = 8086

    def setUp(self):
        site = _MethodSite()
        self.server = reactor.listenTCP(self.http_port, site, interface=self._lo0)

    def tearDown(self):
        return self.server.stopListening()

    @property
    def baseUrl(self):
        return 'http://%s:%d/' % (self._lo0, self.http_port)

    @property
    def deleteableUrl(self):
        return self.baseUrl + 'deleteme'

    @property
    def generatorUrl(self):
        return self.baseUrl + 'generator/'

    @property
    def puttableUrl(self):
        return self.baseUrl + 'aminal'

    @inlineCallbacks
    def test_get(self):
        result = yield self.getPage(self.baseUrl)
        self.assertTrue(result.status in OKAY_CODES)
        self.assertEquals(len(_CONFUSION_IS_SEX), len(result))

    @inlineCallbacks
    def test_head(self):
        result = yield self.getPage(self.baseUrl, method='HEAD')
        self.assertTrue(result.status in OKAY_CODES)
        self.assertEquals(0, len(result))
        self.assertTrue(len(result.headers) > 0)

    @inlineCallbacks
    def test_post(self):
        resource = 'naboo'
        createdUrl = self.generatorUrl + resource
        postEntity = json.dumps({'resource': resource})
        headers = {'Content-type': 'application/json'}
        try:
            yield self.getPage(createdUrl, method='GET')
        except WebError, we:
            self.assertEquals(http.NOT_FOUND, we.status)
        else:
            self.fail('Fetched %s before it was created' % createdUrl)

        log.msg('POSTing to generate content.')
        result = yield self.getPage(self.generatorUrl, method='POST', headers=headers, data=postEntity)
        log.msg('POSTed to generate content.')
        self.assertEquals(http.CREATED, result.status)
        self.assertHeader(result, 'Location', createdUrl)
        result = yield self.getPage(createdUrl, method='GET')
        self.assertTrue(result.status in OKAY_CODES)
        try:
            yield self.getPage(self.generatorUrl, method='POST', headers=headers, data=postEntity)
        except WebError, we:
            self.assertEquals(http.CONFLICT, we.status)
        else:
            reason = 'Re-created %s after it was created' % createdUrl
            self.assertTrue(False, reason)

    @inlineCallbacks
    def test_put(self):
        result = yield self.getPage(self.puttableUrl, method='GET')
        self.assertHeader(result, 'Content-Type', 'application/json')
        repr = json.loads(result.content)
        self.assertEquals('monkey', repr['animal'])
        putEntity = json.dumps({'animal': 'puffin'})
        result = yield self.getPage(self.puttableUrl, method='PUT', headers={'Content-type': 'application/json'}, data=putEntity)
        self.assertTrue(result.status in OKAY_CODES)
        self.assertHeader(result, 'Content-Type', 'application/json')
        self.assertEquals(putEntity, result.content)
        result = yield self.getPage(self.puttableUrl, method='GET')
        self.assertTrue(result.status in OKAY_CODES)
        self.assertHeader(result, 'Content-Type', 'application/json')
        self.assertEquals(putEntity, result.content)

    @inlineCallbacks
    def test_delete(self):
        result = yield self.getPage(self.deleteableUrl, method='GET')
        self.assertTrue(result.status in OKAY_CODES)
        result = yield self.getPage(self.deleteableUrl, method='DELETE')
        deletionCodes = (http.OK, http.ACCEPTED, http.NO_CONTENT)
        self.assertTrue(result.status in deletionCodes)
        try:
            yield self.getPage(self.deleteableUrl, method='GET')
        except WebError, we:
            self.assertTrue(we.status in (http.NOT_FOUND, http.GONE))
        else:
            reason = 'Fetched %s after it was deleted' % self.deleteableUrl
            self.assertTrue(False, reason)

    @inlineCallbacks
    def test_options(self):
        result = yield self.getPage(self.baseUrl, method='OPTIONS')
        self.assertTrue(result.status in OKAY_CODES)
        self.assertHeader(result, 'Allow', 'GET, HEAD, OPTIONS')
        result = yield self.getPage(self.deleteableUrl, method='OPTIONS')
        self.assertEquals(http.OK, result.status)
        self.assertHeader(result, 'Allow', 'DELETE, GET, HEAD, OPTIONS')
        result = yield self.getPage(self.generatorUrl, method='OPTIONS')
        self.assertEquals(http.OK, result.status)
        self.assertHeader(result, 'Allow', 'GET, HEAD, OPTIONS, POST')


class PendrellHTTPMethodTests(PendrellTestMixin, HTTPMethodTestMixin, TestCase):
    timeout = 5

    def setUp(self):
        PendrellTestMixin.setUp(self)
        HTTPMethodTestMixin.setUp(self)

    @inlineCallbacks
    def tearDown(self):
        yield PendrellTestMixin.tearDown(self)
        yield HTTPMethodTestMixin.tearDown(self)