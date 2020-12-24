# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/i_reference_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1907 bytes
from abc import ABCMeta, abstractmethod

class IReferenceConverter(object):
    __doc__ = 'This class represents a abstract super class for all possible reference converters, e.g. for nest, SpiNNaker or LEMS.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert_binary_op(self, binary_operator):
        pass

    @abstractmethod
    def convert_function_call(self, function_call, prefix=''):
        pass

    @abstractmethod
    def convert_name_reference(self, variable):
        pass

    @abstractmethod
    def convert_constant(self, constant_name):
        pass

    @abstractmethod
    def convert_unary_op(self, unary_operator):
        pass

    @abstractmethod
    def convert_encapsulated(self):
        pass

    @abstractmethod
    def convert_logical_not(self):
        pass

    @abstractmethod
    def convert_arithmetic_operator(self, op):
        pass

    @abstractmethod
    def convert_bit_operator(self, op):
        pass

    @abstractmethod
    def convert_comparison_operator(self, op):
        pass

    @abstractmethod
    def convert_logical_operator(self, op):
        pass

    @abstractmethod
    def convert_ternary_operator(self):
        pass