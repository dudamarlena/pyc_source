# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/platyutil/version.py
# Compiled at: 2016-03-16 11:30:00
__all__ = 'get_git_version'
import os.path
from subprocess import Popen, PIPE
RELEASE_VERSION_FILE = os.path.join(os.path.dirname(__file__), 'RELEASE-VERSION')
GIT_REPO = os.path.join(os.path.dirname(__file__), '..', '..', '.git')

def get_git_version(abbrev=4, cwd=None):
    try:
        p = Popen(['git', '--git-dir=%s' % GIT_REPO,
         'describe', '--abbrev=%d' % abbrev], stdout=PIPE, stderr=PIPE)
        stdout, _stderr = p.communicate()
        return stdout.strip()
    except Exception:
        return

    return


def read_release_version():
    try:
        with open(RELEASE_VERSION_FILE) as (f):
            return f.readline().strip()
    except Exception:
        return

    return


def write_release_version(version):
    with open(RELEASE_VERSION_FILE, 'w') as (f):
        f.write('%s\n' % version)


def get_version(abbrev=4):
    git_version = get_git_version(abbrev)
    release_version = read_release_version()
    if git_version:
        if git_version != release_version:
            write_release_version(git_version)
        return git_version
    if release_version:
        return release_version
    else:
        print '#!!! Cannot find a version number! Use <Unknown> instead.'
        return 'Unknown'


if __name__ == '__main__':
    print get_git_version()