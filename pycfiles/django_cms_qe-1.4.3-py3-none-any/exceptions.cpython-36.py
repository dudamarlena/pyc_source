# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/exceptions.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 350 bytes


class TableDoesNotExists(Exception):
    __doc__ = '\n    Exception when plugin is configured with table which does not exists\n    anymore. For example developer changed name or application providing\n    that table is not used anymore.\n    '

    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name