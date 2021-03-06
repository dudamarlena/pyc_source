# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/address.py
# Compiled at: 2015-12-21 17:12:57
import os, socket
from pyage.core.inject import Inject

class AddressProvider(object):

    def generate_address(self, obj):
        raise NotImplementedError()


counter = 0

class SequenceAddressProvider(AddressProvider):

    def __init__(self):
        super(SequenceAddressProvider, self).__init__()

    def generate_address(self, obj):
        global counter
        counter += 1
        return str(counter) + '.' + socket.gethostname() + '.' + str(os.getpid())


class Addressable(object):

    @Inject('address_provider')
    def __init__(self):
        super(Addressable, self).__init__()
        if hasattr(self, 'name') and self.name:
            self.address = self.name + '.' + socket.gethostname() + '.' + str(os.getpid())
        else:
            self.address = self.address_provider.generate_address(self)

    def get_address(self):
        return self.address