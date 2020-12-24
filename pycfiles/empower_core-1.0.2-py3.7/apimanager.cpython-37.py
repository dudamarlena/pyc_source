# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/apimanager/apimanager.py
# Compiled at: 2020-05-10 08:35:05
# Size of source mod 2**32: 16035 bytes
"""API Manager (REST Northbound Interface)."""
import inspect, json, base64, re
from uuid import UUID
import tornado.web, tornado.httpserver
from tornado.web import Application
from pymodm.errors import ValidationError
import empower_core.serialize as serialize
from empower_core.service import EService
from empower_core.launcher import srv_or_die, srv
DEBUG = True
DEFAULT_PORT = 8888
DEFAULT_WEBUI = '/var/www/webui/'
COOKIE_SECRET = b'xyRTvZpRSUyk8/9/McQAvsQPB4Rqv0w9mBtIpH9lf1o='
LOGIN_URL = '/auth/login'

def validate(returncode=200, min_args=0, max_args=0):
    """Validate REST method."""

    def decorator(func):

        def magic(self, *args):
            try:
                if len(args) < min_args or len(args) > max_args:
                    msg = 'Invalid url (%u, %u)' % (min_args, max_args)
                    raise ValueError(msg)
                params = {}
                if self.request.body:
                    if json.loads(self.request.body):
                        params = json.loads(self.request.body)
                if 'version' in params:
                    del params['version']
                output = func(self, *args, **params)
                if returncode == 200:
                    self.write_as_json(output)
            except KeyError as ex:
                try:
                    self.send_error(404, message=(str(ex)))
                finally:
                    ex = None
                    del ex

            except ValueError as ex:
                try:
                    self.send_error(400, message=(str(ex)))
                finally:
                    ex = None
                    del ex

            except AttributeError as ex:
                try:
                    self.send_error(400, message=(str(ex)))
                finally:
                    ex = None
                    del ex

            except TypeError as ex:
                try:
                    self.send_error(400, message=(str(ex)))
                finally:
                    ex = None
                    del ex

            except ValidationError as ex:
                try:
                    self.send_error(400, message=(ex.message))
                finally:
                    ex = None
                    del ex

            self.set_status(returncode, None)

        magic.__doc__ = func.__doc__
        return magic

    return decorator


class BaseHandler(tornado.web.RequestHandler):
    __doc__ = 'Base Handler.'
    service = None
    URLS = []

    def get_current_user(self):
        """Return username of the currently logged user or None."""
        return self.get_secure_cookie('username')

    @classmethod
    def auth_based(cls):
        """Return true if both account and project managers are available"""
        pmngr = srv('projectsmanager')
        amngr = srv('accountsmanager')
        return bool(pmngr and amngr)


class IndexHandler(BaseHandler):
    __doc__ = 'Index page handler.'
    URLS = [
     '/', '/([a-z]*).html']

    def get_project(self):
        """Get the current project or return None if not project is set."""
        project_id = self.get_secure_cookie('project_id')
        if not project_id:
            return
        project_id = UUID(project_id.decode('UTF-8'))
        projects_manager = srv_or_die('projectsmanager')
        if project_id not in projects_manager.projects:
            self.clear_cookie('project_id')
            return
        return projects_manager.projects[project_id]

    @tornado.web.authenticated
    def get(self, args=None):
        """Render index page."""
        try:
            if self.auth_based():
                username = self.get_secure_cookie('username').decode('UTF-8')
                accounts_manager = srv_or_die('accountsmanager')
                account = accounts_manager.accounts[username]
                page = 'index.html' if not args else '%s.html' % args
                self.render(page, username=(account.username),
                  password=(account.password),
                  name=(account.name),
                  email=(account.email),
                  project=(self.get_project()))
            else:
                page = 'index.html' if not args else '%s.html' % args
                self.render(page)
        except KeyError as ex:
            try:
                self.send_error(404, message=(str(ex)))
            finally:
                ex = None
                del ex

        except ValueError as ex:
            try:
                self.send_error(400, message=(str(ex)))
            finally:
                ex = None
                del ex


class AuthSwitchProjectHandler(BaseHandler):
    __doc__ = 'Login page handler.'
    URLS = [
     '/auth/switch_project']

    def get(self):
        """Set the active project."""
        username = self.get_secure_cookie('username').decode('UTF-8')
        if username == 'root':
            self.clear_cookie('project_id')
            self.redirect('/')
            return
        project_id = self.get_argument('project_id', None)
        if not project_id:
            self.clear_cookie('project_id')
            self.redirect('/')
            return
        try:
            project_id = UUID(project_id)
            projects_manager = srv_or_die('projectsmanager')
            project = projects_manager.projects[project_id]
            if project.owner != username:
                self.clear_cookie('project_id')
                self.redirect('/')
                return
            self.set_secure_cookie('project_id', str(project.project_id))
        except KeyError:
            self.clear_cookie('project_id')
        except ValueError:
            self.clear_cookie('project_id')

        self.redirect('/')


class AuthLoginHandler(BaseHandler):
    __doc__ = 'Login page handler.'
    URLS = [
     '/auth/login']

    def get(self):
        """Render login page."""
        if not self.auth_based():
            self.redirect('/')
            return
        if self.get_current_user():
            self.redirect('/')
            return
        self.render('login.html', error=(self.get_argument('error', '')))

    def post(self):
        """Process login credentials."""
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        accounts_manager = srv_or_die('accountsmanager')
        if accounts_manager.check_permission(username, password):
            self.set_secure_cookie('username', username)
            self.redirect('/index.html')
        else:
            self.clear_cookie('username')
            self.redirect('/auth/login?error=Wrong credentials!')


class AuthLogoutHandler(BaseHandler):
    __doc__ = 'Logout page handler.'
    URLS = [
     '/auth/logout']

    def get(self):
        """Process logout request."""
        self.clear_cookie('username')
        self.clear_cookie('project_id')
        self.redirect('/auth/login')


class APIHandler(tornado.web.RequestHandler):
    __doc__ = 'Base class for all the REST calls.'
    service = None

    @classmethod
    def auth_based(cls):
        """Return true if both account and project managers are available"""
        pmngr = srv('projectsmanager')
        amngr = srv('accountsmanager')
        return bool(pmngr and amngr)

    def write_error(self, status_code, **kwargs):
        """Write error as JSON message."""
        self.set_header('Content-Type', 'application/json')
        value = {'title':self._reason, 
         'status_code':status_code, 
         'detail':kwargs.get('message')}
        self.finish(json.dumps((serialize(value)), indent=4))

    def write_as_json(self, value):
        """Return reply as a json document."""
        self.write(json.dumps((serialize(value)), indent=4))

    def prepare(self):
        """Prepare to handler reply."""
        self.set_header('Content-Type', 'application/json')
        if not self.auth_based():
            return
        if self.request.method == 'GET':
            return
        accounts_manager = srv_or_die('accountsmanager')
        projects_manager = srv_or_die('projectsmanager')
        auth_header = self.request.headers.get('Authorization')
        if not (auth_header is None or auth_header.startswith('Basic ')):
            self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
            self.send_error(401, message='Missing authorization header')
            return
        auth_bytes = bytes(auth_header[6:], 'utf-8')
        auth_decoded = base64.b64decode(auth_bytes).decode()
        username, password = auth_decoded.split(':', 2)
        if not accounts_manager.check_permission(username, password):
            self.send_error(401, message='Invalid username/password')
            return
        account = accounts_manager.accounts[username]
        if account.username == 'root':
            return
        if self.request.uri.startswith('/api/v1/accounts'):
            pattern = re.compile('/api/v1/accounts/([a-zA-Z0-9:-]*)/?')
            match = pattern.match(self.request.uri)
            if match and match.group(1):
                username = match.group(1)
                if username == account.username:
                    return
        if self.request.uri.startswith('/api/v1/projects'):
            pattern = re.compile('/api/v1/projects/([a-zA-Z0-9-]*)/?')
            match = pattern.match(self.request.uri)
            if match and match.group(1):
                project_id = UUID(match.group(1))
                if project_id in projects_manager.projects:
                    project = projects_manager.projects[project_id]
                    if account.username == project.owner:
                        return
        self.send_error(401, message='URI not authorized')


BOILER_PLATE = '# REST API\n\nThe REST API consists of a set of RESTful resources and their attributes.\nThe base URL for the REST API is the following:\n\n    http{s}://{username}:{password}@{hostname}:{port}/api/v1/{resource}\n\nOf course, you need to replace hostname and port with the hostname/port\ncombination for your controller.\n\nThe current (and only) version of the API is v1.\n\nThe REST API uses HTTP basic authentication control access to RESTful resource.\n\nNotice that there are two kinds of accounts:\n\n * user accounts, which have complete CRUD access only to all the URLs that\n begins with /api/v1/projects/{project_id}.\n\n * root account, which has complete CRUD access to all URLs. All the URLs that\n DO NOT start with /api/v1/projects/{project_id} require a root account to\n be accessed. The only exception is the URL /api/v1/accounts/{user_id} which\n is fully accessible to all users.\n '

class DocHandler(APIHandler):
    __doc__ = 'Generates markdown documentation.'
    URLS = [
     '/api/v1/doc/?']

    def get(self):
        """Generates markdown documentation.

        Args:

            None

        Example URLs:

            GET /api/v1/doc
        """
        exclude_list = [
         'StaticFileHandler', 'DocHandler']
        handlers = set()
        accum = [BOILER_PLATE]
        for rule in self.service.application.default_router.rules:
            if not rule.target.rules:
                continue
            handlers.add(rule.target.rules[0].target)

        handlers = sorted(handlers, key=(lambda x: x.__name__))
        accum.append("## <a name='handlers'></a>Handlers\n")
        for handler in handlers:
            if handler.__name__ in exclude_list:
                continue
            accum.append(' * [%s](#%s)' % (
             handler.__name__, handler.__name__))

        accum.append('\n')
        for handler in handlers:
            if handler.__name__ in exclude_list:
                continue
            else:
                accum.append("# <a name='%s'></a>%s ([Top](#handlers))\n" % (
                 handler.__name__, handler.__name__))
                accum.append('%s\n' % inspect.getdoc(handler))
                if hasattr(handler, 'URLS'):
                    if handler.URLS:
                        accum.append('### URLs\n')
                        for url in handler.URLS:
                            accum.append('    %s' % url)

                accum.append('\n')
                if hasattr(handler, 'get'):
                    doc = inspect.getdoc(getattr(handler, 'get'))
                    if doc:
                        accum.append('### GET\n')
                        accum.append(doc)
                        accum.append('\n')
                if hasattr(handler, 'put'):
                    doc = inspect.getdoc(getattr(handler, 'put'))
                    if doc:
                        accum.append('### PUT\n')
                        accum.append(doc)
                        accum.append('\n')
            if hasattr(handler, 'post'):
                doc = inspect.getdoc(getattr(handler, 'post'))
                if doc:
                    accum.append('### POST\n')
                    accum.append(doc)
                    accum.append('\n')
                if hasattr(handler, 'delete'):
                    doc = inspect.getdoc(getattr(handler, 'delete'))
                    if doc:
                        accum.append('### DELETE\n')
                        accum.append(doc)
                        accum.append('\n')

        self.write('\n'.join(accum))


class APIManager(EService):
    __doc__ = 'Service exposing a REST API\n\n    Parameters:\n        port: the port on which the HTTP server should listen (optional,\n            default: 8888)\n    '
    HANDLERS = [
     IndexHandler, AuthLoginHandler, AuthLogoutHandler,
     DocHandler, AuthSwitchProjectHandler]

    def __init__(self, context, service_id, webui, port):
        super().__init__(context=context, service_id=service_id, webui=webui, port=port)
        self.settings = {'static_path':self.webui + 'static/', 
         'cookie_secret':COOKIE_SECRET, 
         'template_path':self.webui + 'templates/', 
         'login_url':LOGIN_URL, 
         'debug':DEBUG}
        self.application = Application([], **self.settings)
        self.http_server = tornado.httpserver.HTTPServer(self.application)

    @property
    def webui(self):
        """Return path to Web UI."""
        return self.params['webui']

    @webui.setter
    def webui(self, value):
        """Set path to Web UI."""
        if 'webui' in self.params:
            if self.params['webui']:
                raise ValueError('Param webui can not be changed')
        self.params['webui'] = value

    @property
    def port(self):
        """Return port."""
        return self.params['port']

    @port.setter
    def port(self, value):
        """Set port."""
        if 'port' in self.params:
            if self.params['port']:
                raise ValueError('Param port can not be changed')
        self.params['port'] = int(value)

    def start(self):
        super().start()
        self.http_server.listen(self.port)
        self.log.info('Listening on port %u', self.port)
        self.http_server.start()

    def register_handler(self, handler):
        """Add a new handler class."""
        for url in handler.URLS:
            self.log.info('Registering URL: %s', url)
            self.application.add_handlers('.*$', [(url, handler)])


def launch(context, service_id, webui=DEFAULT_WEBUI, port=DEFAULT_PORT):
    """ Initialize the module. """
    return APIManager(context=context, service_id=service_id, webui=webui, port=port)