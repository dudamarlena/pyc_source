# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/version.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 1595 bytes
import datetime, os, subprocess
symbol = {'alpha':'a', 
 'beta':'b'}

def get_version(version, filename=None):
    if not len(version) == 5:
        raise AssertionError
    elif not version[3] in ('alpha', 'beta', 'rc', 'final'):
        raise AssertionError
    else:
        main = '.'.join(map(str, version[:3]))
        sub = ''
        if version[3] == 'alpha':
            if version[4] == 0:
                git_changeset = get_git_changeset(filename)
                if git_changeset:
                    sub = '.dev%s' % git_changeset
        if version[3] != 'final':
            if not sub:
                sub = '%s%s' % (symbol.get(version[3], version[3]), version[4])
    return main + sub


def sh(command, cwd=None):
    return subprocess.Popen(command, stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      shell=True,
      cwd=cwd,
      universal_newlines=True).communicate()[0]


def get_git_changeset(filename=None):
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    dirname = os.path.dirname(filename or __file__)
    git_show = sh('git show --pretty=format:%ct --quiet HEAD', cwd=dirname)
    timestamp = git_show.partition('\n')[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return
    else:
        return timestamp.strftime('%Y%m%d%H%M%S')