# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/__init__.py
# Compiled at: 2020-03-06 05:24:58
# Size of source mod 2**32: 318 bytes
"""Buildout Versions Checker"""
from bvc.checker import VersionsChecker
from bvc.configparser import VersionsConfigParser
from bvc.scripts.check_buildout_updates import cmdline
__all__ = [
 VersionsChecker.__name__,
 VersionsConfigParser.__name__]
if __name__ == '__main__':
    cmdline()