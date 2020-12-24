# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/startup_widget.py
# Compiled at: 2017-08-29 09:44:06
from qtpy import QtWidgets, QtGui, QtCore
import socket, logging
from ..sshshell import SshShell
from ..async_utils import APP

class HostnameSelectorWidget(QtWidgets.QDialog):
    _HIDE_PASSWORDS = False
    _SKIP_REDPITAYA_SIGNATURE = True
    _SCAN_TIMEOUT = 0.04
    _CONNECT_TIMEOUT = 1.0

    def __init__(self, parent=None):
        self.parent = parent
        self.items = []
        self.ips_and_macs = []
        self._logger = logging.getLogger(__name__)
        super(HostnameSelectorWidget, self).__init__()
        self.setWindowTitle('Red Pitaya connection - find a valid hostname')
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.hlay1 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.hlay1)
        self.user_label = QtWidgets.QLabel('user')
        self.hlay1.addWidget(self.user_label)
        self.user_input = QtWidgets.QLineEdit('root')
        self.hlay1.addWidget(self.user_input)
        self.password_label = QtWidgets.QLabel('password')
        self.password_input = QtWidgets.QLineEdit('root')
        if self._HIDE_PASSWORDS:
            self.password_input.setEchoMode(self.password_input.PasswordEchoOnEdit)
        self.hlay1.addWidget(self.password_label)
        self.hlay1.addWidget(self.password_input)
        self.sshport_input = QtWidgets.QLineEdit(text='22')
        self.sshport_label = QtWidgets.QLabel('ssh port')
        self.hlay1.addWidget(self.sshport_label)
        self.hlay1.addWidget(self.sshport_input)
        self.refresh = QtWidgets.QPushButton('Refresh list')
        self.refresh.clicked.connect(self.scan)
        self.hlay1.addWidget(self.refresh)
        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setGeometry(200, 80, 250, 20)
        self.hlay1.addWidget(self.progressbar)
        self.progressbar.hide()
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(['IP address', 'MAC address'])
        self.layout.addWidget(self.tree)
        self.hlay2 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.hlay2)
        self.hostname_label = QtWidgets.QLabel('Hostname')
        self.hostname_input = QtWidgets.QLineEdit()
        self.hostname_input.setPlaceholderText('e.g.: 192.168.1.100')
        self.hlay2.addWidget(self.hostname_label)
        self.hlay2.addWidget(self.hostname_input)
        self.hlay3 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.hlay3)
        self.ok_button = QtWidgets.QPushButton('OK')
        self.ok_button.clicked.connect(self.ok)
        self.ok_button.setDefault(True)
        self.hlay2.addWidget(self.ok_button)
        self.tree.itemSelectionChanged.connect(self.item_selected)
        self.tree.itemDoubleClicked.connect(self.item_double_clicked)
        self.scanning = False
        for signalname in ['cursorPositionChanged',
         'editingFinished',
         'returnPressed',
         'selectionChanged',
         'textChanged',
         'textEdited']:
            for textbox in [self.user_input, self.password_input,
             self.sshport_input,
             self.hostname_input]:
                getattr(textbox, signalname).connect(self.countdown_cancel)

    def showEvent(self, QShowEvent):
        ret = super(HostnameSelectorWidget, self).showEvent(QShowEvent)
        if not self.ips_and_macs:
            self._aux_timer = QtCore.QTimer.singleShot(10, self.scan)
        return ret

    @property
    def hostname(self):
        return self.hostname_input.text()

    @hostname.setter
    def hostname(self, val):
        self.hostname_input.setText(val)

    @property
    def password(self):
        return self.password_input.text()

    @password.setter
    def password(self, val):
        self.password_input.setText(val)

    @property
    def user(self):
        return self.user_input.text()

    @user.setter
    def user(self, val):
        self.user_input.setText(val)

    @property
    def sshport(self):
        return int(self.sshport_input.text())

    @sshport.setter
    def sshport(self, val):
        self.sshport_input.setText(str(val))

    def item_selected(self):
        self.countdown_cancel()
        try:
            item = self.tree.selectedItems()[0]
        except:
            pass
        else:
            self.hostname = item.text(0)

    def item_double_clicked(self, item, row):
        self.countdown_cancel()
        self.hostname = item.text(0)
        self.ok()

    def ok(self):
        self.countdown_cancel()
        self.scanning = False
        self.hide()
        self.accept()

    @property
    def scanning(self):
        return self._scanning

    @scanning.setter
    def scanning(self, v):
        self._scanning = v
        self.refresh.setEnabled(not v)
        if v:
            self.refresh.setText('Searching LAN for Red Pitayas...')
        else:
            self.refresh.setText('Refresh list')
        self.sshport_input.setEnabled(not v)
        self.user_input.setEnabled(not v)
        self.password_input.setEnabled(not v)
        if v:
            self.progressbar.show()
        else:
            self.progressbar.hide()

    def scan(self):
        """
        Scan the local area network for available Red Pitayas.

        In order to work, the specified username and password must be correct.
        """
        self.countdown_cancel()
        if self.scanning:
            self._logger.debug('Scan is already running. Please wait for it to finish before starting a new one! ')
            return
        self.progressbar.setValue(0)
        self.scanning = True
        self.tree.clear()
        del self.items[:]
        del self.ips_and_macs[:]
        self.add_device('_FAKE_', 'Simulated Red Pitaya')
        port = self.sshport
        user = self.user
        password = self.password
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            try:
                s.connect(('10.255.255.255', 1))
                ip = s.getsockname()[0]
            except:
                ip = '127.0.0.1'

        finally:
            s.close()

        self._logger.debug('Your own ip is: %s', ip)
        end = ip.split('.')[(-1)]
        start = ip[:-len(end)]
        ips = [ start + str(i) for i in range(256) ]
        self.progressbar.setRange(0, len(ips))
        for i, ip in enumerate(ips):
            if not self.scanning:
                return
            self.progressbar.setValue(i)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self._SCAN_TIMEOUT)
            err = s.connect_ex((ip, port))
            s.close()
            if err == 0:
                self._logger.debug('%s:%d is open', ip, port)
                try:
                    ssh = SshShell(hostname=ip, user=user, password=password, timeout=self._CONNECT_TIMEOUT)
                except BaseException as e:
                    self._logger.debug('Cannot log in with user=%s, pw=%s at %s: %s', user, password, ip, e)

                macs = ssh.get_mac_addresses()
                del ssh
                for mac in macs:
                    if mac.startswith('00:26:32:') or self._SKIP_REDPITAYA_SIGNATURE:
                        self._logger.debug('RP device found: IP %s, MAC %s', ip, mac)
                        self.add_device(ip, mac)

            APP.processEvents()

        self.scanning = False
        if len(self.ips_and_macs) == 2:
            self.countdown_start()

    def countdown_start(self, countdown_s=10.0):
        self.countdown_cancel()
        self.countdown_cancelled = False
        self.countdown_remaining = countdown_s
        if not hasattr(self, 'countdown_timer'):
            self.countown_timer = QtCore.QTimer.singleShot(1, self.countdown_iteration)

    def countdown_iteration(self):
        if self.countdown_cancelled:
            return
        self.countdown_remaining -= 1
        self.ok_button.setText('OK (auto-clicked in %d s)' % self.countdown_remaining)
        if self.countdown_remaining >= 0:
            self.countown_timer = QtCore.QTimer.singleShot(1000, self.countdown_iteration)
        else:
            self.ok()

    def countdown_cancel(self, *args, **kwargs):
        self.countdown_cancelled = True
        self.ok_button.setText('OK')

    def add_device(self, hostname, token):
        self.ips_and_macs.append((hostname, token))
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, hostname)
        item.setText(1, token)
        self.items.append(item)
        self.tree.addTopLevelItem(item)
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)
        if len(self.ips_and_macs) == 2 and self.hostname == '' or self.hostname == hostname:
            self.hostname = hostname
            self.tree.clearSelection()
            item.setSelected(True)
        return item

    def remove_device(self, item):
        self.items.remove(item)
        self.tree.removeItemWidget(item, 0)

    def get_kwds(self):
        self.exec_()
        return dict(hostname=self.hostname, password=self.password, user=self.user, sshport=self.sshport)