# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/middleware/fault.py
# Compiled at: 2016-06-13 14:11:03
import webob.dec, webob.exc
from vsm.api.openstack import wsgi
from vsm.openstack.common import log as logging
from vsm import utils
from vsm import wsgi as base_wsgi
LOG = logging.getLogger(__name__)

class FaultWrapper(base_wsgi.Middleware):
    """Calls down the middleware stack, making exceptions into faults."""
    _status_to_type = {}

    @staticmethod
    def status_to_type(status):
        if not FaultWrapper._status_to_type:
            for clazz in utils.walk_class_hierarchy(webob.exc.HTTPError):
                FaultWrapper._status_to_type[clazz.code] = clazz

        return FaultWrapper._status_to_type.get(status, webob.exc.HTTPInternalServerError)()

    def _error(self, inner, req):
        LOG.exception(_('Caught error: %s'), unicode(inner))
        safe = getattr(inner, 'safe', False)
        headers = getattr(inner, 'headers', None)
        status = getattr(inner, 'code', 500)
        if status is None:
            status = 500
        msg_dict = dict(url=req.url, status=status)
        LOG.info(_('%(url)s returned with HTTP %(status)d') % msg_dict)
        outer = self.status_to_type(status)
        if headers:
            outer.headers = headers
        if safe:
            outer.explanation = '%s: %s' % (inner.__class__.__name__,
             unicode(inner))
        return wsgi.Fault(outer)

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        try:
            return req.get_response(self.application)
        except Exception as ex:
            return self._error(ex, req)