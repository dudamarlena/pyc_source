# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/filehash/__init__.py
# Compiled at: 2018-05-07 01:48:26
# Size of source mod 2**32: 186 bytes
try:
    from filehash import FileHash, SUPPORTED_ALGORITHMS
except ImportError:
    from .filehash import FileHash, SUPPORTED_ALGORITHMS
else:
    __all__ = [
     'FileHash', 'SUPPORTED_ALGORITHMS']