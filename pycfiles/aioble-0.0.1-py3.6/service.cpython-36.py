# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/service.py
# Compiled at: 2019-06-13 01:58:06
# Size of source mod 2**32: 411 bytes


class Service(object):
    __doc__ = 'The Service Base Class'

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