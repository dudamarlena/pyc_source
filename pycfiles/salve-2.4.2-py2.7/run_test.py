# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/unit/cli/run_test.py
# Compiled at: 2015-11-06 23:45:35
import mock
from nose.tools import istest
from salve import cli
from tests.util import ensure_except

@istest
def run_on_deploy_subcommand():
    """
    Unit: Run With Deploy Subcommand
    Verifies that running on arguments starting with "deploy" correctly invokes
    the deploy main method.
    """
    fake_argv = [
     './salve.py', 'deploy', '-m', '/a/b/c.manifest']
    fake_main = mock.Mock()
    with mock.patch('sys.argv', fake_argv):
        with mock.patch('salve.cli.deploy.main', fake_main):
            cli.main()
    assert fake_main.called


@istest
def old_python_version_errors():
    """
    Unit: Run On Python < 2.5 Exits
    Verifies that running on arguments starting with "backup" correctly invokes
    the backup main method.
    """
    with mock.patch('sys.version_info', (2, 5)):
        ensure_except(SystemExit, cli.main)