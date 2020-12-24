# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/sessions.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 14527 bytes
"""
    flask.sessions
    ~~~~~~~~~~~~~~

    Implements cookie based sessions based on itsdangerous.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import uuid, hashlib
from base64 import b64encode, b64decode
from datetime import datetime
from werkzeug.http import http_date, parse_date
from werkzeug.datastructures import CallbackDict
from . import Markup, json
from ._compat import iteritems, text_type
from itsdangerous import URLSafeTimedSerializer, BadSignature

def total_seconds(td):
    return td.days * 60 * 60 * 24 + td.seconds


class SessionMixin(object):
    __doc__ = 'Expands a basic dictionary with an accessors that are expected\n    by Flask extensions and users for the session.\n    '

    def _get_permanent(self):
        return self.get('_permanent', False)

    def _set_permanent(self, value):
        self['_permanent'] = bool(value)

    permanent = property(_get_permanent, _set_permanent)
    del _get_permanent
    del _set_permanent
    new = False
    modified = True


class TaggedJSONSerializer(object):
    __doc__ = 'A customized JSON serializer that supports a few extra types that\n    we take for granted when serializing (tuples, markup objects, datetime).\n    '

    def dumps(self, value):

        def _tag(value):
            if isinstance(value, tuple):
                return {' t': [_tag(x) for x in value]}
            else:
                if isinstance(value, uuid.UUID):
                    return {' u': value.hex}
                else:
                    if isinstance(value, bytes):
                        return {' b': b64encode(value).decode('ascii')}
                    else:
                        if callable(getattr(value, '__html__', None)):
                            return {' m': text_type(value.__html__())}
                        if isinstance(value, list):
                            return [_tag(x) for x in value]
                        if isinstance(value, datetime):
                            pass
                        return {' d': http_date(value)}
                    if isinstance(value, dict):
                        pass
                    return dict((k, _tag(v)) for k, v in iteritems(value))
                if isinstance(value, str):
                    try:
                        return text_type(value)
                    except UnicodeError:
                        raise UnexpectedUnicodeError('A byte string with non-ASCII data was passed to the session system which can only store unicode strings.  Consider base64 encoding your string (String was %r)' % value)

                return value

        return json.dumps(_tag(value), separators=(',', ':'))

    def loads(self, value):

        def object_hook(obj):
            if len(obj) != 1:
                return obj
            else:
                the_key, the_value = next(iteritems(obj))
                if the_key == ' t':
                    return tuple(the_value)
                else:
                    if the_key == ' u':
                        return uuid.UUID(the_value)
                    if the_key == ' b':
                        return b64decode(the_value)
                    if the_key == ' m':
                        pass
                    return Markup(the_value)
                if the_key == ' d':
                    pass
                return parse_date(the_value)
            return obj

        return json.loads(value, object_hook=object_hook)


session_json_serializer = TaggedJSONSerializer()

class SecureCookieSession(CallbackDict, SessionMixin):
    __doc__ = 'Baseclass for sessions based on signed cookies.'

    def __init__(self, initial=None):

        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.modified = False


class NullSession(SecureCookieSession):
    __doc__ = 'Class used to generate nicer error messages if sessions are not\n    available.  Will still allow read-only access to the empty session\n    but fail on setting.\n    '

    def _fail(self, *args, **kwargs):
        raise RuntimeError('the session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.')

    __setitem__ = __delitem__ = clear = pop = popitem = update = setdefault = _fail
    del _fail


class SessionInterface(object):
    __doc__ = "The basic interface you have to implement in order to replace the\n    default session interface which uses werkzeug's securecookie\n    implementation.  The only methods you have to implement are\n    :meth:`open_session` and :meth:`save_session`, the others have\n    useful defaults which you don't need to change.\n\n    The session object returned by the :meth:`open_session` method has to\n    provide a dictionary like interface plus the properties and methods\n    from the :class:`SessionMixin`.  We recommend just subclassing a dict\n    and adding that mixin::\n\n        class Session(dict, SessionMixin):\n            pass\n\n    If :meth:`open_session` returns `None` Flask will call into\n    :meth:`make_null_session` to create a session that acts as replacement\n    if the session support cannot work because some requirement is not\n    fulfilled.  The default :class:`NullSession` class that is created\n    will complain that the secret key was not set.\n\n    To replace the session interface on an application all you have to do\n    is to assign :attr:`flask.Flask.session_interface`::\n\n        app = Flask(__name__)\n        app.session_interface = MySessionInterface()\n\n    .. versionadded:: 0.8\n    "
    null_session_class = NullSession
    pickle_based = False

    def make_null_session(self, app):
        """Creates a null session which acts as a replacement object if the
        real session support could not be loaded due to a configuration
        error.  This mainly aids the user experience because the job of the
        null session is to still support lookup without complaining but
        modifications are answered with a helpful error message of what
        failed.

        This creates an instance of :attr:`null_session_class` by default.
        """
        return self.null_session_class()

    def is_null_session(self, obj):
        """Checks if a given object is a null session.  Null sessions are
        not asked to be saved.

        This checks if the object is an instance of :attr:`null_session_class`
        by default.
        """
        return isinstance(obj, self.null_session_class)

    def get_cookie_domain(self, app):
        """Helpful helper method that returns the cookie domain that should
        be used for the session cookie if session cookies are used.
        """
        if app.config['SESSION_COOKIE_DOMAIN'] is not None:
            return app.config['SESSION_COOKIE_DOMAIN']
        else:
            if app.config['SERVER_NAME'] is not None:
                rv = '.' + app.config['SERVER_NAME'].rsplit(':', 1)[0]
                if rv == '.localhost':
                    rv = None
                if rv is not None:
                    path = self.get_cookie_path(app)
                    if path != '/':
                        rv = rv.lstrip('.')
                return rv
            return

    def get_cookie_path(self, app):
        """Returns the path for which the cookie should be valid.  The
        default implementation uses the value from the SESSION_COOKIE_PATH``
        config var if it's set, and falls back to ``APPLICATION_ROOT`` or
        uses ``/`` if it's `None`.
        """
        return app.config['SESSION_COOKIE_PATH'] or app.config['APPLICATION_ROOT'] or '/'

    def get_cookie_httponly(self, app):
        """Returns True if the session cookie should be httponly.  This
        currently just returns the value of the ``SESSION_COOKIE_HTTPONLY``
        config var.
        """
        return app.config['SESSION_COOKIE_HTTPONLY']

    def get_cookie_secure(self, app):
        """Returns True if the cookie should be secure.  This currently
        just returns the value of the ``SESSION_COOKIE_SECURE`` setting.
        """
        return app.config['SESSION_COOKIE_SECURE']

    def get_expiration_time(self, app, session):
        """A helper method that returns an expiration date for the session
        or `None` if the session is linked to the browser session.  The
        default implementation returns now + the permanent session
        lifetime configured on the application.
        """
        if session.permanent:
            return datetime.utcnow() + app.permanent_session_lifetime

    def should_set_cookie(self, app, session):
        """Indicates weather a cookie should be set now or not.  This is
        used by session backends to figure out if they should emit a
        set-cookie header or not.  The default behavior is controlled by
        the ``SESSION_REFRESH_EACH_REQUEST`` config variable.  If
        it's set to `False` then a cookie is only set if the session is
        modified, if set to `True` it's always set if the session is
        permanent.

        This check is usually skipped if sessions get deleted.

        .. versionadded:: 1.0
        """
        if session.modified:
            return True
        save_each = app.config['SESSION_REFRESH_EACH_REQUEST']
        return save_each and session.permanent

    def open_session(self, app, request):
        """This method has to be implemented and must either return `None`
        in case the loading failed because of a configuration error or an
        instance of a session object which implements a dictionary like
        interface + the methods and attributes on :class:`SessionMixin`.
        """
        raise NotImplementedError()

    def save_session(self, app, session, response):
        """This is called for actual sessions returned by :meth:`open_session`
        at the end of the request.  This is still called during a request
        context so if you absolutely need access to the request you can do
        that.
        """
        raise NotImplementedError()


class SecureCookieSessionInterface(SessionInterface):
    __doc__ = 'The default session interface that stores sessions in signed cookies\n    through the :mod:`itsdangerous` module.\n    '
    salt = 'cookie-session'
    digest_method = staticmethod(hashlib.sha1)
    key_derivation = 'hmac'
    serializer = session_json_serializer
    session_class = SecureCookieSession

    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        else:
            signer_kwargs = dict(key_derivation=self.key_derivation, digest_method=self.digest_method)
            return URLSafeTimedSerializer(app.secret_key, salt=self.salt, serializer=self.serializer, signer_kwargs=signer_kwargs)

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return
        else:
            val = request.cookies.get(app.session_cookie_name)
            if not val:
                return self.session_class()
            max_age = total_seconds(app.permanent_session_lifetime)
            try:
                data = s.loads(val, max_age=max_age)
                return self.session_class(data)
            except BadSignature:
                return self.session_class()

            return

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return
        if not self.should_set_cookie(app, session):
            return
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val, expires=expires, httponly=httponly, domain=domain, path=path, secure=secure)


from flask.debughelpers import UnexpectedUnicodeError