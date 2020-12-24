# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/outdated/mywarnings.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 705 bytes
from warnings import filterwarnings

class OutdatedWarningBase(Warning):
    __doc__ = '\n    Base class for warnings in this module. Use this to filter all\n    warnings from this module.\n    '


class OutdatedPackageWarning(OutdatedWarningBase):
    __doc__ = '\n    Warning emitted when a package is found to be out of date.\n    '


filterwarnings('always', category=OutdatedPackageWarning)

class OutdatedCheckFailedWarning(OutdatedWarningBase):
    __doc__ = '\n    Warning emitted when checking the version of a package fails\n    with an exception.\n    '


class OutdatedCacheFailedWarning(OutdatedWarningBase):
    __doc__ = '\n    Warning emitted when writing to or reading from the cache\n    fails with an exception.\n    '