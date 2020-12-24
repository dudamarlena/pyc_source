# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/exceptions.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 238 bytes


class MigrationLoadError(Exception):
    __doc__ = 'MigrationLoadError happens if there is something wrong with migration.\n\n    This exception will be thrown whenever a bad thing about a migration file\n    is discovered by tool.\n\n    '