# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/test_self.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 24254 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, configparser, contextlib, json, os, re, subprocess, sys, tempfile, textwrap
from io import StringIO
from os.path import abspath, dirname, join
from unittest import mock
import pytest
from pylint import utils
from pylint.lint import Run
from pylint.reporters import BaseReporter, JSONReporter
from pylint.reporters.text import *
HERE = abspath(dirname(__file__))

@contextlib.contextmanager
def _patch_streams(out):
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


@contextlib.contextmanager
def _configure_lc_ctype(lc_ctype):
    lc_ctype_env = 'LC_CTYPE'
    original_lctype = os.environ.get(lc_ctype_env)
    os.environ[lc_ctype_env] = lc_ctype
    try:
        yield
    finally:
        os.environ.pop(lc_ctype_env)
        if original_lctype:
            os.environ[lc_ctype_env] = original_lctype


class MultiReporter(BaseReporter):

    def __init__(self, reporters):
        self._reporters = reporters
        self.path_strip_prefix = os.getcwd() + os.sep

    def on_set_current_module(self, *args, **kwargs):
        for rep in self._reporters:
            (rep.on_set_current_module)(*args, **kwargs)

    def handle_message(self, msg):
        for rep in self._reporters:
            rep.handle_message(msg)

    def display_reports(self, layout):
        pass

    @property
    def out(self):
        return self._reporters[0].out

    @property
    def linter(self):
        return self._linter

    @linter.setter
    def linter(self, value):
        self._linter = value
        for rep in self._reporters:
            rep.linter = value


class TestRunTC(object):

    def _runtest(self, args, reporter=None, out=None, code=None):
        if out is None:
            out = StringIO()
        else:
            pylint_code = self._run_pylint(args, reporter=reporter, out=out)
            if reporter:
                output = reporter.out.getvalue()
            else:
                if hasattr(out, 'getvalue'):
                    output = out.getvalue()
                else:
                    output = None
            msg = 'expected output status %s, got %s' % (code, pylint_code)
            if output is not None:
                msg = '%s. Below pylint output: \n%s' % (msg, output)
            @py_assert1 = pylint_code == code
            if @py_assert1 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=114)
            @py_format3 = @py_assert1 or @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (pylint_code, code)) % {'py0':@pytest_ar._saferepr(pylint_code) if 'pylint_code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pylint_code) else 'pylint_code',  'py2':@pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
            @py_format5 = (@pytest_ar._format_assertmsg(msg) + '\n>assert %(py4)s') % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def _run_pylint(self, args, out, reporter=None):
        args = args + ['--persistent=no']
        with _patch_streams(out):
            with pytest.raises(SystemExit) as (cm):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    Run(args, reporter=reporter)
            return cm.value.code

    def _clean_paths(self, output):
        """Remove version-specific tox parent directories from paths."""
        return re.sub('^py.+/site-packages/',
          '', (output.replace('\\', '/')), flags=(re.MULTILINE))

    def _test_output(self, args, expected_output):
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue())
        @py_assert1 = expected_output.strip
        @py_assert3 = @py_assert1()
        @py_assert7 = actual_output.strip
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 in @py_assert9
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=135)
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('in', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.strip\n}()\n} in %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.strip\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(actual_output) if 'actual_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_output) else 'actual_output',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None

    def test_pkginfo(self):
        """Make pylint check itself."""
        self._runtest(['pylint.__pkginfo__'], reporter=(TextReporter(StringIO())), code=0)

    def test_all(self):
        """Make pylint check itself."""
        reporters = [
         TextReporter(StringIO()),
         ColorizedTextReporter(StringIO()),
         JSONReporter(StringIO())]
        self._runtest([
         join(HERE, 'functional/arguments.py')],
          reporter=(MultiReporter(reporters)),
          code=2)

    def test_no_ext_file(self):
        self._runtest([join(HERE, 'input', 'noext')], code=0)

    def test_w0704_ignored(self):
        self._runtest([join(HERE, 'input', 'ignore_except_pass_by_default.py')], code=0)

    def test_exit_zero(self):
        self._runtest([
         '--exit-zero', join(HERE, 'regrtest_data', 'syntax_error.py')],
          code=0)

    def test_generate_config_option(self):
        self._runtest(['--generate-rcfile'], code=0)

    def test_generate_config_option_order(self):
        out1 = StringIO()
        out2 = StringIO()
        self._runtest(['--generate-rcfile'], code=0, out=out1)
        self._runtest(['--generate-rcfile'], code=0, out=out2)
        output1 = out1.getvalue()
        output2 = out2.getvalue()
        @py_assert1 = output1 == output2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=175)
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (output1, output2)) % {'py0':@pytest_ar._saferepr(output1) if 'output1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output1) else 'output1',  'py2':@pytest_ar._saferepr(output2) if 'output2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output2) else 'output2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_generate_config_disable_symbolic_names(self):
        out = StringIO()
        self._run_pylint(['--generate-rcfile', '--rcfile='], out=out)
        output = out.getvalue()
        master = re.search('\\[MASTER', output)
        out = StringIO(output[master.start():])
        parser = configparser.RawConfigParser()
        parser.read_file(out)
        messages = utils._splitstrip(parser.get('MESSAGES CONTROL', 'disable'))
        @py_assert0 = 'suppressed-message'
        @py_assert2 = @py_assert0 in messages
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=192)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, messages)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(messages) if 'messages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(messages) else 'messages'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_generate_rcfile_no_obsolete_methods(self):
        out = StringIO()
        self._run_pylint(['--generate-rcfile'], out=out)
        output = out.getvalue()
        @py_assert0 = 'profile'
        @py_assert2 = @py_assert0 not in output
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=198)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, output)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None

    def test_inexisting_rcfile(self):
        out = StringIO()
        with pytest.raises(IOError) as (excinfo):
            self._run_pylint(['--rcfile=/tmp/norcfile.txt'], out=out)
        @py_assert0 = "The config file /tmp/norcfile.txt doesn't exist!"
        @py_assert5 = excinfo.value
        @py_assert7 = str(@py_assert5)
        @py_assert2 = @py_assert0 == @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=204)
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.value\n})\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4':@pytest_ar._saferepr(excinfo) if 'excinfo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(excinfo) else 'excinfo',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None

    def test_help_message_option(self):
        self._runtest(['--help-msg', 'W0101'], code=0)

    def test_error_help_message_option(self):
        self._runtest(['--help-msg', 'WX101'], code=0)

    def test_error_missing_arguments(self):
        self._runtest([], code=32)

    def test_no_out_encoding(self):
        """test redirection of stdout with non ascii caracters
        """
        if sys.version_info < (3, 0):
            strio = tempfile.TemporaryFile()
        else:
            strio = StringIO()
        @py_assert1 = strio.encoding
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=225)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.encoding\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(strio) if 'strio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strio) else 'strio',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        self._runtest([
         join(HERE, 'regrtest_data/no_stdout_encoding.py'), '--enable=all'],
          out=strio,
          code=28)

    def test_parallel_execution(self):
        self._runtest([
         '-j 2',
         join(HERE, 'functional/arguments.py'),
         join(HERE, 'functional/arguments.py')],
          code=2)

    def test_parallel_execution_missing_arguments(self):
        self._runtest(['-j 2', 'not_here', 'not_here_too'], code=1)

    def test_py3k_option(self):
        rc_code = 0
        self._runtest([
         join(HERE, 'functional', 'unpacked_exceptions.py'), '--py3k'],
          code=rc_code)

    def test_py3k_jobs_option(self):
        rc_code = 0
        self._runtest([
         join(HERE, 'functional', 'unpacked_exceptions.py'), '--py3k', '-j 2'],
          code=rc_code)

    @pytest.mark.skipif((sys.version_info[0] > 2), reason='Requires the --py3k flag.')
    def test_py3k_commutative_with_errors_only(self):
        module = join(HERE, 'regrtest_data', 'py3k_error_flag.py')
        expected = textwrap.dedent('\n        ************* Module py3k_error_flag\n        Explicit return in __init__\n        ')
        self._test_output([
         module, '-E', "--msg-template='{msg}'"],
          expected_output=expected)
        expected = textwrap.dedent('\n        ************* Module py3k_error_flag\n        Use raise ErrorClass(args) instead of raise ErrorClass, args.\n        ')
        self._test_output([
         module, '-E', '--py3k', "--msg-template='{msg}'"],
          expected_output=expected)
        self._test_output([
         module, '--py3k', '-E', "--msg-template='{msg}'"],
          expected_output=expected)

    @pytest.mark.skipif((sys.version_info[0] > 2), reason='Requires the --py3k flag.')
    def test_py3k_commutative_with_config_disable(self):
        module = join(HERE, 'regrtest_data', 'py3k_errors_and_warnings.py')
        rcfile = join(HERE, 'regrtest_data', 'py3k-disabled.rc')
        cmd = [module, "--msg-template='{msg}'", '--reports=n']
        expected = textwrap.dedent('\n        ************* Module py3k_errors_and_warnings\n        import missing `from __future__ import absolute_import`\n        Use raise ErrorClass(args) instead of raise ErrorClass, args.\n        Calling a dict.iter*() method\n        print statement used\n        ')
        self._test_output((cmd + ['--py3k']), expected_output=expected)
        expected = textwrap.dedent('\n        ************* Module py3k_errors_and_warnings\n        Use raise ErrorClass(args) instead of raise ErrorClass, args.\n        Calling a dict.iter*() method\n        print statement used\n        ')
        self._test_output((cmd + ['--py3k', '--rcfile', rcfile]),
          expected_output=expected)
        expected = textwrap.dedent('\n        ************* Module py3k_errors_and_warnings\n        Use raise ErrorClass(args) instead of raise ErrorClass, args.\n        print statement used\n        ')
        self._test_output((cmd + ['--py3k', '-E', '--rcfile', rcfile]),
          expected_output=expected)
        self._test_output((cmd + ['-E', '--py3k', '--rcfile', rcfile]),
          expected_output=expected)

    def test_abbreviations_are_not_supported(self):
        expected = 'no such option: --load-plugin'
        self._test_output(['.', '--load-plugin'], expected_output=expected)

    def test_enable_all_works(self):
        module = join(HERE, 'data', 'clientmodule_test.py')
        expected = textwrap.dedent("\n        ************* Module data.clientmodule_test\n        pylint/test/data/clientmodule_test.py:10:8: W0612: Unused variable 'local_variable' (unused-variable)\n        pylint/test/data/clientmodule_test.py:18:4: C0111: Missing method docstring (missing-docstring)\n        pylint/test/data/clientmodule_test.py:22:0: C0111: Missing class docstring (missing-docstring)\n        ")
        self._test_output([
         module, '--disable=all', '--enable=all', '-rn'],
          expected_output=expected)

    def test_wrong_import_position_when_others_disabled(self):
        expected_output = textwrap.dedent('\n        ************* Module wrong_import_position\n        pylint/test/regrtest_data/wrong_import_position.py:11:0: C0413: Import "import os" should be placed at the top of the module (wrong-import-position)\n        ')
        module1 = join(HERE, 'regrtest_data', 'import_something.py')
        module2 = join(HERE, 'regrtest_data', 'wrong_import_position.py')
        args = [
         module2,
         module1,
         '--disable=all',
         '--enable=wrong-import-position',
         '-rn',
         '-sn']
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue().strip())
        to_remove = 'No config file found, using default configuration'
        if to_remove in actual_output:
            actual_output = actual_output[len(to_remove):]
        if actual_output.startswith('Using config file '):
            actual_output = actual_output[actual_output.find('\n'):]
        @py_assert1 = expected_output.strip
        @py_assert3 = @py_assert1()
        @py_assert7 = actual_output.strip
        @py_assert9 = @py_assert7()
        @py_assert5 = @py_assert3 == @py_assert9
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=380)
        if not @py_assert5:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.strip\n}()\n} == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s.strip\n}()\n}', ), (@py_assert3, @py_assert9)) % {'py0':@pytest_ar._saferepr(expected_output) if 'expected_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_output) else 'expected_output',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(actual_output) if 'actual_output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual_output) else 'actual_output',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None

    def test_import_itself_not_accounted_for_relative_imports(self):
        expected = 'Your code has been rated at 10.00/10'
        package = join(HERE, 'regrtest_data', 'dummy')
        self._test_output([
         package, '--disable=locally-disabled', '-rn'],
          expected_output=expected)

    def test_reject_empty_indent_strings(self):
        expected = "indent string can't be empty"
        module = join(HERE, 'data', 'clientmodule_test.py')
        self._test_output([module, '--indent-string='], expected_output=expected)

    def test_json_report_when_file_has_syntax_error(self):
        out = StringIO()
        module = join(HERE, 'regrtest_data', 'syntax_error.py')
        self._runtest([module], code=2, reporter=(JSONReporter(out)))
        output = json.loads(out.getvalue())
        @py_assert3 = isinstance(output, list)
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=399)
        if not @py_assert3:
            @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        @py_assert2 = len(output)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=400)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert1 = output[0]
        @py_assert4 = isinstance(@py_assert1, dict)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=401)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        expected = {'obj':'', 
         'column':0, 
         'line':1, 
         'type':'error', 
         'symbol':'syntax-error', 
         'module':'syntax_error'}
        message = output[0]
        for key, value in expected.items():
            @py_assert1 = key in message
            if @py_assert1 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=412)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (key, message)) % {'py0':@pytest_ar._saferepr(key) if 'key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key) else 'key',  'py2':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None
            @py_assert0 = message[key]
            @py_assert2 = @py_assert0 == value
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=413)
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None

        @py_assert0 = 'invalid syntax'
        @py_assert3 = message['message']
        @py_assert5 = @py_assert3.lower
        @py_assert7 = @py_assert5()
        @py_assert2 = @py_assert0 in @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=414)
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.lower\n}()\n}', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_json_report_when_file_is_missing(self):
        out = StringIO()
        module = join(HERE, 'regrtest_data', 'totally_missing.py')
        self._runtest([module], code=1, reporter=(JSONReporter(out)))
        output = json.loads(out.getvalue())
        @py_assert3 = isinstance(output, list)
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=421)
        if not @py_assert3:
            @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        @py_assert2 = len(output)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=422)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert1 = output[0]
        @py_assert4 = isinstance(@py_assert1, dict)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=423)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        expected = {'obj':'', 
         'column':0, 
         'line':1, 
         'type':'fatal', 
         'symbol':'fatal', 
         'module':module}
        message = output[0]
        for key, value in expected.items():
            @py_assert1 = key in message
            if @py_assert1 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=434)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (key, message)) % {'py0':@pytest_ar._saferepr(key) if 'key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key) else 'key',  'py2':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None
            @py_assert0 = message[key]
            @py_assert2 = @py_assert0 == value
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=435)
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None

        @py_assert0 = message['message']
        @py_assert2 = @py_assert0.startswith
        @py_assert4 = 'No module named'
        @py_assert6 = @py_assert2(@py_assert4)
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=436)
        if not @py_assert6:
            @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}' % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_json_report_does_not_escape_quotes(self):
        out = StringIO()
        module = join(HERE, 'regrtest_data', 'unused_variable.py')
        self._runtest([module], code=4, reporter=(JSONReporter(out)))
        output = json.loads(out.getvalue())
        @py_assert3 = isinstance(output, list)
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=443)
        if not @py_assert3:
            @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py4':@pytest_ar._saferepr(@py_assert3)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert3 = None
        @py_assert2 = len(output)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=444)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert1 = output[0]
        @py_assert4 = isinstance(@py_assert1, dict)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=445)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        expected = {'symbol':'unused-variable', 
         'module':'unused_variable', 
         'column':4, 
         'message':"Unused variable 'variable'", 
         'message-id':'W0612', 
         'line':4, 
         'type':'warning'}
        message = output[0]
        for key, value in expected.items():
            @py_assert1 = key in message
            if @py_assert1 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=457)
            if not @py_assert1:
                @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (key, message)) % {'py0':@pytest_ar._saferepr(key) if 'key' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(key) else 'key',  'py2':@pytest_ar._saferepr(message) if 'message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(message) else 'message'}
                @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = None
            @py_assert0 = message[key]
            @py_assert2 = @py_assert0 == value
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=458)
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None

    def test_information_category_disabled_by_default(self):
        expected = 'Your code has been rated at 10.00/10'
        path = join(HERE, 'regrtest_data', 'meta.py')
        self._test_output([path], expected_output=expected)

    def test_error_mode_shows_no_score(self):
        expected_output = textwrap.dedent("\n        ************* Module application_crash\n        pylint/test/regrtest_data/application_crash.py:1:6: E0602: Undefined variable 'something_undefined' (undefined-variable)\n        ")
        module = join(HERE, 'regrtest_data', 'application_crash.py')
        self._test_output([module, '-E'], expected_output=expected_output)

    def test_evaluation_score_shown_by_default(self):
        expected_output = 'Your code has been rated at '
        module = join(HERE, 'regrtest_data', 'application_crash.py')
        self._test_output([module], expected_output=expected_output)

    def test_confidence_levels(self):
        expected = 'Your code has been rated at'
        path = join(HERE, 'regrtest_data', 'meta.py')
        self._test_output([
         path, '--confidence=HIGH,INFERENCE'],
          expected_output=expected)

    def test_bom_marker(self):
        path = join(HERE, 'regrtest_data', 'meta.py')
        config_path = join(HERE, 'regrtest_data', '.pylintrc')
        expected = 'Your code has been rated at 10.00/10'
        self._test_output([
         path, '--rcfile=%s' % config_path, '-rn'],
          expected_output=expected)

    def test_pylintrc_plugin_duplicate_options(self):
        dummy_plugin_path = join(HERE, 'regrtest_data', 'dummy_plugin')
        sys.path.append(dummy_plugin_path)
        config_path = join(HERE, 'regrtest_data', 'dummy_plugin.rc')
        expected = ':dummy-message-01 (I9061): *Dummy short desc 01*\n  Dummy long desc This message belongs to the dummy_plugin checker.\n\n:dummy-message-02 (I9060): *Dummy short desc 02*\n  Dummy long desc This message belongs to the dummy_plugin checker.'
        self._test_output([
         '--rcfile=%s' % config_path,
         '--help-msg=dummy-message-01,dummy-message-02'],
          expected_output=expected)
        expected = '[DUMMY_PLUGIN]\n\n# Dummy option 1\ndummy_option_1=dummy value 1\n\n# Dummy option 2\ndummy_option_2=dummy value 2'
        self._test_output([
         '--rcfile=%s' % config_path, '--generate-rcfile'],
          expected_output=expected)
        sys.path.remove(dummy_plugin_path)

    def test_pylintrc_comments_in_values(self):
        path = join(HERE, 'regrtest_data', 'test_pylintrc_comments.py')
        config_path = join(HERE, 'regrtest_data', 'comments_pylintrc')
        expected = textwrap.dedent('\n        ************* Module test_pylintrc_comments\n        pylint/test/regrtest_data/test_pylintrc_comments.py:2:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)\n        pylint/test/regrtest_data/test_pylintrc_comments.py:1:0: C0111: Missing module docstring (missing-docstring)\n        pylint/test/regrtest_data/test_pylintrc_comments.py:1:0: C0111: Missing function docstring (missing-docstring)\n        ')
        self._test_output([
         path, '--rcfile=%s' % config_path, '-rn'],
          expected_output=expected)

    def test_no_crash_with_formatting_regex_defaults(self):
        self._runtest([
         '--ignore-patterns=a'],
          reporter=(TextReporter(StringIO())), code=32)

    def test_getdefaultencoding_crashes_with_lc_ctype_utf8(self):
        expected_output = textwrap.dedent("\n        ************* Module application_crash\n        pylint/test/regrtest_data/application_crash.py:1:6: E0602: Undefined variable 'something_undefined' (undefined-variable)\n        ")
        module = join(HERE, 'regrtest_data', 'application_crash.py')
        with _configure_lc_ctype('UTF-8'):
            self._test_output([module, '-E'], expected_output=expected_output)

    @pytest.mark.skipif((sys.platform == 'win32'), reason='only occurs on *nix')
    def test_parseable_file_path(self):
        file_name = 'test_target.py'
        fake_path = HERE + os.getcwd()
        module = join(fake_path, file_name)
        try:
            os.makedirs(fake_path)
            with open(module, 'w') as (test_target):
                test_target.write('a,b = object()')
            self._test_output([
             module, '--output-format=parseable'],
              expected_output=(join(os.getcwd(), file_name)))
        finally:
            os.remove(module)
            os.removedirs(fake_path)

    @pytest.mark.parametrize('input_path,module,expected_path', [
     (
      join(HERE, 'mymodule.py'), 'mymodule', 'pylint/test/mymodule.py'),
     ('mymodule.py', 'mymodule', 'mymodule.py')])
    def test_stdin(self, input_path, module, expected_path):
        expected_output = '************* Module {module}\n{path}:1:0: C0111: Missing module docstring (missing-docstring)\n{path}:1:0: W0611: Unused import os (unused-import)\n\n'.format(path=expected_path,
          module=module)
        with mock.patch('pylint.lint._read_stdin',
          return_value='import os\n') as (mock_stdin):
            self._test_output([
             '--from-stdin', input_path],
              expected_output=expected_output)
            @py_assert1 = mock_stdin.call_count
            @py_assert4 = 1
            @py_assert3 = @py_assert1 == @py_assert4
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=594)
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.call_count\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(mock_stdin) if 'mock_stdin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_stdin) else 'mock_stdin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_stdin_missing_modulename(self):
        self._runtest(['--from-stdin'], code=32)

    @pytest.mark.parametrize('write_bpy_to_disk', [False, True])
    def test_relative_imports(self, write_bpy_to_disk, tmpdir):
        a = tmpdir.join('a')
        b_code = textwrap.dedent("\n            from .c import foobar\n            from .d import bla  # module does not exist\n\n            foobar('hello')\n            bla()\n            ")
        c_code = textwrap.dedent('\n            def foobar(arg):\n                pass\n            ')
        a.mkdir()
        a.join('__init__.py').write('')
        if write_bpy_to_disk:
            a.join('b.py').write(b_code)
        a.join('c.py').write(c_code)
        curdir = os.getcwd()
        try:
            os.chdir(str(tmpdir))
            expected = "************* Module a.b\na/b.py:1:0: C0111: Missing module docstring (missing-docstring)\na/b.py:3:0: E0401: Unable to import 'a.d' (import-error)\n\n"
            if write_bpy_to_disk:
                self._test_output(['a/b.py'], expected_output=expected)
            with mock.patch('pylint.lint._read_stdin', return_value=b_code):
                self._test_output([
                 '--from-stdin', join('a', 'b.py')],
                  expected_output=expected)
        finally:
            os.chdir(curdir)

    def test_version(self):

        def check(lines):
            @py_assert0 = lines[0]
            @py_assert2 = @py_assert0.startswith
            @py_assert4 = 'pylint '
            @py_assert6 = @py_assert2(@py_assert4)
            if @py_assert6 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=652)
            if not @py_assert6:
                @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}' % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
            @py_assert0 = lines[1]
            @py_assert2 = @py_assert0.startswith
            @py_assert4 = 'astroid '
            @py_assert6 = @py_assert2(@py_assert4)
            if @py_assert6 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=653)
            if not @py_assert6:
                @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}' % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
            @py_assert0 = lines[2]
            @py_assert2 = @py_assert0.startswith
            @py_assert4 = 'Python '
            @py_assert6 = @py_assert2(@py_assert4)
            if @py_assert6 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_self.py', lineno=654)
            if not @py_assert6:
                @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}' % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

        out = StringIO()
        self._run_pylint(['--version'], out=out)
        check(out.getvalue().splitlines())
        result = subprocess.check_output([sys.executable, '-m', 'pylint', '--version'])
        result = result.decode('utf-8')
        check(result.splitlines())