# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ome/omero-fpbioimage/omero_fpbioimage/utils.py
# Compiled at: 2020-01-13 09:06:30
# Size of source mod 2**32: 1411 bytes


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
    return str(res)


def get_full_version(value=None):
    """
    Returns a tuple of the version.
    """
    if value is None:
        from .version import VERSION as value
    return value