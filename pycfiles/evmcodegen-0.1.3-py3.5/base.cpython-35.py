# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmcodegen\generators\base.py
# Compiled at: 2018-10-12 11:44:35
# Size of source mod 2**32: 549 bytes


class _BaseCodeGen(object):
    TYPE_OPCODE_ONLY = 1
    TYPE_OPCODE_WITH_OPERAND = 2

    def __init__(self):
        self.type = None

    def generate(self, length=None):
        raise NotImplementedError('--not implemented--')

    def __iter__(self):
        return self

    def __next__(self):
        return self.generate()