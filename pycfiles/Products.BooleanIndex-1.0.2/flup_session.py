# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/flup_session.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = "\nCreates a session object.\n\nIn your application, use::\n\n    environ['paste.flup_session_service'].session\n\nThis will return a dictionary.  The contents of this dictionary will\nbe saved to disk when the request is completed.  The session will be\ncreated when you first fetch the session dictionary, and a cookie will\nbe sent in that case.  There's current no way to use sessions without\ncookies, and there's no way to delete a session except to clear its\ndata.\n"
from paste import httpexceptions
from paste import wsgilib
import flup.middleware.session
flup_session = flup.middleware.session
store_cache = {}

class NoDefault(object):
    pass


class SessionMiddleware(object):
    session_classes = {'memory': (
                flup_session.MemorySessionStore,
                [
                 (
                  'session_timeout', 'timeout', int, 60)]), 
       'disk': (
              flup_session.DiskSessionStore,
              [
               (
                'session_timeout', 'timeout', int, 60),
               (
                'session_dir', 'storeDir', str, '/tmp/sessions')]), 
       'shelve': (
                flup_session.ShelveSessionStore,
                [
                 (
                  'session_timeout', 'timeout', int, 60),
                 (
                  'session_file', 'storeFile', str,
                  '/tmp/session.shelve')])}

    def __init__(self, app, global_conf=None, session_type=NoDefault, cookie_name=NoDefault, **store_config):
        self.application = app
        if session_type is NoDefault:
            session_type = global_conf.get('session_type', 'disk')
        self.session_type = session_type
        try:
            (self.store_class, self.store_args) = self.session_classes[self.session_type]
        except KeyError:
            raise KeyError('The session_type %s is unknown (I know about %s)' % (
             self.session_type,
             (', ').join(self.session_classes.keys())))

        kw = {}
        for (config_name, kw_name, coercer, default) in self.store_args:
            value = coercer(store_config.get(config_name, default))
            kw[kw_name] = value

        self.store = self.store_class(**kw)
        if cookie_name is NoDefault:
            cookie_name = global_conf.get('session_cookie', '_SID_')
        self.cookie_name = cookie_name

    def __call__(self, environ, start_response):
        service = flup_session.SessionService(self.store, environ, cookieName=self.cookie_name, fieldName=self.cookie_name)
        environ['paste.flup_session_service'] = service

        def cookie_start_response(status, headers, exc_info=None):
            service.addCookie(headers)
            return start_response(status, headers, exc_info)

        try:
            app_iter = self.application(environ, cookie_start_response)
        except httpexceptions.HTTPException, e:
            headers = (e.headers or {}).items()
            service.addCookie(headers)
            e.headers = dict(headers)
            service.close()
            raise
        except:
            service.close()
            raise

        return wsgilib.add_close(app_iter, service.close)


def make_session_middleware(app, global_conf, session_type=NoDefault, cookie_name=NoDefault, **store_config):
    """
    Wraps the application in a session-managing middleware.
    The session service can then be found in
    ``environ['paste.flup_session_service']``
    """
    return SessionMiddleware(app, global_conf=global_conf, session_type=session_type, cookie_name=cookie_name, **store_config)