# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/DataType.py
# Compiled at: 2018-08-16 06:12:07
# Size of source mod 2**32: 2466 bytes
"""
Copyright (c) 2017
Fraunhofer Institute for Manufacturing Engineering
and Automation (IPA)
Author: Daniel Stock
mailto: daniel DOT stock AT ipa DOT fraunhofer DOT com
See the file "LICENSE" for the full license governing this code.
"""
import datetime
from enum import Enum

class DataType(Enum):
    STRING = 'string'
    INT32 = 'int32'
    INT64 = 'int64'
    DOUBLE = 'double'
    FLOAT = 'float'
    DATETIME = 'date-time'
    BOOLEAN = 'boolean'
    BYTE = 'byte'


def getDataType--- This code section failed: ---

 L.  27         0  BUILD_MAP_0           0 
                2  STORE_FAST               'dataType'

 L.  28         4  LOAD_FAST                'format'
                6  LOAD_STR                 'string'
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_TRUE     30  'to 30'
               12  LOAD_FAST                'format'
               14  LOAD_GLOBAL              DataType
               16  LOAD_ATTR                STRING
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'format'
               24  LOAD_GLOBAL              str
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    42  'to 42'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'

 L.  29        30  LOAD_STR                 'string'
               32  LOAD_FAST                'dataType'
               34  LOAD_STR                 'type'
               36  STORE_SUBSCR     
            38_40  JUMP_FORWARD        380  'to 380'
             42_0  COME_FROM            28  '28'

 L.  30        42  LOAD_FAST                'format'
               44  LOAD_STR                 'int32'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_TRUE     60  'to 60'
               50  LOAD_FAST                'format'
               52  LOAD_GLOBAL              DataType
               54  LOAD_ATTR                INT32
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    80  'to 80'
             60_0  COME_FROM            48  '48'

 L.  31        60  LOAD_STR                 'integer'
               62  LOAD_FAST                'dataType'
               64  LOAD_STR                 'type'
               66  STORE_SUBSCR     

 L.  32        68  LOAD_STR                 'int32'
               70  LOAD_FAST                'dataType'
               72  LOAD_STR                 'format'
               74  STORE_SUBSCR     
            76_78  JUMP_FORWARD        380  'to 380'
             80_0  COME_FROM            58  '58'

 L.  34        80  LOAD_FAST                'format'
               82  LOAD_STR                 'int64'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE    114  'to 114'

 L.  35        88  LOAD_FAST                'format'
               90  LOAD_GLOBAL              DataType
               92  LOAD_ATTR                INT64
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_TRUE    114  'to 114'

 L.  36        98  LOAD_FAST                'format'
              100  LOAD_GLOBAL              int
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_TRUE    114  'to 114'

 L.  37       106  LOAD_FAST                'format'
              108  LOAD_STR                 'integer'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   132  'to 132'
            114_0  COME_FROM           104  '104'
            114_1  COME_FROM            96  '96'
            114_2  COME_FROM            86  '86'

 L.  39       114  LOAD_STR                 'integer'
              116  LOAD_FAST                'dataType'
              118  LOAD_STR                 'type'
              120  STORE_SUBSCR     

 L.  40       122  LOAD_STR                 'int64'
              124  LOAD_FAST                'dataType'
              126  LOAD_STR                 'format'
              128  STORE_SUBSCR     
              130  JUMP_FORWARD        380  'to 380'
            132_0  COME_FROM           112  '112'

 L.  41       132  LOAD_FAST                'format'
              134  LOAD_STR                 'float'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_TRUE    150  'to 150'
              140  LOAD_FAST                'format'
              142  LOAD_GLOBAL              DataType
              144  LOAD_ATTR                FLOAT
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   168  'to 168'
            150_0  COME_FROM           138  '138'

 L.  42       150  LOAD_STR                 'number'
              152  LOAD_FAST                'dataType'
              154  LOAD_STR                 'type'
              156  STORE_SUBSCR     

 L.  43       158  LOAD_STR                 'float'
              160  LOAD_FAST                'dataType'
              162  LOAD_STR                 'format'
              164  STORE_SUBSCR     
              166  JUMP_FORWARD        380  'to 380'
            168_0  COME_FROM           148  '148'

 L.  45       168  LOAD_FAST                'format'
              170  LOAD_STR                 'double'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_TRUE    202  'to 202'

 L.  46       176  LOAD_FAST                'format'
              178  LOAD_GLOBAL              DataType
              180  LOAD_ATTR                DOUBLE
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_TRUE    202  'to 202'

 L.  47       186  LOAD_FAST                'format'
              188  LOAD_GLOBAL              float
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_TRUE    202  'to 202'

 L.  48       194  LOAD_FAST                'format'
              196  LOAD_STR                 'number'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   220  'to 220'
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           184  '184'
            202_2  COME_FROM           174  '174'

 L.  50       202  LOAD_STR                 'number'
              204  LOAD_FAST                'dataType'
              206  LOAD_STR                 'type'
              208  STORE_SUBSCR     

 L.  51       210  LOAD_STR                 'double'
              212  LOAD_FAST                'dataType'
              214  LOAD_STR                 'format'
              216  STORE_SUBSCR     
              218  JUMP_FORWARD        380  'to 380'
            220_0  COME_FROM           200  '200'

 L.  53       220  LOAD_FAST                'format'
              222  LOAD_STR                 'date-time'
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_TRUE    264  'to 264'

 L.  54       230  LOAD_FAST                'format'
              232  LOAD_GLOBAL              DataType
              234  LOAD_ATTR                DATETIME
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_TRUE    264  'to 264'

 L.  55       242  LOAD_FAST                'format'
              244  LOAD_GLOBAL              datetime
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_TRUE    264  'to 264'

 L.  56       252  LOAD_FAST                'format'
              254  LOAD_GLOBAL              datetime
              256  LOAD_ATTR                datetime
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   282  'to 282'
            264_0  COME_FROM           248  '248'
            264_1  COME_FROM           238  '238'
            264_2  COME_FROM           226  '226'

 L.  58       264  LOAD_STR                 'string'
              266  LOAD_FAST                'dataType'
              268  LOAD_STR                 'type'
              270  STORE_SUBSCR     

 L.  59       272  LOAD_STR                 'date-time'
              274  LOAD_FAST                'dataType'
              276  LOAD_STR                 'format'
              278  STORE_SUBSCR     
              280  JUMP_FORWARD        380  'to 380'
            282_0  COME_FROM           260  '260'

 L.  60       282  LOAD_FAST                'format'
              284  LOAD_STR                 'boolean'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_TRUE    314  'to 314'
              292  LOAD_FAST                'format'
              294  LOAD_GLOBAL              DataType
              296  LOAD_ATTR                BOOLEAN
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_TRUE    314  'to 314'
              304  LOAD_FAST                'format'
              306  LOAD_GLOBAL              bool
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   324  'to 324'
            314_0  COME_FROM           300  '300'
            314_1  COME_FROM           288  '288'

 L.  61       314  LOAD_STR                 'boolean'
              316  LOAD_FAST                'dataType'
              318  LOAD_STR                 'type'
              320  STORE_SUBSCR     
              322  JUMP_FORWARD        380  'to 380'
            324_0  COME_FROM           310  '310'

 L.  62       324  LOAD_FAST                'format'
              326  LOAD_STR                 'byte'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_TRUE    346  'to 346'
              334  LOAD_FAST                'format'
              336  LOAD_GLOBAL              DataType
              338  LOAD_ATTR                BYTE
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   364  'to 364'
            346_0  COME_FROM           330  '330'

 L.  63       346  LOAD_STR                 'string'
              348  LOAD_FAST                'dataType'
              350  LOAD_STR                 'type'
              352  STORE_SUBSCR     

 L.  64       354  LOAD_STR                 'byte'
              356  LOAD_FAST                'dataType'
              358  LOAD_STR                 'format'
              360  STORE_SUBSCR     
              362  JUMP_FORWARD        380  'to 380'
            364_0  COME_FROM           342  '342'

 L.  66       364  LOAD_GLOBAL              print
              366  LOAD_STR                 'Unknown dataType: '
              368  LOAD_GLOBAL              str
              370  LOAD_FAST                'format'
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  BINARY_ADD       
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  POP_TOP          
            380_0  COME_FROM           362  '362'
            380_1  COME_FROM           322  '322'
            380_2  COME_FROM           280  '280'
            380_3  COME_FROM           218  '218'
            380_4  COME_FROM           166  '166'
            380_5  COME_FROM           130  '130'
            380_6  COME_FROM            76  '76'
            380_7  COME_FROM            38  '38'

 L.  67       380  LOAD_FAST                'dataType'
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 130


def convertDataType(format):
    dataType = {}
    if format == DataType.STRING:
        return str
    if format == DataType.INT32:
        return int
    if format == DataType.INT64:
        return int
    if format == DataType.FLOAT:
        return float
    if format == DataType.DOUBLE:
        return float
    if format == DataType.DATETIME:
        return datetime.datetime
    if DataType.BOOLEAN:
        return bool
    if format == DataType.BYTE:
        return bytes
    print('Unknown dataType: ' + str(format))
    return dataType