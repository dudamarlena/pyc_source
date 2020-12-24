# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/setuptools_git_version_cc.py
# Compiled at: 2019-05-24 05:08:39
# Size of source mod 2**32: 2408 bytes
from pkg_resources import get_distribution
import subprocess, sys

def get_git_version_cc(dist, attr, value):
    try:
        version = get_git_version()
    except:
        version = get_distribution(dist.get_name()).version

    dist.metadata.version = version


def entry_point():
    """
    """
    version = get_git_version()
    sys.stdout.write('{}'.format(version))
    sys.exit(0)


def get_git_version():
    """
    Computes the version of a git repository (in current path)
    
    The version is computed assuming that the commit messages are formatted according 
    to SemVer and Conventional Commits. The version format is the following:
    
        <major>.<minor>.<patch>-r<release>
    
    The convention used here is the following
    - 'breaking:' types increase major version (rather than 'refactor:')
    - 'feat:' types increase minor version
    - 'fix:' types increase patch version
    - any other type that conforms to '<type>:' (where <type> can be chore, ci, test, ...)
    
    :return: The version number as a string
    """
    cmd = [
     'git', 'log', '--reverse', '--pretty=oneline']
    p = subprocess.Popen(cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    major = 1
    minor = 0
    patch = 0
    release = 0
    for l in p.stdout:
        f = l.split()
        if len(f) >= 2:
            s = f[1].decode('utf-8')
            if 'breaking:' in s:
                major += 1
                minor = 0
                patch = 0
                release = 0
                continue
            if 'feat:' in s:
                minor += 1
                patch = 0
                release = 0
                continue
            if 'fix:' in s:
                patch += 1
                release = 0
                continue
            if s.endswith(':'):
                release += 1

    ver = '{}.{}.{}'.format(major, minor, patch)
    if release > 0:
        ver = ver + '-r{}'.format(release)
    return ver


if __name__ == '__main__':
    git_version = get_git_version()
    import setuptools
    original_setup = setuptools.setup

    def setup(version=None, *args, **kw):
        return original_setup(args, version=git_version, **kw)


    setuptools.setup = setup
    import setup