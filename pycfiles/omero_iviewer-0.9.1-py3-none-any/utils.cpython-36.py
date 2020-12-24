# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ome/omero-iviewer/plugin/omero_iviewer/utils.py
# Compiled at: 2020-02-27 05:54:44
# Size of source mod 2**32: 1437 bytes


def get_version(version=None):
    """
    Returns a PEP 386-compliant version number.
    See https://www.python.org/dev/peps/pep-0440/
    """
    version = get_full_version(version)
    parts = 3
    res = '.'.join(str(x) for x in version[:parts])
    if len(version) > 3:
        res = '%s%s' % (res, version[3])
    return str(res) + get_rc_version()


def get_full_version(value=None):
    """
    Returns a tuple of the iviewer version.
    """
    if value is None:
        from .version import VERSION as value
    return value


def get_rc_version(value=None):
    """
    Returns a tuple of the iviewer version.
    """
    if value is None:
        from .version import RC as value
    return value