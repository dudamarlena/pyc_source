# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_iface_pyqt4.py
# Compiled at: 2014-02-15 07:04:03
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from . import upd_core
from . import upd_iface
from .upd_log import logger

class UpdatePyQt4Interface(QObject, upd_iface.UpdateGenericGuiInterface):

    def __init__(self, updater, parent=None, **kwargs):
        self.timer = None
        QObject.__init__(self, parent=parent)
        upd_iface.UpdateGenericGuiInterface.__init__(self, updater, **kwargs)
        return

    def get_settings_object(self):
        """
        Subclasses may reimplement this function to cusomize where the settings are stored.
        """
        settings = QSettings()
        settings.beginGroup('updater4pyi')
        return settings

    def load_settings(self, keylist):
        settings = self.get_settings_object()
        d = {}
        for key in keylist:
            if settings.contains(key):
                d[key] = settings.value(key).toPyObject()

        logger.debug('load_settings: read settings: %r', d)
        return d

    def save_settings(self, d=None):
        if d is None:
            d = self.all_settings()
        logger.debug('save_settings: saving settings: %r', d)
        settings = self.get_settings_object()
        for k, v in d.iteritems():
            settings.setValue(k, QVariant(v))

        settings.sync()
        return

    def ask_first_time(self):
        msgBox = QMessageBox(parent=None)
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setText(unicode(self.tr('Would you like to regularly check for software updates%s?')) % (unicode(self.tr(' for %s')) % self.progname if self.progname else ''))
        msgBox.addButton(QMessageBox.Yes)
        msgBox.addButton(QMessageBox.No)
        msgBox.setIcon(QMessageBox.Question)
        msgBox.show()
        msgBox.raise_()
        while msgBox.isVisible():
            QApplication.processEvents()

        if msgBox.clickedButton() == msgBox.button(QMessageBox.Yes):
            return True
        else:
            return False

    def ask_to_update(self, rel_info):
        msgBox = QMessageBox(parent=None)
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setText(unicode(self.tr('A new software update is available (%sversion %s). Do you want to install it?')) % (
         self.progname + ' ' if self.progname else '', rel_info.get_version()))
        msgBox.setInformativeText(self.tr('Please make sure you save all your changes to your files before installing the update.'))
        btnInstall = msgBox.addButton('Install', QMessageBox.AcceptRole)
        btnNotNow = msgBox.addButton('Not now', QMessageBox.RejectRole)
        btnDisableUpdates = msgBox.addButton('Disable Update Checks', QMessageBox.RejectRole)
        msgBox.setDefaultButton(btnInstall)
        msgBox.setEscapeButton(btnNotNow)
        msgBox.setIcon(QMessageBox.Question)
        msgBox.show()
        msgBox.raise_()
        while msgBox.isVisible():
            QApplication.processEvents()

        clickedbutton = msgBox.clickedButton()
        if clickedbutton == btnInstall:
            return True
        else:
            if clickedbutton == btnDisableUpdates:
                self.setCheckForUpdatesEnabled(False)
            return False

    def ask_to_restart(self):
        msgBox = QMessageBox(parent=None)
        msgBox.setText(self.tr('The software update is now complete.'))
        thisprog = str(self.tr('This program'))
        if self.progname:
            thisprog = str('<b>' + Qt.escape(self.progname) + '</b>')
        msgBox.setInformativeText(str(self.tr('%s needs to be restarted for the changes to take effect. Restart now?')) % thisprog)
        btnRestart = msgBox.addButton('Restart', QMessageBox.AcceptRole)
        btnIgnore = msgBox.addButton('Ignore', QMessageBox.RejectRole)
        msgBox.setDefaultButton(btnRestart)
        msgBox.setEscapeButton(btnIgnore)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.show()
        msgBox.raise_()
        msgBox.exec_()
        clickedbutton = msgBox.clickedButton()
        if clickedbutton == btnRestart:
            return True
        else:
            return False

    def set_timeout_check(self, interval_timedelta):
        interval_ms = int(interval_timedelta.total_seconds() * 1000)
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.check_for_updates)
            self.timer.setSingleShot(True)
        elif self.timer.isActive():
            self.timer.stop()
        self.timer.setInterval(interval_ms)
        self.timer.start()
        logger.debug('single-shot timer started with interval=%d ms', interval_ms)
        return

    initCheckDelayMsChanged = pyqtSignal([int])

    def initCheckDelayMs(self):
        return int(self.initCheckDelay().total_seconds() * 1000)

    @pyqtSlot(int)
    def setInitCheckDelayMs(self, init_check_delay_ms, save=True):
        self.setInitCheckDelay(datetime.timedelta(days=0, microseconds=init_check_delay_ms * 1000), save=save)

    def setInitCheckDelay(self, init_check_delay_td, save=True):
        if self._timedelta_equal(init_check_delay_td, self.initCheckDelay()):
            return
        super(UpdatePyQt4Interface, self).setInitCheckDelay(init_check_delay_td, save=save)
        self.initCheckDelayMsChanged.emit(int(init_check_delay_td.total_seconds() * 1000))

    checkForUpdatesEnabledChanged = pyqtSignal([bool])

    @pyqtSlot(bool)
    def setCheckForUpdatesEnabled(self, enabled, save=True):
        if enabled == self.checkForUpdatesEnabled():
            return
        super(UpdatePyQt4Interface, self).setCheckForUpdatesEnabled(enabled, save=save)
        self.checkForUpdatesEnabledChanged.emit(enabled)

    checkIntervalMsChanged = pyqtSignal([int])

    def checkIntervalMs(self):
        return int(self.checkInterval().total_seconds() * 1000)

    @pyqtSlot(int)
    def setCheckIntervalMs(self, check_interval_ms, save=True):
        self.setCheckInterval(datetime.timedelta(days=0, microseconds=check_interval_ms * 1000), save=save)

    def setCheckInterval(self, check_interval_td, save=True):
        if self._timedelta_equal(check_interval_td, self.checkInterval()):
            return
        super(UpdatePyQt4Interface, self).setCheckInterval(check_interval_td, save)
        self.checkIntervalMsChanged.emit(int(check_interval_td.total_seconds() * 1000))

    def _timedelta_equal(self, a, b):
        return abs((a - b).total_seconds()) < 1.0