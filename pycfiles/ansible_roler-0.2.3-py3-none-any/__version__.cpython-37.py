# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ansible_readme/__version__.py
# Compiled at: 2019-10-28 06:42:11
# Size of source mod 2**32: 218 bytes
__doc__ = 'Version handling module.'
try:
    import pkg_resources
except ImportError:
    pass

try:
    __version__ = pkg_resources.get_distribution('ansible_readme').version
except Exception:
    __version__ = 'unknown'