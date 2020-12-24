# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/matcher/plugin.py
# Compiled at: 2019-06-26 17:07:29
# Size of source mod 2**32: 11016 bytes
import pathlib, platform, pytest, re, shutil, sys, yaml

class _content_match_result:
    __doc__ = '\n        TODO Is this job for Python `dataclass`?\n    '

    def __init__(self, result, text, regex, filename):
        self._filename = filename
        self._result = result
        self._text = text
        self._regex = regex

    def __eq__(self, other):
        if isinstance(other, bool):
            return self._result == other
        else:
            return False

    def __bool__(self):
        return self._result

    def report_regex_mismatch(self):
        return [
         '', "The test output doesn't match to the expected regex", '(from `{}`):'.format(self._filename), '---[BEGIN actual output]---'] + self._text + ['---[END actual output]---', '---[BEGIN expected regex]---'] + self._regex.splitlines() + [
         '---[END expected regex]---']


class _content_check_or_store_pattern:

    def __init__(self, filename, store):
        self._pattern_filename = filename
        self._store = store
        self._expected_file_content = None

    def _store_pattern_handle_error(fn):

        def _inner(self, text, *args, **kwargs):
            if self._store:
                if not self._pattern_filename.parent.exists():
                    self._pattern_filename.parent.mkdir(parents=True)
                self._pattern_filename.write_text(text)
                return True
            else:
                if not self._pattern_filename.exists():
                    pytest.skip('Pattern file not found `{}`'.format(self._pattern_filename))
                    return False
                return fn(self, text, *args, **kwargs)

        return _inner

    def _read_expected_file_content(self):
        if sys.version_info >= (3, 5):
            self._expected_file_content = self._pattern_filename.read_text()
        else:
            with self._pattern_filename.open('r') as (fd):
                self._expected_file_content = fd.read()
        assert self._expected_file_content is not None

    @_store_pattern_handle_error
    def __eq__(self, text):
        self._read_expected_file_content()
        return self._expected_file_content == text

    @_store_pattern_handle_error
    def match(self, text, flags=0):
        self._read_expected_file_content()
        content = ('.*\n' if flags & re.MULTILINE else ' ').join(self._expected_file_content.strip().splitlines())
        try:
            if flags & re.MULTILINE:
                what = re.compile(('.*' + content + '.*'), flags=flags)
            else:
                what = re.compile(content, flags=flags)
        except Exception as ex:
            pytest.skip('Compile a regualar expression from the pattern has failed: {}'.format(str(ex)))
            return False

        text_lines = text.splitlines()
        m = what.fullmatch(('\n' if flags & re.MULTILINE else ' ').join(text_lines))
        return _content_match_result(m is not None and bool(m), text_lines, self._expected_file_content, self._pattern_filename)

    def report_compare_mismatch(self, actual):
        assert self._expected_file_content is not None
        return [
         '', "The test output doesn't equal to the expected", '(from `{}`):'.format(self._pattern_filename), '---[BEGIN actual output]---'] + actual.splitlines() + ['---[END actual output]---', '---[BEGIN expected output]---'] + self._expected_file_content.splitlines() + [
         '---[END expected output]---']


def _try_cli_option(request):
    result = request.config.getoption('--pm-patterns-base-dir')
    return (pathlib.Path(result) if result is not None else None, True)


def _try_ini_option(request):
    result = request.config.getini('pm-patterns-base-dir')
    return (pathlib.Path(result) if result else None, False)


def _try_module_path(request):
    assert request.fspath.dirname is not None
    return (
     pathlib.Path(request.fspath.dirname) / 'data' / 'expected', False)


def _make_expected_filename(request, ext: str, use_system_suffix=True) -> pathlib.Path:
    result = None
    use_cwd_as_base = False
    for alg in [_try_cli_option, _try_ini_option, _try_module_path]:
        result, use_cwd_as_base = alg(request)
        if result is not None:
            break

    assert result is not None
    if use_system_suffix:
        use_system_suffix = request.config.getini('pm-pattern-file-use-system-name')
        use_system_suffix = True if use_system_suffix == 'true' or use_system_suffix == '1' else False
    if not result.is_absolute():
        if use_cwd_as_base:
            result = pathlib.Path.cwd()
        else:
            if request.config.inifile is not None:
                result = pathlib.Path(request.config.inifile.dirname) / result
            elif not 0:
                raise AssertionError
    if not result.exists():
        raise pytest.skip('Base directory for pattern-matcher do not exists: `{}`'.format(result))
    if request.cls is not None:
        result /= request.cls.__name__
    result /= request.function.__name__ + ('-' + platform.system() if use_system_suffix else '') + ext
    return result


@pytest.fixture
def expected_out(request):
    """
        A pytest fixture to match `STDOUT` against a file.
    """
    return _content_check_or_store_pattern(_make_expected_filename(request, '.out'), request.config.getoption('--pm-save-patterns'))


@pytest.fixture
def expected_err(request):
    """
        A pytest fixture to match `STDERR` against a file.
    """
    return _content_check_or_store_pattern(_make_expected_filename(request, '.err'), request.config.getoption('--pm-save-patterns'))


class _yaml_check_or_store_pattern:

    def __init__(self, filename, store):
        self._expected_file = filename
        self._store = store

    def _store_pattern_file(self, result_file):
        assert self._store, 'Code review required!'
        if not self._expected_file.parent.exists():
            self._expected_file.parent.mkdir(parents=True)
        shutil.copy(str(result_file), str(self._expected_file))

    def __eq__(self, result_file):
        assert isinstance(result_file, pathlib.Path)
        if self._store:
            self._store_pattern_file(result_file)
            return True
        if not result_file.exists():
            pytest.skip('Result YAML file not found `{}`'.format(result_file))
            return False
        else:
            if not self._expected_file.exists():
                pytest.skip('Expected YAML file not found `{}`'.format(self._expected_file))
                return False
            with result_file.open('r') as (result_fd):
                with self._expected_file.open('r') as (expected_fd):
                    self._result = yaml.safe_load(result_fd)
                    self._expected = yaml.safe_load(expected_fd)
            return self._result == self._expected

    def report_compare_mismatch(self, actual):
        if not self._result is not None:
            raise AssertionError
        elif not self._expected is not None:
            raise AssertionError
        return [
         '', 'Comparing the test result (`{}`) and the expected (`{}`) YAML files:'.format(actual, self._expected_file), '---[BEGIN actual result]---'] + [repr(self._result)] + ['---[END actual result]---', '---[BEGIN expected result]---'] + [repr(self._expected)] + [
         '---[END expected result]---']


@pytest.fixture
def expected_yaml(request):
    return _yaml_check_or_store_pattern(_make_expected_filename(request, '.yaml', use_system_suffix=False), request.config.getoption('--pm-save-patterns'))


def pytest_assertrepr_compare(op, left, right):
    if op == '==':
        if isinstance(left, _content_match_result):
            if isinstance(right, bool):
                return left.report_regex_mismatch()
            else:
                if isinstance(left, _content_check_or_store_pattern):
                    if isinstance(right, str):
                        return left.report_compare_mismatch(right)
                if isinstance(right, _content_check_or_store_pattern):
                    if isinstance(left, str):
                        return right.report_compare_mismatch(left)
                if isinstance(left, _yaml_check_or_store_pattern):
                    if isinstance(right, pathlib.Path):
                        return left.report_compare_mismatch(right)
        else:
            if isinstance(right, _yaml_check_or_store_pattern):
                if isinstance(left, pathlib.Path):
                    return right.report_compare_mismatch(left)


def pytest_addoption(parser):
    group = parser.getgroup('pattern-matcher')
    group.addoption('--pm-save-patterns',
      action='store_true',
      help='store matching patterns instead of checking them')
    group.addoption('--pm-patterns-base-dir',
      metavar='PATH',
      help='base directory to read/write pattern files')
    parser.addini('pm-patterns-base-dir',
      help='base directory to read/write pattern files',
      default=None)
    parser.addini('pm-pattern-file-use-system-name',
      help='expect a system name (`platform.system()`) to be a pattern filename suffix',
      default=False)