# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/sa.py
# Compiled at: 2007-03-21 11:18:16
"""SQL Alchemy utilities
"""

class TableDeclarationStatement:
    __module__ = __name__
    no_create = False

    def __init__(self, no_create=False):
        self.no_create = no_create

    def __call__(self, *tables):
        for tbl in tables:
            if not tbl.exists():
                tbl.create()


declare_tables = TableDeclarationStatement()