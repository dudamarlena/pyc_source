# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/packageutils/version.py
# Compiled at: 2010-02-10 15:33:50
__all__ = 'get_git_version'
from subprocess import Popen, PIPE

def call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()
    except:
        return

    return


def read_release_version():
    try:
        f = open('RELEASE-VERSION', 'r')
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()

    except:
        return

    return


def write_release_version(version):
    f = open('RELEASE-VERSION', 'w')
    f.write('%s\n' % version)
    f.close()


def get_git_version(abbrev=4):
    release_version = read_release_version()
    version = call_git_describe(abbrev)
    if version is None:
        version = release_version
    if version is None:
        raise ValueError('Cannot find the version number!')
    if version != release_version:
        write_release_version(version)
    return version


if __name__ == '__main__':
    print get_git_version()