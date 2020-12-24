# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\native_git.py
# Compiled at: 2019-09-05 14:04:47
# Size of source mod 2**32: 1235 bytes
""" For interacting with git via the shell. Requires git to be in PATH """
import subprocess
DEFAULT_GIT_CONFIG_STRING = [
 '-c', "user.name='Foo Bar'", '-c', "user.email='foo@example.com'"]
DEFAULT_GIT_ENV = {'GIT_COMMITTER_NAME':'Foo Bar',  'GIT_COMMITTER_EMAIL':'foo@example.com', 
 'GIT_CONFIG_NOSYSTEM':'1'}

def bundle(repo_path, bundle_abspath):
    print('Bundling', repo_path, 'to', bundle_abspath)
    subprocess.check_call((['git'] + DEFAULT_GIT_CONFIG_STRING + [
     'bundle', 'create', bundle_abspath, '--all']),
      cwd=repo_path,
      env=DEFAULT_GIT_ENV)


def clone(url, repo_path, *clone_args):
    subprocess.check_call([
     'git'] + DEFAULT_GIT_CONFIG_STRING + ['clone'] + DEFAULT_GIT_CONFIG_STRING + list(clone_args) + ['--', url, repo_path])


def add_remote(repo_path, remote):
    subprocess.call(['git'] + DEFAULT_GIT_CONFIG_STRING + [
     'remote', 'add', 'origin', remote])
    subprocess.check_call(['git'] + DEFAULT_GIT_CONFIG_STRING + [
     'remote', 'set-url', 'origin', remote])