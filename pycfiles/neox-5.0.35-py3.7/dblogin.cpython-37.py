# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/dblogin.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 6966 bytes
import sys, os, gettext, logging
from collections import OrderedDict
from pathlib import Path
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton, QLineEdit, QHBoxLayout, QDialog, QFrame, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from neox.commons import connection
from neox.commons import common
from neox.commons.config import Params
from neox.commons.dialogs import QuickDialog
from neox.commons.forms import GridForm
_ = gettext.gettext
__all__ = [
 'Login', 'xconnection']
pkg_dir = str(Path(os.path.dirname(__file__)).parents[0])
path_logo = os.path.join(pkg_dir, 'share', 'login.png')
file_base_css = os.path.join(pkg_dir, 'css', 'base.css')
file_tablet_css = os.path.join(pkg_dir, 'css', 'tablet.css')

class Login(QDialog):

    def __init__(self, parent=None, file_config=''):
        super(Login, self).__init__(parent)
        logging.info(' Start login Neox system X...')
        self.connection = None
        params = Params(file_config)
        self.params = params.params
        self.setObjectName('dialog_login')
        if self.params.get('tablet_mode') == 'True':
            self.tablet_mode = eval(self.params['tablet_mode'])
            self.set_style([file_tablet_css])
        else:
            self.set_style([file_base_css])
            self.tablet_mode = None
        self.init_UI()

    def set_style(self, style_files):
        styles = []
        for style in style_files:
            with open(style, 'r') as (infile):
                styles.append(infile.read())

        self.setStyleSheet(''.join(styles))

    def init_UI(self):
        hbox_logo = QHBoxLayout()
        label_logo = QLabel()
        label_logo.setObjectName('label_logo')
        hbox_logo.addWidget(label_logo, 0)
        pixmap_logo = QPixmap(path_logo)
        label_logo.setPixmap(pixmap_logo)
        hbox_logo.setAlignment(label_logo, Qt.AlignHCenter)
        values = OrderedDict([
         (
          'host', {'name':self.tr('HOST'),  'readonly':True}),
         (
          'database', {'name':self.tr('DATABASE'),  'readonly':True}),
         (
          'user', {'name': self.tr('USER')}),
         (
          'password', {'name': self.tr('PASSWORD')})])
        formLayout = GridForm(self, values=values, col=1)
        self.field_password.setEchoMode(QLineEdit.Password)
        self.field_password.textChanged.connect(self.clear_message)
        box_buttons = QDialogButtonBox()
        pushButtonCancel = QPushButton(self.tr('C&ANCEL'))
        pushButtonCancel.setObjectName('button_cancel')
        box_buttons.addButton(pushButtonCancel, QDialogButtonBox.RejectRole)
        pushButtonOk = QPushButton(self.tr('&CONNECT'))
        pushButtonOk.setAutoDefault(True)
        pushButtonOk.setDefault(False)
        pushButtonOk.setObjectName('button_ok')
        box_buttons.addButton(pushButtonOk, QDialogButtonBox.AcceptRole)
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(box_buttons)
        line = QFrame()
        line.setFrameShape(line.HLine)
        line.setFrameShadow(line.Sunken)
        hbox_line = QHBoxLayout()
        hbox_line.addWidget(line)
        hbox_msg = QHBoxLayout()
        MSG = self.tr('Error: username or password invalid...!')
        self.error_msg = QLabel(MSG)
        self.error_msg.setObjectName('login_msg_error')
        self.error_msg.setAlignment(Qt.AlignCenter)
        hbox_msg.addWidget(self.error_msg)
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(hbox_logo)
        vbox_layout.addLayout(formLayout)
        vbox_layout.addLayout(hbox_msg)
        vbox_layout.addLayout(hbox_line)
        vbox_layout.addLayout(hbox_buttons)
        self.setLayout(vbox_layout)
        self.setWindowTitle('Login Presik System')
        self.clear_message()
        self.field_password.setFocus()
        box_buttons.accepted.connect(self.accept)
        box_buttons.rejected.connect(self.reject)

    def clear_message(self):
        self.error_msg.hide()

    def run(self, profile=None):
        if self.params['database']:
            self.field_database.setText(self.params['database'])
        if self.params['user']:
            self.field_user.setText(self.params['user'])
        if self.params['server']:
            self.field_host.setText(self.params['server'])

    def accept(self):
        self.validate_access()
        super(Login, self).accept()

    def reject(self):
        sys.exit()

    def validate_access(self):
        user = self.field_user.text()
        password = self.field_password.text()
        self.connection = xconnection(user, password, self.params['server'], self.params['port'], self.params['database'], self.params['protocol'])
        print(('  >> > ', self.connection))
        if not self.connection:
            self.field_password.setText('')
            self.field_password.setFocus()
            self.error_message()
        self.params['user'] = user
        self.params['password'] = password

    def error_message(self):
        self.error_msg.show()


def xconnection(user, password, host, port, database, protocol):
    try:
        url = 'http://%s:%s@%s:%s/%s/' % (
         user, password, host, port, database)
        try:
            if not common.test_server_version(host, int(port)):
                print('Incompatible version of the server')
                return
        except:
            pass

        if protocol == 'json':
            print(('::::::::::::  Usando protocolo JSON > ', url))
            conn = connection.set_jsonrpc(url[:-1])
        else:
            if protocol == 'local':
                conn = connection.set_trytond(database=database,
                  user=user)
            else:
                if protocol == 'xml':
                    print((':::::::::::: Usando protocolo XML > ', url))
                    conn = connection.set_xmlrpc(url)
                else:
                    print('Protocol error...!')
                    return
        return conn
    except:
        print('LOG: Data connection invalid!')
        return


def safe_reconnect(main):
    field_password = QLineEdit()
    field_password.setEchoMode(QLineEdit.Password)
    field_password.cursorPosition()
    field_password.cursor()
    dialog_password = QuickDialog(main, 'question', info=(main.tr('Enter your password:')),
      widgets=[
     field_password],
      buttons=[
     'ok'],
      response=True)
    field_password.setFocus()
    password = field_password.text()
    if not password or password == '':
        safe_reconnect(main)
    else:
        main.conn = xconnection(main.user, str(password), main.server, main.port, main.database, main.protocol)
        if main.conn:
            field_password.setText('')
            dialog_password.hide()
            main.global_timer = 0
        else:
            safe_reconnect(main)