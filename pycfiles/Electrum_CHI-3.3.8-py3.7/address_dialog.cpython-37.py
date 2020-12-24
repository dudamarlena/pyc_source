# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/address_dialog.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 3857 bytes
from electrum.i18n import _
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from .util import WindowModalDialog, ButtonsLineEdit, ColorScheme, Buttons, CloseButton
from .history_list import HistoryList, HistoryModel
from .qrtextedit import ShowQRTextEdit

class AddressHistoryModel(HistoryModel):

    def __init__(self, parent, address):
        super().__init__(parent)
        self.address = address

    def get_domain(self):
        return [
         self.address]


class AddressDialog(WindowModalDialog):

    def __init__(self, parent, address):
        WindowModalDialog.__init__(self, parent, _('Address'))
        self.address = address
        self.parent = parent
        self.config = parent.config
        self.wallet = parent.wallet
        self.app = parent.app
        self.saved = True
        self.setMinimumWidth(700)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(QLabel(_('Address:')))
        self.addr_e = ButtonsLineEdit(self.address)
        self.addr_e.addCopyButton(self.app)
        icon = 'qrcode_white.png' if ColorScheme.dark_scheme else 'qrcode.png'
        self.addr_e.addButton(icon, self.show_qr, _('Show QR Code'))
        self.addr_e.setReadOnly(True)
        vbox.addWidget(self.addr_e)
        try:
            pubkeys = self.wallet.get_public_keys(address)
        except BaseException as e:
            try:
                pubkeys = None
            finally:
                e = None
                del e

        if pubkeys:
            vbox.addWidget(QLabel(_('Public keys') + ':'))
            for pubkey in pubkeys:
                pubkey_e = ButtonsLineEdit(pubkey)
                pubkey_e.addCopyButton(self.app)
                pubkey_e.setReadOnly(True)
                vbox.addWidget(pubkey_e)

        try:
            redeem_script = self.wallet.pubkeys_to_redeem_script(pubkeys)
        except BaseException as e:
            try:
                redeem_script = None
            finally:
                e = None
                del e

        if redeem_script:
            vbox.addWidget(QLabel(_('Redeem Script') + ':'))
            redeem_e = ShowQRTextEdit(text=redeem_script)
            redeem_e.addCopyButton(self.app)
            vbox.addWidget(redeem_e)
        vbox.addWidget(QLabel(_('History')))
        addr_hist_model = AddressHistoryModel(self.parent, self.address)
        self.hw = HistoryList(self.parent, addr_hist_model)
        addr_hist_model.set_view(self.hw)
        vbox.addWidget(self.hw)
        vbox.addLayout(Buttons(CloseButton(self)))
        self.format_amount = self.parent.format_amount
        addr_hist_model.refresh('address dialog constructor')

    def show_qr(self):
        text = self.address
        try:
            self.parent.show_qrcode(text, 'Address', parent=self)
        except Exception as e:
            try:
                self.show_message(repr(e))
            finally:
                e = None
                del e