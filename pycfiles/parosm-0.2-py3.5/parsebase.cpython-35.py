# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parosm/parse/parsebase.py
# Compiled at: 2018-04-22 12:47:39
# Size of source mod 2**32: 491 bytes
from abc import ABC, abstractmethod

class BaseParser:
    __doc__ = '\n    This is the base class for Parsers\n    it defines the interface for a parser\n    '

    @abstractmethod
    def __init__(self, file, callback=None):
        """
        Initializes the parser

        :param file: path to file
        :param callback: callback is called with element
        """
        pass

    @abstractmethod
    def parse(self):
        """
        Start the parsing process
        """
        pass