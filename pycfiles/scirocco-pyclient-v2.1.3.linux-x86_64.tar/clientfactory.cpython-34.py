# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/clientfactory.py
# Compiled at: 2016-11-22 16:46:46
# Size of source mod 2**32: 2235 bytes
import urllib3
from sciroccoclient.client import Client
from sciroccoclient.http.messagedao import MessageDAO
from sciroccoclient.http.messagequeuedao import MessageQueueDAO
from sciroccoclient.http.requestadapter import RequestsAdapter, RequestManagerResponseHandler, RequestManagerDataResponseHandler, RequestManagerContentTypeDetector
from sciroccoclient.messages import SciroccoMessageValidator
from sciroccoclient.metadata import MetaDataDescriptor, MetaData, MetaDataHTTPHeadersFilter, MetaDataHydrator

class ClientFactory:

    def get_http_client(self, api_url, node_id, auth_token):
        """
        :param api_url: string
            scirocco instance to connect to.
        :param node_id: string
            identify this instance as a node of the system.
        :param auth_token: string
            Token that authorizes this node to access the server.
        :return: Client intance.
        """
        metadata_entity = MetaData()
        metadata_hydrator = MetaDataHydrator()
        metadata_descriptor = MetaDataDescriptor(metadata_entity)
        message_validator = SciroccoMessageValidator()
        system_headers_filter = MetaDataHTTPHeadersFilter(metadata_descriptor)
        request_manager_response_handler = RequestManagerResponseHandler(system_headers_filter, metadata_hydrator, RequestManagerDataResponseHandler())
        request_adapter = RequestsAdapter(urllib3.PoolManager(), request_manager_response_handler, metadata_descriptor, RequestManagerContentTypeDetector())
        request_adapter.api_url = api_url
        request_adapter.node_id = node_id
        request_adapter.auth_token = auth_token
        message_dao = MessageDAO(request_adapter, metadata_hydrator)
        message_queue_dao = MessageQueueDAO(request_adapter, metadata_descriptor)
        client = Client(message_dao, message_queue_dao, message_validator)
        return client

    def get_mongo_client(self):
        raise NotImplementedError