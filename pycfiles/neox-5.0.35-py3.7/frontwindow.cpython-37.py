# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/frontwindow.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 4448 bytes
import os, time, logging
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from neox.commons.dialogs import QuickDialog
from neox.commons.dblogin import safe_reconnect
__all__ = [
 'FrontWindow', 'ClearUi']
parent = Path(__file__).parent.parent
file_base_css = os.path.join(str(parent), 'css', 'base.css')
_DEFAULT_TIMEOUT = 60000
path_trans = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale', 'i18n_es.qm')

class FrontWindow(QMainWindow):

    def __init__(self, connection, params, title=None, show_mode=None):
        super(FrontWindow, self).__init__()
        if not title:
            title = self.tr('APPLICATION')
        self._state = None
        self._keyStates = {}
        self.window().setWindowTitle(title)
        self.setObjectName('WinMain')
        self.conn = connection
        self._context = connection.context
        self.set_params(params)
        self.logger = logging.getLogger('neox_logger')
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        screen_width = screen.width()
        print(('Screen width : ', screen_width))
        self.screen_size = 'large'
        if screen_width <= 1024:
            self.screen_size = 'small'
        else:
            if screen_width <= 1366:
                self.screen_size = 'medium'
            else:
                self.timeout = _DEFAULT_TIMEOUT
                self.set_stack_messages()
                if show_mode == 'fullscreen':
                    self.window().showFullScreen()
                else:
                    self.window().show()
            self.setFocus()
            self.global_timer = 0

    def set_stack_messages(self):
        self.stack_msg = {}

    def get_geometry(self):
        screen = QDesktopWidget().screenGeometry()
        return (screen.width(), screen.height())

    def set_statusbar(self, values):
        status_bar = self.statusBar()
        status_bar.setSizeGripEnabled(False)
        for k, v in list(values.items()):
            _label = QLabel(v['name'] + ':')
            _label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            status_bar.addWidget(_label, 1)
            setattr(self, k, QLabel(str(v['value'])))
            _label_info = getattr(self, k)
            _label_info.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            status_bar.addWidget(_label_info)

    def set_style(self, file_css):
        styles = []
        for style in [file_base_css, file_css]:
            with open(style, 'r') as (infile):
                styles.append(infile.read())

        self.setStyleSheet(''.join(styles))

    def set_timeout(self):
        if self.active_timeout != 'True':
            return
        self.timeout = eval(self.timeout)
        if not self.timeout:
            self.timeout = _DEFAULT_TIMEOUT
        timer = QTimer(self)
        timer.timeout.connect(self.count_time)
        timer.start(1000)

    def count_time(self):
        self.global_timer += 1
        if self.global_timer > self.timeout:
            self.global_timer = 0
            safe_reconnect()

    def dialog(self, name, response=False):
        res = QuickDialog(parent=self,
          kind=(self.stack_msg[name][0]),
          string=(self.stack_msg[name][1]))
        return res

    def set_params(self, values):
        for k, v in list(values.items()):
            if v in ('False', 'True'):
                v = eval(v)
            setattr(self, k, v)

    def action_block(self):
        safe_reconnect(self)

    def dialog_password_accept(self):
        self.connection()

    def dialog_password_rejected(self):
        self.connection()

    def keyReleaseEvent(self, event):
        self._keyStates[event.key()] = False


class ClearUi(QThread):
    sigActionClear = pyqtSignal()
    state = None

    def __init__(self, wait_time):
        QThread.__init__(self)
        self.wait_time = wait_time

    def run(self):
        time.sleep(self.wait_time)
        self.sigActionClear.emit()