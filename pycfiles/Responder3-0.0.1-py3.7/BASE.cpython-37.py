# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\crypto\BASE.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1152 bytes
from abc import ABC, abstractmethod
import enum

class cipherMODE(enum.Enum):
    ECB = enum.auto()
    CBC = enum.auto()
    CTR = enum.auto()


class symmetricBASE:

    def __init__(self):
        self._cipher = None
        self.setup_cipher()

    @abstractmethod
    def setup_cipher(self):
        pass

    @abstractmethod
    def encrypt(self, data):
        pass

    @abstractmethod
    def decrypt(self):
        pass


class hashBASE:

    def __init__(self, data):
        self._hash = None
        self.setup_hash()
        if data is not None:
            self._hash.update(data)

    @abstractmethod
    def setup_hash(self):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def digest(self):
        pass

    @abstractmethod
    def hexdigest(self):
        pass


class hmacBASE:

    def __init__(self, key):
        self._key = key
        self._hash = None
        self.setup_hash()

    @abstractmethod
    def setup_hash(self):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def digest(self):
        pass

    @abstractmethod
    def hexdigest(self):
        pass