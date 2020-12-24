# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nosegae.py
# Compiled at: 2016-12-15 10:23:22
import os, logging, sys, tempfile
from nose.plugins.base import Plugin
from nose.case import FunctionTestCase
from pkg_resources import get_distribution, DistributionNotFound
try:
    _dist = get_distribution('nosegae')
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'nosegae')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'DEVELOPMENT'
else:
    __version__ = _dist.version

logger = logging.getLogger(__name__)

class NoseGAE(Plugin):
    """Activate this plugin to run tests in Google App Engine dev environment. When the plugin is active,
    Google App Engine dev stubs such as the datastore, memcache, taskqueue, and more can be made available.
    """
    name = 'gae'

    def options(self, parser, env=os.environ):
        super(NoseGAE, self).options(parser, env)
        parser.add_option('--gae-lib-root', default='/usr/local/google_appengine', dest='gae_lib_root', help='Set the path to the root directory of the Google Application Engine installation')
        parser.add_option('--gae-application', default=None, action='store', dest='gae_app', help='Set the path to the GAE application under test. Default is the nose `where` directory (generally the cwd)')
        parser.add_option('--gae-datastore', default=None, action='store', dest='gae_data', help='Set the path to the GAE datastore to use in tests. Note that when using an existing datastore directory, the datastore will not be cleared before testing begins.')
        return

    def configure(self, options, config):
        super(NoseGAE, self).configure(options, config)
        if not self.enabled:
            return
        if sys.version_info[0:2] < (2, 7):
            raise EnvironmentError('Python version must be 2.7 or greater, like the Google App Engine environment.  Tests are running with: %s' % sys.version)
        try:
            self._app_path = options.gae_app.split(',')
        except AttributeError:
            self._app_path = [
             config.workingDir]

        self._data_path = options.gae_data or os.path.join(tempfile.gettempdir(), 'nosegae.sqlite3')
        if options.gae_lib_root not in sys.path:
            options.gae_lib_root = os.path.realpath(options.gae_lib_root)
            sys.path.insert(0, options.gae_lib_root)
        for path_ in self._app_path:
            path_ = os.path.realpath(path_)
            if not os.path.isdir(path_):
                path_ = os.path.dirname(path_)
            if path_ not in sys.path:
                sys.path.insert(0, path_)

        if 'google' in sys.modules:
            reload(sys.modules['google'])
        try:
            import appengine_config
        except ImportError:
            pass

        import dev_appserver
        dev_appserver.fix_sys_path()
        import google.appengine.tools.os_compat
        from google.appengine.tools.devappserver2 import application_configuration
        self.configuration = application_configuration.ApplicationConfiguration(self._app_path)
        os.environ['APPLICATION_ID'] = self.configuration.app_id
        os.environ['CURRENT_VERSION_ID'] = self.configuration.modules[0].version_id
        self.is_doctests = options.enable_plugin_doctest
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

    def startTest(self, test):
        """Initializes Testbed stubs based off of attributes of the executing test

        allow tests to register and configure stubs by setting properties like
        nosegae_<stub_name> and nosegae_<stub_name>_kwargs

        Example

        class MyTest(unittest.TestCase):
            nosegae_datastore_v3 = True
            nosegae_datastore_v3_kwargs = {
              'datastore_file': '/tmp/nosegae.sqlite3,
              'use_sqlite': True
            }

            def test_something(self):
               entity = MyModel(name='NoseGAE')
               entity.put()
               self.assertNotNone(entity.key.id())

        Args
            :param test: The unittest.TestCase being run
            :type test: unittest.TestCase
        """
        from google.appengine.ext import testbed
        self._add_missing_stubs(testbed)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        the_test = test.test
        if isinstance(the_test, FunctionTestCase):
            the_test = the_test.test
        the_test.testbed = self.testbed
        for stub_name, stub_init in testbed.INIT_STUB_METHOD_NAMES.iteritems():
            if not getattr(the_test, 'nosegae_%s' % stub_name, False):
                continue
            stub_kwargs = getattr(the_test, 'nosegae_%s_kwargs' % stub_name, {})
            if stub_name == testbed.TASKQUEUE_SERVICE_NAME:
                self._init_taskqueue_stub(**stub_kwargs)
            elif stub_name == testbed.DATASTORE_SERVICE_NAME:
                if not self.testbed.get_stub(testbed.MEMCACHE_SERVICE_NAME):
                    self.testbed.init_memcache_stub()
                self._init_datastore_v3_stub(**stub_kwargs)
            elif stub_name == testbed.USER_SERVICE_NAME:
                self._init_user_stub(**stub_kwargs)
            elif stub_name == testbed.MODULES_SERVICE_NAME:
                self._init_modules_stub(**stub_kwargs)
            else:
                self._init_stub(stub_init, **stub_kwargs)

        if self.is_doctests:
            self._doctest_compat(the_test)
        self.the_test = the_test

    def stopTest(self, test):
        self.testbed.deactivate()
        del self.the_test.testbed
        del self.the_test

    def _doctest_compat(self, the_test):
        """Enable compatibility with doctests by setting the current testbed into the doctest scope"""
        try:
            the_test._dt_test.globs['testbed'] = self.testbed
        except AttributeError:
            pass

    def _add_missing_stubs(self, testbed):
        """Monkeypatch the testbed for stubs that do not have an init method yet"""
        pass

    def _init_taskqueue_stub(self, **stub_kwargs):
        """Initializes the taskqueue stub using nosegae config magic"""
        task_args = {}
        if 'root_path' not in stub_kwargs:
            for p in self._app_path:
                dir_ = os.path.dirname(p) if os.path.isfile(p) else p
                if os.path.isfile(os.path.join(dir_, 'queue.yaml')) or os.path.isfile(os.path.join(dir_, 'queue.yml')):
                    task_args['root_path'] = dir_
                    break

        task_args.update(stub_kwargs)
        self.testbed.init_taskqueue_stub(**task_args)

    def _init_datastore_v3_stub(self, **stub_kwargs):
        """Initializes the datastore stub using nosegae config magic"""
        task_args = dict(datastore_file=self._data_path)
        task_args.update(stub_kwargs)
        self.testbed.init_datastore_v3_stub(**task_args)

    def _init_user_stub(self, **stub_kwargs):
        """Initializes the user stub using nosegae config magic"""
        task_args = stub_kwargs.copy()
        self.testbed.setup_env(overwrite=True, USER_ID=task_args.pop('USER_ID', 'testuser'), USER_EMAIL=task_args.pop('USER_EMAIL', 'testuser@example.org'), USER_IS_ADMIN=task_args.pop('USER_IS_ADMIN', '1'))
        self.testbed.init_user_stub(**task_args)

    def _init_modules_stub(self, **_):
        """Initializes the modules stub based off of your current yaml files

        Implements solution from
        http://stackoverflow.com/questions/28166558/invalidmoduleerror-when-using-testbed-to-unit-test-google-app-engine
        """
        from google.appengine.api import request_info
        all_versions = {}
        def_versions = {}
        m2h = {}
        for module in self.configuration.modules:
            module_name = module._module_name or 'default'
            module_version = module._version or '1'
            all_versions[module_name] = [module_version]
            def_versions[module_name] = module_version
            m2h[module_name] = {module_version: 'localhost:8080'}

        request_info._local_dispatcher = request_info._LocalFakeDispatcher(module_names=list(all_versions), module_name_to_versions=all_versions, module_name_to_default_versions=def_versions, module_name_to_version_to_hostname=m2h)
        self.testbed.init_modules_stub()

    def _init_stub(self, stub_init, **stub_kwargs):
        """Initializes all other stubs for consistency's sake"""
        getattr(self.testbed, stub_init, lambda **kwargs: None)(**stub_kwargs)