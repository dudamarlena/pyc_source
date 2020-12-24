# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/multiwsgi.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from moya.wsgi import WSGIApplication
from moya.sites import Sites
from moya.settings import SettingsContainer
from moya.compat import py2bytes, itervalues, text_type
from moya.loggingconf import init_logging
from moya.logtools import LoggerFile
from moya import pilot
try:
    import objgraph
except:
    objgraph = None

from webob import Response
import sys, os, io, glob, tempfile, threading
from collections import OrderedDict
import logging
log = logging.getLogger(b'moya.srv')
DEFAULT_HOME_DIR = b'/etc/moya'
not_found_response = b'<!DOCTYPE html>\n<html>\n<head>\n    <title>404 Not Found</title>\n    <style type="text/css">\n        body {{font-family: arial,sans-serif;}}\n    </style>\n</head>\n<body>\n<h1>404 Not Found</h1>\n<small>moya-srv does not know about this domain</small>\n</body>\n</html>\n'

class Server(object):

    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.load()
        self.application = None
        return

    def load(self):
        settings = SettingsContainer.read_os(self.settings_path)
        self.name = settings.get(b'service', b'name')
        self.domains = settings.get_list(b'service', b'domains')
        self.location = settings.get(b'service', b'location')
        self.ini = settings.get_list(b'service', b'ini') or [b'production.ini']
        self.master_settings = settings

    def __repr__(self):
        return (b"<project '{}'>").format(self.name)

    def build(self):
        log.debug(b'building %r', self)
        try:
            pilot.service[b'name'] = self.name
            try:
                application = WSGIApplication(self.location, self.ini, disable_autoreload=True, logging=None, master_settings=self.master_settings)
                self.application = application
            finally:
                del pilot.service[b'name']

        except:
            log.exception(b'error building %r', self)
            raise

        return


def memory_tracker(f):

    def deco(self, *args, **kwargs):
        if self.debug_memory:
            objgraph.show_growth(limit=1)
        try:
            return f(self, *args, **kwargs)
        finally:
            if self.debug_memory:
                log.info(b'New objects:')
                objgraph.show_growth(file=LoggerFile(b'moya.srv'))

    return deco


class MultiWSGIApplication(object):

    def __init__(self):
        self.servers = OrderedDict()
        self.sites = Sites()
        self._lock = threading.Lock()
        self.debug_memory = False

    def add_project(self, settings_path, logging_path=None):
        server = Server(settings_path)
        self.servers[server.name] = server
        self.sites.add(server.domains, name=server.name)
        log.debug(b'registered %r', server)

    def build_all(self):
        for server in itervalues(self.servers):
            server.build()

    def not_found(self):
        response = Response(charset=py2bytes(b'utf8'), status=404)
        response.text = not_found_response
        return response.app_iter

    def reload_required(server_name):
        return False

    def reload(self, server_name):
        """
        Reload the server

        This actually creates a new server object, so that if the load fails it will continue to
        process requests with the old server instance.
        """
        log.debug(b"reloading '%s'", server_name)
        server = self.servers[server_name]
        try:
            new_server = Server(server.settings_path)
            new_server.build()
        except:
            log.exception(b"reload of '%s' failed", server_name)

        self.servers[server_name] = new_server
        self.sites.clear()
        for server in itervalues(self.servers):
            self.sites.add(server.domains, name=server.name)

    @memory_tracker
    def __call__(self, environ, start_response):
        try:
            domain = environ[b'SERVER_NAME']
            with self._lock:
                site_match = self.sites.match(domain)
                if site_match is None:
                    return self.not_found()
                server_name = site_match[b'name']
                if self.reload_required(server_name):
                    self.reload(server_name)
                server = self.servers[server_name]
            pilot.service[b'name'] = server_name
            try:
                return server.application(environ, start_response)
            finally:
                del pilot.service[b'name']

        except:
            log.exception(b'error in multiwsgi MultiWSGIApplication.__call__')
            raise

        return


class Service(MultiWSGIApplication):
    """WSGI application to load projects from /etc/moya"""

    def error(self, msg, code=-1):
        sys.stderr.write(msg + b'\n')
        sys.exit(code)

    def __init__(self, home_dir=None):
        super(Service, self).__init__()
        self.changes = {}
        self.home_dir = home_dir = os.environ.get(b'MOYA_SERVICE_HOME', None) or DEFAULT_HOME_DIR
        settings_path = os.path.join(home_dir, b'moya.conf')
        try:
            with io.open(settings_path, b'rt') as (f):
                self.settings = SettingsContainer.read_from_file(f)
        except IOError:
            self.error((b'unable to read {}').format(settings_path))
            return -1

        logging_setting = self.settings.get(b'projects', b'logging', b'logging.ini')
        logging_path = os.path.join(self.home_dir, logging_setting)
        try:
            init_logging(logging_path)
        except Exception as e:
            log.error(b"unable to initialize logging from '%s'", logging_path)
            sys.stderr.write((b"unable to initialize logging from '{}' ({})\n").format(logging_path, e))
            return -1

        log.debug(b'read conf from %s', settings_path)
        log.debug(b'read logging from %s', logging_path)
        temp_dir_root = self.settings.get(b'service', b'temp_dir', tempfile.gettempdir())
        self.debug_memory = objgraph and self.settings.get_bool(b'service', b'debug_memory', False)
        self.temp_dir = os.path.join(temp_dir_root, b'moyasrv')
        try:
            os.makedirs(self.temp_dir)
        except OSError:
            pass

        for path in self._get_projects(self.settings, self.home_dir):
            log.debug(b'reading project settings %s', path)
            try:
                self.add_project(path)
            except:
                log.exception(b"error adding project from '%s'", path)

        for server_name in self.servers:
            path = os.path.join(self.temp_dir, (b'{}.changes').format(server_name))
            try:
                if not os.path.exists(path):
                    with open(path, b'wb'):
                        pass
            except IOError as e:
                sys.stderr.write((b'{}\n').format(text_type(e)))
                return -1

            self.changes[server_name] = os.path.getmtime(path)

        self.build_all()
        return

    @classmethod
    def get_project_settings(cls, project_name):
        """Get the settings for a single project"""
        home_dir = os.environ.get(b'MOYA_SERVICE_HOME', None) or DEFAULT_HOME_DIR
        settings_path = os.path.join(home_dir, b'moya.conf')
        try:
            with io.open(settings_path, b'rt') as (f):
                service_settings = SettingsContainer.read_from_file(f)
        except IOError:
            log.error(b"unable to read moya service settings from '{}'", settings_path)
            return -1

        for path in cls._get_projects(service_settings, home_dir):
            try:
                settings = SettingsContainer.read_os(path)
            except Exception as e:
                log.error(b"error reading '%s' (%s)", path, e)

            if settings.get(b'service', b'name', None) == project_name:
                return settings

        return

    def reload_required(self, server_name):
        """Detect if a reload is required"""
        path = os.path.join(self.temp_dir, (b'{}.changes').format(server_name))
        mtime = os.path.getmtime(path)
        return self.changes[server_name] != mtime

    def reload(self, server_name):
        path = os.path.join(self.temp_dir, (b'{}.changes').format(server_name))
        self.changes[server_name] = os.path.getmtime(path)
        super(Service, self).reload(server_name)

    @classmethod
    def _get_projects(self, settings, home_dir):
        project_paths = settings.get_list(b'projects', b'read')
        paths = []
        cwd = os.getcwd()
        try:
            os.chdir(home_dir)
            for path in project_paths:
                glob_paths = glob.glob(path)
                paths.extend([ os.path.abspath(p) for p in glob_paths ])

        finally:
            os.chdir(cwd)

        return paths