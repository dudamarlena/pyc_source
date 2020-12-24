# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/trustedcoin/kivy.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 4365 bytes
from functools import partial
from threading import Thread
import re
from decimal import Decimal
from kivy.clock import Clock
from electrum.i18n import _
from electrum.plugin import hook
from .trustedcoin import TrustedCoinPlugin, server, KIVY_DISCLAIMER, TrustedCoinException, ErrorConnectingServer

class Plugin(TrustedCoinPlugin):
    disclaimer_msg = KIVY_DISCLAIMER

    def __init__(self, parent, config, name):
        super().__init__(parent, config, name)

    @hook
    def load_wallet(self, wallet, window):
        if not isinstance(wallet, self.wallet_class):
            return
        self.start_request_thread(wallet)

    def go_online_dialog(self, wizard):
        wizard.run('accept_terms_of_use')

    def prompt_user_for_otp(self, wallet, tx, on_success, on_failure):
        from gui.kivy.uix.dialogs.label_dialog import LabelDialog
        msg = _('Please enter your Google Authenticator code')
        d = LabelDialog(msg, '', lambda otp: self.on_otp(wallet, tx, otp, on_success, on_failure))
        d.open()

    def on_otp(self, wallet, tx, otp, on_success, on_failure):
        try:
            wallet.on_otp(tx, otp)
        except TrustedCoinException as e:
            try:
                if e.status_code == 400:
                    Clock.schedule_once(lambda dt: on_failure(_('Invalid one-time password.')))
                else:
                    Clock.schedule_once(lambda dt, bound_e=e: on_failure(_('Error') + ':\n' + str(bound_e)))
            finally:
                e = None
                del e

        except Exception as e:
            try:
                Clock.schedule_once(lambda dt, bound_e=e: on_failure(_('Error') + ':\n' + str(bound_e)))
            finally:
                e = None
                del e

        else:
            on_success(tx)

    def accept_terms_of_use(self, wizard):

        def handle_error(msg, e):
            wizard.show_error(msg + ':\n' + repr(e))
            wizard.terminate()

        try:
            tos = server.get_terms_of_service()
        except ErrorConnectingServer as e:
            try:
                Clock.schedule_once(lambda dt, bound_e=e: handle_error(_('Error connecting to server'), bound_e))
            finally:
                e = None
                del e

        except Exception as e:
            try:
                Clock.schedule_once(lambda dt, bound_e=e: handle_error(_('Error'), bound_e))
            finally:
                e = None
                del e

        else:
            f = lambda x: self.read_email(wizard)
            wizard.tos_dialog(tos=tos, run_next=f)

    def read_email(self, wizard):
        f = lambda x: self.create_remote_key(x, wizard)
        wizard.email_dialog(run_next=f)

    def request_otp_dialog(self, wizard, short_id, otp_secret, xpub3):
        f = lambda otp, reset: self.check_otp(wizard, short_id, otp_secret, xpub3, otp, reset)
        wizard.otp_dialog(otp_secret=otp_secret, run_next=f)

    @hook
    def abort_send(self, window):
        wallet = window.wallet
        if not isinstance(wallet, self.wallet_class):
            return
        if wallet.can_sign_without_server():
            return
        if wallet.billing_info is None:
            self.start_request_thread(wallet)
            Clock.schedule_once(lambda dt: window.show_error(_('Requesting account info from TrustedCoin server...') + '\n' + _('Please try again.')))
            return True
        return False