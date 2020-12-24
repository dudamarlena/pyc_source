# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/__init__.py
# Compiled at: 2017-02-15 04:26:41
# Size of source mod 2**32: 148 bytes
from postpy._version import version_info, __version__
from postpy.connections import connect
from postpy.pg_encodings import get_postgres_encoding