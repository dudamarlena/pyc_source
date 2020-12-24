# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/asyncio/dispatcher.py
# Compiled at: 2018-05-09 13:32:53
# Size of source mod 2**32: 2095 bytes
import logging, sys, traceback
from mercury.common.exceptions import EndpointError
log = logging.getLogger(__name__)

class AsyncDispatcher(object):

    def __init__(self, controller, acknowledge_only=False):
        """
        Asynchronous generic dispatcher

        :param controller: An controller containing async endpoints
        :param acknowledge_only: Immediately sync the response to the client
        request.
        """
        self.controller = controller
        log.debug(f"Registered endpoints: {self.controller.endpoints}")

    async def dispatch(self, message):
        endpoint = message.get('endpoint')
        args = message.get('args', [])
        kwargs = message.get('kwargs', {})
        if not endpoint:
            log.debug('Received message with no endpoint')
            return dict(error=True, message='Endpoint not specified in message')
        if endpoint not in self.controller.endpoints:
            log.debug('Received request to unsupported endpoint: %s' % endpoint)
            return dict(error=True, message='Endpoint is not supported')
        try:
            response = await (self.controller.endpoints[endpoint])(
 self.controller, *args, **kwargs)
        except EndpointError as endpoint_error:
            try:
                tb = (traceback.format_exception)(*sys.exc_info())
                log.error('Endpoint Error: endpoint=%s, message=%s, traceback=%s' % (
                 endpoint,
                 endpoint_error.message,
                 '\n'.join(tb)))
                return dict(error=True, traceback=tb, message=(endpoint_error.message))
            finally:
                endpoint_error = None
                del endpoint_error

        except Exception as e:
            try:
                tb = (traceback.format_exception)(*sys.exc_info())
                log.error('An unhandled exception has been encountered: endpoint=%s, message=%s, traceback=%s' % (
                 endpoint,
                 str(e),
                 '\n'.join(tb)))
                return dict(error=True, traceback=tb, message=(str(e)))
            finally:
                e = None
                del e

        return dict(error=False, message=response)