# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\testutil.py
# Compiled at: 2011-03-26 09:20:22
"""TurboGears Test Utilities."""
__all__ = [
 'BrowsingSession', 'DBTest', 'DBTestSA', 'DBTestSO', 'DummySession', 'TGTest', 'capture_log', 'make_app', 'make_wsgiapp', 'mount', 'print_log', 'get_log', 'sqlalchemy_cleanup', 'start_server', 'stop_server', 'unmount']
import os, types, logging, string, unittest, cherrypy
from cherrypy.process.wspbus import states
from webtest import TestApp
try:
    import sqlobject
    from sqlobject.inheritance import InheritableSQLObject
except ImportError:
    sqlobject = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

from turbogears import config, database, startup, update_config, validators
from turbogears.util import get_model

def unmount():
    """Remove an application from the object traversal tree."""
    for app in cherrypy.tree.apps.keys():
        del cherrypy.tree.apps[app]


def mount(controller, path='/'):
    """Mount a controller at a path.  Returns a WSGI application."""
    startup.config_static()
    if path == '/':
        startup.config_root()
    config.update({'environment': 'test_suite', 'log.screen': False})
    cherrypy.tree.mount(controller, path, config=config.app)
    return make_wsgiapp()


def make_wsgiapp():
    """Return a WSGI application from CherryPy."""
    return cherrypy.tree


def make_app(controller=None):
    """Return a WebTest.TestApp instance from CherryPy.

    If a Controller object is provided, it will be mounted at the root level.
    If not, it'll look for an already mounted root.

    """
    if controller:
        wsgiapp = mount(controller(), '/')
    else:
        wsgiapp = make_wsgiapp()
    return TestApp(wsgiapp)


def start_server(tg_only=True):
    """Start the server if it's not already started.

    Use tg_only=False to run the CherryPy engine as well.

    """
    if not tg_only and not config.get('cp_started'):
        cherrypy.engine.start()
        config.update({'cp_started': True})
    if not config.get('server_started'):
        startup.start_turbogears()
        config.update({'server_started': True})


def stop_server(tg_only=False):
    """Stop the server and unmount the application.

    Use tg_only=True to leave CherryPy running (for faster tests).

    """
    if config.get('server_started'):
        startup.stop_turbogears()
        config.update({'server_started': False})
    unmount()
    if not tg_only and config.get('cp_started'):
        if cherrypy.engine.state != states.STOPPED:
            cherrypy.engine.exit()
        config.update({'cp_started': False})


_currentcat = None

class MemoryListHandler(logging.Handler):
    __module__ = __name__

    def __init__(self):
        logging.Handler.__init__(self, level=logging.DEBUG)
        self.log = []

    def emit(self, record):
        print 'Got record: %s' % record
        print 'formatted as: %s' % self.format(record)
        self.log.append(self.format(record))

    def print_log(self):
        print ('\n').join(self.log)
        self.log = []

    def get_log(self):
        log = self.log
        self.log = []
        return log


_memhandler = MemoryListHandler()

def catch_validation_errors(widget, value):
    """Catch and unpack validation errors (for testing purposes)."""
    try:
        value = widget.validate(value)
    except validators.Invalid, errors:
        try:
            errors = errors.unpack_errors()
        except AttributeError:
            pass

    else:
        errors = {}

    return (
     value, errors)


def capture_log(category):
    """Capture log for one category.

    The category can either be a single category (a string like 'foo.bar')
    or a list of them. You *must* call print_log() to reset when you're done.

    """
    global _currentcat
    assert not _currentcat, '_currentcat not cleared.  Use get_log to reset.'
    if not isinstance(category, list) and not isinstance(category, tuple):
        category = [
         category]
    _currentcat = category
    for cat in category:
        log = logging.getLogger(cat)
        log.setLevel(logging.DEBUG)
        log.addHandler(_memhandler)


def _reset_logging():
    """Manage the resetting of the loggers."""
    global _currentcat
    if not _currentcat:
        return
    for cat in _currentcat:
        log = logging.getLogger(cat)
        log.removeHandler(_memhandler)

    _currentcat = None
    return


def print_log():
    """Print the log captured by capture_log to stdout.

    Resets that log and resets the temporarily added handlers.

    """
    _reset_logging()
    _memhandler.print_log()


def get_log():
    """Return the list of log messages captured by capture_log.

    Resets that log and resets the temporarily added handlers.

    """
    _reset_logging()
    return _memhandler.get_log()


def sqlalchemy_cleanup():
    database.metadata.clear()
    try:
        database.metadata.dispose()
    except AttributeError:
        if database.metadata.bind:
            database.metadata.bind.dispose()

    database._engine = None
    sqlalchemy.orm.clear_mappers()
    return


class TGTest(unittest.TestCase):
    """A WebTest enabled unit testing class.

    To use, subclass and set root to your controller object, or set app to a
    webtest.TestApp instance.

    In your tests, use self.app to make WebTest calls.

    """
    __module__ = __name__
    root = None
    app = None
    stop_tg_only = False
    config = None

    def setUp(self):
        """Set up the WebTest by starting the server.

        You should override this and make sure you have properly
        mounted a root for your server before calling super,
        or simply pass a root controller to super.
        Otherwise the CherryPy hooks for TurboGears will not be used.

        """
        assert self.root or self.app, 'Either self.root or self.app must be set'
        if not self.app:
            self.app = make_app(self.root)
        if not self.config:
            self.config = config.copy()
        start_server()

    def tearDown(self):
        """Tear down the WebTest by stopping the server."""
        stop_server(tg_only=self.stop_tg_only)
        config.update(self.config)

    def login_user(self, user):
        """Log a specified user object into the system."""
        self.app.post(config.get('identity.failure_url'), dict(user_name=user.user_name, password=user.password, login='Login'))


class BrowsingSession(object):
    __module__ = __name__

    def __init__(self):
        self.visit = None
        (self.response, self.status) = (None, None)
        self.cookie = {}
        self.app = make_app()
        return

    def goto(self, path, headers=None, **kwargs):
        if headers is None:
            headers = {}
        if self.cookie:
            headers['Cookie'] = self.cookie_encoded
        response = self.app.get(path, headers=headers, **kwargs)
        ctype_parts = response.headers['Content-Type'].split(';')
        for parameter in ctype_parts[1:]:
            value = parameter.strip().split('=', 1)[(-1)]
            try:
                self.unicode_response = response.body.decode(value)
                break
            except:
                pass

        self.response = response.body
        self.full_response = response
        self.status = response.status
        self.cookie = response.cookies_set
        self.cookie_encoded = response.headers.get('Set-Cookie', '')
        return


class DummySession:
    """A very simple dummy session."""
    __module__ = __name__
    session_storage = dict
    to_be_loaded = None


class AbstractDBTest(unittest.TestCase):
    """A database enabled unit testing class.

    Creates and destroys your database before and after each unit test.
    You must set the model attribute in order for this class to
    function correctly.

    """
    __module__ = __name__
    model = None

    def setUp(self):
        raise NotImplementedError()

    def tearDown(self):
        raise NotImplementedError()


class DBTestSO(AbstractDBTest):
    __module__ = __name__

    def _get_soClasses(self):
        try:
            return [ self.model.__dict__[x] for x in self.model.soClasses ]
        except AttributeError:
            return self.model.__dict__.values()

    def setUp(self):
        if not self.model:
            self.model = get_model()
            if not self.model:
                raise Exception('Unable to run database tests without a model')
        constraints = list()
        for item in self._get_soClasses():
            if isinstance(item, types.TypeType) and issubclass(item, sqlobject.SQLObject) and item is not sqlobject.SQLObject and item is not InheritableSQLObject:
                collected_constraints = item.createTable(ifNotExists=True, applyConstraints=False)
                if collected_constraints:
                    constraints.extend(collected_constraints)

        for postponed_constraint in constraints:
            item._connection.query(postponed_constraint)

    def tearDown(self):
        database.rollback_all()
        for item in reversed(self._get_soClasses()):
            if isinstance(item, types.TypeType) and issubclass(item, sqlobject.SQLObject) and item is not sqlobject.SQLObject and item is not InheritableSQLObject:
                item.dropTable(ifExists=True, cascade=True)


class DBTestSA(AbstractDBTest):
    __module__ = __name__

    def setUp(self):
        database.get_engine()
        database.metadata.create_all()

    def tearDown(self):
        database.metadata.drop_all()


for w in os.walk('.'):
    if os.sep + '.' not in w[0]:
        for f in w[2]:
            if f.endswith('.kid'):
                f = os.path.join(w[0], f[:-3] + 'pyc')
                if os.path.exists(f):
                    os.remove(f)

if os.path.exists('test.cfg'):
    for (dirpath, dirs, dummy2) in os.walk('.'):
        basename = os.path.basename(dirpath)
        dirname = os.path.basename(os.path.dirname(dirpath))
        init_py = os.path.join(dirpath, '__init__.py')
        if basename == 'config' and dirname[0] in string.ascii_letters + '_' and os.path.exists(init_py):
            modulename = '%s.app' % dirpath[2:].replace(os.sep, '.')
            break
    else:
        modulename = None

    try:
        update_config(configfile='test.cfg', modulename=modulename)
    except ImportError, exc:
        import warnings
        warnings.warn('Could not import configuration from module: %s' % exc, RuntimeWarning)
        update_config(configfile='test.cfg', modulename=None)

else:
    database.set_db_uri('sqlite:///:memory:')
config.update({'global': {'engine.autoreload.on': False}})
if config.get('sqlobject.dburi'):
    DBTest = DBTestSO
elif config.get('sqlalchemy.dburi'):
    DBTest = DBTestSA
else:
    raise Exception('Unable to find SQLAlchemy or SQLObject dburi')