# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blooser/anaconda3/lib/python3.7/site-packages/youtubedownloader/dialog_manager.py
# Compiled at: 2020-04-30 10:14:00
# Size of source mod 2**32: 1078 bytes
from PySide2.QtCore import QObject, Qt, QStandardPaths, Slot, Signal, Property
import sys, os, pathlib
from .paths import Paths
from .logger import create_logger

class DialogManager(QObject):
    DIALOG_PATH = os.path.join(os.path.dirname(__file__), 'qml/dialogs')
    open = Signal(str, 'QVariantMap', 'QVariant', arguments=['dialog', 'properties', 'callback'])
    close = Signal(str, arguments=['dialog'])

    def __init__(self):
        super(DialogManager, self).__init__(None)
        self.logger = create_logger(__name__)
        self.dialogs = Paths.collect_files(DialogManager.DIALOG_PATH)
        self.logger.info('Loaded {dialogs} dialogs'.format(dialogs=(len(self.dialogs))))

    @Slot(str, 'QVariantMap', 'QVariant')
    def open_dialog(self, dialog, properties, callback):
        self.logger.info('Creating {dialog}'.format(dialog=dialog))
        self.open.emit(self.dialogs[dialog], properties, callback)

    @Slot(str)
    def close_dialog(self, dialog):
        self.logger.info('Closing {dialog}'.format(dialog=dialog))
        self.close.emit(dialog)