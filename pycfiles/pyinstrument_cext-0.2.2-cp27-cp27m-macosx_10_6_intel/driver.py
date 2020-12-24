# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\driver.py
# Compiled at: 2013-10-09 11:09:05
__doc__ = '\ndefines the base class for a driver. This abstract class can be inherited by \nivicom, ividotnet, visa or serial\n'
from pyhardware.utils.class_utils import list_all_child_classes

class Driver(object):
    """Base class to interface an instrument
    """

    def __init__(self, logical_name, address, simulate):
        self.logical_name = logical_name
        self.address = address
        self.simulate = simulate

    @classmethod
    def is_ivi_instrument(self):
        """returns True if the driver complies with ivi specification, 
        False otherwise. A visa or serial driver could be ivi-compliant !"""
        return False

    @classmethod
    def instrument_type(self):
        """gives the instrument type ("scope", "spec_an", "na" ...)"""
        raise NotImplementedError()

    @classmethod
    def supported_models(cls):
        """
        returns the list of models supported by this driver. The
        model is the string between the first and second "," in the 
        *IDN? query reply.
        """
        models = []
        for subclass in cls.__subclasses__():
            models += subclass.supported_models()

        return models