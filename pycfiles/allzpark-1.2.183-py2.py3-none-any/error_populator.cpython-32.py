# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/error_populator.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Aug 9, 2011\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the error code conversion to response.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import PATH_NOT_FOUND
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    parameters = requires(list)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)
    allows = defines(list)


@injected
class ErrorPopulator(HandlerProcessorProceed):
    """
    Provides the error processor, practically it just populates error data that the other processors can convert to
    a proper response.
    """
    nameStatus = 'status'
    nameAllow = 'allow'
    statusToCode = dict

    def __init__(self):
        assert isinstance(self.nameStatus, str), 'Invalid name status %s' % self.nameStatus
        assert isinstance(self.nameAllow, str), 'Invalid name allow %s' % self.nameAllow
        assert isinstance(self.statusToCode, dict), 'Invalid status to code %s' % self.statusToCode
        super().__init__()

    def process(self, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provides the error data populating.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False:
            return
        else:
            status, allows = None, []
            for name, value in request.parameters:
                if status is None and name == self.nameStatus:
                    try:
                        status = int(value)
                    except ValueError:
                        if not log.debug("Invalid status value '%s'", value):
                            assert True

                elif name == self.nameAllow:
                    allows.append(value)
                    continue

            response.code, response.status, response.isSuccess = self.statusToCode.get(status, PATH_NOT_FOUND)
            if response.allows is None:
                response.allows = allows
            else:
                response.allows.extend(allows)
            return