# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/optionsdialog.py
# Compiled at: 2011-04-23 08:43:29
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_optionsdialog import Ui_OptionsDialog
logger = logging.getLogger('qtoptionsdialog')
d = lambda x: x.decode('utf-8')

class QtOptionsDialog(Ui_OptionsDialog, QDialog):
    saveSettings = pyqtSignal()
    TTS_SETTINGS = (
     (0, 'Off'),
     (-1, 'Automatic'),
     (10, '10 Seconds'),
     (20, '20 Seconds'),
     (30, '30 Seconds'),
     (50, '50 Seconds'),
     (100, '100 Seconds'),
     (180, '3 Minutes'),
     (300, '5 Minutes'),
     (600, '10 Minutes'))

    def __init__(self, core, settings, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.core = core
        self.buttonBox.clicked.connect(self.__button_clicked)
        self.load_settings(settings)

    def load_settings(self, settings):
        self.lineEditUserName.setText(d(settings['options_username']))
        self.lineEditPassword.setText(d(settings['options_password']))
        self.checkBoxHideFound.setCheckState(Qt.Checked if settings['options_hide_found'] else Qt.Unchecked)
        self.checkBoxShowName.setCheckState(Qt.Checked if settings['options_show_name'] else Qt.Unchecked)
        self.checkBoxDoubleSize.setCheckState(Qt.Checked if settings['options_map_double_size'] else Qt.Unchecked)
        self.comboBoxTTS.clear()
        i = 0
        for (time, text) in self.TTS_SETTINGS:
            self.comboBoxTTS.addItem(text)
            if time == settings['tts_interval']:
                self.comboBoxTTS.setCurrentIndex(i)
            i += 1

    def get_settings(self):
        return {'options_username': unicode(self.lineEditUserName.text()), 
           'options_password': unicode(self.lineEditPassword.text()), 
           'options_hide_found': self.checkBoxHideFound.checkState() == Qt.Checked, 
           'options_show_name': self.checkBoxShowName.checkState() == Qt.Checked, 
           'options_map_double_size': self.checkBoxDoubleSize.checkState() == Qt.Checked, 
           'tts_interval': self.TTS_SETTINGS[self.comboBoxTTS.currentIndex()][0]}

    def __button_clicked(self, button):
        id = self.buttonBox.standardButton(button)
        if id == QDialogButtonBox.Ok:
            self.saveSettings.emit()