# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\driver.py
# Compiled at: 2013-10-05 04:00:20
"""
defines the base class for a driver. This abstract class can be inherited by 
ivicom, ividotnet, visa or serial
"""
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