# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/version.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import datetime, os, subprocess

def get_version(version=None):
    """Returns a PEP 386-compliant version number from VERSION."""
    if version is None:
        from django import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')
    parts = 2 if version[2] == 0 else 3
    main = (b'.').join(str(x) for x in version[:parts])
    sub = b''
    if version[3] == b'alpha' and version[4] == 0:
        git_changeset = get_git_changeset()
        if git_changeset:
            sub = b'.dev%s' % git_changeset
    elif version[3] != b'final':
        mapping = {b'alpha': b'a', b'beta': b'b', b'rc': b'c'}
        sub = mapping[version[3]] + str(version[4])
    return str(main + sub)


def get_git_changeset():
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen(b'git log --pretty=format:%ct --quiet -1 HEAD', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=repo_dir, universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return

    return timestamp.strftime(b'%Y%m%d%H%M%S')