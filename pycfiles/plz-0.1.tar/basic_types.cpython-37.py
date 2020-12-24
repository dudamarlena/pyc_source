# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/basic_types.py
# Compiled at: 2019-04-20 19:48:40
# Size of source mod 2**32: 139 bytes
from .symbol_table import global_table
global_table.set('Integer', int)
global_table.set('Decimal', float)
global_table.set('String', str)