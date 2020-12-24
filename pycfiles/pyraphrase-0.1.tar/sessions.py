# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mareike/work/app/pyrap-dev/python3/pyrap/sessions.py
# Compiled at: 2017-12-06 07:44:47
__doc__ = '\nCreated on Oct 27, 2015\n\n@author: nyga\n'
import base64, datetime, json, re, os, io, urllib
from dnutils.threads import current_thread, Thread, ThreadInterrupt, sleep, SuspendableThread
import web, time
from dnutils import Lock, out, RLock, ifnone, logs
import dnutils
from web.session import sha1
from pyrap import threads
from web.utils import Storage
from web import utils
from pyrap.ptypes import Event
_defconf = utils.storage({'cookie_name': 'webpy_session_id', 
   'cookie_domain': None, 
   'timeout': 7200, 
   'ignore_expiry': True, 
   'ignore_change_ip': True, 
   'secret_key': 'fLjUfxqXtfNoIldA0A0J', 
   'expired_message': 'Session expired', 
   'httponly': True, 
   'secure': False})
_idregex = re.compile('^[0-9a-fA-F]+$')

class SessionKilled(Event):

    def _notify(self, listener, data):
        listener(data)


class InvalidSessionError(Exception):
    pass


class SessionError(Exception):
    pass


class PyRAPSession(object):
    """
    Session management for pyRAP.
    """

    def __init__(self, server=None, config=None):
        if server:
            server.add_processor(self._prepare_thread)
        self.__sessions = {}
        self.__locals = web.threadeddict()
        self._config = ifnone(config, _defconf)

    def _prepare_thread(self, handler):
        request = Storage()
        request.query = {str(k):str(v) for k, v in urllib.parse.parse_qsl(web.ctx.query[1:], keep_blank_values=True)}
        self.__locals['session_id'] = request.query.get('cid')
        try:
            return handler()
        finally:
            self._postprocess()

    def _postprocess(self):
        try:
            if self.client is not None:
                cookie = json.dumps(self.client.data)
                cookie = base64.b64encode(cookie.encode('utf8'))
                web.setcookie('pyrap', cookie.decode('ascii'), path='/%s' % self.app.config.path)
        except KeyError:
            pass

        return

    @property
    def __lock(self):
        return self.__sessiondata.lock

    def new(self):
        lock = RLock()
        with lock:
            sid = self.__generate_session_id()
            self.__locals['session_id'] = sid
            store = Storage()
            self.__sessions[sid] = store
            self.connect_client()
            store.lock = lock
            store.on_kill = SessionKilled()
            store.ip = web.ctx.ip
            store.expired = False
            store.threads = []
            store.ctime = datetime.datetime.now()
            store.atime = store.ctime

    @property
    def _threads(self):
        return self.__sessiondata.threads

    def fromid(self, sid):
        session = PyRAPSession()
        session.__locals = {'session_id': sid}
        session.__sessions = self.__sessions
        return session

    @property
    def __sessiondata(self):
        sid = self.__locals['session_id']
        if sid not in self.__sessions:
            raise SessionError()
        return self.__sessions[sid]

    def __generate_session_id(self):
        """Generate a random id for session"""
        while True:
            rand = os.urandom(16)
            now = time.time()
            secret_key = self._config.secret_key
            hashable = '%s%s%s%s' % (rand, now, utils.safestr(web.ctx.ip), secret_key)
            sid = sha1(hashable.encode('utf8'))
            sid = sid.hexdigest()
            if sid not in self.__sessions:
                break

        return sid

    def touch(self):
        self.__sessiondata.atime = datetime.datetime.now()

    @property
    def app(self):
        return self.__sessiondata.app

    @property
    def on_kill(self):
        return self.__sessiondata.on_kill

    @on_kill.setter
    def on_kill(self, e):
        if not isinstance(e, SessionKilled):
            raise ValueError('on_kill event cannot be set to value %s' % str(e))
        self.__sessiondata.on_kill = e

    @property
    def client(self):
        if self.id in self.__sessions:
            return self.__sessiondata.client
        else:
            return

    @property
    def ctime(self):
        return self.__sessiondata.ctime

    @property
    def atime(self):
        return self.__sessiondata.atime

    @atime.setter
    def atime(self, t):
        self.__sessiondata.atime = t

    @property
    def runtime(self):
        return self.__sessiondata.runtime

    @property
    def id(self):
        return self.__locals.get('session_id')

    @property
    def ip(self):
        return self.client.ip

    def check_validity(self):
        return PyRAPSession.check_id(self.id) and self.check_ip()

    @staticmethod
    def check_id(sid):
        return _idregex.match(sid)

    def check_ip(self):
        return self.client is None or self.ip == web.ctx.ip or self._config.ignore_change_ip

    @property
    def expired(self):
        conditions = self.id in self.__sessions and self.client is not None and not self.__sessiondata.expired
        if not conditions:
            return True
        else:
            if self.atime:
                now = datetime.datetime.now()
                return (now - self.atime).seconds > self._config.timeout
            return False

    def expire(self):
        """Expire the session, make it no longer available"""
        self.__sessiondata.expired = True

    def connect_client(self):
        """Connects the client to this session by storing a cooking with the session id."""
        client = Storage()
        client.ip = web.ctx.ip
        client.orig_ip = web.ctx.env.get('HTTP_X_FORWARDED_FOR', web.ctx.ip)
        client.useragent = web.ctx.env['HTTP_USER_AGENT']
        client.data = Storage()
        cookie = web.cookies().get('pyrap')
        if cookie is not None:
            cookie = base64.b64decode(cookie)
            cookie = json.loads(cookie.decode('utf8'))
            try:
                client.data = Storage(cookie)
            except (KeyError, AttributeError):
                pass

        self.__sessiondata.client = client
        return

    def disconnect_client(self):
        """Deletes from the client the cookie that holds the session id."""
        self.__sessiondata.client = None
        return

    def __str__(self):
        return '<Session id:%s ctime:%s>' % (self.id, self.ctime.strftime('%Y-%m-%d %H:%M:%S'))

    def __repr__(self):
        return str(self)


class SessionCleanupThread(SuspendableThread):

    def __init__(self, session):
        SuspendableThread.__init__(self, name='session_cleanup')
        self.session = session

    def run(self):
        try:
            logger = logs.getlogger('/pyrap/session_cleanup')
            logger.info('session cleanup thread running.')
            session = self.session
            while not dnutils.threads.interrupted():
                logger.debug(len(list(session._PyRAPSession__sessions.keys())), 'sessions active.')
                for sid in set(session._PyRAPSession__sessions.keys()):
                    session._PyRAPSession__locals['session_id'] = sid
                    with session._PyRAPSession__lock:
                        if session.expired:
                            logger.debug('killing session', session.id)
                            session.on_kill.notify(session)
                            for t in session._threads:
                                if isinstance(t, threads.SuspendableThread):
                                    t.interrupt()

                            for t in session._threads:
                                t.join()

                            del session._PyRAPSession__sessions[sid]

                sleep(2)

        except ThreadInterrupt:
            logger.info('session cleanup thread terminated.')