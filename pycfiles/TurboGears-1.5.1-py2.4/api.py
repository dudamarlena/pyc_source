# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\visit\api.py
# Compiled at: 2011-11-20 05:32:13
"""Base API of the TurboGears Visit Framework."""
__all__ = [
 'BaseVisitManager', 'Visit', 'VisitTool', 'create_extension_model', 'current', 'enable_visit_plugin', 'disable_visit_plugin', 'set_current', 'start_extension', 'shutdown_extension']
import logging
try:
    from hashlib import sha1
except ImportError:
    from sha import new as sha1

import threading, time
from Cookie import Morsel
from random import random
from datetime import timedelta, datetime
import cherrypy, pkg_resources
from turbogears import config
from turbogears.util import load_class
log = logging.getLogger('turbogears.visit')
_manager = None
_plugins = list()

def current():
    """Retrieve the current visit record from the CherryPy request."""
    return getattr(cherrypy.request, 'tg_visit', None)


def set_current(visit):
    """Set the current visit record on the CherryPy request being processed."""
    cherrypy.request.tg_visit = visit


def _create_visit_manager(timeout):
    """Create a VisitManager based on the plugin specified in the config file."""
    plugin_name = config.get('visit.manager', 'sqlalchemy')
    plugins = pkg_resources.iter_entry_points('turbogears.visit.manager', plugin_name)
    log.info('Loading visit manager from plugin: %s', plugin_name)
    provider_class = None
    for entrypoint in plugins:
        try:
            provider_class = entrypoint.load()
            break
        except ImportError, e:
            log.error("Error loading visit plugin '%s': %s", entrypoint, e)

    if not provider_class and '.' in plugin_name:
        try:
            provider_class = load_class(plugin_name)
        except ImportError, e:
            log.error("Error loading visit class '%s': %s", plugin_name, e)

    if not provider_class:
        raise RuntimeError('VisitManager plugin missing: %s' % plugin_name)
    return provider_class(timeout)


def start_extension():
    global _manager
    if not config.get('visit.on', False):
        return
    if _manager:
        log.warning('Visit manager already running.')
        return
    timeout = timedelta(minutes=config.get('visit.timeout', 20))
    _manager = _create_visit_manager(timeout)


def shutdown_extension():
    global _manager
    if not _manager:
        return
    _manager.shutdown()
    _manager = None
    return


def create_extension_model():
    """Create the data model of the VisitManager if one exists."""
    if _manager:
        _manager.create_model()


def enable_visit_plugin(plugin):
    """Register a visit tracking plugin.

    These plugins will be called for each request.

    """
    _plugins.append(plugin)


def disable_visit_plugin(plugin):
    """Unregister a visit tracking plugin."""
    _plugins[:] = [ p for p in _plugins if p is not plugin ]


class Visit(object):
    """Basic container for visit related data."""
    __module__ = __name__

    def __init__(self, key, is_new):
        self.key = key
        self.is_new = is_new


class VisitTool(object):
    """A tool that automatically tracks visitors."""
    __module__ = __name__

    def __init__(self):
        log.info('Visit tool initialized.')

    def __call__(self, **kw):
        """Check whether submitted request belongs to an existing visit."""
        get = kw.get
        source = [ s.strip().lower() for s in kw.get('source', 'cookie').split(',') ]
        if set(source).difference(('cookie', 'form')):
            log.error('Unsupported visit.source in configuration.')
        self.cookie_name = get('cookie.name', 'tg-visit')
        if Morsel().isReservedKey(self.cookie_name):
            log.error('Reserved name chosen as visit.cookie.name.')
        visit_key_param = get('form.name', 'tg_visit')
        self.cookie_path = get('cookie.path', '/')
        self.cookie_secure = get('cookie.secure', False)
        self.cookie_domain = get('cookie.domain', None)
        if self.cookie_domain == 'localhost':
            log.error("Invalid value 'localhost' for visit.cookie.domain. Try None instead.")
        self.cookie_max_age = get('cookie.permanent', False) and int(get('timeout', '20')) * 60 or None
        self.cookie_httponly = get('visit.cookie.httponly', False)
        if self.cookie_httponly:
            if not Morsel().isReservedKey('httponly'):
                log.error('The visit.cookie.httponly setting is not supported by this Python version.')
                self.cookie_httponly = False
            log.debug('Visit tool configured.')
            visit = current()
            visit_key = visit or None
            for source in source:
                if source == 'cookie':
                    visit_key = cherrypy.request.cookie.get(self.cookie_name)
                    if visit_key:
                        visit_key = visit_key.value
                        log.debug("Retrieved visit key '%s' from cookie '%s'.", visit_key, self.cookie_name)
                elif source == 'form':
                    visit_key = cherrypy.request.params.pop(visit_key_param, None)
                    log.debug("Retrieved visit key '%s' from request param '%s'.", visit_key, visit_key_param)
                if visit_key:
                    visit = _manager.visit_for_key(visit_key)
                    break

            if visit:
                log.debug('Using visit from request with key: %s', visit_key)
            else:
                visit_key = self._generate_key()
                visit = _manager.new_visit_with_key(visit_key)
                log.debug('Created new visit with key: %s', visit_key)
            self.send_cookie(visit_key)
            set_current(visit)
        try:
            for plugin in _plugins:
                plugin.record_request(visit)

        except cherrypy.InternalRedirect, e:
            cherrypy.request.path_info = e.path

        return

    @staticmethod
    def _generate_key():
        """Return a (pseudo)random hash based on seed."""
        key_string = '%s%s%s%s' % (random(), datetime.now(), cherrypy.request.remote.ip, cherrypy.request.remote.port)
        return sha1(key_string).hexdigest()

    def clear_cookie(self):
        """Clear any existing visit ID cookie."""
        cookies = cherrypy.response.cookie
        log.debug('Clearing visit ID cookie')
        cookies[self.cookie_name] = ''
        cookies[self.cookie_name]['path'] = self.cookie_path
        cookies[self.cookie_name]['expires'] = ''
        cookies[self.cookie_name]['max-age'] = 0

    def send_cookie(self, visit_key):
        """Send an visit ID cookie back to the browser."""
        cookies = cherrypy.response.cookie
        cookies[self.cookie_name] = visit_key
        cookies[self.cookie_name]['path'] = self.cookie_path
        if self.cookie_secure:
            cookies[self.cookie_name]['secure'] = True
        if self.cookie_domain:
            cookies[self.cookie_name]['domain'] = self.cookie_domain
        max_age = self.cookie_max_age
        if max_age:
            cookies[self.cookie_name]['expires'] = '"%s"' % time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(time.time() + max_age))
            cookies[self.cookie_name]['max-age'] = max_age
        if self.cookie_httponly:
            cookies[self.cookie_name]['httponly'] = True
        log.debug('Sending visit ID cookie: %s', cookies[self.cookie_name].output())


class BaseVisitManager(threading.Thread):
    __module__ = __name__

    def __init__(self, timeout):
        super(BaseVisitManager, self).__init__(name='VisitManager')
        self.timeout = timeout
        self.queue = dict()
        self.lock = threading.Lock()
        self._shutdown = threading.Event()
        self.interval = config.get('visit.interval', 30)
        self.create_model()
        self.setDaemon(True)
        log.info('Visit Tracking starting (timeout = %is)...', timeout.seconds)
        self.start()

    def create_model(self):
        pass

    def new_visit_with_key(self, visit_key):
        """Return a new Visit object with the given key."""
        raise NotImplementedError

    def visit_for_key(self, visit_key):
        """Return the visit for this key.

        Return None if the visit doesn't exist or has expired.

        """
        raise NotImplementedError

    def update_queued_visits(self, queue):
        """Extend the expiration of the queued visits."""
        raise NotImplementedError

    def update_visit(self, visit_key, expiry):
        try:
            self.lock.acquire()
            self.queue[visit_key] = expiry
        finally:
            self.lock.release()

    def shutdown(self, timeout=None):
        log.info('Visit Tracking shutting down...')
        try:
            self.lock.acquire()
            self._shutdown.set()
            self.join(timeout)
        finally:
            self.lock.release()
        if self.isAlive():
            log.error('Visit Manager thread failed to shut down.')
        else:
            log.info('Visit Manager thread has been shut down.')

    def run(self):
        while not self._shutdown.isSet():
            self.lock.acquire()
            if self._shutdown.isSet():
                self.lock.release()
                continue
            queue = None
            try:
                if self.queue:
                    queue = self.queue.copy()
                    self.queue.clear()
                if queue is not None:
                    self.update_queued_visits(queue)
            finally:
                self.lock.release()
            self._shutdown.wait(self.interval)

        return