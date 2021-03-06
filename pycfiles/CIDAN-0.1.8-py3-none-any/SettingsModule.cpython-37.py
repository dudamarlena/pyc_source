# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/SettingWidget/SettingsModule.py
# Compiled at: 2020-04-29 15:33:21
# Size of source mod 2**32: 1474 bytes
import sys, qdarkstyle
from CIDAN.GUI.SettingWidget.SettingBlockModule import *

class SettingsModule(QFrame):

    def __init__(self, name, *args, show_name=True):
        super().__init__()
        self.setting_block_list = args
        self.layout = QVBoxLayout()
        if show_name:
            self.setStyleSheet('SettingsModule { border:1px solid rgb(50, 65, 75);} ')
            self.header = QLabel()
            self.header.setText(name)
            self.header.setStyleSheet('font-size: 20px')
            self.layout.addWidget(self.header)
        self.setting_block_layout = QToolBox()
        for block in self.setting_block_list:
            self.setting_block_layout.addItem(block, block.name)

        self.layout.addWidget(self.setting_block_layout)
        self.setLayout(self.layout)


def preprocessing_settings(main_widget):
    return SettingsModule('Preprocessing Settings', dataset_setting_block(main_widget), filter_setting_block(main_widget))


def roi_extraction_settings(main_widget):
    return SettingsModule('ROI Extraction Settings', (multiprocessing_settings_block(main_widget)), (roi_extraction_settings_block(main_widget)), (roi_advanced_settings_block(main_widget)), show_name=False)


if __name__ == '__main__':
    app = QApplication([])
    widget = preprocessing_settings()
    widget.setStyleSheet(qdarkstyle.load_stylesheet())
    widget.show()
    sys.exit(app.exec_())