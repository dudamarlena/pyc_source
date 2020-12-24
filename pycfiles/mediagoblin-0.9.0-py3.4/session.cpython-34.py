# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/session.py
# Compiled at: 2014-01-02 16:06:37
# Size of source mod 2**32: 2493 bytes
import itsdangerous, logging
from mediagoblin.tools import crypto
_log = logging.getLogger(__name__)
MAX_AGE = 2592000

class Session(dict):

    def __init__(self, *args, **kwargs):
        self.send_new_cookie = False
        dict.__init__(self, *args, **kwargs)

    def save(self):
        self.send_new_cookie = True

    def is_updated(self):
        return self.send_new_cookie

    def delete(self):
        self.clear()
        self.save()


class SessionManager(object):

    def __init__(self, cookie_name='MGSession', namespace=None):
        if namespace is None:
            namespace = cookie_name
        self.signer = crypto.get_timed_signer_url(namespace)
        self.cookie_name = cookie_name

    def load_session_from_cookie(self, request):
        cookie = request.cookies.get(self.cookie_name)
        if not cookie:
            return Session()
        try:
            return Session(self.signer.loads(cookie))
        except itsdangerous.BadData:
            return Session()

    def save_session_to_cookie(self, session, request, response):
        if not session.is_updated():
            return
        if not session:
            response.delete_cookie(self.cookie_name)
        else:
            if session.get('stay_logged_in', False):
                max_age = MAX_AGE
            else:
                max_age = None
            response.set_cookie(self.cookie_name, self.signer.dumps(session), max_age=max_age, httponly=True)