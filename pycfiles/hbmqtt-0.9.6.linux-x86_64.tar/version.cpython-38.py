# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/version.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1900 bytes
import datetime, os, subprocess

def get_version(version=None):
    """Returns a PEP 386-compliant version number from VERSION."""
    if version is None:
        from hbmqtt import VERSION as version
    else:
        if not len(version) == 5:
            raise AssertionError
        elif not version[3] in ('alpha', 'beta', 'rc', 'final'):
            raise AssertionError
        else:
            parts = 2 if version[2] == 0 else 3
            main = '.'.join((str(x) for x in version[:parts]))
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
    """Returns a numeric identifier of the latest git changeset.
    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
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
        return timestamp.strftime('%Y%m%d%H%M%S')