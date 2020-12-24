# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\argtypes.py
# Compiled at: 2018-10-08 17:02:52
# Size of source mod 2**32: 993 bytes


class BaseArgument(str):
    pass


class Internal(BaseArgument):
    _type = 'internal'


class Value(BaseArgument):
    _type = 'int64'


class Address(BaseArgument):
    _type = 'int160'


class Label(BaseArgument):
    _type = 'label'


class Bool(BaseArgument):
    _type = 'boolean'


class Byte(BaseArgument):
    _type = 'byte'


class Word(BaseArgument):
    _type = 'word'


class Index32(BaseArgument):
    _type = 'index32'


class Index64(BaseArgument):
    _type = 'index64'


class Index256(BaseArgument):
    _type = 'index256'


class MemOffset(BaseArgument):
    _type = 'memoffset'


class Length(BaseArgument):
    _type = 'length'


class Gas(BaseArgument):
    _type = 'gas'


class CallValue(BaseArgument):
    _type = 'callvalue'


class Data(BaseArgument):
    _type = 'data'


class Timestamp(BaseArgument):
    _type = 'timestamp'