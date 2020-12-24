# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/jsonparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 790 bytes
__doc__ = '\nModule containing an abstract base class for JSON OWM Weather API responses parsing\n'
from abc import ABCMeta, abstractmethod

class JSONParser(object):
    """JSONParser"""
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