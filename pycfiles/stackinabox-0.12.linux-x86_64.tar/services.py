# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmeyer/Devel/stackInABox/.tox/twine/lib/python2.7/site-packages/stackinabox/tests/utils/services.py
# Compiled at: 2017-10-30 00:49:57
import json, logging, re, six
from six.moves.urllib import parse
from stackinabox.services.service import StackInABoxService
logger = logging.getLogger(__name__)

class AdvancedService(StackInABoxService):
    POTENTIAL_RESPONSES = {'head': (204, ''), 
       'post': (200, 'created'), 
       'put': (200, 'updated'), 
       'patch': (200, 'patched'), 
       'options': (200, 'options'), 
       'delete': (204, '')}

    def __init__(self):
        super(AdvancedService, self).__init__('advanced')
        self.register(StackInABoxService.GET, '/', AdvancedService.handler)
        self.register(StackInABoxService.GET, '/h', AdvancedService.alternate_handler)
        self.register(StackInABoxService.GET, '/g', AdvancedService.query_handler)
        self.register(StackInABoxService.GET, re.compile('^/\\d+$'), AdvancedService.regex_handler)
        for key in self.POTENTIAL_RESPONSES.keys():
            self.register(key.upper(), '/', AdvancedService.extra_method_handler)

    def extra_method_handler(self, request, uri, headers):
        method = request.method.lower()
        try:
            status_code, response_body = self.POTENTIAL_RESPONSES[method]
            response = (
             status_code,
             headers,
             response_body)
        except LookupError:
            response = (589, headers, ('unknown method: {0}').format(method))

        return response

    def handler(self, request, uri, headers):
        return (
         200, headers, 'Hello')

    def alternate_handler(self, request, uri, headers):
        return (
         200, headers, 'Good-Bye')

    def query_handler(self, request, uri, headers):
        parsed_uri = parse.urlparse(uri)
        query = parsed_uri.query
        if len(query) > 0:
            queries = parse.parse_qsl(query)
            body = {}
            for k, v in queries:
                body[k] = ('{0}: Good-Bye {1}').format(k, v)

            return (
             200, headers, json.dumps(body))
        else:
            logger.debug('No query string')
            return (200, headers, 'Where did you go?')

    def regex_handler(self, request, uri, headers):
        return (200, headers, 'okay')