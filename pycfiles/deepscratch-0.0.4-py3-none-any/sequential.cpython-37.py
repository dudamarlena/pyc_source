# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuguldur/Documents/ml from scratch/build/lib/deepscratch/sequential.py
# Compiled at: 2019-06-16 07:08:11
# Size of source mod 2**32: 598 bytes


class Sequential:

    def __init__(self, layers=None, name='Sequential'):
        self.name = name
        self.layers = layers

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)

        return x

    def backward(self, grad):
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def __repr__(self):
        result = ''
        result += f"\x1b[01m{self.name}\x1b[00m ( \n"
        for layer in self.layers:
            result += f"\t{layer.__repr__()} \n".expandtabs(4)

        result += ')'
        return result