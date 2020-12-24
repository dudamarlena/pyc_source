# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ome/omero-mapr/omero_mapr/utils/version.py
# Compiled at: 2020-01-13 06:52:00
# Size of source mod 2**32: 1416 bytes


def get_version(version=None):
    """
    Returns a PEP 386-compliant version number.
    See https://www.python.org/dev/peps/pep-0440/
    """
    version = get_full_version(version)
    parts = 2 if version[2] == 0 else 3
    res = '.'.join(str(x) for x in version[:parts])
    if len(version) > 3:
        res = '%s%s' % (res, version[3])
    return str(res)


def get_full_version(version=None):
    """
    Returns a tuple of the mapr version.
    """
    if version is None:
        from omero_mapr import VERSION as version
    return version