# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/http/messagequeuedao.py
# Compiled at: 2016-11-22 16:46:46
# Size of source mod 2**32: 2330 bytes
from sciroccoclient.exceptions import SciroccoHTTPDAOError
from sciroccoclient.responses import ClientMessageResponse

class MessageQueueDAO:

    def __init__(self, request_adapter, metadata_descriptor):
        self.request_adapter = request_adapter
        self.metadata_descriptor = metadata_descriptor
        self.end_point = '/messageQueue'

    def pull(self):
        request_response = self.request_adapter.request('GET', self.end_point)
        if request_response.http_status is 200:
            ro = ClientMessageResponse()
            ro.metadata = request_response.metadata
            ro.payload = request_response.payload
            return ro
        if request_response.http_status is 204:
            return
        raise SciroccoHTTPDAOError(request_response.http_status)

    def push(self, message):
        headers = {self.metadata_descriptor.get_http_header_by_field_name('node_destination'): message.node_destination, 
         self.metadata_descriptor.get_http_header_by_field_name('status'): message.status}
        if message.payload_type:
            headers.update({self.metadata_descriptor.get_http_header_by_field_name('payload_type'): message.payload_type})
        if message.status == 'scheduled':
            if message.scheduled_time:
                headers.update({self.metadata_descriptor.get_http_header_by_field_name('scheduled_time'): message.scheduled_time})
        request_response = self.request_adapter.request('POST', self.end_point, message.payload, headers)
        if request_response.http_status is 201:
            ro = ClientMessageResponse()
            ro.metadata = request_response.metadata
            ro.payload = request_response.payload
            return ro
        raise SciroccoHTTPDAOError(request_response.http_status)

    def ack(self, msg_id):
        request_response = self.request_adapter.request('PATCH', ''.join([self.end_point, '/', msg_id, '/ack']))
        if request_response.http_status == 200:
            ro = ClientMessageResponse()
            ro.metadata = request_response.metadata
            ro.payload = request_response.payload
            return ro
        raise SciroccoHTTPDAOError(request_response.http_status)