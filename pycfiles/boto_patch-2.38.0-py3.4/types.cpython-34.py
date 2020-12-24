# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/dynamodb2/types.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 932 bytes
from boto.dynamodb.types import NonBooleanDynamizer, Dynamizer
STRING = 'S'
NUMBER = 'N'
BINARY = 'B'
STRING_SET = 'SS'
NUMBER_SET = 'NS'
BINARY_SET = 'BS'
NULL = 'NULL'
BOOLEAN = 'BOOL'
MAP = 'M'
LIST = 'L'
QUERY_OPERATORS = {'eq': 'EQ', 
 'lte': 'LE', 
 'lt': 'LT', 
 'gte': 'GE', 
 'gt': 'GT', 
 'beginswith': 'BEGINS_WITH', 
 'between': 'BETWEEN'}
FILTER_OPERATORS = {'eq': 'EQ', 
 'ne': 'NE', 
 'lte': 'LE', 
 'lt': 'LT', 
 'gte': 'GE', 
 'gt': 'GT', 
 'nnull': 'NOT_NULL', 
 'null': 'NULL', 
 'contains': 'CONTAINS', 
 'ncontains': 'NOT_CONTAINS', 
 'beginswith': 'BEGINS_WITH', 
 'in': 'IN', 
 'between': 'BETWEEN'}