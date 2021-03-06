# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/web/session.py
# Compiled at: 2020-04-16 16:21:25
# Size of source mod 2**32: 12834 bytes
"""
web2ldap.web.session - server-side web session handling

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import string, re, time, threading
from ldap0.pw import random_string
SESSION_ID_CHARS = string.ascii_letters + string.digits + '-._'
SESSION_CROSSCHECKVARS = ('REMOTE_ADDR', 'REMOTE_HOST', 'REMOTE_IDENT', 'REMOTE_USER',
                          'FORWARDED_FOR', 'HTTP_X_FORWARDED_FOR', 'HTTP_USER_AGENT',
                          'HTTP_ACCEPT_CHARSET', 'SSL_SESSION_ID', 'SSL_CLIENT_V_START',
                          'SSL_CLIENT_V_END', 'SSL_CLIENT_I_DN', 'SSL_CLIENT_IDN',
                          'SSL_CLIENT_S_DN', 'SSL_CLIENT_SDN', 'SSL_CLIENT_M_SERIAL',
                          'SSL_CLIENT_CERT_SERIAL')

class SessionException(Exception):
    __doc__ = 'Base class for session errors'

    def __init__(self, *args):
        self.args = args


class CorruptData(SessionException):
    __doc__ = 'Raised if data was corrupt, e.g. UnpicklingError occurred'

    def __str__(self):
        return 'Error during retrieving corrupted session data. Session deleted.'


class GenerateIDError(SessionException):
    __doc__ = 'Raised if generation of unique session ID failed.'

    def __init__(self, maxtry):
        self.maxtry = maxtry

    def __str__(self):
        return 'Could not create new session id. Tried %d times.' % self.maxtry


class SessionHijacked(SessionException):
    __doc__ = 'Raised if hijacking of session was detected.'

    def __init__(self, failed_vars):
        self.failed_vars = failed_vars

    def __str__(self):
        return 'Crosschecking of the following env vars failed: %s.' % self.failed_vars


class MaxSessionCountExceeded(SessionException):
    __doc__ = 'Raised if maximum number of sessions is exceeded.'

    def __init__(self, max_session_count):
        self.max_session_count = max_session_count

    def __str__(self):
        return 'Maximum number of sessions exceeded. Limit is %d.' % self.max_session_count


class MaxSessionPerIPExceeded(SessionException):
    __doc__ = 'Raised if maximum number of sessions is exceeded.'

    def __init__(self, remote_ip, max_session_count):
        self.remote_ip = remote_ip
        self.max_session_count = max_session_count

    def __str__(self):
        return 'Maximum number of sessions exceeded for %r. Limit is %d.' % (
         self.remote_ip,
         self.max_session_count)


class BadSessionId(SessionException):
    __doc__ = 'Raised if session ID not found in session dictionary.'

    def __init__(self, session_id):
        self.session_id = session_id

    def __str__(self):
        return 'No session with key %s.' % self.session_id


class InvalidSessionId(SessionException):
    __doc__ = 'Raised if session ID not found in session dictionary.'

    def __init__(self, session_id):
        self.session_id = session_id

    def __str__(self):
        return 'No session with key %s.' % self.session_id


class CleanUpThread(threading.Thread):
    __doc__ = '\n    Thread class for clean-up thread\n    '

    def __init__(self, sessionInstance, interval=60):
        self._sessionInstance = sessionInstance
        self._interval = interval
        self._stop_event = threading.Event()
        self._removed = 0
        threading.Thread.__init__(self, name=(self.__class__.__module__ + self.__class__.__name__))

    def run(self):
        """
        Thread function for cleaning up session database
        """
        while not self._stop_event.isSet():
            self._removed += self._sessionInstance.clean()
            self._stop_event.wait(self._interval)

    def __repr__(self):
        return '%s: %d sessions removed' % (
         self.getName(),
         self._removed)

    def join(self, timeout=0.0):
        self._stop_event.set()
        threading.Thread.join(self, timeout)


class WebSession:
    __doc__ = '\n    The session class which handles storing and retrieving of session data\n    in a dictionary-like sessiondict object.\n    '
    dict_class = dict

    def __init__(self, dictobj=None, session_ttl=0, crossCheckVars=None, maxSessionCount=None, sessionIDLength=12, sessionIDChars=None):
        """
        dictobj
            has to be a instance of a dictionary-like object
            (e.g. derived from UserDict or shelve)
        session_ttl
            Amount of time (secs) after which a session
            expires and the session data is silently deleted.
            A InvalidSessionId exception is raised in this case if
            the application tries to access the session ID again.
        crossCheckVars
            List of keys of variables cross-checked for each
            retrieval of session data in retrieveSession(). If None
            SESSION_CROSSCHECKVARS is used.
        maxSessionCount
            Maximum number of valid sessions. This affects
            behaviour of retrieveSession() which raises.
            None means unlimited number of sessions.
        sessionIDLength
            Exact integer length of the session ID generated
        sessionIDChars
            String containing the valid chars for session IDs
            (if this is zero-value the default is SESSION_ID_CHARS)
        """
        if dictobj is None:
            self.sessiondict = self.dict_class()
        else:
            self.sessiondict = dictobj
        self.session_ttl = session_ttl
        self._session_lock = threading.Lock()
        if crossCheckVars is None:
            crossCheckVars = SESSION_CROSSCHECKVARS
        self.crossCheckVars = crossCheckVars
        self.maxSessionCount = maxSessionCount
        self.sessionCounter = 0
        self.session_id_len = sessionIDLength
        self.session_id_chars = sessionIDChars or SESSION_ID_CHARS
        self.session_id_re = re.compile('^[%s]+$' % re.escape(self.session_id_chars))

    def _validateSessionIdFormat(self, session_id):
        """
        Validate the format of session_id. Implementation
        has to match IDs produced in method _generateSessionID()
        """
        if len(session_id) != self.session_id_len or self.session_id_re.match(session_id) is None:
            raise BadSessionId(session_id)

    @staticmethod
    def _crosscheckSessionEnv(stored_env, env):
        """
        Returns a list of keys of items which differ in
        stored_env and env.
        """
        return [skey for skey, sval in stored_env.items() if not skey not in env if sval != env[skey]]

    def _generateCrosscheckEnv--- This code section failed: ---

 L. 244         0  LOAD_CLOSURE             'env'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'WebSession._generateCrosscheckEnv.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L. 246        10  LOAD_FAST                'self'
               12  LOAD_ATTR                crossCheckVars

 L. 244        14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _generateSessionID(self, maxtry=1):
        """
        Generate a new random and unique session id string
        """
        newid = random_string(alphabet=SESSION_ID_CHARS, length=(self.session_id_len))
        tried = 0
        while newid in self.sessiondict:
            tried += 1
            if maxtry:
                if tried >= maxtry:
                    raise GenerateIDError(maxtry)
            newid = random_string(alphabet=SESSION_ID_CHARS, length=(self.session_id_len))

        return newid

    def save(self, session_id, session_data):
        """
        Store session_data under session_id.
        """
        assert isinstance(session_id, str), TypeError('Expected session_id to be str, got %r' % session_id)
        self._session_lock.acquire()
        try:
            self.sessiondict[session_id] = (time.time(), session_data)
        finally:
            self._session_lock.release()

        return session_id

    def delete(self, session_id):
        """
        Delete session_data referenced by session_id.
        """
        assert isinstance(session_id, str), TypeError('Expected session_id to be str, got %r' % session_id)
        self._session_lock.acquire()
        try:
            if session_id in self.sessiondict:
                del self.sessiondict[session_id]
            if '__session_checkvars__' + session_id in self.sessiondict:
                del self.sessiondict['__session_checkvars__' + session_id]
        finally:
            self._session_lock.release()

        return session_id

    def retrieveSession(self, session_id, env):
        """
        Retrieve session data
        """
        if not isinstance(session_id, str):
            raise AssertionError(TypeError('Expected session_id to be str, got %r' % session_id))
        else:
            self._validateSessionIdFormat(session_id)
            session_vars_key = '__session_checkvars__' + session_id
            if session_id not in self.sessiondict or session_vars_key not in self.sessiondict:
                raise InvalidSessionId(session_id)
            self._session_lock.acquire()
            try:
                session_checkvars = self.sessiondict[session_vars_key]
                timestamp, session_data = self.sessiondict[session_id]
            finally:
                self._session_lock.release()

            current_time = time.time()
            if self.session_ttl and current_time > timestamp + self.session_ttl:
                self.delete(session_id)
                raise InvalidSessionId(session_id)
        failed_vars = self._crosscheckSessionEnv(session_checkvars, env)
        if failed_vars:
            raise SessionHijacked(failed_vars)
        return session_data

    def new(self, env=None):
        """
        Store session data under session id
        """
        env = env or {}
        if self.maxSessionCount:
            if len(self.sessiondict) / 2 + 1 > self.maxSessionCount:
                raise MaxSessionCountExceeded(self.maxSessionCount)
        self._session_lock.acquire()
        try:
            session_id = self._generateSessionID(maxtry=3)
            self.sessiondict[session_id] = (
             time.time(), '_created_')
            self.sessiondict['__session_checkvars__' + session_id] = self._generateCrosscheckEnv(env)
            self.sessionCounter += 1
        finally:
            self._session_lock.release()

        return session_id

    def clean(self):
        """
        Search for expired session entries and delete them.

        Returns integer counter of deleted sessions as result.
        """
        current_time = time.time()
        result = 0
        for session_id in self.sessiondict.keys():
            if not session_id.startswith('__'):
                try:
                    session_timestamp = self.sessiondict[session_id][0]
                except InvalidSessionId:
                    self.delete(session_id)

                if session_timestamp + self.session_ttl < current_time:
                    self.delete(session_id)
                    result += 1
            return result