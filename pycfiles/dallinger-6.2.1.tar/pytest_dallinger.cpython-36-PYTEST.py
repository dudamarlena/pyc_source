# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/pytest_dallinger.py
# Compiled at: 2020-04-26 19:37:24
# Size of source mod 2**32: 15577 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, mock, os, pexpect, pytest, shutil, sys, tempfile, time
from selenium import webdriver
from dallinger import information
from dallinger import models
from dallinger import networks
from dallinger import nodes
from dallinger.bots import BotBase
from dallinger.recruiters import NEW_RECRUIT_LOG_PREFIX
from dallinger.recruiters import CLOSE_RECRUITMENT_LOG_PREFIX
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'rep_' + rep.when, rep)


@pytest.fixture(scope='session')
def root(request):
    try:
        path = request.fspath.strpath
        return os.path.abspath(os.path.join(path, '..'))
    except AttributeError:
        return request.node.fspath.strpath


@pytest.fixture(scope='class')
def cwd(root):
    os.chdir(root)


@pytest.fixture
def reset_sys_modules():
    to_clear = [k for k in sys.modules if k.startswith('dallinger_experiment')]
    for key in to_clear:
        del sys.modules[key]


@pytest.fixture
def clear_workers():
    import subprocess

    def _zap():
        kills = [
         [
          'pkill', '-f', 'heroku']]
        for kill in kills:
            try:
                subprocess.check_call(kill)
            except Exception as e:
                if e.returncode != 1:
                    raise

    _zap()
    yield
    _zap()


@pytest.fixture(scope='session')
def env():
    environ_orig = os.environ.copy()
    running_on_ci = environ_orig.get('CI', False)
    have_home_dir = environ_orig.get('HOME', False)
    if not running_on_ci:
        if have_home_dir:
            yield environ_orig
    else:
        fake_home = tempfile.mkdtemp()
        environ_patched = environ_orig.copy()
        environ_patched.update({'HOME': fake_home})
        os.environ = environ_patched
        yield environ_patched
        os.environ = environ_orig
        shutil.rmtree(fake_home, ignore_errors=True)


@pytest.fixture
def tempdir():
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def in_tempdir(tempdir):
    cwd = os.getcwd()
    os.chdir(tempdir)
    yield tempdir
    os.chdir(cwd)


@pytest.fixture
def stub_config():
    """Builds a standardized Configuration object and returns it, but does
    not load it as the active configuration returned by
    dallinger.config.get_config()
    """
    defaults = {'ad_group':'Test ad group', 
     'approve_requirement':95, 
     'assign_qualifications':True, 
     'auto_recruit':True, 
     'aws_access_key_id':'fake aws key', 
     'aws_secret_access_key':'fake aws secret', 
     'aws_region':'us-east-1', 
     'base_payment':0.01, 
     'base_port':5000, 
     'browser_exclude_rule':'MSIE, mobile, tablet', 
     'clock_on':False, 
     'contact_email_on_error':'error_contact@test.com', 
     'dallinger_email_address':'test@example.com', 
     'database_size':'standard-0', 
     'redis_size':'premium-0', 
     'database_url':'postgresql://postgres@localhost/dallinger', 
     'description':'fake HIT description', 
     'duration':1.0, 
     'dyno_type':'free', 
     'heroku_auth_token':'heroku secret', 
     'heroku_python_version':'3.6.10', 
     'heroku_team':'', 
     'host':'0.0.0.0', 
     'id':'some experiment uid', 
     'keywords':'kw1, kw2, kw3', 
     'lifetime':1, 
     'logfile':'-', 
     'loglevel':0, 
     'mode':'debug', 
     'num_dynos_web':1, 
     'num_dynos_worker':1, 
     'organization_name':'Monsters University', 
     'sentry':True, 
     'smtp_host':'smtp.fakehost.com:587', 
     'smtp_username':'fake email username', 
     'smtp_password':'fake email password', 
     'threads':'1', 
     'title':'fake experiment title', 
     'us_only':True, 
     'webdriver_type':'phantomjs', 
     'whimsical':True, 
     'replay':False, 
     'worker_multiplier':1.5}
    from dallinger.config import default_keys
    from dallinger.config import Configuration
    config = Configuration()
    for key in default_keys:
        (config.register)(*key)

    config.extend(defaults.copy())
    config.load = mock.Mock(side_effect=(lambda : setattr(config, 'ready', True)))
    config.ready = True
    return config


@pytest.fixture
def active_config(stub_config):
    """Loads the standard config as the active configuration returned by
    dallinger.config.get_config() and returns it.
    """
    from dallinger import config as c
    orig_config = c.config
    c.config = stub_config
    yield c.config
    c.config = orig_config


@pytest.fixture
def db_session():
    import dallinger.db
    dallinger.db.session.close()
    session = dallinger.db.init_db(drop_all=True)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def a(db_session):
    """ Provides a standard way of building model objects in tests.

        def test_using_all_defaults(self, a):
            assert a.info()

        def test_with_participant_node(self, a):
            participant = a.participant(worker_id=42)
            info = a.info(origin=a.node(participant=participant))
    """

    class ModelFactory(object):

        def __init__(self, db):
            self.db = db

        def agent(self, **kw):
            defaults = {'network': self.network}
            defaults.update(kw)
            return self._build(nodes.Agent, defaults)

        def info(self, **kw):
            defaults = {'origin':self.star, 
             'contents':None}
            defaults.update(kw)
            return self._build(models.Info, defaults)

        def gene(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(information.Gene, defaults)

        def meme(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(information.Meme, defaults)

        def participant(self, **kw):
            defaults = {'recruiter_id':'hotair', 
             'worker_id':'1', 
             'assignment_id':'1', 
             'hit_id':'1', 
             'mode':'test'}
            defaults.update(kw)
            return self._build(models.Participant, defaults)

        def network(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(models.Network, defaults)

        def burst(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.Burst, defaults)

        def chain(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.Chain, defaults)

        def delayed_chain(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.DelayedChain, defaults)

        def empty(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.Empty, defaults)

        def fully_connected(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.FullyConnected, defaults)

        def replicator(self, **kw):
            defaults = {'network': self.network}
            defaults.update(kw)
            return self._build(nodes.ReplicatorAgent, defaults)

        def scale_free(self, **kw):
            defaults = {'m0':1, 
             'm':1}
            defaults.update(kw)
            return self._build(networks.ScaleFree, defaults)

        def sequential_microsociety(self, **kw):
            defaults = {'n': 1}
            defaults.update(kw)
            return self._build(networks.SequentialMicrosociety, defaults)

        def split_sample(self, **kw):
            defaults = {}
            defaults.update(kw)
            return self._build(networks.SplitSampleNetwork, defaults)

        def star(self, **kw):
            defaults = {'max_size': 2}
            defaults.update(kw)
            return self._build(networks.Star, defaults)

        def node(self, **kw):
            defaults = {'network': self.star}
            defaults.update(kw)
            return self._build(models.Node, defaults)

        def source(self, **kw):
            defaults = {'network': self.star}
            defaults.update(kw)
            return self._build(nodes.RandomBinaryStringSource, defaults)

        def _build(self, klass, attrs):
            for k, v in attrs.items():
                if callable(v):
                    attrs[k] = v()

            obj = klass(**attrs)
            self._insert(obj)
            return obj

        def _insert(self, thing):
            db_session.add(thing)
            db_session.flush()

    return ModelFactory(db_session)


@pytest.fixture
def webapp(active_config):
    from dallinger.experiment_server import sockets
    app = sockets.app
    app.root_path = os.getcwd()
    app.config.update({'DEBUG':True,  'TESTING':True})
    client = app.test_client()
    yield client


@pytest.fixture
def test_request(webapp):
    return webapp.application.test_request_context


@pytest.fixture
def debug_experiment(request, env, clear_workers):
    timeout = pytest.config.getvalue('recruiter_timeout', 30)
    p = pexpect.spawn('dallinger',
      ['debug', '--no-browsers'], env=env, encoding='utf-8')
    p.logfile = sys.stdout
    try:
        p.expect_exact('Server is running', timeout=timeout)
        yield p
        if request.node.rep_setup.passed:
            if request.node.rep_call.passed:
                p.expect_exact('Experiment completed', timeout=timeout)
                p.expect_exact('Local Heroku process terminated', timeout=timeout)
    finally:
        try:
            p.sendcontrol('c')
            p.read()
        except IOError:
            pass


@pytest.fixture
def recruitment_loop(debug_experiment):

    def recruitment_looper():
        timeout = pytest.config.getvalue('recruiter_timeout', 30)
        urls = set()
        while 1:
            index = debug_experiment.expect([
             '{}: (.*)$'.format(NEW_RECRUIT_LOG_PREFIX),
             '{}'.format(CLOSE_RECRUITMENT_LOG_PREFIX)],
              timeout=timeout)
            if index == 1:
                return
            if index == 0:
                url = debug_experiment.match.group(1)
                if url in urls:
                    pass
                else:
                    urls.add(url)
                    yield url
                    time.sleep(5)

    yield recruitment_looper()


DRIVER_MAP = {'phantomjs':webdriver.PhantomJS, 
 'firefox':webdriver.Firefox, 
 'chrome':webdriver.Chrome}

def pytest_generate_tests(metafunc):
    """Runs selenium based tests using all enabled driver types"""
    driver_types = []
    for d in DRIVER_MAP:
        if metafunc.config.getvalue(d, None):
            driver_types.append(d)

    if 'selenium_recruits' in metafunc.fixturenames:
        metafunc.parametrize('selenium_recruits', driver_types, indirect=True)
    if 'bot_recruits' in metafunc.fixturenames:
        metafunc.parametrize('bot_recruits', driver_types, indirect=True)


@pytest.fixture
def selenium_recruits(request, recruitment_loop):

    def recruits():
        for url in recruitment_loop:
            kwargs = {}
            driver_class = DRIVER_MAP.get(request.param, webdriver.PhantomJS)
            if driver_class is webdriver.PhantomJS:
                tmpdirname = tempfile.mkdtemp()
                kwargs = {'service_args': ['--local-storage-path={}'.format(tmpdirname)]}
            driver = driver_class(**kwargs)
            driver.get(url)
            try:
                yield driver
            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

    yield recruits()


@pytest.fixture
def bot_recruits(request, active_config, recruitment_loop):
    driver_type = request.param or 'phantomjs'
    active_config.set('webdriver_type', driver_type)

    def recruit_bots():
        bot_class = getattr(request.module, 'PYTEST_BOT_CLASS', BotBase)
        for url in recruitment_loop:
            bot = bot_class(url)
            try:
                bot.sign_up()
                yield bot
                if bot.sign_off():
                    bot.complete_experiment('worker_complete')
                else:
                    bot.complete_experiment('worker_failed')
            finally:
                try:
                    bot.driver.quit()
                except Exception:
                    pass

    yield recruit_bots()


def pytest_addoption(parser):
    parser.addoption('--chrome', action='store_true', help='Run chrome tests')
    parser.addoption('--firefox', action='store_true', help='Run firefox tests')
    parser.addoption('--phantomjs', action='store_true', help='Run phantomjs tests')
    parser.addoption('--runslow',
      action='store_true', default=False, help='run slow tests')
    parser.addoption('--recruiter-timeout',
      type=int,
      dest='recruiter_timeout',
      default=30,
      help='Maximum time fot webdriver experiment sessions in seconds')


def wait_for_element(driver, el_id, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, el_id)))


def wait_until_clickable(driver, el_id, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, el_id)))


def wait_for_text(driver, el_id, value, removed=False, timeout=10):
    el = wait_for_element(driver, el_id, timeout)
    if value in el.text:
        if not removed:
            return el
    if removed:
        if value not in el.text:
            return el
    wait = WebDriverWait(driver, timeout)
    condition = EC.text_to_be_present_in_element((By.ID, el_id), value)
    if removed:
        wait.until_not(condition)
        if value not in el.text:
            return el
    else:
        wait.until(condition)
    if value in el.text:
        return el
    raise AttributeError