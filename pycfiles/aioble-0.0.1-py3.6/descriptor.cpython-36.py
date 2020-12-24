# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/descriptor.py
# Compiled at: 2019-08-18 16:44:13
# Size of source mod 2**32: 448 bytes


class Descriptor(object):
    __doc__ = 'The Descriptor Base Class'

    def __init__(self, characteristic, *args, **kwargs):
        self.characteristic = characteristic

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Descriptor(identifier={self.identifier})"

    @property
    def identifier(self):
        """An identifier that uniquely identifies this descriptor"""
        raise NotImplementedError()