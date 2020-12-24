# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/GenericValue.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 1070 bytes
from binding import *
from .namespace import llvm
from .Type import Type
GenericValue = llvm.Class()

@GenericValue
class GenericValue:
    delete = Destructor()

    def _factory(name, *argtys):
        return CustomStaticMethod(('GenericValue_' + name), ptr(GenericValue), *argtys)

    CreateFloat = _factory('CreateFloat', cast(float, Float))
    CreateDouble = _factory('CreateDouble', cast(float, Float))
    CreateInt = _factory('CreateInt', ptr(Type), cast(int, UnsignedLongLong), cast(bool, Bool))
    CreatePointer = _factory('CreatePointer', cast(int, VoidPtr))

    def _accessor(name, *argtys):
        return CustomMethod(('GenericValue_' + name), *argtys)

    valueIntWidth = _accessor('ValueIntWidth', cast(Unsigned, int))
    toSignedInt = _accessor('ToSignedInt', cast(LongLong, int))
    toUnsignedInt = _accessor('ToUnsignedInt', cast(UnsignedLongLong, int))
    toFloat = _accessor('ToFloat', cast(Double, float), ptr(Type))
    toPointer = _accessor('ToPointer', cast(VoidPtr, int))