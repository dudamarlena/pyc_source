# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/persistence/data_obfuscator.py
# Compiled at: 2014-11-30 00:17:44
# Size of source mod 2**32: 849 bytes
import dill
from abc import ABCMeta, abstractmethod

class DataObfuscator(metaclass=ABCMeta):
    __doc__ = 'Interface for data hashers\n\n    Obfuscation is the method to make easily comparable, storage efficent, potentially secure versions of the data.\n    '

    @staticmethod
    def _hashable_representation(data):
        """Generate a hashable representation of the data. Current implentation is pickle based.
        """
        return dill.dumps(data)

    @abstractmethod
    def obfuscate(self, data):
        """Create the hashed data representation

        This is method must be overridden by subclasses.

        :param data: data to obfuscate

        :return: obfuscated representation such as a hash
        """
        pass