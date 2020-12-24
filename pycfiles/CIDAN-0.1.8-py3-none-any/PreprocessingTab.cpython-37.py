# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Tabs/PreprocessingTab.py
# Compiled at: 2020-04-29 15:54:20
# Size of source mod 2**32: 2919 bytes
import CIDAN.GUI.Tabs.Tab as Tab
from PySide2.QtWidgets import *
import CIDAN.GUI.Data_Interaction.PreprocessThread as PreprocessThread
from CIDAN.GUI.SettingWidget.SettingsModule import preprocessing_settings

class PreprocessingTab(Tab):
    """PreprocessingTab"""

    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.data_handler = self.main_widget.data_handler
        process_button = QPushButton()
        process_button.setText('Apply Settings')
        thread = PreprocessThread(main_widget, process_button)
        main_widget.thread_list.append(thread)
        process_button.clicked.connect(lambda : thread.runThread())
        self.main_widget.preprocess_image_view.setImage(self.data_handler.calculate_filters())
        image_buttons = QWidget()
        image_buttons_layout = QHBoxLayout()
        image_buttons.setLayout(image_buttons_layout)
        max_image_button = QPushButton()
        max_image_button.setText('Max Image')
        max_image_button.clicked.connect(lambda : self.main_widget.preprocess_image_view.setImage(self.data_handler.max_image))
        stack_button = QPushButton()
        stack_button.setText('Filtered Stack')
        stack_button.clicked.connect(lambda : self.main_widget.preprocess_image_view.setImage(self.data_handler.dataset_filtered))
        orig_stack_button = QPushButton()
        orig_stack_button.setText('Original Stack')
        orig_stack_button.clicked.connect(lambda : self.main_widget.preprocess_image_view.setImage(self.data_handler.dataset))
        mean_image_button = QPushButton()
        mean_image_button.setText('Mean Image')
        mean_image_button.clicked.connect(lambda : self.main_widget.preprocess_image_view.setImage(self.data_handler.mean_image))
        image_buttons_layout.addWidget(orig_stack_button)
        image_buttons_layout.addWidget(stack_button)
        image_buttons_layout.addWidget(max_image_button)
        image_buttons_layout.addWidget(mean_image_button)
        super().__init__('Preprocessing', column_1=[preprocessing_settings(main_widget),
         process_button],
          column_2=[
         main_widget.preprocess_image_view, image_buttons])