# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/setuptools/setuptools/version.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 144 bytes
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution('setuptools').version
except Exception:
    __version__ = 'unknown'