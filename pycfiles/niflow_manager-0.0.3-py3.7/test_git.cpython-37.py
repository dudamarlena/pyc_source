# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/util/tests/test_git.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 1293 bytes
import pytest, subprocess as sp
from configparser import ConfigParser
from ..git import git_variables
GIT_AUTHOR = 'Test Author'
GIT_EMAIL = 'unreal3214@fake2182.tld'

@pytest.mark.parametrize('variables, expected, exception', [
 (
  [
   (
    'user', 'name', GIT_AUTHOR)], {'user.name': GIT_AUTHOR}, None),
 (
  [
   (
    'user', 'name', GIT_AUTHOR), ('user', 'email', GIT_EMAIL)],
  {'user.name':GIT_AUTHOR, 
   'user.email':GIT_EMAIL},
  None),
 (
  [
   (
    'user', 'name', GIT_AUTHOR), ('user', 'email', GIT_EMAIL)],
  {'user.name':GIT_AUTHOR, 
   'user.fake':'EXCEPTION'},
  KeyError)])
def test_git_variables(tmpdir, variables, expected, exception):
    sp.run(['git', '-C', str(tmpdir), 'init'], check=True)
    config = ConfigParser()
    for section, name, value in variables:
        config.setdefault(section, {})
        config[section][name] = value

    with open(tmpdir / '.git' / 'config', 'at') as (fobj):
        config.write(fobj)
    args = (tmpdir, *expected.keys())
    if exception is not None:
        (pytest.raises)(exception, git_variables, *args)
    else:
        test_vars = git_variables(*args)
        assert test_vars == expected