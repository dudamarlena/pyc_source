# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sushi/Projects/CTU/MI-PYT_B171/labelord/tests/conftest.py
# Compiled at: 2017-11-22 03:33:06
# Size of source mod 2**32: 10065 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, configparser, json, os, subprocess, sys, requests, betamax
from betamax_serializers.pretty_json import PrettyJSONSerializer
import pytest
ABS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = ABS_PATH + '/fixtures'
CASSETTES_PATH = FIXTURES_PATH + '/cassettes'
CONFIGS_PATH = FIXTURES_PATH + '/configs'
DATA_PATH = FIXTURES_PATH + '/data'
DUMMY_TOKEN = 'thisIsNotRealToken'
BAD_TOKEN = 'thisIsBadToken'
sys.path.insert(0, ABS_PATH + '/../')

def decode_if_bytes(obj, encoding='utf-8'):
    if isinstance(obj, bytes):
        return obj.decode(encoding)
    else:
        return obj


class MissingConfigError(Exception):

    def __init__(self, *args):
        (super().__init__)(*args)


class GitHubMatcher(betamax.BaseMatcher):
    name = 'mipyt-github'

    @staticmethod
    def _has_correct_token(request, recorded_request):
        header_token = request.headers.get('Authorization', '')
        correct_token = recorded_request['headers']['Authorization']
        correct_token = correct_token.replace('<TOKEN>', DUMMY_TOKEN)
        correct_token = correct_token.replace('<BAD_TOKEN>', BAD_TOKEN)
        return header_token == correct_token

    @staticmethod
    def _has_user_agent(request):
        return request.headers.get('User-Agent', None) is not None

    @staticmethod
    def _match_body_json(request, recorded_request):
        if request.body is None:
            return recorded_request['body']['string'] == ''
        else:
            if recorded_request['body']['string'] == '':
                return False
            data1 = json.loads(recorded_request['body']['string'])
            data2 = json.loads(decode_if_bytes(request.body))
            return data1 == data2

    def match(self, request, recorded_request):
        return self._has_correct_token(request, recorded_request) and self._has_user_agent(request) and self._match_body_json(request, recorded_request)


betamax.Betamax.register_request_matcher(GitHubMatcher)
betamax.Betamax.register_serializer(PrettyJSONSerializer)
with betamax.Betamax.configure() as (config):
    config.cassette_library_dir = CASSETTES_PATH
    config.default_cassette_options['serialize_with'] = 'prettyjson'
    config.default_cassette_options['match_requests_on'] = [
     'method',
     'uri',
     'mipyt-github']
    token = os.environ.get('GITHUB_TOKEN', DUMMY_TOKEN)
    if 'GITHUB_TOKEN' in os.environ:
        config.default_cassette_options['record_mode'] = 'all'
    else:
        config.default_cassette_options['record_mode'] = 'none'
    config.define_cassette_placeholder('<TOKEN>', token)
    config.define_cassette_placeholder('<BAD_TOKEN>', BAD_TOKEN)

@pytest.fixture()
def github_maker(betamax_session):
    from labelord.github import GitHub

    def inner_maker(github_token):
        return GitHub(github_token, session=betamax_session)

    return inner_maker


@pytest.fixture()
def github_token():
    return os.environ.get('GITHUB_TOKEN', DUMMY_TOKEN)


@pytest.fixture()
def github(github_maker, github_token):
    return github_maker(github_token)


@pytest.fixture()
def github_bad_token(github_maker):
    return github_maker(BAD_TOKEN)


class Utils:
    BETAMAX_ERRORS = 0

    @staticmethod
    def config(name):
        return CONFIGS_PATH + '/' + name + '.cfg'

    @staticmethod
    def load_data(name):
        with open(DATA_PATH + '/' + name + '.json') as (f):
            return f.read()

    @staticmethod
    def create_auth(username, password):
        import base64
        return {'Authorization': 'Basic ' + base64.b64encode(bytes(username + ':' + password, 'ascii')).decode('ascii')}

    @classmethod
    def monkeypatch_betamaxerror(cls, monkeypatch):
        cls.BETAMAX_ERRORS = 0

        def monkey_init(self, message):
            super(betamax.BetamaxError, self).__init__(message)
            cls.BETAMAX_ERRORS += 1

        monkeypatch.setattr(betamax.BetamaxError, '__init__', monkey_init)


@pytest.fixture
def utils():
    return Utils()


class ModuleUtils:

    def __init__(self, cfg, tmpdir, sh):
        self.cfg = cfg
        self.tmpdir = tmpdir
        self.sh = sh

    @property
    def git(self):
        return self.cfg['commands']['git']

    @property
    def create_venv(self):
        return self.cfg['commands']['create_venv']

    @property
    def python(self):
        return str(self.tmpdir.join(self.cfg['commands']['python']))

    @property
    def pytest(self):
        return '{} -m {}'.format(self.python, self.cfg['commands']['pytest'])

    @property
    def pip(self):
        return '{} -m {}'.format(self.python, self.cfg['commands']['pip'])

    @property
    def pip_testpypi(self):
        return '{} -m {}'.format(self.python, self.cfg['commands']['pip_testpypi'])

    @staticmethod
    def ssh_github(reposlug):
        return 'git@github.com:{}.git'.format(reposlug)

    @staticmethod
    def https_github(reposlug):
        return 'https://github.com/{}.git'.format(reposlug)

    @property
    def repo_ssh(self):
        return self.cfg['vars']['repo_full']

    @property
    def repo_branch(self):
        return self.cfg['vars']['branch']

    def get_set(self, set_name):
        return frozenset(self.cfg.get('sets', set_name, fallback='').split(' '))

    def create_fresh_venv(self):
        result = self.sh(self.create_venv)
        @py_assert1 = result.was_successful
        if not @py_assert1:
            @py_format3 = (@pytest_ar._format_assertmsg('Could not create virtualenv for Python: {}'.format(result.stderr)) + '\n>assert %(py2)s\n{%(py2)s = %(py0)s.was_successful\n}') % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None

    def clone_repo(self, repo_dir):
        result = self.sh(self.git, 'clone', '-b', self.repo_branch, self.repo_ssh, repo_dir)
        @py_assert1 = result.was_successful
        if not @py_assert1:
            @py_format3 = (@pytest_ar._format_assertmsg('Could not clone the repository {}: {}'.format(self.repo_ssh, result.stderr)) + '\n>assert %(py2)s\n{%(py2)s = %(py0)s.was_successful\n}') % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format3))
        @py_assert1 = None

    def clone_repo_with_fresh_venv(self, repo_dir):
        self.create_fresh_venv()
        self.clone_repo(repo_dir)


class ShellExecutionResult:

    def __init__(self, stdout, stderr, return_code):
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code

    @property
    def was_successful(self):
        return self.return_code == 0

    @property
    def outerr(self):
        return '{}\n{}\n{}'.format(self.stdout, '-' * 80, self.stderr)


@pytest.fixture()
def config():
    ext_vars = {'LABELORD_BRANCH': 'master'}
    ext_vars.update(os.environ)
    cfg = configparser.ConfigParser(ext_vars)
    cfg.read(CONFIGS_PATH + '/test_config.cfg')
    if not cfg.has_option('vars', 'ctu_username'):
        raise MissingConfigError('CTU_USERNAME env var is missing!')
    if not cfg.has_option('vars', 'repo_full'):
        raise MissingConfigError('LABELORD_REPO env var is missing!')
    return cfg


@pytest.fixture()
def sh():

    def shell_executor(command, *args):
        p = subprocess.Popen((' '.join([command, *args])),
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          shell=True,
          universal_newlines=True)
        stdout, stderr = p.communicate()
        return ShellExecutionResult(stdout, stderr, p.returncode)

    return shell_executor


@pytest.fixture()
def moduleutils(config, tmpdir, sh):
    return ModuleUtils(config, tmpdir, sh)


class LabelordInvocation:

    def __init__(self, runner, result, session):
        self.runner = runner
        self.result = result
        self.session = session


@pytest.fixture
def invoker(betamax_session):
    from click.testing import CliRunner
    from flexmock import flexmock
    from labelord import cli

    def invoker_inner(*args, isolated=False, session_expectations=None):
        session_mock = flexmock(betamax_session or requests.Session())
        if os.environ.get('LABELORD_SESSION_SPY', '').lower() != 'off':
            if session_expectations is not None:
                for what, count in session_expectations.items():
                    session_mock.should_call(what).times(count)

        else:
            runner = CliRunner()
            args = [a for a in args if a is not None]
            if isolated:
                with runner.isolated_filesystem():
                    result = runner.invoke(cli, args, obj={'session': session_mock})
            result = runner.invoke(cli, args, obj={'session': session_mock})
        return LabelordInvocation(runner, result, session_mock)

    return invoker_inner


@pytest.fixture
def invoker_norec():
    return invoker(None)


@pytest.fixture
def client_maker(betamax_session, utils, monkeypatch):

    def inner_maker(config, own_config_path=False, session_expectations=None):
        from flexmock import flexmock
        if not own_config_path:
            config = Utils.config(config)
        session_mock = flexmock(betamax_session or requests.Session())
        utils.monkeypatch_betamaxerror(monkeypatch)
        if os.environ.get('LABELORD_SESSION_SPY', '').lower() != 'off':
            if session_expectations is not None:
                for what, count in session_expectations.items():
                    session_mock.should_call(what).times(count)

        os.environ['LABELORD_CONFIG'] = config
        from labelord import app
        app.inject_session(betamax_session)
        app.reload_config()
        client = app.test_client()
        return client

    yield inner_maker
    try:
        @py_assert1 = utils.BETAMAX_ERRORS
        @py_assert4 = 0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.BETAMAX_ERRORS\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = (@pytest_ar._format_assertmsg('There were some BetamaxErrors (although you might have caught them)!') + '\n>assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    finally:
        Utils.BETAMAX_ERRORS = 0