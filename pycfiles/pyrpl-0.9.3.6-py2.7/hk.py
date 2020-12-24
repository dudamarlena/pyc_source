# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/hk.py
# Compiled at: 2017-08-29 09:44:06
from ..attributes import IntRegister, SelectRegister, IORegister
from ..modules import HardwareModule
import numpy as np

class HK(HardwareModule):
    _setup_attributes = [
     'led'] + [ 'expansion_P' + str(i) for i in range(8) ] + [ 'expansion_N' + str(i) for i in range(8) ]
    _gui_attributes = [
     'id', 'led']
    addr_base = 1073741824
    for i in range(8):
        locals()['expansion_P' + str(i)] = IORegister(32, 24, 16, bit=i, outputmode=True, doc='positive digital io')
        locals()['expansion_N' + str(i)] = IORegister(36, 28, 20, bit=i, outputmode=True, doc='positive digital io')

    id = SelectRegister(0, doc='device ID', options={'prototype0': 0, 'release1': 1})
    digital_loop = IntRegister(12, doc='enables digital loop')
    led = IntRegister(48, doc='LED control with bits 1:8', min=0, max=256)

    def _setup(self):
        """
        Sets the HouseKeeping module of the redpitaya up. (just setting the attributes is OK)
        """
        pass