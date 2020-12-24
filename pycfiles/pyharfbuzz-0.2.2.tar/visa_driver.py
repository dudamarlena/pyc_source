# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\visa\visa_driver.py
# Compiled at: 2013-10-05 04:00:20
__doc__ = '\nVisa communication using the module "visa"\n'
from pyhardware.drivers import Driver
import visa

class VisaDriver(Driver):
    """
    Base class for device interfaced with Visa
    """

    def __init__(self, *args):
        """
        args are logical_name, address, simulate
        """
        super(VisaDriver, self).__init__(*args)
        self.visa_instr = visa.instrument(self.address)

    def ask(self, val):
        """
        Asks the driver
        """
        return self.visa_instr.ask(val)

    def read(self):
        """
        reads a value
        """
        return self.visa_instr.read()

    def write(self, val):
        """
        writes a value
        """
        return self.visa_instr.write(val)

    @classmethod
    def supported_models(cls):
        """
        returns the list of models supported by this driver. The
        model is the string between the first and second "," in the 
        *IDN? query reply.
        """
        models = []
        if hasattr(cls, '_supported_models'):
            return cls._supported_models
        for child in cls.__subclasses__():
            models += child.supported_models()

        return models