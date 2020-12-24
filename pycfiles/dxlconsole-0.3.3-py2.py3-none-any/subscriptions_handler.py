# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opendxl/viji/opendxl-console/dxlconsole/modules/monitor/subscriptions_handler.py
# Compiled at: 2019-06-07 18:26:01
from __future__ import absolute_import
import json, logging, tornado, dxlconsole.util
from dxlconsole.handlers import BaseRequestHandler
logger = logging.getLogger(__name__)

class SubscriptionsHandler(BaseRequestHandler):
    """
    Handles requests for the subscriptions list including fetch, add, and remove.
    """

    def __init__(self, application, request, module):
        super(SubscriptionsHandler, self).__init__(application, request)
        self._module = module

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        client_id = self.get_query_argument('clientId')
        if client_id == 'null':
            self.write(dxlconsole.util.create_sc_error_response('No client ID sent with request.'))
            return
        client = self._module.get_dxl_client(str(client_id))
        response_wrapper = dxlconsole.util.create_sc_response_wrapper()
        response = response_wrapper['response']
        if self.get_query_argument('_operationType') == 'add':
            topic = str(self.get_query_argument('topic'))
            client.subscribe(topic)
        elif self.get_query_argument('_operationType') == 'remove':
            topic = str(self.get_query_argument('topic'))
            client.unsubscribe(topic)
        else:
            for subscription in client.subscriptions:
                if '/mcafee/client' not in subscription:
                    subscription_entry = {'topic': subscription}
                    response['data'].append(subscription_entry)

            response['endRow'] = len(client.subscriptions) - 1
            response['totalRows'] = len(client.subscriptions) - 1
        logger.debug('Subscription handler response: %s', json.dumps(response_wrapper))
        self.write(response_wrapper)