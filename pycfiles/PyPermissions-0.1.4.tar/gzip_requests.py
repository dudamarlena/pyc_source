# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pypermedia/gzip_requests.py
# Compiled at: 2016-02-16 21:09:46
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from requests import Request
import zlib

class GzipRequest(Request):
    """Encapsulates gzip requests. Currently just adds a header but may be extended in the future to do more."""

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        :param args: all of request's normal positional arguments, unused by GzipRequest itself
        :param kwargs: all of request's normal kwargs, unused by GzipRequest itself
        """
        super(GzipRequest, self).__init__(*args, **kwargs)
        self.headers[b'Accept-Encoding'] = b'gzip, deflate'

    def prepare(self):
        """
        Constructs a prepared request and compresses its contents.
        :return: prepared request with compressed payload
        :rtype: requests.PreparedRequest
        """
        p = super(GzipRequest, self).prepare()
        if p.body and (self.method == b'POST' or self.method == b'PUT' or self.method == b'PATCH'):
            p.method = p.method.encode(b'utf-8')
            p.body = self.gzip_compress(p.body)
            p.headers[b'Content-Length'] = len(p.body)
            p.headers[b'Content-Encoding'] = b'gzip'
        return p

    @staticmethod
    def gzip_compress(data):
        """
        Gzip compresses the data.

        :param data: data to compress
        :type data: str
        :return: compressed data
        :rtype: str
        """
        gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
        return gzip_compress.compress(data) + gzip_compress.flush()