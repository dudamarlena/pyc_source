# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/session.py
# Compiled at: 2016-08-31 16:32:16
import os, webapp2, contextlib
from webapp2_extras import sessions

class RequestHandler(webapp2.RequestHandler):
    """ Integrate webapp2's session handling features by default.
        This provides |RequestHandler.session|, deferring request
        dispatch into a context manager to handle session retrieval
        and storage after the request is processed.

    """

    def dispatch(self):
        with self.session_wrapper() as (_session):
            self.session = _session
            result = super(RequestHandler, self).dispatch()
            return result

    @property
    def application_id(self):
        return os.environ.get('APPLICATION_ID', None)

    @contextlib.contextmanager
    def session_wrapper(self, backend='datastore'):
        """ Context handling for HTTP sessions
            Usage:

                with self.session_wrapper() as _session:
                    _session['key'] = value

            This approach ensures that we save session state correctly.
        """
        assert backend in ('datastore', 'memcache', 'securecookie')
        session_store = None
        try:
            session_store = sessions.get_store(request=self.request)
            _session = session_store.get_session(backend=backend, name='_session')
            yield _session
        finally:
            if session_store is not None:
                session_store.save_sessions(self.response)

        return