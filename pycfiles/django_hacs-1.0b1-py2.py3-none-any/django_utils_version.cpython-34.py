# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/django_utils_version.py
# Compiled at: 2016-04-30 06:39:51
# Size of source mod 2**32: 2503 bytes
import os, datetime, subprocess

def get_version(version=None):
    """Returns a PEP 386-compliant version number from VERSION."""
    version = get_complete_version(version)
    main = get_main_version(version)
    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev%s' % git_changeset
    elif version[3] != 'final':
        mapping = {'alpha': 'a',  'beta': 'b',  'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])
    return str(main + sub)


def get_main_version(version=None):
    """Returns main version (X.Y[.Z]) from VERSION."""
    version = get_complete_version(version)
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


def get_complete_version(version):
    """Returns a tuple of the django version. If version argument is non-empty,
    then checks for correctness of the tuple provided.
    """
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')
    return version


def get_docs_version(version=None):
    version = get_complete_version(version)
    if version[3] != 'final':
        return 'dev'
    else:
        return '%d.%d' % version[:2]


def get_git_changeset():
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=repo_dir, universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return

    return timestamp.strftime('%Y%m%d%H%M%S')