# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/dialogs/auth.py
# Compiled at: 2013-09-07 09:08:02
from qtalchemy import *
from PySide import QtCore, QtGui
from .auth_settings import AuthSettings
from .objectforms import MapperDialog, exception_message_box

class LoginDialog(MapperDialog):
    """
    >>> from qtalchemy.dialogs import LoginDialog
    >>> app = qtapp()
    >>> d=LoginDialog()
    >>> d.exec_()  #doctest: +SKIP
    0
    """

    def __init__(self, parent=None, init_session_maker=None, init_db=None):
        MapperDialog.__init__(self, parent)
        self.init_session_maker = init_session_maker
        self.init_db = init_db
        self.settings = AuthSettings()
        self.settings.loadSettings()
        self.setWindowTitle(self.tr('Log In'))
        main = QtGui.QVBoxLayout(self)
        user_grid = LayoutLayout(main, QtGui.QFormLayout())
        self.m_user = self.mapClass(AuthSettings)
        self.m_user.addBoundField(user_grid, 'user')
        self.m_user.addBoundField(user_grid, 'password')
        self.m_user.addBoundField(user_grid, 'server_string')
        self.server_details = QtGui.QGroupBox('Server Details')
        main_ext = QtGui.QVBoxLayout(self.server_details)
        user_grid = LayoutLayout(main_ext, QtGui.QFormLayout())
        self.m_server = self.mapClass(AuthSettings)
        self.m_server.addBoundField(user_grid, 'server')
        self.m_server.addBoundField(user_grid, 'database')
        self.showing_details = False
        self.server_details.setVisible(self.showing_details)
        LayoutWidget(main, self.server_details)
        remember_layout = LayoutLayout(main, QtGui.QHBoxLayout())
        self.m_user.addBoundField(remember_layout, 'remember_server')
        self.m_user.addBoundField(remember_layout, 'remember_user')
        self.m_user.connect_instance(self.settings)
        self.m_server.connect_instance(self.settings)
        buttonbox = LayoutWidget(main, QtGui.QDialogButtonBox())
        buttonbox.addButton(QtGui.QDialogButtonBox.Ok)
        buttonbox.addButton(QtGui.QDialogButtonBox.Cancel)
        self.detailsBtn = ButtonBoxButton(buttonbox, QtGui.QPushButton('&Server'), QtGui.QDialogButtonBox.ActionRole)
        self.detailsBtn.clicked.connect(self.details_handler)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

    def details_handler(self):
        self.showing_details = not self.showing_details
        self.server_details.setVisible(self.showing_details)
        self.setFixedHeight(self.sizeHint().height())
        self.setFixedWidth(self.sizeHint().width())

    def accept(self):
        self.submit()
        self.settings.saveSettings()
        self.connection = '%s://%s:%s@%s/%s' % (self.settings.server_type, self.settings.user, self.settings.password, self.settings.server, self.settings.database)
        try:
            if self.init_session_maker is not None:
                self.init_session_maker(self.connection)
            super(LoginDialog, self).accept()
        except Exception as e:
            exception_message_box(e, 'There was an error initializing the data.', icon=QtGui.QMessageBox.Warning)

        return


def auth_dialog(parent=None, init_session_maker=None, init_db=None):
    a = LoginDialog(parent, init_session_maker, init_db)
    a.show()
    return a.exec_()