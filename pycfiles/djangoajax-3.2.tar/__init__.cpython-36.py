# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yceruto/github/yceruto/django-ajax/django_ajax/__init__.py
# Compiled at: 2020-01-25 07:24:07
# Size of source mod 2**32: 1899 bytes
"""
Init
"""
from __future__ import unicode_literals
import datetime, os, subprocess
VERSION = (3, 2, 0, 'final', 0)

def get_version(version=None):
    """
    Returns a PEP 386-compliant version number from VERSION.
    """
    if not version:
        version = VERSION
    elif not len(version) == 5:
        raise AssertionError
    else:
        assert version[3] in ('alpha', 'beta', 'rc', 'final')
        parts = 2 if version[2] == 0 else 3
        main = '.'.join(str(x) for x in version[:parts])
        sub = ''
        if version[3] == 'alpha' and version[4] == 0:
            git_changeset = get_git_changeset()
            if git_changeset:
                sub = '.dev%s' % git_changeset
        elif version[3] != 'final':
            mapping = {'alpha':'a', 
             'beta':'b',  'rc':'c'}
            sub = mapping[version[3]] + str(version[4])
    return str(main + sub)


def get_git_changeset():
    """
    Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD', stdout=(subprocess.PIPE),
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
        return timestamp.strftime('%Y%m%d%H%M%S')