# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/middleware/session.py
# Compiled at: 2016-02-16 00:41:00
"""
session中间件,支持disk，进程内缓存cache,memcache
sessioin过期策略分为三种情形：
1.固定时间过期，例如10天内没有访问则过期，timeout=xxx
    *cookie策略：每次访问时设置cookie为过期时间
    *缓存策略：每次访问设置缓存失效时间为固定过期时间
2.会话过期，关闭浏览器即过期timeout=0
    *cookie策略：岁浏览器关闭而过期
    *缓存策略：设置缓存失效期为1天，每次访问更新失效期，如果浏览器关闭，则一天后被清除

3.永不过期(记住我)
    *cookie策略：timeout1年
    *缓存策略：1年
"""
import os, time, re
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new

from torngas.storage import storage
from torngas.utils import safestr
from torngas.settings_manager import settings
from torngas.cache import caches
rx = re.compile('^[0-9a-fA-F]+$')

class SessionMiddleware(object):
    _cachestore = None
    session = None

    def process_init(self, application):
        self._cachestore = caches[settings.SESSION.session_cache_alias]

    def process_request(self, handler, clear):
        session = SessionManager(handler, self._cachestore, settings.SESSION)
        session.load_session()
        handler.session = session

    def process_response(self, handler, clear, chunk):
        if hasattr(handler, 'session'):
            handler.session.save()
            del handler.session


_DAY1 = 86400
_DAY30 = _DAY1 * 30
session_parameters = storage({'session_name': '__TORNADOSSID', 
   'cookie_domain': None, 
   'cookie_path': '/', 
   'expires': 0, 
   'ignore_change_ip': False, 
   'httponly': True, 
   'secure': False, 
   'secret_key': 'fLjUfxqXtfNoIldA0A0J', 
   'session_version': ''})

class SessionManager(object):
    _killed = False

    def __init__(self, handler, store, config=None):
        self._get_cookie = handler.get_cookie
        self._set_cookie = handler.set_cookie
        self.remote_ip = handler.request.remote_ip
        self.store = store
        self.config = storage(session_parameters)
        if config:
            self.config.update(config)
        self._data = {}

    def __contains__(self, key):
        return key in self._data

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __delitem__(self, key):
        del self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def load_session(self):
        u"""
        加载session
        :return:
        """
        self.sessionid = self._get_cookie(self.config.session_name)
        if self.sessionid and not self._valid_session_id(self.sessionid):
            self.expired()
        if self.sessionid:
            if self.sessionid in self.store:
                expires, _data = self.store.get(self.sessionid)
                self._data.update(_data)
                self.config.expires = expires
            self._validate_ip()
        if not self.sessionid:
            self.sessionid = self._create_sessionid()
        self._data['remote_ip'] = self.remote_ip

    def save(self):
        if not self._killed:
            httponly = self.config.httponly
            secure = self.config.secure
            expires = self.config.expires
            cache_expires = expires
            if expires == 0:
                cache_expires = _DAY1
            if not secure:
                secure = ''
            if not httponly:
                httponly = ''
            set_expire = 0 if expires == 0 else time.time() + expires
            self._set_cookie(self.config.session_name, self.sessionid, domain=self.config.cookie_domain or '', expires=set_expire, path=self.config.cookie_path, secure=secure, httponly=httponly)
            self.store.set(self.sessionid, (expires, self._data), cache_expires)
        else:
            self._set_cookie(self.config.session_name, self.sessionid, expires=-1)
            self.store.delete(self.sessionid)
            self.sessionid = None
            self._killed = False
        return

    def _valid_session_id(self, session_id):
        u"""
        验证sessionid格式
        :return:bool
        """
        if session_id:
            sess = session_id.split('|')
            if len(sess) > 1:
                return rx.match(sess[0]) and sess[1] == self.config.session_version

    def expired(self):
        u"""
        强制过期
        :return:None
        """
        self._killed = True
        self.save()

    def _create_sessionid(self):
        rand = os.urandom(16)
        now = time.time()
        secret_key = self.config.secret_key
        session_id = sha1('%s%s%s%s' % (rand, now, safestr(self.remote_ip), secret_key))
        session_id = session_id.hexdigest()
        return str(session_id).upper() + '|' + self.config.session_version

    def _validate_ip(self):
        if self.sessionid and self._data.get('remote_ip', None) != self.remote_ip:
            if not self.config.ignore_change_ip:
                return self.expired()
        return

    def set_expire(self, expires):
        self.config.expires = expires
        self.save()