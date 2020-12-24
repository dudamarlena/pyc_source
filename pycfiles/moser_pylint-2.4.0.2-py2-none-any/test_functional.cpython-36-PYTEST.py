# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/test_functional.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 12446 bytes
"""Functional full-module tests for PyLint."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, collections, csv, io, operator, os, platform, re, sys, pytest, six
from six.moves import configparser
from pylint import checkers, interfaces, lint, reporters

class test_dialect(csv.excel):
    if sys.version_info[0] < 3:
        delimiter = b':'
        lineterminator = b'\n'
    else:
        delimiter = ':'
        lineterminator = '\n'


csv.register_dialect('test', test_dialect)

class NoFileError(Exception):
    pass


UPDATE = False

class OutputLine(collections.namedtuple('OutputLine', [
 'symbol', 'lineno', 'object', 'msg', 'confidence'])):

    @classmethod
    def from_msg(cls, msg):
        return cls(msg.symbol, msg.line, msg.obj or '', msg.msg.replace('\r\n', '\n'), msg.confidence.name if msg.confidence != interfaces.UNDEFINED else interfaces.HIGH.name)

    @classmethod
    def from_csv(cls, row):
        confidence = row[4] if len(row) == 5 else interfaces.HIGH.name
        return cls(row[0], int(row[1]), row[2], row[3], confidence)

    def to_csv(self):
        if self.confidence == interfaces.HIGH.name:
            return self[:-1]
        else:
            return self


_MESSAGE = {'msg': '[a-z][a-z\\-]+'}
_EXPECTED_RE = re.compile('\\s*#\\s*(?:(?P<line>[+-]?[0-9]+):)?(?:(?P<op>[><=]+) *(?P<version>[0-9.]+):)?\\s*\\[(?P<msgs>%(msg)s(?:,\\s*%(msg)s)*)\\]' % _MESSAGE)

def parse_python_version(str):
    return tuple(int(digit) for digit in str.split('.'))


class FunctionalTestReporter(reporters.BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []

    def display_reports(self, layout):
        """Ignore layouts."""
        pass


class FunctionalTestFile(object):
    __doc__ = 'A single functional test case file with options.'
    _CONVERTERS = {'min_pyver':parse_python_version, 
     'max_pyver':parse_python_version, 
     'requires':lambda s: s.split(',')}

    def __init__(self, directory, filename):
        self._directory = directory
        self.base = filename.replace('.py', '')
        self.options = {'min_pyver':(2, 5), 
         'max_pyver':(4, 0), 
         'requires':[],  'except_implementations':[]}
        self._parse_options()

    def _parse_options(self):
        cp = configparser.ConfigParser()
        cp.add_section('testoptions')
        try:
            cp.read(self.option_file)
        except NoFileError:
            pass

        for name, value in cp.items('testoptions'):
            conv = self._CONVERTERS.get(name, lambda v: v)
            self.options[name] = conv(value)

    @property
    def option_file(self):
        return self._file_type('.rc')

    @property
    def module(self):
        package = os.path.basename(self._directory)
        return '.'.join([package, self.base])

    @property
    def expected_output(self):
        return self._file_type('.txt', check_exists=False)

    @property
    def source(self):
        return self._file_type('.py')

    def _file_type(self, ext, check_exists=True):
        name = os.path.join(self._directory, self.base + ext)
        if not check_exists or os.path.exists(name):
            return name
        raise NoFileError


_OPERATORS = {'>':operator.gt, 
 '<':operator.lt, 
 '>=':operator.ge, 
 '<=':operator.le}

def parse_expected_output(stream):
    return [OutputLine.from_csv(row) for row in csv.reader(stream, 'test')]


def get_expected_messages(stream):
    """Parses a file and get expected messages.

    :param stream: File-like input stream.
    :returns: A dict mapping line,msg-symbol tuples to the count on this line.
    """
    messages = collections.Counter()
    for i, line in enumerate(stream):
        match = _EXPECTED_RE.search(line)
        if match is None:
            pass
        else:
            line = match.group('line')
            if line is None:
                line = i + 1
            else:
                if line.startswith('+') or line.startswith('-'):
                    line = i + 1 + int(line)
                else:
                    line = int(line)
            version = match.group('version')
            op = match.group('op')
            if version:
                required = parse_python_version(version)
                if not _OPERATORS[op](sys.version_info, required):
                    continue
            for msg_id in match.group('msgs').split(','):
                messages[(line, msg_id.strip())] += 1

    return messages


def multiset_difference(left_op, right_op):
    """Takes two multisets and compares them.

    A multiset is a dict with the cardinality of the key as the value.

    :param left_op: The expected entries.
    :param right_op: Actual entries.

    :returns: The two multisets of missing and unexpected messages.
    """
    missing = left_op.copy()
    missing.subtract(right_op)
    unexpected = {}
    for key, value in list(six.iteritems(missing)):
        if value <= 0:
            missing.pop(key)
            if value < 0:
                unexpected[key] = -value

    return (
     missing, unexpected)


class LintModuleTest(object):
    maxDiff = None

    def __init__(self, test_file):
        test_reporter = FunctionalTestReporter()
        self._linter = lint.PyLinter()
        self._linter.set_reporter(test_reporter)
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)
        self._linter.disable('I')
        try:
            self._linter.read_config_file(test_file.option_file)
            self._linter.load_config_file()
        except NoFileError:
            pass

        self._test_file = test_file

    def setUp(self):
        if self._should_be_skipped_due_to_version():
            pytest.skip('Test cannot run with Python %s.' % (sys.version.split(' ')[0],))
        else:
            missing = []
            for req in self._test_file.options['requires']:
                try:
                    __import__(req)
                except ImportError:
                    missing.append(req)

            if missing:
                pytest.skip('Requires %s to be present.' % (','.join(missing),))
            if self._test_file.options['except_implementations']:
                implementations = [item.strip() for item in self._test_file.options['except_implementations'].split(',')]
                implementation = platform.python_implementation()
                if implementation in implementations:
                    pytest.skip('Test cannot run with Python implementation %r' % (
                     implementation,))

    def _should_be_skipped_due_to_version(self):
        return sys.version_info < self._test_file.options['min_pyver'] or sys.version_info > self._test_file.options['max_pyver']

    def __str__(self):
        return '%s (%s.%s)' % (self._test_file.base, self.__class__.__module__,
         self.__class__.__name__)

    def _open_expected_file(self):
        return open(self._test_file.expected_output)

    def _open_source_file(self):
        if self._test_file.base == 'invalid_encoded_data':
            return open(self._test_file.source)
        else:
            if 'latin1' in self._test_file.base:
                return io.open((self._test_file.source), encoding='latin1')
            return io.open((self._test_file.source), encoding='utf8')

    def _get_expected(self):
        with self._open_source_file() as (fobj):
            expected_msgs = get_expected_messages(fobj)
        if expected_msgs:
            with self._open_expected_file() as (fobj):
                expected_output_lines = parse_expected_output(fobj)
        else:
            expected_output_lines = []
        return (
         expected_msgs, expected_output_lines)

    def _get_received(self):
        messages = self._linter.reporter.messages
        messages.sort(key=(lambda m: (m.line, m.symbol, m.msg)))
        received_msgs = collections.Counter()
        received_output_lines = []
        for msg in messages:
            received_msgs[(msg.line, msg.symbol)] += 1
            received_output_lines.append(OutputLine.from_msg(msg))

        return (
         received_msgs, received_output_lines)

    def _runTest(self):
        self._linter.check([self._test_file.module])
        expected_messages, expected_text = self._get_expected()
        received_messages, received_text = self._get_received()
        if expected_messages != received_messages:
            msg = [
             'Wrong results for file "%s":' % self._test_file.base]
            missing, unexpected = multiset_difference(expected_messages, received_messages)
            if missing:
                msg.append('\nExpected in testdata:')
                msg.extend(' %3d: %s' % msg for msg in sorted(missing))
            if unexpected:
                msg.append('\nUnexpected in testdata:')
                msg.extend(' %3d: %s' % msg for msg in sorted(unexpected))
            pytest.fail('\n'.join(msg))
        self._check_output_text(expected_messages, expected_text, received_text)

    def _split_lines(self, expected_messages, lines):
        emitted, omitted = [], []
        for msg in lines:
            if (msg[1], msg[0]) in expected_messages:
                emitted.append(msg)
            else:
                omitted.append(msg)

        return (
         emitted, omitted)

    def _check_output_text(self, expected_messages, expected_lines, received_lines):
        @py_assert0 = self._split_lines(expected_messages, expected_lines)[0]
        @py_assert2 = @py_assert0 == received_lines
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_functional.py', lineno=335)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, received_lines)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(received_lines) if 'received_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(received_lines) else 'received_lines'}
            @py_format6 = (@pytest_ar._format_assertmsg(self._test_file.base) + '\n>assert %(py5)s') % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


class LintModuleOutputUpdate(LintModuleTest):

    def _open_expected_file(self):
        try:
            return super(LintModuleOutputUpdate, self)._open_expected_file()
        except IOError:
            return io.StringIO()

    def _check_output_text(self, expected_messages, expected_lines, received_lines):
        if not expected_messages:
            return
        emitted, remaining = self._split_lines(expected_messages, expected_lines)
        if emitted != received_lines:
            remaining.extend(received_lines)
            remaining.sort(key=(lambda m: (m[1], m[0], m[3])))
            with open(self._test_file.expected_output, 'w') as (fobj):
                writer = csv.writer(fobj, dialect='test')
                for line in remaining:
                    writer.writerow(line.to_csv())


def get_tests():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'functional')
    suite = []
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            suite.append(FunctionalTestFile(input_dir, fname))

    return suite


TESTS = get_tests()
TESTS_NAMES = [t.base for t in TESTS]

@pytest.mark.parametrize('test_file', TESTS, ids=TESTS_NAMES)
def test_functional(test_file):
    LintTest = LintModuleOutputUpdate(test_file) if UPDATE else LintModuleTest(test_file)
    LintTest.setUp()
    LintTest._runTest()


if __name__ == '__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')
    pytest.main(sys.argv)