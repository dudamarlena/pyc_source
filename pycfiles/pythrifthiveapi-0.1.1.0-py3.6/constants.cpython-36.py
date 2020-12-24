# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pythrifthiveapi/TCLIService/constants.py
# Compiled at: 2017-06-13 11:27:15
# Size of source mod 2**32: 1011 bytes
from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
import sys
from .ttypes import *
PRIMITIVE_TYPES = set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19))
COMPLEX_TYPES = set((10, 11, 12, 13, 14))
COLLECTION_TYPES = set((10, 11))
TYPE_NAMES = {0:'BOOLEAN', 
 1:'TINYINT', 
 2:'SMALLINT', 
 3:'INT', 
 4:'BIGINT', 
 5:'FLOAT', 
 6:'DOUBLE', 
 7:'STRING', 
 8:'TIMESTAMP', 
 9:'BINARY', 
 10:'ARRAY', 
 11:'MAP', 
 12:'STRUCT', 
 13:'UNIONTYPE', 
 15:'DECIMAL', 
 16:'NULL', 
 17:'DATE', 
 18:'VARCHAR', 
 19:'CHAR'}
CHARACTER_MAXIMUM_LENGTH = 'characterMaximumLength'
PRECISION = 'precision'
SCALE = 'scale'