# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/requirements.py
# Compiled at: 2020-04-01 07:23:01
# Size of source mod 2**32: 512 bytes
from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions

class Requirements(SuiteRequirements):
    __doc__ = '@property\n    def table_reflection(self):\n        return exclusions.closed()'

    @property
    def independent_connections(self):
        return exclusions.closed()

    @property
    def returning(self):
        return exclusions.open()

    @property
    def index_reflection(self):
        return exclusions.closed()