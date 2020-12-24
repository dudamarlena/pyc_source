# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/gui/qt/configure_name_dialog.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 8380 bytes
import sys, traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from electrum.bitcoin import TYPE_ADDRESS
from electrum.commands import NameAlreadyExistsError
from electrum.i18n import _
from electrum.names import format_name_identifier
from electrum.network import TxBroadcastError, BestEffortRequestFailed
from electrum.util import NotEnoughFunds, NoDynamicFeeEstimates
from electrum.wallet import InternalAddressCorruption
from .paytoedit import PayToEdit
dialogs = []

def show_configure_name(identifier, value, parent, is_new):
    d = ConfigureNameDialog(identifier, value, parent, is_new)
    dialogs.append(d)
    d.show()


class ConfigureNameDialog(QDialog):

    def __init__(self, identifier, value, parent, is_new):
        QDialog.__init__(self, parent=None)
        self.main_window = parent
        self.setMinimumWidth(545)
        self.setMinimumHeight(245)
        if is_new:
            self.setWindowTitle(_('Configure New Name'))
        else:
            self.setWindowTitle(_('Reconfigure Name'))
        form_layout = QFormLayout()
        self.identifier = identifier
        formatted_name = format_name_identifier(identifier)
        form_layout.addRow(QLabel(formatted_name))
        self.dataEdit = QLineEdit()
        self.dataEdit.setText(value.decode('ascii'))
        form_layout.addRow(_('Data:'), self.dataEdit)
        self.transferTo = PayToEdit(self.main_window)
        form_layout.addRow(_('Transfer to:'), self.transferTo)
        form = QWidget()
        form.setLayout(form_layout)
        self.buttons_box = QDialogButtonBox()
        self.buttons_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addStretch()
        buttons_hbox.addWidget(self.buttons_box)
        buttons = QWidget()
        buttons.setLayout(buttons_hbox)
        vbox = QVBoxLayout()
        vbox.addWidget(form)
        vbox.addWidget(buttons)
        self.setLayout(vbox)
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        if is_new:
            self.accepted.connect(lambda : self.register_and_broadcast(self.identifier, self.dataEdit.text().encode('ascii'), self.transferTo))
        else:
            self.accepted.connect(lambda : self.update_and_broadcast(self.identifier, self.dataEdit.text().encode('ascii'), self.transferTo))

    def register_and_broadcast(self, identifier, value, transfer_to):
        if transfer_to.toPlainText() == '':
            recipient_address = None
        else:
            recipient = transfer_to.get_recipient()
            if recipient is None:
                recipient_type, recipient_address = None, transfer_to.toPlainText()
            else:
                recipient_type, recipient_address = recipient
            if recipient_type != TYPE_ADDRESS:
                self.main_window.show_error(_('Invalid address ') + recipient_address)
                return
            else:
                name_register = self.main_window.console.namespace.get('name_register')
                broadcast = self.main_window.console.namespace.get('broadcast')
                try:
                    tx = name_register(identifier.decode('utf-8'), value.decode('ascii'), recipient_address)['hex']
                except NameAlreadyExistsError as e:
                    try:
                        self.main_window.show_message(_('Error registering ') + formatted_name + ': ' + str(e))
                        return
                    finally:
                        e = None
                        del e

                except (NotEnoughFunds, NoDynamicFeeEstimates) as e:
                    try:
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_message(_('Error registering ') + formatted_name + ': ' + str(e))
                        return
                    finally:
                        e = None
                        del e

                except InternalAddressCorruption as e:
                    try:
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_error(_('Error registering ') + formatted_name + ': ' + str(e))
                        raise
                    finally:
                        e = None
                        del e

                except BaseException as e:
                    try:
                        traceback.print_exc(file=(sys.stdout))
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_message(_('Error registering ') + formatted_name + ': ' + str(e))
                        return
                    finally:
                        e = None
                        del e

            try:
                broadcast(tx)
            except Exception as e:
                try:
                    formatted_name = format_name_identifier(identifier)
                    self.main_window.show_error(_('Error broadcasting registration for ') + formatted_name + ': ' + str(e))
                    return
                finally:
                    e = None
                    del e

    def update_and_broadcast(self, identifier, value, transfer_to):
        if transfer_to.toPlainText() == '':
            recipient_address = None
        else:
            recipient = transfer_to.get_recipient()
            if recipient is None:
                recipient_type, recipient_address = None, transfer_to.toPlainText()
            else:
                recipient_type, recipient_address = recipient
            if recipient_type != TYPE_ADDRESS:
                self.main_window.show_error(_('Invalid address ') + recipient_address)
                return
            else:
                name_update = self.main_window.console.namespace.get('name_update')
                broadcast = self.main_window.console.namespace.get('broadcast')
                try:
                    tx = name_update(identifier.decode('utf-8'), value.decode('ascii'), recipient_address)['hex']
                except (NotEnoughFunds, NoDynamicFeeEstimates) as e:
                    try:
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_message(_('Error creating update for ') + formatted_name + ': ' + str(e))
                        return
                    finally:
                        e = None
                        del e

                except InternalAddressCorruption as e:
                    try:
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_error(_('Error creating update for ') + formatted_name + ': ' + str(e))
                        raise
                    finally:
                        e = None
                        del e

                except BaseException as e:
                    try:
                        traceback.print_exc(file=(sys.stdout))
                        formatted_name = format_name_identifier(identifier)
                        self.main_window.show_message(_('Error creating update for ') + formatted_name + ': ' + str(e))
                        return
                    finally:
                        e = None
                        del e

            try:
                broadcast(tx)
            except Exception as e:
                try:
                    formatted_name = format_name_identifier(identifier)
                    self.main_window.show_error(_('Error broadcasting update for ') + formatted_name + ': ' + str(e))
                    return
                finally:
                    e = None
                    del e