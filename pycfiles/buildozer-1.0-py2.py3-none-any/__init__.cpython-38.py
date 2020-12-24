# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/__init__.py
# Compiled at: 2020-03-06 05:24:58
# Size of source mod 2**32: 318 bytes
__doc__ = 'Buildout Versions Checker'
from bvc.checker import VersionsChecker
from bvc.configparser import VersionsConfigParser
from bvc.scripts.check_buildout_updates import cmdline
__all__ = [
 VersionsChecker.__name__,
 VersionsConfigParser.__name__]
if __name__ == '__main__':
    cmdline()