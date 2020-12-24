# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/git_semver/__init__.py
# Compiled at: 2020-04-04 13:31:03
# Size of source mod 2**32: 620 bytes
from semantic_version import Version as _Version
from git_semver._version import __version__

def get_current_version(repo, Version=_Version):
    latest = None
    for tag in repo.tags:
        v = tag.name
        if v.startswith('v.'):
            v = v[2:]
        else:
            if v.startswith('v'):
                v = v[1:]
            try:
                v = Version(v)
            except ValueError:
                continue

        if not latest or v > latest:
            latest = v

    return latest