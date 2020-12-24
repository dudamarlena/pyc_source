# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/logic/http/cookies.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  HTTP cookie logic\n  ~~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import json
from canteen.base import logic
from canteen.core import runtime
from canteen.util import decorators
from ..session import SessionEngine
with runtime.Library('werkzeug', strict=True) as (library, werkzeug):
    securecookie = library.load('contrib.securecookie')

    @decorators.bind('http.cookies')
    class Cookies(logic.Logic):
        """  """
        __modes__ = {}

        @classmethod
        def add_mode(cls, name):
            """  """

            def _mode_adder(mode_klass):
                """  """
                cls.__modes__[name] = mode_klass
                cls.__default__ = cls.__modes__[name]
                return mode_klass

            return _mode_adder

        @classmethod
        def get_mode(cls, name):
            """  """
            if name in cls.__modes__:
                return cls.__modes__[name]
            return cls.__default__

        @SessionEngine.configure('cookies')
        class CookieSessions(SessionEngine):
            """  """

            def load(self, request, http):
                """  """
                if self.config.get('key', 'canteen') in request.cookies:
                    _serializer = Cookies.get_mode(self.config.get('mode', 'json'))
                    session = _serializer.unserialize(*(
                     request.cookies[self.config.get('key', 'canteen')], self.api.secret))
                    if not session.new:
                        return request.set_session(session, self)
                return request.set_session(None, self)

            def commit(self, request, response, session):
                """  """
                _serializer, _key = Cookies.get_mode(self.config.get('mode', 'json')), self.config.get('key', 'canteen')
                serialized = _serializer({'uuid': session.id}, self.api.secret).serialize()
                if _key in request.cookies and request.cookies[_key] == serialized:
                    return
                else:
                    _params = {}
                    if 'max_age' not in self.config:
                        if 'expires' not in self.config:
                            _params['max_age'] = None
                        else:
                            _params['expires'] = self.config['expires']
                    else:
                        _params['max_age'] = self.config['max_age']
                    _params.update({'path': self.config.get('path', '/'), 
                       'secure': self.config.get('secure', False), 
                       'domain': self.config.get('domain', request.host.split(':')[0]), 
                       'httponly': self.config.get('http_only', self.config.get('httponly', False))})
                    response.set_cookie(_key, serialized, **_params)
                    return


    @Cookies.add_mode('json')
    class JSONCookie(securecookie.SecureCookie):
        """  """

        class CookieSerializer(json.JSONEncoder):
            """  """

            @classmethod
            def dumps(cls, structure):
                """  """
                return cls().encode(structure)

            @classmethod
            def loads(cls, serialized):
                """  """
                return json.loads(serialized)

            def default(self, obj):
                """  """
                if isinstance(obj, Exception):
                    if hasattr(obj, 'message'):
                        return obj.message
                return json.JSONEncoder.default(self, obj)

        serialization_method = CookieSerializer


    with runtime.Library('flask') as (flib, flask):
        flask_sessions = flib.load('sessions')

        class FlaskSessionBridge(JSONCookie, flask_sessions.SessionMixin):
            """  """


        flask_sessions.SecureCookieSessionInterface.session_class = FlaskSessionBridge