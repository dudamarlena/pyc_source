# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/base.py
# Compiled at: 2017-08-17 16:01:19
from __future__ import absolute_import, division, print_function, unicode_literals
import six
from abc import ABCMeta, abstractmethod
__author__ = b'Kiran Mathew'
__email__ = b'kmathew@lbl.gov'

class AbstractBuilder(six.with_metaclass(ABCMeta)):
    """
    Abstract builder class. Defines the contract and must be subclassed by all builders.
    """

    @abstractmethod
    def run(self):
        """
        Run the builder.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Unset the building.
        """
        pass

    @classmethod
    @abstractmethod
    def from_file(cls, filename):
        """
        Set the builder from a config file, e.g., a db file
        """
        pass