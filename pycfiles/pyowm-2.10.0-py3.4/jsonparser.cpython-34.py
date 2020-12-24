# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/jsonparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 790 bytes
"""
Module containing an abstract base class for JSON OWM Weather API responses parsing
"""
from abc import ABCMeta, abstractmethod

class JSONParser(object):
    __doc__ = '\n    A global abstract class representing a JSON to object parser.\n\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse_JSON(self, JSON_string):
        """
        Returns a proper object parsed from the input JSON_string. Subclasses
        know from their specific type which object is to be parsed and returned

        :param JSON_string: a JSON text string
        :type JSON_string: str
        :returns: an object
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the resulting object

        """
        raise NotImplementedError