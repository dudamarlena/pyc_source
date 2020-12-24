# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/trustedcoin/cmdline.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 1854 bytes
from electrum.i18n import _
from electrum.plugin import hook
from .trustedcoin import TrustedCoinPlugin

class Plugin(TrustedCoinPlugin):

    def prompt_user_for_otp(self, wallet, tx):
        if not isinstance(wallet, self.wallet_class):
            return
        if not wallet.can_sign_without_server():
            self.logger.info('twofactor:sign_tx')
            auth_code = None
            if wallet.keystores['x3/'].get_tx_derivations(tx):
                msg = _('Please enter your Google Authenticator code:')
                auth_code = int(input(msg))
            else:
                self.logger.info('twofactor: xpub3 not needed')
            wallet.auth_code = auth_code