# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/sparse/operator.py
# Compiled at: 2013-06-07 13:57:48


class OperatorBase(object):

    @property
    def dtype(self):
        raise NotImplementedError

    @property
    def shape(self):
        raise NotImplementedError

    def __neg__(self):
        return NegOperator(self)


class IdentityOperator(OperatorBase):

    def __init__(self, dtype, n):
        self.my_dtype = dtype
        self.n = n

    @property
    def dtype(self):
        return self.my_dtype

    @property
    def shape(self):
        return (
         self.n, self.n)

    def __call__(self, operand):
        return operand


class DiagonalPreconditioner(OperatorBase):

    def __init__(self, diagonal):
        self.diagonal = diagonal

    @property
    def dtype(self):
        return self.diagonal.dtype

    @property
    def shape(self):
        n = self.diagonal.shape[0]
        return (
         n, n)

    def __call__(self, operand):
        return self.diagonal * operand