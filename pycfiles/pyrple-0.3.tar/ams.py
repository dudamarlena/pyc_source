# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/ams.py
# Compiled at: 2017-08-29 09:44:06
from ..modules import HardwareModule
from ..attributes import PWMRegister

class AMS(HardwareModule):
    """mostly deprecated module (redpitaya has removed adc support).
    only here for dac2 and dac3"""
    addr_base = 1077936128
    dac0 = PWMRegister(32, doc='PWM output 0 [V]')
    dac1 = PWMRegister(36, doc='PWM output 1 [V]')
    dac2 = PWMRegister(40, doc='PWM output 2 [V]')
    dac3 = PWMRegister(44, doc='PWM output 3 [V]')

    def _setup(self):
        """
        sets up the AMS (just setting the attributes is OK)
        """
        pass