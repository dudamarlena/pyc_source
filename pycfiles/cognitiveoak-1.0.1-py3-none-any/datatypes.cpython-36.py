# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo/cognitivegeo/src\segpy\datatypes.py
# Compiled at: 2017-02-16 13:30:26
# Size of source mod 2**32: 1195 bytes
DATA_SAMPLE_FORMAT_TO_SEG_Y_TYPE = {1:'ibm',  2:'int32', 
 3:'int16', 
 5:'float32', 
 8:'int8'}
SEG_Y_TYPE_TO_CTYPE = {'int32':'i', 
 'uint32':'I', 
 'int16':'h', 
 'uint16':'H', 
 'int8':'b', 
 'uint8':'B', 
 'float32':'f', 
 'ibm':'ibm'}
SEG_Y_TYPE_DESCRIPTION = {'ibm':'IBM float', 
 'int32':'32 bit signed integer', 
 'uint32':'32 bit unsigned integer', 
 'int16':'16 bit signed integer', 
 'uint16':'16 bit unsigned integer', 
 'float32':'IEEE float32', 
 'int8':'8 bit signed integer (byte)', 
 'uint8':'8 bit unsigned integer (byte)'}
CTYPE_TO_SIZE = dict(i=4, I=4,
  h=2,
  H=2,
  b=1,
  B=1,
  f=4,
  ibm=4)

def size_in_bytes(ctype):
    return CTYPE_TO_SIZE[ctype]