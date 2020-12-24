# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyazure\storage\queue.py
# Compiled at: 2012-01-28 13:48:49
__doc__ = '\nPython wrapper around Windows Azure storage and management APIs\n\nAuthors:\n    Sriram Krishnan <sriramk@microsoft.com>\n    Steve Marx <steve.marx@microsoft.com>\n    Tihomir Petkov <tpetkov@gmail.com>\n    Blair Bethwaite <blair.bethwaite@gmail.com>\n\nLicense:\n    GNU General Public Licence (GPL)\n    \n    This file is part of pyazure.\n    \n    pyazure is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyazure is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with pyazure. If not, see <http://www.gnu.org/licenses/>.\n'
import base64, time
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

from urllib2 import Request, urlopen, URLError
from . import Storage
from pyazure.util import *

class QueueMessage:
    pass


class Queue(object):

    def __init__(self, name='', url='', metadata=None):
        self.name = name
        self.url = url
        self.metadata = metadata


class QueueStorage(Storage):
    CLOUD_HOST = 'queue.core.windows.net'
    DEVSTORE_HOST = '127.0.0.1:10001'

    def __init__(self, *args, **kwargs):
        super(QueueStorage, self).__init__(*args, **kwargs)

    def create_queue(self, name):
        req = RequestWithMethod('PUT', '%s/%s' % (self.base_url, name))
        req.add_header('Content-Length', '0')
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def delete_queue(self, name):
        req = RequestWithMethod('DELETE', '%s/%s' % (self.base_url, name))
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def list_queues(self, prefix=None, marker=None, maxresults=None, include_metadata=False):
        request_string = self.base_url + '/?comp=list'
        if prefix:
            request_string = add_url_parameter(request_string, 'prefix', prefix)
        if marker:
            request_string = add_url_parameter(request_string, 'marker', marker)
        if maxresults:
            request_string = add_url_parameter(request_string, 'maxresults', maxresults)
        if include_metadata:
            request_string = add_url_parameter(request_string, 'include', 'metadata')
        req = Request(request_string)
        req = self.credentials.sign_request(req)
        response = urlopen(req)
        dom = etree.fromstring(response.read())
        entries = dom.findall('.//Queue')
        next_marker = dom.find('.//NextMarker').text
        parsed_queues = [ self._parse_queue(e) for e in entries ]
        return dict(next_marker=next_marker, queues=parsed_queues)

    def get_queue_metadata(self, queue_name):
        req = RequestWithMethod('HEAD', '%s/%s?comp=metadata' % (
         self.base_url, queue_name))
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
        except URLError as e:
            return e.code

        approx_msg_count = response.headers.getheader('x-ms-approximate-messages-count')
        metadata = {}
        for k, v in zip(response.headers.keys(), response.headers.values()):
            if k.startswith('x-ms-meta-') and not metadata.has_key(k[10:]):
                metadata[k[10:]] = v

        return (
         approx_msg_count, metadata)

    def set_queue_metadata(self, queue_name, metadata={}):
        req = RequestWithMethod('PUT', '%s/%s?comp=metadata' % (
         self.base_url, queue_name))
        req.add_header('Content-Length', '0')
        for k, v in metadata.iteritems():
            req.add_header('x-ms-meta-' + unicode(k), unicode(v))

        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
        except URLError as e:
            return e.code

        return response.code

    def clear_messages(self, queue_name, retry_on_errors=True, number_of_retries=3, retry_sleep_time=2):
        sent_requests = 0
        while True:
            result = self._clear_messages(queue_name)
            sent_requests += 1
            if result == 204:
                return result
            if retry_on_errors and sent_requests <= number_of_retries:
                time.sleep(retry_sleep_time)
                continue
            else:
                return result

    def put_message(self, queue_name, payload):
        data = '<QueueMessage><MessageText>%s</MessageText></QueueMessage>' % base64.encodestring(payload)
        req = RequestWithMethod('POST', '%s/%s/messages' % (self.base_url, queue_name), data=data)
        req.add_header('Content-Type', 'application/xml')
        req.add_header('Content-Length', len(data))
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def get_message(self, queue_name):
        req = Request('%s/%s/messages' % (self.base_url, queue_name))
        self.credentials.sign_request(req)
        response = urlopen(req)
        dom = etree.fromstring(response.read())
        messages = dom.findall('QueueMessage')
        result = None
        if len(messages) == 1:
            message = messages[0]
            result = QueueMessage()
            result.id = message.find('MessageId').text
            result.pop_receipt = message.find('PopReceipt').text
            result.text = base64.decodestring(message.find('MessageText').text)
        return result

    def delete_message(self, queue_name, message):
        id = message.id
        pop_receipt = message.pop_receipt
        req = RequestWithMethod('DELETE', '%s/%s/messages/%s?popreceipt=%s' % (self.base_url, queue_name, id, pop_receipt))
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def _parse_queue(self, entry):
        queue = Queue()
        queue.name = entry.find('QueueName').text
        queue.url = entry.find('Url').text
        metadata = entry.find('Metadata')
        if metadata:
            parsed_meta = {}
            for m in metadata.getchildren():
                if not parsed_meta.has_key(m.tag):
                    parsed_meta[m.tag] = m.text

            queue.metadata = parsed_meta
        return queue

    def _clear_messages(self, queue_name):
        request_string = self.base_url + '/' + queue_name + '/messages'
        req = RequestWithMethod('DELETE', request_string)
        req = self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code