# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/f/develop/github/pkg-init/rapidrush/utils/version.py
# Compiled at: 2019-02-03 12:58:19
# Size of source mod 2**32: 1939 bytes
import datetime, os, platform, subprocess, sys
repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_version(version):
    main = '.'.join(map(str, version[0:3]))
    sub = ''
    if version[3] != 'stable':
        mapping = {'alpha':'a', 
         'beta':'b',  'rc':'rc'}
        sub = mapping[version[3]] + str(version[4])
    return main + sub


def git_commit_hash():
    git_log = subprocess.Popen('git log --pretty=format:%H -1 HEAD',
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      shell=True,
      cwd=repo_dir,
      universal_newlines=True)
    commit_hash = git_log.communicate()[0].strip()
    return commit_hash


def git_commit_date():
    git_log = subprocess.Popen('git log --pretty=format:%ct -1 HEAD',
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      shell=True,
      cwd=repo_dir,
      universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return
    else:
        return timestamp.strftime('%Y-%m-%d__%H:%M:%S').strip()


def git_commit_count():
    git_log = subprocess.Popen('git rev-list HEAD --count',
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      shell=True,
      cwd=repo_dir,
      universal_newlines=True)
    commit_count = git_log.communicate()[0].strip()
    return commit_count


def git_describe():
    git_log = subprocess.Popen('git describe --tags',
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      shell=True,
      cwd=repo_dir,
      universal_newlines=True)
    commit_hash = git_log.communicate()[0].strip()
    return commit_hash