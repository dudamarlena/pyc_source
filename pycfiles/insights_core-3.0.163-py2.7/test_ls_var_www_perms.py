# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_www_perms.py
# Compiled at: 2020-04-30 14:03:01
import doctest, pytest
from insights.parsers import ls_var_www_perms
from insights.parsers.ls_var_www_perms import LsVarWwwPerms
from insights.tests import context_wrap
from insights.util.file_permissions import FilePermissions
GOOD_FOLDER_OUTPUT = '\ncrw-rw-rw-. 1 root root 1, 3 Dec 18 09:18 /dev/null\n\n/var/www:\ntotal 16\ndrwxr-xr-x.  4 root root  33 Dec 15 08:12 .\ndrwxr-xr-x. 20 root root 278 Dec 15 08:12 ..\ndrwxr-xr-x.  2 root root   6 Oct  3 09:37 cgi-bin\ndrwxr-xr-x.  2 root root   6 Oct  3 09:37 html\n'
GOOD_FOLDER_EXPECTED_OUTPUT = [
 'drwxr-xr-x.  4 root root  33 Dec 15 08:12 .',
 'drwxr-xr-x. 20 root root 278 Dec 15 08:12 ..',
 'drwxr-xr-x.  2 root root   6 Oct  3 09:37 cgi-bin',
 'drwxr-xr-x.  2 root root   6 Oct  3 09:37 html']
EMPTY_FOLDER_OUTPUT = '\ncrw-rw-rw-. 1 root root 1, 3 Dec 18 09:18 /dev/null\n\n/var/www:\ntotal 0\ndrwxr-xr-x.  4 root root  33 Dec 15 08:12 .\ndrwxr-xr-x. 20 root root 278 Dec 15 08:12 ..\n'
EMPTY_FOLDER_EXPECTED_OUTPUT = [
 'drwxr-xr-x.  4 root root  33 Dec 15 08:12 .',
 'drwxr-xr-x. 20 root root 278 Dec 15 08:12 ..']
NO_FOLDER_OUTPUT = "\n/bin/ls: cannot access '/var/www': No such file or directory\ncrw-rw-rw-. 1 root root 1, 3 Dec 18 09:18 /dev/null\n"
NO_FOLDER_EXPECTED_OUTPUT = []
OUTPUTS_FROM_FOLDERS = [
 (
  GOOD_FOLDER_OUTPUT, GOOD_FOLDER_EXPECTED_OUTPUT),
 (
  EMPTY_FOLDER_OUTPUT, EMPTY_FOLDER_EXPECTED_OUTPUT),
 (
  NO_FOLDER_OUTPUT, NO_FOLDER_EXPECTED_OUTPUT)]

@pytest.mark.parametrize('output, expected_output', OUTPUTS_FROM_FOLDERS)
def test_ls_var(output, expected_output):
    test = LsVarWwwPerms(context_wrap(output))
    assert len(test.file_permissions) == len(expected_output)
    for test_line, expected_line in zip(test.file_permissions, expected_output):
        assert repr(test_line) == repr(FilePermissions(expected_line))
        assert test_line.line == FilePermissions(expected_line).line


def test_doc_examples():
    env = {'ls_var_www_perms': LsVarWwwPerms(context_wrap(GOOD_FOLDER_OUTPUT))}
    failed, total = doctest.testmod(ls_var_www_perms, globs=env)
    assert failed == 0