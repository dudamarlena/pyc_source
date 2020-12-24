# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\segpy\types.py
# Compiled at: 2017-02-16 13:30:26
# Size of source mod 2**32: 969 bytes


class Int16(int):
    MINIMUM = -32768
    MAXIMUM = 32767
    SIZE = 2
    SEG_Y_TYPE = 'int16'

    def __new__(cls, *args, **kwargs):
        instance = (super().__new__)(cls, *args, **kwargs)
        if not Int16.MINIMUM <= instance <= Int16.MAXIMUM:
            raise ValueError('{} value {!r} outside range {} to {}'.format(cls.__name__, instance, cls.MINIMUM, cls.MAXIMUM))
        return instance


class Int32(int):
    MINIMUM = -2147483648
    MAXIMUM = 2147483647
    SIZE = 4
    SEG_Y_TYPE = 'int32'

    def __new__(cls, *args, **kwargs):
        instance = (super().__new__)(cls, *args, **kwargs)
        if not Int32.MINIMUM <= instance <= Int32.MAXIMUM:
            raise ValueError('{} value {!r} outside range {} to {}'.format(cls.__name__, instance, cls.MINIMUM, cls.MAXIMUM))
        return instance