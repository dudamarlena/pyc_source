# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/encrypted_mode_calculation_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1888 bytes
from federatedml.param.base_param import BaseParam

class EncryptedModeCalculatorParam(BaseParam):
    __doc__ = "\n    Define the encrypted_mode_calulator parameters.\n\n    Parameters\n    ----------\n    mode: str, support 'strict', 'fast', 'balance', 'confusion_opt', ' only, default: strict\n\n    re_encrypted_rate: float or int, numeric number in [0, 1], use when mode equals to 'balance, default: 1\n\n    "

    def __init__(self, mode='strict', re_encrypted_rate=1):
        self.mode = mode
        self.re_encrypted_rate = re_encrypted_rate

    def check(self):
        descr = 'encrypted_mode_calculator param'
        self.mode = self.check_and_change_lower(self.mode, [
         'strict', 'fast', 'balance', 'confusion_opt', 'confusion_opt_balance'], descr)
        if self.mode in ('balance', 'confusion_opt_balance'):
            if type(self.re_encrypted_rate).__name__ not in ('int', 'long', 'float'):
                raise ValueError('re_encrypted_rate should be a numeric number')
            if not 0.0 <= self.re_encrypted_rate <= 1:
                raise ValueError('re_encrypted_rate should  in [0, 1]')
        return True