# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/version.py
# Compiled at: 2015-06-14 13:30:57
"""Version wrapper

Access to the version as configured as part of installation package.
Leverages pbr (Python Build Reasonableness)
"""
from pbr import version as pbr_version
version_info = pbr_version.VersionInfo('SeedboxManager')

def version_string():
    """Provide a string representing the version of the project.

    :return: project version
    :rtype: string
    """
    return version_info.version_string()


def release_string():
    """Provide a string representing the release of the project.

    :return: project release
    :rtype: string
    """
    return version_info.release_string()