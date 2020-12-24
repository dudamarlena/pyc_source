# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/__version__.py
# Compiled at: 2019-10-28 06:42:11
# Size of source mod 2**32: 218 bytes
"""Version handling module."""
try:
    import pkg_resources
except ImportError:
    pass

try:
    __version__ = pkg_resources.get_distribution('ansible_readme').version
except Exception:
    __version__ = 'unknown'