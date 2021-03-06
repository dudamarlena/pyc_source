# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tests/test_urlrelay.py
# Compiled at: 2009-01-14 21:28:13
"""Unit tests for urlrelay."""
import urlrelay, unittest

def dummy_sr(status, headers, exc_info=None):
    pass


@urlrelay.url('^/$')
def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['index']


@urlrelay.url('^/handle$', 'GET')
def get_handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['GET']


@urlrelay.url('^/handle$', 'POST')
def post_handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['POST']


@urlrelay.url('^/handle$', 'PUT')
def put_handle(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['PUT']


@urlrelay.url('^/argtest/(?P<kwarg1>\\w+)/(?P<kwarg2>\\w+)/(\\w+)/(\\w+)$')
def argtests(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    (args, kw) = environ['wsgiorg.routing_args']
    return [(' ').join([args[0], args[1], kw['kwarg1'], kw['kwarg2']])]


@urlrelay.url('^/methtest/(?P<kwarg1>\\w+)/(?P<kwarg2>\\w+)/(\\w+)/(\\w+)$', 'GET')
def meth_get(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    (args, kw) = environ['wsgiorg.routing_args']
    return [(' ').join(['GET', args[0], args[1], kw['kwarg1'], kw['kwarg2']])]


@urlrelay.url('^/methtest/(?P<kwarg1>\\w+)/(?P<kwarg2>\\w+)/(\\w+)/(\\w+)$', 'POST')
def meth_post2(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    (args, kw) = environ['wsgiorg.routing_args']
    return [(' ').join(['POST', args[0], args[1], kw['kwarg1'], kw['kwarg2']])]


@urlrelay.url('^/methtest/(?P<kwarg1>\\w+)/(?P<kwarg2>\\w+)/(\\w+)/(\\w+)$', 'PUT')
def meth_put(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    (args, kw) = environ['wsgiorg.routing_args']
    return [(' ').join(['PUT', args[0], args[1], kw['kwarg1'], kw['kwarg2']])]


@urlrelay.url('/spectest/', 'POST')
def meth_post(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Empty post']


@urlrelay.url('/spectest/(.*)', 'GET')
def meth_get2(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    (args, kw) = environ['wsgiorg.routing_args']
    return [(' ').join(['GET', args[0]])]


urlrelay.register('^/notfound$', 'urlrelay._handler')
urlrelay.register('^/notfound2$', 'urlrelay._handler', 'GET')
urlrelay.register('^/notfound2$', 'urlrelay._handler', 'PUT')
urlrelay.register('^/notfound2$', 'urlrelay._handler', 'POST')
urlrelay.register('^/notfound4$', '_handler')
urlrelay.register('^/notfound3$', '_handler', 'GET')
urlrelay.register('^/notfound3$', '_handler', 'PUT')
urlrelay.register('^/notfound3$', '_handler', 'POST')

class UrlRelayTest(unittest.TestCase):

    def test_inmem_root(self):
        """Checks simple url."""
        environ = {'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'index')

    def test_inmem_method_get(self):
        """Checks url + get method."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'GET')

    def test_inmem_method_post(self):
        """Checks url + post method."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'POST'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'POST')

    def test_inmem_method_put(self):
        """Checks url + put method."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'PUT'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'PUT')

    def test_inmem_argextract(self):
        """Checks arg/kwarg extraction from URL."""
        environ = {'PATH_INFO': '/argtest/kwarg1/kwarg2/arg1/arg2', 
           'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'arg1 arg2 kwarg1 kwarg2')

    def test_inmem_method_extract_get(self):
        """Checks arg/kwarg extraction from URL + get method."""
        environ = {'PATH_INFO': '/methtest/kwarg1/kwarg2/arg1/arg2', 
           'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'GET arg1 arg2 kwarg1 kwarg2')

    def test_inmem_method_extract_post(self):
        """Checks arg/kwarg extraction from URL + post method."""
        environ = {'PATH_INFO': '/methtest/kwarg1/kwarg2/arg1/arg2', 
           'REQUEST_METHOD': 'POST'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'POST arg1 arg2 kwarg1 kwarg2')

    def test_inmem_method_extract_put(self):
        """Checks arg/kwarg extraction from URL + put method."""
        environ = {'PATH_INFO': '/methtest/kwarg1/kwarg2/arg1/arg2', 
           'REQUEST_METHOD': 'PUT'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'PUT arg1 arg2 kwarg1 kwarg2')

    def test_offdisk_method(self):
        """Checks loading handler off of a disk."""
        environ = {'PATH_INFO': '/notfound', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_get(self):
        """Checks loading handler off of a disk + get method."""
        environ = {'PATH_INFO': '/notfound2', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_put(self):
        """Checks loading handler off of a disk + put method."""
        environ = {'PATH_INFO': '/notfound2', 'REQUEST_METHOD': 'PUT'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_post(self):
        """Checks loading handler off of a disk + post method."""
        environ = {'PATH_INFO': '/notfound2', 'REQUEST_METHOD': 'POST'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_modpath(self):
        """Checks loading handler off of a disk."""
        environ = {'PATH_INFO': '/notfound4', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(modpath='urlrelay')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_get_modpath(self):
        """Checks loading handler off of a disk + get method."""
        environ = {'PATH_INFO': '/notfound3', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(modpath='urlrelay')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_put_modpath(self):
        """Checks loading handler off of a disk + put method."""
        environ = {'PATH_INFO': '/notfound3', 'REQUEST_METHOD': 'PUT'}
        result = urlrelay.URLRelay(modpath='urlrelay')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_offdisk_method_post_modpath(self):
        """Checks loading handler off of a disk + post method."""
        environ = {'PATH_INFO': '/notfound3', 'REQUEST_METHOD': 'POST'}
        result = urlrelay.URLRelay(modpath='urlrelay')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_inmem_defaultapp(self):
        """Checks using default app url."""
        environ = {'PATH_INFO': '/plt', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(default=index)(environ, dummy_sr)
        self.assertEqual(result[0], 'index')

    def test_inmem_defaultapp2(self):
        """Checks using default app url."""
        environ = {'PATH_INFO': '/plt', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(default=index)(environ, dummy_sr)
        self.assertEqual(result[0], 'index')

    def test_ondisk_defaultapp(self):
        """Checks arg/kwarg extraction from URL + put method."""
        environ = {'PATH_INFO': '/methkwarg1', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(default='urlrelay._handler')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_ondisk_defaultapp_modpath(self):
        """Checks arg/kwarg extraction from URL + put method."""
        environ = {'PATH_INFO': '/methkwarg1', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(default='_handler', modpath='urlrelay')(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_handler_override(self):
        """Checks overriding the default 404 handler."""

        def handle(environ, start_response):
            start_response('404 Not Found', [('content-type', 'text/plain')])
            return ['404']

        environ = {'PATH_INFO': '/methkwarg1', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay(handler=handle)(environ, dummy_sr)
        self.assertEqual(result[0], '404')

    def test_notfound(self):
        """Checks that default 404 handler responds."""
        environ = {'PATH_INFO': '/methkwarg1', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEqual(result[0], 'Requested URL was not found on this server.')

    def test_nonregistry_paths_index(self):
        """Checks use of non-global path registry."""
        environ = {'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}
        tpaths = (
         (
          '^/$', index),
         (
          '^/handle$',
          {'GET': get_handle, 
             'POST': post_handle, 'PUT': put_handle}))
        result = urlrelay.URLRelay(paths=tpaths)(environ, dummy_sr)
        self.assertEqual(result[0], 'index')

    def test_nonregistry_paths_get(self):
        """Checks use of non-global path registry."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'GET'}
        tpaths = (
         (
          '^/$', index),
         (
          '^/handle$',
          {'GET': get_handle, 
             'POST': post_handle, 'PUT': put_handle}))
        result = urlrelay.URLRelay(paths=tpaths)(environ, dummy_sr)
        self.assertEqual(result[0], 'GET')

    def test_nonregistry_paths_post(self):
        """Checks use of non-global path registry."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'POST'}
        tpaths = (
         (
          '^/$', index),
         (
          '^/handle$',
          {'GET': get_handle, 
             'POST': post_handle, 'PUT': put_handle}))
        result = urlrelay.URLRelay(paths=tpaths)(environ, dummy_sr)
        self.assertEqual(result[0], 'POST')

    def test_nonregistry_paths_put(self):
        """Checks use of non-global path registry."""
        environ = {'PATH_INFO': '/handle', 'REQUEST_METHOD': 'PUT'}
        tpaths = (
         (
          '^/$', index),
         (
          '^/handle$',
          {'GET': get_handle, 
             'POST': post_handle, 'PUT': put_handle}))
        result = urlrelay.URLRelay(paths=tpaths)(environ, dummy_sr)
        self.assertEqual(result[0], 'PUT')

    def test_noncallable_in_registry(self):
        """Checks that non-callables or module strings are not allowed in
        non-global path registry."""
        environ = {'PATH_INFO': '/', 'REQUEST_METHOD': 'PUT'}

        def tempfunc():
            test = urlrelay.URLRelay(paths=(('^/$', []),))
            test(environ, dummy_sr)

        self.assertRaises(AssertionError, tempfunc)

    def test_call_more_specific(self):
        """Checks calling a more-specific URL than one that has a method
        associated with it."""
        environ = {'PATH_INFO': '/spectest/foo', 'REQUEST_METHOD': 'GET'}
        result = urlrelay.URLRelay()(environ, dummy_sr)
        self.assertEquals('GET foo', result[0])


if __name__ == '__main__':
    unittest.main()