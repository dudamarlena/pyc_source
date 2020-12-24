# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/gateway/http/impl/processor/respository.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Apr 12, 2012\n\n@package: gateway service\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the gateway repository processor.\n'
from ally.container.ioc import injected
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, Chain
from ally.design.processor.handler import HandlerBranchingProceed
from ally.design.processor.processor import Using
from ally.gateway.http.spec.gateway import IRepository, RepositoryJoined
from ally.http.spec.codes import BAD_GATEWAY, isSuccess
from ally.http.spec.server import RequestHTTP, ResponseHTTP, ResponseContentHTTP, HTTP_GET, HTTP, HTTP_OPTIONS
from ally.support.util import immut
from ally.support.util_io import IInputStream
from io import BytesIO
from sched import scheduler
from threading import Thread
from urllib.parse import urlparse, parse_qsl
import codecs, json, logging, re, time
log = logging.getLogger(__name__)

class GatewayRepository(Context):
    """
    The gateway context based on @see: gateway-http/gateway.http.gateway
    """
    filters = defines(list, doc="\n    @rtype: list[string]\n    Contains a list of URIs that need to be called in order to allow the gateway Navigate. The filters are\n    allowed to have place holders of form '{1}' or '{2}' ... '{n}' where n is the number of groups obtained\n    from the Pattern, the place holders will be replaced with their respective group value. All filters\n    need to return a True value in order to allow the gateway Navigate, also parameters are allowed\n    for filter URI.\n    ")
    navigate = defines(str, doc="\n    @rtype: string\n    A pattern like string of forms like '*', 'resources/*' or 'redirect/Model/{1}'. The pattern is allowed to\n    have place holders and also the '*' which stands for the actual called URI, also parameters are allowed\n    for navigate URI, the parameters will be appended to the actual parameters.\n    ")
    putHeaders = defines(list, doc="\n    @rtype: list[tuple(string, string)]\n    The headers to be put on the forwarded requests. The values are provided as 'Name:Value', the name is\n    not allowed to contain ':'.\n    ")


class MatchRepository(Context):
    """
    The match context.
    """
    gateway = defines(Context, doc='\n    @rtype: Context\n    The matched gateway.\n    ')
    groupsURI = defines(tuple, doc='\n    @rtype: tuple(string)\n    The match groups for the URI.\n    ')


class Request(Context):
    """
    The request context.
    """
    repository = defines(IRepository)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)


class RequestGateway(RequestHTTP):
    """
    The request gateway context.
    """
    accTypes = defines(list)
    accCharSets = defines(list)


@injected
class GatewayRepositoryHandler(HandlerBranchingProceed):
    """
    Implementation for a handler that provides the gateway repository by using REST data received from either internal or
    external server. The Gateway structure is defined as in the @see: gateway-http plugin.
    """
    scheme = HTTP
    mimeTypeJson = 'json'
    encodingJson = 'utf-8'
    uri = str
    cleanupInterval = float
    assembly = Assembly

    def __init__(self):
        assert isinstance(self.scheme, str), 'Invalid scheme %s' % self.scheme
        assert isinstance(self.mimeTypeJson, str), 'Invalid json mime type %s' % self.mimeTypeJson
        assert isinstance(self.encodingJson, str), 'Invalid json encoding %s' % self.encodingJson
        assert isinstance(self.uri, str), 'Invalid URI %s' % self.uri
        assert isinstance(self.cleanupInterval, int), 'Invalid cleanup interval %s' % self.cleanupInterval
        assert isinstance(self.assembly, Assembly), 'Invalid assembly %s' % self.assembly
        super().__init__(Using(self.assembly, request=RequestGateway).sources('requestCnt', 'response', 'responseCnt'))
        self.initialize()

    def process(self, processing, request: Request, response: Response, Gateway: GatewayRepository, Match: MatchRepository, **keyargs):
        """
        @see: HandlerBranchingProceed.process
        
        Obtains the repository.
        """
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert issubclass(Gateway, GatewayRepository), 'Invalid gateway class %s' % Gateway
        assert issubclass(Match, MatchRepository), 'Invalid match class %s' % Match
        if not self._repository:
            robj, status, text = self.obtainGateways(processing, self.uri)
            if robj is None or not isSuccess(status):
                log.info("Cannot fetch the gateways from URI '%s', with response %s %s", self.uri, status, text)
                response.code, response.status, response.isSuccess = BAD_GATEWAY
                response.text = text
                return
            assert 'GatewayList' in robj, 'Invalid objects %s, not GatewayList' % robj
            self._repository = Repository([self.populate(Identifier(Gateway()), obj) for obj in robj['GatewayList']], Match)
        if request.repository:
            request.repository = RepositoryJoined(request.repository, self._repository)
        else:
            request.repository = self._repository
        return

    def obtainGateways(self, processing, uri):
        """
        Get the gateway objects representation.
        
        @param processing: Processing
            The processing used for delivering the request.
        @param uri: string
            The URI to call, parameters are allowed.
        @return: tuple(dictionary{...}|None, integer, string)
            A tuple containing as the first position the gateway objects representation, None if the gateways cannot be fetched,
            on the second position the response status and on the last position the response text.
        """
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        assert isinstance(uri, str), 'Invalid URI %s' % uri
        request = processing.ctx.request()
        assert isinstance(request, RequestGateway), 'Invalid request %s' % request
        url = urlparse(uri)
        request.scheme, request.method = self.scheme, HTTP_GET
        request.headers = {}
        request.uri = url.path.lstrip('/')
        request.parameters = parse_qsl(url.query, True, False)
        request.accTypes = [self.mimeTypeJson]
        request.accCharSets = [self.encodingJson]
        chain = Chain(processing)
        chain.process(request=request, requestCnt=processing.ctx.requestCnt(), response=processing.ctx.response(), responseCnt=processing.ctx.responseCnt()).doAll()
        response, responseCnt = chain.arg.response, chain.arg.responseCnt
        assert isinstance(response, ResponseHTTP), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContentHTTP), 'Invalid response content %s' % responseCnt
        if ResponseHTTP.text in response and response.text:
            text = response.text
        else:
            if ResponseHTTP.code in response and response.code:
                text = response.code
            else:
                text = None
        if ResponseContentHTTP.source not in responseCnt or responseCnt.source is None or not isSuccess(response.status):
            return (None, response.status, text)
        else:
            if isinstance(responseCnt.source, IInputStream):
                source = responseCnt.source
            else:
                source = BytesIO()
                for bytes in responseCnt.source:
                    source.write(bytes)

                source.seek(0)
            return (json.load(codecs.getreader(self.encodingJson)(source)), response.status, text)

    def initialize(self):
        """
        Initialize the repository.
        """
        self._repository = None
        self.startCleanupThread('Cleanup gateways thread')
        return

    def startCleanupThread(self, name):
        """
        Starts the cleanup thread.
        
        @param name: string
            The name for the thread.
        """
        schedule = scheduler(time.time, time.sleep)

        def executeCleanup():
            self.performCleanup()
            schedule.enter(self.cleanupInterval, 1, executeCleanup, ())

        schedule.enter(self.cleanupInterval, 1, executeCleanup, ())
        scheduleRunner = Thread(name=name, target=schedule.run)
        scheduleRunner.daemon = True
        scheduleRunner.start()

    def performCleanup(self):
        """
        Performs the cleanup for gateways.
        """
        self._repository = None
        return

    def populate(self, identifier, obj):
        """
        Populates the gateway based on the provided dictionary object.
        @see: gateway-http/gateway.http.gateway
        
        @param identifier: Identifier
            The identifier object to populate.
        @param obj: dictionary{string: string|list[string]}
            The dictionary used for defining the gateway object, the object as is defined from response.
        @return: Identifier
            The populated identifier object.
        """
        assert isinstance(identifier, Identifier), 'Invalid identifier %s' % identifier
        assert isinstance(obj, dict), 'Invalid object %s' % obj
        pattern = obj.get('Pattern')
        if pattern:
            assert isinstance(pattern, str), 'Invalid pattern %s' % pattern
            identifier.pattern = re.compile(pattern)
        headers = obj.get('Headers', immut()).get('Headers')
        if headers:
            assert isinstance(headers, list), 'Invalid headers %s' % headers
            for header in headers:
                if not isinstance(header, str):
                    raise AssertionError('Invalid header value %s' % header)

            identifier.headers.extend(re.compile(header) for header in headers)
        methods = obj.get('Methods', immut()).get('Methods')
        if methods:
            assert isinstance(methods, list), 'Invalid methods %s' % methods
            for method in methods:
                if not isinstance(method, str):
                    raise AssertionError('Invalid method value %s' % method)

            identifier.methods.update(method.upper() for method in methods)
        errors = obj.get('Errors', immut()).get('Errors')
        if errors:
            assert isinstance(errors, list), 'Invalid errors %s' % errors
            for error in errors:
                try:
                    identifier.errors.add(int(error))
                except ValueError:
                    raise ValueError("Invalid error value '%s'" % error)

        gateway = identifier.gateway
        assert isinstance(gateway, GatewayRepository), 'Invalid gateway %s' % gateway
        gateway.filters = obj.get('Filters', immut()).get('Filters')
        if __debug__ and gateway.filters:
            assert isinstance(gateway.filters, list), 'Invalid filters %s' % gateway.filters
            for item in gateway.filters:
                if not isinstance(item, str):
                    raise AssertionError('Invalid filter value %s' % item)

        gateway.navigate = obj.get('Navigate')
        if not not gateway.navigate:
            assert isinstance(gateway.navigate, str), 'Invalid navigate %s' % gateway.navigate
        putHeaders = obj.get('PutHeaders', immut()).get('PutHeaders')
        if putHeaders:
            assert isinstance(putHeaders, list), 'Invalid put headers %s' % putHeaders
            for putHeader in putHeaders:
                assert isinstance(putHeader, str), 'Invalid put header value %s' % putHeader
                if not len(putHeader.split(':')):
                    raise AssertionError('Invalid put header value %s' % putHeader)

            gateway.putHeaders = [putHeader.split(':', 1) for putHeader in putHeaders]
        return identifier


class Identifier:
    """
    Class that maps the gateway identifier.
    """
    __slots__ = ('gateway', 'pattern', 'headers', 'errors', 'methods')

    def __init__(self, gateway):
        """
        Construct the identifier for the provided gateway.
        
        @param gateway: GatewayRepository
            The gateway for the identifier.
        """
        assert isinstance(gateway, GatewayRepository), 'Invalid gateway %s' % gateway
        self.gateway = gateway
        self.pattern = None
        self.headers = []
        self.errors = set()
        self.methods = set()
        return


class Repository(IRepository):
    """
    The gateways repository.
    """
    __slots__ = ('_identifiers', '_cache', '_Match')

    def __init__(self, identifiers, Match):
        """
        Construct the gateways repository based on the provided dictionary object.
        
        @param identifiers: list[Identifier]
            The identifiers to be used by the repository.
        """
        assert isinstance(identifiers, list), 'Invalid identifiers %s' % identifiers
        assert issubclass(Match, MatchRepository), 'Invalid match class %s' % Match
        self._identifiers = identifiers
        self._Match = Match
        self._cache = {}

    def find(self, method=None, headers=None, uri=None, error=None):
        """
        @see: IRepository.find
        """
        for identifier in self._identifiers:
            assert isinstance(identifier, Identifier), 'Invalid identifier %s' % identifier
            groupsURI = self._macth(identifier, method, headers, uri, error)
            if groupsURI is not None:
                return self._Match(gateway=identifier.gateway, groupsURI=groupsURI)

        return

    def allowsFor(self, headers=None, uri=None):
        """
        @see: IRepository.allowsFor
        """
        allowed = set()
        for identifier in self._identifiers:
            assert isinstance(identifier, Identifier), 'Invalid identifier %s' % identifier
            groupsURI = self._macth(identifier, None, headers, uri, None)
            if groupsURI is not None:
                allowed.update(identifier.methods)
                continue

        allowed.discard(HTTP_OPTIONS)
        return allowed

    def obtainCache(self, identifier):
        """
        @see: IRepository.obtainCache
        """
        cache = self._cache.get(identifier)
        if cache is None:
            cache = self._cache[identifier] = {}
        return cache

    def _macth(self, identifier, method, headers, uri, error):
        """
        Checks the match for the provided identifier and parameters.
        
        @return: tuple(string)|None
            The URI match groups, None if there is no match.
        """
        assert isinstance(identifier, Identifier)
        groupsURI = ()
        if method is not None:
            assert isinstance(method, str), 'Invalid method %s' % method
            if identifier.methods:
                if method.upper() not in identifier.methods:
                    return
        if headers is not None:
            assert isinstance(headers, dict), 'Invalid headers %s' % uri
            isOk = False
            if identifier.headers:
                for nameValue in headers.items():
                    header = '%s:%s' % nameValue
                    for pattern in identifier.headers:
                        if pattern.match(header):
                            isOk = True
                            break

                    if isOk:
                        break

                if not isOk:
                    return
        elif identifier.headers:
            return
        if uri is not None:
            assert isinstance(uri, str), 'Invalid URI %s' % uri
            if identifier.pattern:
                matcher = identifier.pattern.match(uri)
                if matcher:
                    groupsURI = matcher.groups()
                else:
                    return
        elif identifier.pattern:
            return
        if error is not None:
            assert isinstance(error, int), 'Invalid error %s' % error
            if identifier.errors:
                if error not in identifier.errors:
                    return
            else:
                return
        elif identifier.errors:
            return
        return groupsURI