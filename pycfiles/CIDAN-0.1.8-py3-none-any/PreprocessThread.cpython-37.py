# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/PreprocessThread.py
# Compiled at: 2020-04-29 15:53:10
# Size of source mod 2**32: 1260 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from CIDAN.GUI.Data_Interaction.Signals import *
import CIDAN.GUI.Data_Interaction.Thread as Thread

class PreprocessThread(Thread):

    def __init__(self, main_widget, button):
        super().__init__(main_widget.data_handler)
        self.main_widget = main_widget
        self.button = button
        self.signal.sig.connect(lambda x: self.endThread(x))

    def run(self):
        try:
            self.signal.sig.emit(self.data_handler.calculate_filters())
        except:
            print('Unexpected error:', sys.exc_info()[0])
            self.signal.sig.emit(np.matrix([0]))

    def runThread(self):
        if not any([x.isRunning() for x in self.main_widget.thread_list]):
            print('Starting preprocessing sequence')
            self.button.setEnabled(False)
            self.start()
        else:
            print('Previous process in process, please wait to start new one till finished')

    def endThread(self, image_data):
        self.button.setEnabled(True)
        if image_data.shape != [1]:
            print('Finished preprocessing sequence')
            self.main_widget.preprocess_image_view.setImage(image_data)