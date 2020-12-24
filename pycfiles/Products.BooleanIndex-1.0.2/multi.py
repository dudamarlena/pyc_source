# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/auth/multi.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nAuthentication via Multiple Methods\n\nIn some environments, the choice of authentication method to be used\ndepends upon the environment and is not "fixed".  This middleware allows\nN authentication methods to be registered along with a goodness function\nwhich determines which method should be used. The following example\ndemonstrates how to use both form and digest authentication in a server\nstack; by default it uses form-based authentication unless\n``*authmeth=digest`` is specified as a query argument.\n\n>>> from paste.auth import form, cookie, digest, multi\n>>> from paste.wsgilib import dump_environ\n>>> from paste.httpserver import serve\n>>>\n>>> multi = multi.MultiHandler(dump_environ)\n>>> def authfunc(environ, realm, user):\n...     return digest.digest_password(realm, user, user)\n>>> multi.add_method(\'digest\', digest.middleware, "Test Realm", authfunc)\n>>> multi.set_query_argument(\'digest\')\n>>>\n>>> def authfunc(environ, username, password):\n...     return username == password\n>>> multi.add_method(\'form\', form.middleware, authfunc)\n>>> multi.set_default(\'form\')\n>>> serve(cookie.middleware(multi))\nserving on...\n\n'

class MultiHandler(object):
    """
    Multiple Authentication Handler

    This middleware provides two othogonal facilities:

      - a manner to register any number of authentication middlewares

      - a mechanism to register predicates which cause one of the
        registered middlewares to be used depending upon the request

    If none of the predicates returns True, then the application is
    invoked directly without middleware
    """

    def __init__(self, application):
        self.application = application
        self.default = application
        self.binding = {}
        self.predicate = []

    def add_method(self, name, factory, *args, **kwargs):
        self.binding[name] = factory(self.application, *args, **kwargs)

    def add_predicate(self, name, checker):
        self.predicate.append((checker, self.binding[name]))

    def set_default(self, name):
        """ set default authentication method """
        self.default = self.binding[name]

    def set_query_argument(self, name, key='*authmeth', value=None):
        """ choose authentication method based on a query argument """
        lookfor = '%s=%s' % (key, value or name)
        self.add_predicate(name, lambda environ: lookfor in environ.get('QUERY_STRING', ''))

    def __call__(self, environ, start_response):
        for (checker, binding) in self.predicate:
            if checker(environ):
                return binding(environ, start_response)

        return self.default(environ, start_response)


middleware = MultiHandler
__all__ = [
 'MultiHandler']
if '__main__' == __name__:
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)