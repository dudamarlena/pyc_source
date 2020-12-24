# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_internal/models/scheme.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 679 bytes
"""
For types associated with installation schemes.

For a general overview of available schemes and their context, see
https://docs.python.org/3/install/index.html#alternate-installation.
"""

class Scheme(object):
    __doc__ = 'A Scheme holds paths which are used as the base directories for\n    artifacts associated with a Python package.\n    '

    def __init__(self, platlib, purelib, headers, scripts, data):
        self.platlib = platlib
        self.purelib = purelib
        self.headers = headers
        self.scripts = scripts
        self.data = data