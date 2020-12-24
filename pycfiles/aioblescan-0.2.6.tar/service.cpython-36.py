# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/service.py
# Compiled at: 2019-06-13 01:58:06
# Size of source mod 2**32: 411 bytes


class Service(object):
    """Service"""

    def __init__(self, device, *args, **kwargs):
        self.device = device

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Service(identifier={self.identifier})"

    @property
    def identifier(self):
        """An identifier that uniquely identifies this service"""
        raise NotImplementedError()