# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/middleware/sizelimit.py
# Compiled at: 2016-06-13 14:11:03
"""
Request Body limiting middleware.

"""
from oslo.config import cfg
import webob.dec, webob.exc
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import wsgi
max_request_body_size_opt = cfg.IntOpt('osapi_max_request_body_size', default=114688, help='Max size for body of a request')
FLAGS = flags.FLAGS
FLAGS.register_opt(max_request_body_size_opt)
LOG = logging.getLogger(__name__)

class LimitingReader(object):
    """Reader to limit the size of an incoming request."""

    def __init__(self, data, limit):
        """
        :param data: Underlying data object
        :param limit: maximum number of bytes the reader should allow
        """
        self.data = data
        self.limit = limit
        self.bytes_read = 0

    def __iter__(self):
        for chunk in self.data:
            self.bytes_read += len(chunk)
            if self.bytes_read > self.limit:
                msg = _('Request is too large.')
                raise webob.exc.HTTPRequestEntityTooLarge(explanation=msg)
            else:
                yield chunk

    def read(self, i=None):
        result = self.data.read(i)
        self.bytes_read += len(result)
        if self.bytes_read > self.limit:
            msg = _('Request is too large.')
            raise webob.exc.HTTPRequestEntityTooLarge(explanation=msg)
        return result


class RequestBodySizeLimiter(wsgi.Middleware):
    """Add a 'vsm.context' to WSGI environ."""

    def __init__(self, *args, **kwargs):
        super(RequestBodySizeLimiter, self).__init__(*args, **kwargs)

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        if req.content_length > FLAGS.osapi_max_request_body_size:
            msg = _('Request is too large.')
            raise webob.exc.HTTPRequestEntityTooLarge(explanation=msg)
        if req.content_length is None and req.is_body_readable:
            limiter = LimitingReader(req.body_file, FLAGS.osapi_max_request_body_size)
            req.body_file = limiter
        return self.application