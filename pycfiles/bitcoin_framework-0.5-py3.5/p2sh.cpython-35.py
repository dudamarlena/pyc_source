# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/script/sig/p2sh.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 2566 bytes
"""
Models a P2SH scriptSig, including the script with the conditions to spend
and the spend conditions such as signatures in multisig smart contracts,
secrets, etc...
"""
from .model import ScriptSig
from ...field.script import ScriptData

class P2SH(ScriptSig):
    __doc__ = '\n    Models a pay-to-script-hash scriptSig, containing in one side the reedem\n    script payment values (signatures, secrets, ...) and the redeem script\n    itself. The class allows to define separately the spend requirements and\n    the redeem script so when serialized they are put together as in a P2SH,\n    with the push data opcodes\n    needed.\n\n    Attributes:\n        payment_script (Script): script with payment values\n        reedem_script (ReedemScript): script with payment requirements\n    '
    __slots__ = ['_payment_script', '_redeem_script']

    def __init__(self, redeem_script, payment_script, tx_input=None):
        super().__init__(tx_input, None)
        self._payment_script = payment_script
        self._redeem_script = redeem_script

    def serialize(self):
        self._build()
        return super().serialize()

    def _build(self):
        """
        Serializes the P2SH scriptSig, by joining payment and redeem script
        """
        assert self._payment_script is not None, "Can't build the P2SH " + 'scriptSig, the payment script has not been set'
        assert self._redeem_script is not None, "Can't build the P2SH " + 'scriptSig, the redeem script has not been set'
        self._data = [self._payment_script,
         ScriptData(self._redeem_script.serialize())]

    @property
    def redeem_script(self):
        """ Returns the redeem script """
        return self._redeem_script

    @redeem_script.setter
    def redeem_script(self, script):
        """ Sets the redeem script """
        self._redeem_script = script

    @property
    def payment_script(self):
        """ Returns the payment script """
        return self._payment_script

    @payment_script.setter
    def payment_script(self, script):
        """ Sets the payment script """
        self._payment_script = script

    def __str__(self, space):
        txt = '\n%s// %s\n' % (space, self.__class__.__name__)
        txt += '%sPaymentScript:\n%s\n' % (
         space,
         self._payment_script.__str__(space + '    '))
        txt += '%sRedeemScript:\n%s\n' % (
         space,
         self._redeem_script.__str__(space + '    '))
        return txt