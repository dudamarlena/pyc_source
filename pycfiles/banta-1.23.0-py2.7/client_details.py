# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\client_details.py
# Compiled at: 2012-10-12 11:59:32
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import PySide.QtCore as _qc, PySide.QtGui as _qg, banta.utils, banta.db as _db, banta.packages as _pkg

class ClientDetails(_pkg.GenericModule):
    REQUIRES = (
     _pkg.GenericModule.P_ADMIN,)
    NAME = b'client_details'

    def __init__(self, app):
        super(ClientDetails, self).__init__(app)
        self.app.window.bClientAccount.setVisible(False)

    def load(self):
        w = self.app.window
        self.dialog = self.app.uiLoader.load(b':/data/ui/client_details.ui')
        self.dialog.tr = banta.utils.unitr(self.dialog.trUtf8)
        self.dialog.setWindowIcon(w.windowIcon())
        self.dialog.setWindowTitle(self.dialog.tr(b'Detalles de cliente'))
        w.bClientAccount.setDefaultAction(w.acShowClientDetails)

    @_qc.Slot()
    def showDetails(self):
        """Creates a new Client for a temporary use (one shot/one buy)
                The idea of this is not to bloat the client list with one-time shoppers
                """
        d = self.dialog
        w = self.app.window
        model = w.v_clients.model()
        selected = w.v_clients.selectedIndexes()
        if not selected:
            return
        r = selected[0]
        cli_code = r.data(_qc.Qt.UserRole)
        cli = _db.DB.clients[cli_code]
        d.balance.setText(str(cli.balance))
        if d.exec_() != _qg.QDialog.Accepted:
            return