# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/script/redeem/timed.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 3798 bytes
"""
Defines RedeemScripts that contain time conditions in order to spend funds
"""
from .. import pay
from .model import RedeemScript
from ...field import OP_IF, OP_ELSE, OP_ENDIF, OP_CHECKLOCKTIMEVERIFY, OP_DROP, ScriptData, ScriptNum

class TimeLockedScript(RedeemScript):
    __doc__ = '\n    A time locked redeem script allows to set two scripts for spending an UTXO:\n     - lifetime_script\n        Script that will allow to spend the funds at any time\n     - timelocked_script\n        Script that will be allowed to spend after a certain period of time\n     - locktime\n        Time after which the timelocked script is valid to be spent\n\n    This is a model that can be used to create smart contracts by specifying\n    non-standard lifetime and timelocked scripts\n\n    Attributes:\n        _lifetime (Script): script that will allow to redeem the utxo\n                                  at any time\n        _timelocked (Script): script that will allwo to redeem the utxo\n                                  after the specified time\n        _locktime (VarInt):\n            time after which the timelocked script becomes valid\n        _unlocked_script (Serializable):\n        _timelocked_params (Serializable): parameters to add to the timelocked\n            script so it is spendable after the given time\n        Time is specified as BIP-65:\n        https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki\n    '
    __slots__ = ['_lifetime_script', '_timelocked_script', '_unlocked_script',
     '_locktime']

    def __init__(self, locktime, lifetime_script=None, unlocked_script=None, timelocked_script=None):
        """
        Initializes the time locked script with the lifetime script, timelocked
        script and locktime
        """
        super().__init__(None)
        self._locktime = locktime
        self._lifetime_script = lifetime_script
        self._timelocked_script = timelocked_script
        self._unlocked_script = unlocked_script

    def _build(self):
        """
        Builds the script data to be able to serialize it

        The model of the timelocked script is:
            OP_IF
                <time> OP_CHECKLOCKTIMEVERIFY OP_DROP
                <timelocked_script>
            OP_ELSE
                <unlocked_script>
            OP_ENDIF
            <lifetime_script>

        So if you want to spend the script after the locked time, you must
        specify in the payment script a OP_1 (OP_TRUE), and OP_0 (OP_FALSe)
        if you want to spend it before (or at anytime if provided a
        lifetime_script).

        Remember to put the payment script before the OP_0, OP_1
        """
        self._data = [
         OP_IF]
        self._data += [ScriptData(ScriptNum(self._locktime)),
         OP_CHECKLOCKTIMEVERIFY, OP_DROP]
        if self._timelocked_script is not None:
            self._data += [self._timelocked_script]
        if self._unlocked_script is not None:
            self._data += [OP_ELSE, self._unlocked_script]
        self._data += [OP_ENDIF]
        if self._lifetime_script is not None:
            self._data += [self._lifetime_script]

    @property
    def lifetime_script(self):
        return self._lifetime_script

    @property
    def timelocked_script(self):
        return self._timelocked_script

    @property
    def locktime(self):
        return self._locktime

    @property
    def pay_script(self):
        return pay.TimeLockedScript(self)