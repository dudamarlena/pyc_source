# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/descriptor.py
# Compiled at: 2019-08-18 16:44:13
# Size of source mod 2**32: 448 bytes


class Descriptor(object):
    """Descriptor"""

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