# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: wa/framework/version.py
# Compiled at: 2019-12-20 11:09:57
import os, sys
from collections import namedtuple
from subprocess import Popen, PIPE
VersionTuple = namedtuple('Version', ['major', 'minor', 'revision', 'dev'])
version = VersionTuple(3, 2, 0, '')
required_devlib_version = VersionTuple(1, 2, 0, '')

def format_version(v):
    version_string = ('{}.{}.{}').format(v.major, v.minor, v.revision)
    if v.dev:
        version_string += ('.{}').format(v.dev)
    return version_string


def get_wa_version():
    return format_version(version)


def get_wa_version_with_commit():
    version_string = get_wa_version()
    commit = get_commit()
    if commit:
        return ('{}+{}').format(version_string, commit)
    else:
        return version_string


def get_commit():
    p = Popen(['git', 'rev-parse', 'HEAD'], cwd=os.path.dirname(__file__), stdout=PIPE, stderr=PIPE)
    std, _ = p.communicate()
    p.wait()
    if p.returncode:
        return
    else:
        if sys.version_info[0] == 3 and isinstance(std, bytes):
            return std[:8].decode(sys.stdout.encoding or 'utf-8')
        return std[:8]
        return