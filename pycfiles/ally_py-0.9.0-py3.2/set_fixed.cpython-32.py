# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/headers/set_fixed.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 5, 2012

@package: ally http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides support for setting fixed headers on responses.
"""
from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.server import IEncoderHeader
import logging
log = logging.getLogger(__name__)

class Response(Context):
    """
    The response context.
    """
    encoderHeader = requires(IEncoderHeader)


@injected
class HeaderSetEncodeHandler(HandlerProcessorProceed):
    """
    Provides the setting of static header values.
    """
    headers = dict

    def __init__(self):
        assert isinstance(self.headers, dict), 'Invalid header dictionary %s' % self.header
        for name, value in self.headers.items():
            assert isinstance(name, str), 'Invalid header name %s' % name
            if not isinstance(value, list):
                raise AssertionError('Invalid header value %s' % value)

        super().__init__()

    def process(self, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Set the fixed header values on the response.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), 'Invalid header encoder %s' % response.encoderHeader
        for name, value in self.headers.items():
            response.encoderHeader.encode(name, *value)