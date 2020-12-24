# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/s3nb/__init__.py
# Compiled at: 2015-03-28 13:53:37
imported = False
try:
    from .ipy2 import S3NotebookManager
    imported = True
except ImportError:
    pass

try:
    from .ipy3 import S3ContentsManager
    imported = True
except ImportError:
    pass

if not imported:
    raise ImportError('failed to import any s3nb managers')