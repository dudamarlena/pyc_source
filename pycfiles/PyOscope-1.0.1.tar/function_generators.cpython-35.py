# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyosci/function_generators.py
# Compiled at: 2017-02-08 03:59:07
# Size of source mod 2**32: 324 bytes
from . import osci

class Agilent33220A(osci.AbstractBaseOscilloscope):

    def __init__(self, ip='10.25.21.168'):
        """
        An Agilent function generator

        Args:
            ip: The port where this instrument is listening on
        """
        osci.AbstractBaseOscilloscope.__init__(self, ip=ip)