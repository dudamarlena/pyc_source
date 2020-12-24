# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hs2client/genthrift/TCLIService/constants.py
# Compiled at: 2018-05-31 03:46:46
from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec
import sys
from .ttypes import *
PRIMITIVE_TYPES = set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21))
COMPLEX_TYPES = set((10, 11, 12, 13, 14))
COLLECTION_TYPES = set((10, 11))
TYPE_NAMES = {0: 'BOOLEAN', 
   1: 'TINYINT', 
   2: 'SMALLINT', 
   3: 'INT', 
   4: 'BIGINT', 
   5: 'FLOAT', 
   6: 'DOUBLE', 
   7: 'STRING', 
   8: 'TIMESTAMP', 
   9: 'BINARY', 
   10: 'ARRAY', 
   11: 'MAP', 
   12: 'STRUCT', 
   13: 'UNIONTYPE', 
   15: 'DECIMAL', 
   16: 'NULL', 
   17: 'DATE', 
   18: 'VARCHAR', 
   19: 'CHAR', 
   20: 'INTERVAL_YEAR_MONTH', 
   21: 'INTERVAL_DAY_TIME'}
CHARACTER_MAXIMUM_LENGTH = 'characterMaximumLength'
PRECISION = 'precision'
SCALE = 'scale'