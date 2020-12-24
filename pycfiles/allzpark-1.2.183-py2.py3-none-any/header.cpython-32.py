# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/header.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jul 9, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the standard headers handling.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, optional, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.server import IDecoderHeader, IEncoderHeader
from collections import deque, Iterable
import re

class HeaderConfigurations:
    """
    Provides the configurations for handling HTTP headers.
    """
    separatorMain = ','
    separatorAttr = ';'
    separatorValue = '='

    def __init__(self):
        assert isinstance(self.separatorMain, str), 'Invalid main separator %s' % self.separatorMain
        assert isinstance(self.separatorAttr, str), 'Invalid attribute separator %s' % self.separatorAttr
        assert isinstance(self.separatorValue, str), 'Invalid value separator %s' % self.separatorValue
        self.reSeparatorMain = re.compile(self.separatorMain)
        self.reSeparatorAttr = re.compile(self.separatorAttr)
        self.reSeparatorValue = re.compile(self.separatorValue)


class RequestDecode(Context):
    """
    The request context.
    """
    headers = requires(dict)
    parameters = optional(list)
    decoderHeader = defines(IDecoderHeader, doc='\n    @rtype: IDecoderHeader\n    The decoder used for reading the request headers.\n    ')


@injected
class HeaderDecodeRequestHandler(HandlerProcessorProceed, HeaderConfigurations):
    """
    Provides the request decoder for handling HTTP headers.
    """
    useParameters = False

    def __init__(self):
        assert isinstance(self.useParameters, bool), 'Invalid use parameters flag %s' % self.useParameters
        HeaderConfigurations.__init__(self)
        HandlerProcessorProceed.__init__(self)

    def process(self, request: RequestDecode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provide the request headers decoders.
        """
        assert isinstance(request, RequestDecode), 'Invalid request %s' % request
        if not request.decoderHeader:
            if self.useParameters and RequestDecode.parameters in request and request.parameters:
                request.decoderHeader = DecoderHeader(self, request.headers, request.parameters)
            else:
                request.decoderHeader = DecoderHeader(self, request.headers)


class ResponseDecode(Context):
    """
    The response context.
    """
    headers = requires(dict)
    decoderHeader = defines(IDecoderHeader, doc='\n    @rtype: IDecoderHeader\n    The decoder used for reading the response headers.\n    ')


@injected
class HeaderDecodeResponseHandler(HandlerProcessorProceed, HeaderConfigurations):
    """
    Provides the response decoding for handling HTTP headers.
    """

    def __init__(self):
        HeaderConfigurations.__init__(self)
        HandlerProcessorProceed.__init__(self)

    def process(self, response: ResponseDecode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provide the response headers decoders.
        """
        assert isinstance(response, ResponseDecode), 'Invalid response %s' % response
        if not response.decoderHeader and response.headers is not None:
            response.decoderHeader = DecoderHeader(self, response.headers)
        return


class RequestEncode(Context):
    """
    The request encode context.
    """
    headers = defines(dict, doc='\n    @rtype: dictionary{string, string}\n    The raw headers for the request that the encoder will place values to.\n    ')
    encoderHeader = defines(IEncoderHeader, doc='\n    @rtype: IEncoderHeader\n    The header encoder used for encoding headers that will be used in the request.\n    ')


@injected
class HeaderEncodeRequestHandler(HandlerProcessorProceed, HeaderConfigurations):
    """
    Provides the request encoder for handling HTTP headers.
    """

    def __init__(self):
        HeaderConfigurations.__init__(self)
        HandlerProcessorProceed.__init__(self)

    def process(self, request: RequestEncode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provide the request headers encoders.
        """
        assert isinstance(request, RequestEncode), 'Invalid request %s' % request
        if not request.encoderHeader:
            request.encoderHeader = EncoderHeader(self)
            if request.headers:
                request.encoderHeader.headers.update(request.headers)
            request.headers = request.encoderHeader.headers


class ResponseEncode(Context):
    """
    The response context.
    """
    headers = defines(dict, doc='\n    @rtype: dictionary{string, string}\n    The raw headers for the response.\n    ')
    encoderHeader = defines(IEncoderHeader, doc='\n    @rtype: IEncoderHeader\n    The header encoder used for encoding headers that will be rendered in the response.\n    ')


@injected
class HeaderEncodeResponseHandler(HandlerProcessorProceed, HeaderConfigurations):
    """
    Provides the response encoder for handling HTTP headers.
    """

    def __init__(self):
        HeaderConfigurations.__init__(self)
        HandlerProcessorProceed.__init__(self)

    def process(self, response: ResponseEncode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provide the response headers encoders.
        """
        assert isinstance(response, ResponseEncode), 'Invalid response %s' % response
        if not response.encoderHeader:
            response.encoderHeader = EncoderHeader(self)
            if response.headers:
                response.encoderHeader.headers.update(response.headers)
            response.headers = response.encoderHeader.headers


class DecoderHeader(IDecoderHeader):
    """
    Implementation for @see: IDecoderHeader.
    """
    __slots__ = ('configuration', 'headers', 'parameters', 'parametersUsed')

    def __init__(self, configuration, headers, parameters=None):
        """
        Construct the decoder.
        
        @param configuration: HeaderConfigurations
            The header configuration.
        @param headers: dictionary{string, string}
            The header values.
        @param parameters: list[tuple(string, string)]
            The parameter values, this list will have have the used parameters removed.
        """
        assert isinstance(configuration, HeaderConfigurations), 'Invalid configuration %s' % configuration
        assert isinstance(headers, dict), 'Invalid headers %s' % headers
        if not parameters is None:
            assert isinstance(parameters, list), 'Invalid parameters %s' % parameters
        self.configuration = configuration
        self.headers = {hname.lower():hvalue for hname, hvalue in headers.items()}
        self.parameters = parameters
        if parameters:
            self.parametersUsed = {}
        return

    def retrieve(self, name):
        """
        @see: IDecoderHeader.retrieve
        """
        assert isinstance(name, str), 'Invalid name %s' % name
        cfg = self.configuration
        assert isinstance(cfg, HeaderConfigurations)
        name = name.lower()
        value = self.readParameters(name)
        if value:
            return cfg.separatorMain.join(value)
        return self.headers.get(name)

    def decode(self, name):
        """
        @see: IDecoderHeader.decode
        """
        assert isinstance(name, str), 'Invalid name %s' % name
        name = name.lower()
        value = self.readParameters(name)
        if value:
            parsed = []
            for v in value:
                self.parse(v, parsed)

            return parsed
        value = self.headers.get(name)
        if value:
            return self.parse(value)

    def parse(self, value, parsed=None):
        """
        Parses the provided value.
        
        @param value: string
            The value to parse.
        @param parsed: list[tuple(string, dictionary{string, string}]
            The parsed values.
        @return: list[tuple(string, dictionary{string, string}]
            The parsed values, if parsed is provided then it will be the same list.
        """
        assert isinstance(value, str), 'Invalid value %s' % value
        cfg = self.configuration
        assert isinstance(cfg, HeaderConfigurations)
        parsed = [] if parsed is None else parsed
        for values in cfg.reSeparatorMain.split(value):
            valAttr = cfg.reSeparatorAttr.split(values)
            attributes = {}
            for k in range(1, len(valAttr)):
                val = cfg.reSeparatorValue.split(valAttr[k])
                attributes[val[0].strip()] = val[1].strip().strip('"') if len(val) > 1 else None

            parsed.append((valAttr[0].strip(), attributes))

        return parsed

    def readParameters(self, name):
        """
        Read the parameters for the provided name.
        
        @param name: string
            The name (lower case) to read the parameters for.
        @return: deque[string]
            The list of found values, might be empty.
        """
        if not self.parameters:
            return
        else:
            assert isinstance(name, str), 'Invalid name %s' % name
            assert name == name.lower(), 'Invalid name %s, needs to be lower case only' % name
            value = self.parametersUsed.get(name)
            if value is None:
                value, k = deque(), 0
                while k < len(self.parameters):
                    if self.parameters[k][0].lower() == name:
                        value.append(self.parameters[k][1])
                        del self.parameters[k]
                        k -= 1
                    k += 1

                self.parametersUsed[name] = value
            return value


class EncoderHeader(IEncoderHeader):
    """
    Implementation for @see: IEncoderHeader.
    """
    __slots__ = ('configuration', 'headers')

    def __init__(self, configuration):
        """
        Construct the encoder.
        
        @param configuration: HeaderConfigurations
            The header configuration.
        """
        assert isinstance(configuration, HeaderConfigurations), 'Invalid configuration %s' % configuration
        self.configuration = configuration
        self.headers = {}

    def encode(self, name, *value):
        """
        @see: IEncoderHeader.encode
        """
        assert isinstance(name, str), 'Invalid name %s' % name
        cfg = self.configuration
        assert isinstance(cfg, HeaderConfigurations)
        values = []
        for val in value:
            assert isinstance(val, Iterable), 'Invalid value %s' % val
            if isinstance(val, str):
                values.append(val)
            else:
                value, attributes = val
                attributes = cfg.separatorValue.join(attributes)
                values.append(cfg.separatorAttr.join((value, attributes)) if attributes else value)

        self.headers[name] = cfg.separatorMain.join(values)