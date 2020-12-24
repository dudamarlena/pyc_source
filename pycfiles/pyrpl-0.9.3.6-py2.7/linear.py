# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/models/linear.py
# Compiled at: 2017-08-29 09:44:06
from .. import *

class LinearInputDirect(InputDirect):
    slope = FloatProperty(min=-10000000000.0, max=10000000000.0, default=1)
    signal_at_0 = FloatProperty(min=-10000000000.0, max=10000000000.0, default=0)

    def expected_signal(self, variable):
        return self.slope * variable + self.signal_at_0


class Linear(Lockbox):
    """
    A simple linear dependance of variable vs input
    """
    _units = [
     'm', 'deg', 'rad']
    variable = 'x'