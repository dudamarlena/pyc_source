# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/__init__.py
# Compiled at: 2014-04-04 17:09:38
import subprocess, datetime, os
NAME = 'whatsnew'
VERSION = __version__ = (0, 3, 0, 'final', 0)

def get_version():
    """Derives a PEP386-compliant version number from VERSION."""
    assert len(VERSION) == 5
    assert VERSION[3] in ('alpha', 'beta', 'rc', 'final')
    parts = 2 if VERSION[2] == 0 else 3
    main = ('.').join(str(x) for x in VERSION[:parts])
    sub = ''
    if VERSION[3] == 'alpha' and VERSION[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = '.dev-%s' % git_changeset
    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[VERSION[3]] + str(VERSION[4])
    elif VERSION[3] == 'final':
        if VERSION[4] > 0:
            sub += '-%s' % VERSION[4]
    return main + sub


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