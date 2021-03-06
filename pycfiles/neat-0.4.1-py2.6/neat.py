# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/neat/neat.py
# Compiled at: 2010-09-02 10:59:29
import logging, os, time
from urllib import urlencode
from webob import Response, Request
from webob.acceptparse import Accept
from . import errors
from .util import wsgify
try:
    import json
except ImportError:
    import simplejson as json

__all__ = [
 'Resource', 'Response', 'Request', 'Dispatch', 'errors']

def logger(cls):
    name = '%s.%s' % (__name__, cls.__class__.__name__)
    return logging.getLogger(name)


class Resource(object):
    prefix = ''
    methods = {'GET': 'get', 
       'POST': 'post', 
       'PUT': 'put', 
       'DELETE': 'delete', 
       'HEAD': 'head'}
    media = {}
    extensions = {}
    req = None
    params = {}

    @wsgify
    def __call__(self, req):
        """Route a request to an appropriate method of the resource, returning a response.

        *req* is a :class:`webob.Request` instance (either provided by the
        caller or created by the :class:`webob.dec.wsgify` decorator). This
        method will first check the request's HTTP method, mapping it to a local
        method name using :attr:`methods`. If the request's PATH_INFO ends with
        an extension registered in :attr:`extensions`, the extension's media
        type is used; otherwise, this method will try to match the request's
        Accept header against methods registered in :attr:`media`. If no method
        can be found, this method raises an exception from :module:`errors`.

        This method sets :attr:`req`, :attr:`req.response` and
        :attr:`req.content` before calling the matched method.

        For example, a request made with the GET method and an Accept header (or
        PATH_INFO file extension) that matches the "html" handler will be
        dispatched to a method on the :class:`Resource` named "get_html". These
        methods take no arguments; the :class:`webob.Request` instance is
        available in the :attr:`request` attribute.
        """
        log = logger(self)
        try:
            httpmethod = req.GET.pop(self.params['method'])
        except KeyError:
            httpmethod = req.method

        try:
            httpmethod = self.methods[httpmethod]
        except KeyError:
            e = errors.HTTPMethodNotAllowed("HTTP method '%s' is not supported" % req.method, headers={'Allow': (', ').join(self.methods.values())})
            raise e

        req.path_info_pop()
        (root, ext) = os.path.splitext(req.path_info)
        media = self.extensions.get(ext, None)
        try:
            content = req.GET.pop(self.params['content-type'])
        except KeyError:
            content = req.content_type

        content = Accept('Content-Type', content)
        if media is None:
            try:
                accept = Accept('Accept', req.GET.pop(self.params['accept']))
            except KeyError:
                accept = req.accept
            else:
                if not accept:
                    accept = content
        else:
            accept = Accept('Accept', media)
            req.path_info = root
        responsetype = accept.best_match(self.media)
        media = self.media.get(responsetype, None)
        methodname = '%s_%s' % (httpmethod, media)
        method = getattr(self, methodname, getattr(self, httpmethod, None))
        if not callable(method):
            e = errors.HTTPUnsupportedMediaType('Media type %s is not supported for method %s' % (
             media, req.method))
            raise e
        log.debug('Request PATH: %s', req.path)
        log.debug('Request PATH_INFO: %s', req.path_info)
        log.debug('Request HTTP method: %s', httpmethod)
        log.debug('Request Accept header: %s', accept)
        log.debug('Request Content-Type header: %s', content)
        log.debug('Handling request with method %s', methodname)
        if not hasattr(req, 'response'):
            req.response = Response()
        self.req = req
        self.response = req.response
        self.response.content_type = ''
        media = self.media.get(content.best_match(self.media), None)
        handlername = 'handle_%s' % media
        handler = getattr(self, handlername, None)
        if not hasattr(req, 'content'):
            if not callable(handler):
                handler = lambda : self.req.params
            req.content = handler()
        response = method()
        if response is None:
            response = self.response
        content = getattr(response, 'content_type', getattr(self, 'response.content_type', None))
        if not content:
            self.response.content_type = responsetype
        return response


class Dispatch(object):
    """A WSGI application that dispatches to other WSGI applications.

    Incoming requests are passed to registered :class:`Resource` subclasses.
    Resources can be registered by passing them as arguments on initialization
    or by adding them to :attr:`resources` later.
    """
    resources = []

    def __init__(self, *resources):
        self.resources = list(resources)

    @wsgify
    def __call__(self, req):
        """Dispatch the request to a registered resource.

        *req* is a :class:`webob.Request` instance (created if necessary by the
        :class:`webob.dec.wsgify` decorator). This method calls :meth:`match` to
        find a matching resource; if none is found, it raises
        :class:`errors.HTTPNotFound`. It then instantiates the matching :class:`Resource`
        subclass and calls it with the request.
        """
        log = logger(self)
        resource = self.match(req, self.resources)
        if resource is None:
            e = errors.HTTPNotFound('No resource matches the request')
            raise e
        response = None
        try:
            try:
                response = resource(req)
            except Exception, e:
                if isinstance(e, errors.HTTPException):
                    if e.status_int > 400:
                        log.exception('HTTP Exception at %s %s: %s', req.method, req.path_info, e)
                    response = e
                else:
                    log.exception('Server exception: %s', e)
                    response = errors.HTTPInternalServerError()

        finally:
            content_length = None
            status_int = 200
            if response is not None:
                content_length = response.content_length
                status_int = response.status_int
            log.info('%s - - %s "%s" %s %s %s %s', req.remote_addr, time.strftime('%Y-%m-%d %H:%M:%S %z'), req.__str__(skip_body=True).splitlines()[0], status_int, content_length, req.referer, req.user_agent)

        return response

    def match(self, req, resources):
        """Return the resource that matches *req*.

        *req* should be a :class:`webob.Request` instance; *resources* should be
        an iterable of :class:`Resource` subclasses. Returns None if no resource
        matches the request.

        A request matches if:
         
         * PATH_INFO ends in '/' and starts with the resource's
           :attr:`Resource.prefix` attribute; or
         * PATH_INFO is the same as the resource's :attr:`Resource.prefix`
           attribute.

        The first match wins.
        """
        resource = None
        for resource in resources:
            if resource.prefix.endswith('/'):
                matches = req.path_info.startswith(resource.prefix)
            else:
                matches = req.path_info == resource.prefix
            if matches:
                return resource

        return