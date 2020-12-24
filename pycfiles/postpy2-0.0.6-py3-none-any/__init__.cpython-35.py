# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/__init__.py
# Compiled at: 2017-02-15 04:26:41
# Size of source mod 2**32: 148 bytes
from postpy._version import version_info, __version__
from postpy.connections import connect
from postpy.pg_encodings import get_postgres_encoding