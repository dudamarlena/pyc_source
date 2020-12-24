# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyazure\storage\blob.py
# Compiled at: 2012-01-28 14:22:44
__doc__ = '\nPython wrapper around Windows Azure storage and management APIs\n\nAuthors:\n    Sriram Krishnan <sriramk@microsoft.com>\n    Steve Marx <steve.marx@microsoft.com>\n    Tihomir Petkov <tpetkov@gmail.com>\n\nLicense:\n    GNU General Public Licence (GPL)\n    \n    This file is part of pyazure.\n    \n    pyazure is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyazure is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with pyazure. If not, see <http://www.gnu.org/licenses/>.\n'
import time
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

from urllib2 import Request, urlopen, URLError
from . import Storage
from pyazure.util import RequestWithMethod, TIME_FORMAT

class BlobStorage(Storage):
    CLOUD_HOST = 'blob.core.windows.net'
    DEVSTORE_HOST = '127.0.0.1:10000'

    def __init__(self, *args, **kwargs):
        super(BlobStorage, self).__init__(*args, **kwargs)

    def create_container(self, container_name, is_public=False):
        req = RequestWithMethod('PUT', '%s/%s?restype=container' % (self.base_url, container_name))
        req.add_header('x-ms-version', '2011-08-18')
        req.add_header('Content-Length', '0')
        if is_public:
            req.add_header('x-ms-blob-public-access', 'blob')
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def delete_container(self, container_name):
        req = RequestWithMethod('DELETE', '%s/%s?restype=container' % (self.base_url, container_name))
        req.add_header('x-ms-version', '2011-08-18')
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

    def list_containers(self):
        req = RequestWithMethod('GET', '%s/?comp=list' % self.base_url)
        req.add_header('x-ms-version', '2011-08-18')
        self.credentials.sign_request(req)
        dom = etree.parse(urlopen(req))
        containers = dom.findall('.//Container')
        for container in containers:
            container_name = container.find('Name').text
            properties = container.find('Properties')
            etag = properties.find('Etag').text
            last_modified = time.strptime(properties.find('Last-Modified').text, TIME_FORMAT)
            yield (container_name, etag, last_modified)

    def list_blobs(self, container_name):
        req = RequestWithMethod('GET', '%s/%s?restype=container&comp=list' % (self.base_url, container_name))
        req.add_header('x-ms-version', '2011-08-18')
        self.credentials.sign_request(req)
        dom = etree.fromstring(urlopen(req).read())
        blobs = dom.findall('.//Blob')
        for blob in blobs:
            blob_name = blob.find('Name').text
            blob_properties = blob.find('Properties')
            etag = blob_properties.find('Etag').text
            size = blob_properties.find('Content-Length').text
            last_modified = time.strptime(blob_properties.find('Last-Modified').text, TIME_FORMAT)
            yield (blob_name, etag, last_modified, size)

    def put_blob(self, container_name, blob_name, data, content_type=None, page_block=False):
        req = RequestWithMethod('PUT', '%s/%s/%s' % (self.base_url, container_name, blob_name), data=data)
        req.add_header('x-ms-version', '2011-08-18')
        req.add_header('x-ms-blob-type', 'PageBlob' if page_block else 'BlockBlob')
        req.add_header('Content-Length', '%d' % len(data))
        req.add_header('Content-Type', content_type if content_type is not None else '')
        self.credentials.sign_request(req)
        try:
            response = urlopen(req)
            return response.code
        except URLError as e:
            return e.code

        return

    def get_blob(self, container_name, blob_name):
        req = Request('%s/%s/%s' % (self.base_url, container_name, blob_name))
        req.add_header('x-ms-version', '2011-08-18')
        self.credentials.sign_request(req)
        return urlopen(req).read()

    def delete_blob(self, container_name, blob_name):
        req = RequestWithMethod('DELETE', '%s/%s/%s' % (self.base_url, container_name, blob_name))
        req.add_header('x-ms-version', '2011-08-18')
        self.credentials.sign_request(req)
        return urlopen(req).read()