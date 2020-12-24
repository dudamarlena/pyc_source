# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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