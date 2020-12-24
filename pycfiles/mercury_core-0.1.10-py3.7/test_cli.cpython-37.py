# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/helpers/test_cli.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 6700 bytes
import mock, pytest, six, subprocess
from mercury.common.helpers import cli
from tests.common.unit.base import MercuryCommonUnitTest

class CLIResultUnitTest(MercuryCommonUnitTest):
    __doc__ = 'Unit tests for mercury.common.helpers.cli.CLIResult'

    def test_setter(self):
        """Test setters for stdout and stderr."""
        result = cli.CLIResult('', '', 0)
        result.stdout = 'out'
        result.stderr = 'err'
        assert repr(result) == 'out'
        assert result.stderr == 'err'

    def test_decode(self):
        """Test arguments are decoded for new CLIResult instances."""
        output = 'out'
        if isinstance(output, bytes):
            output_str = output.decode(cli.CLIResult.ENCODING)
            output_bytes = output
        else:
            output_str = output
            output_bytes = output.encode(cli.CLIResult.ENCODING)
        result_str = cli.CLIResult(output_str, 'err', 0)
        result_bytes = cli.CLIResult(output_bytes, 'err', 0)
        assert isinstance(result_str.stdout, six.string_types)
        assert isinstance(result_bytes.stdout, six.string_types)


class CliRunUnitTest(MercuryCommonUnitTest):
    __doc__ = 'Unit tests for mercury.common.helpers.cli.run()'

    @mock.patch('mercury.common.helpers.cli.os.environ.copy')
    @mock.patch('subprocess.Popen')
    def test_run(self, mock_subprocess_popen, mock_os_environ):
        """Test run()"""
        mock_subprocess_popen.return_value.returncode = 0
        mock_subprocess_popen.return_value.communicate.return_value = ('out', 'err')
        mock_os_environ.return_value = {'key': 'val'}
        cli_result = cli.run('ls')
        mock_subprocess_popen.assert_called_once_with(['ls'], stdin=None,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          bufsize=1048567,
          env={'key': 'val'})
        mock_subprocess_popen.return_value.communicate.assert_called_once_with(input=None)
        assert cli_result.stdout == 'out'
        assert cli_result.stderr == 'err'
        assert cli_result.returncode == 0

    @mock.patch('mercury.common.helpers.cli.os.environ.copy')
    @mock.patch('subprocess.Popen')
    def test_run_with_input(self, mock_subprocess_popen, mock_os_environ):
        """Test run() with data passed into stdin."""
        mock_subprocess_popen.return_value.returncode = 0
        mock_subprocess_popen.return_value.communicate.return_value = ('foo', '')
        mock_os_environ.return_value = {'key': 'val'}
        cli_result = cli.run('python', _input='print "foo"')
        mock_subprocess_popen.assert_called_once_with(['python'], stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          bufsize=1048567,
          env={'key': 'val'})
        mock_subprocess_popen.return_value.communicate.assert_called_once_with(input='print "foo"')
        assert cli_result.stdout == 'foo'
        assert cli_result.stderr == ''
        assert cli_result.returncode == 0

    @mock.patch('subprocess.Popen')
    def test_run_dry_run(self, mock_subprocess_popen):
        """Test run() in dry_run mode."""
        cli_result = cli.run('ls', dry_run=True)
        mock_subprocess_popen.assert_not_called()
        mock_subprocess_popen.return_value.communicate.assert_not_called()
        assert cli_result.stdout == ''
        assert cli_result.stderr == ''
        assert cli_result.returncode == 0

    @mock.patch('subprocess.Popen')
    def test_run_popen_exception(self, mock_subprocess_popen):
        """Test run() with subprocess.Popen failing."""
        mock_subprocess_popen.side_effect = [
         OSError, ValueError]
        with pytest.raises(cli.CLIException):
            cli.run('ls', raise_exception=True)
        cli_result = cli.run('ls', raise_exception=False)
        assert cli_result.stdout == ''
        assert cli_result.stderr == "Failed while executing 'ls': "
        assert cli_result.returncode == 1
        assert mock_subprocess_popen.call_count == 2
        mock_subprocess_popen.return_value.communicate.assert_not_called()

    @mock.patch('subprocess.Popen')
    def test_run_error(self, mock_subprocess_popen):
        """Test run() when the command returns an error."""
        mock_subprocess_popen.return_value.returncode = 1
        mock_subprocess_popen.return_value.communicate.return_value = ('', 'err')
        with pytest.raises(cli.CLIException):
            cli.run('ls', raise_exception=True)
        cli_result = cli.run('ls', raise_exception=False)
        assert cli_result.stdout == ''
        assert cli_result.stderr == 'err'
        assert cli_result.returncode == 1
        assert mock_subprocess_popen.call_count == 2
        assert mock_subprocess_popen.return_value.communicate.call_count == 2


@mock.patch('mercury.common.helpers.cli.os.path.exists')
def test_find_in_path(mock_os_path_exists):
    """Test find_in_path()."""
    mock_os_path_exists.return_value = True
    path = cli.find_in_path('/does/not/exist')
    assert path == '/does/not/exist'
    with mock.patch.dict('os.environ', {'PATH': '/:/tmp'}):
        path = cli.find_in_path('foo')
        assert path == '/foo'
    mock_os_path_exists.return_value = False
    path = cli.find_in_path('/tmp/foo')
    assert path is None