# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/MainWindow.py
# Compiled at: 2020-04-29 16:44:37
# Size of source mod 2**32: 7786 bytes
import os
os.environ['QT_API'] = 'pyside2'
from PySide2.QtWidgets import QTabWidget
from CIDAN.GUI.Tabs.Tab import AnalysisTab
import CIDAN.GUI.Tabs.FileOpenTab as FileOpenTab
from CIDAN.GUI.Tabs.ROIExtractionTab import *
from CIDAN.GUI.Tabs.PreprocessingTab import *
import qdarkstyle
import CIDAN.GUI.ImageView.ImageViewModule as ImageViewModule
import CIDAN.GUI.Data_Interaction.DataHandler as DataHandler
import CIDAN.GUI.Console.ConsoleWidget as ConsoleWidget
import sys, logging

class MainWindow(QMainWindow):
    __doc__ = 'Initializes the basic window with Main widget being the focused widget'

    def __init__(self, dev=False):
        super().__init__()
        self.title = 'CIDAN'
        self.width = 900
        self.height = 400
        self.setWindowTitle(self.title)
        self.setMinimumSize(self.width, self.height)
        self.main_menu = self.menuBar()
        self.table_widget = MainWidget(self, dev=dev)
        self.setCentralWidget(self.table_widget)
        style = '\n            QTabWidget {font-size: 25px; padding:1px; margin:5px;}\n            QTabBar::tab {\n                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                           stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n                                          stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n                /*border: 2px solid #C4C4C3;*/\n                /*border-bottom-color: #C2C7CB; !* same as the pane color *!*/\n                \n                min-width: 8ex;\n                padding:1px;\n                border:1px;\n            }\n            \n            QComboBox::item:checked {\n              font-weight: bold;\n              height: 12px;\n            }\n            '
        self.setStyleSheet(qdarkstyle.load_stylesheet() + style)
        self.show()


class MainWidget(QWidget):
    __doc__ = 'Main Widget, contains everything\n\n    Attributes\n    ----------\n    main_window : MainWindow\n        A reference to the main window of the application\n    main_menu : ???\n        the top bar menu\n    layout : QLayout\n        The main layout for the widget\n    data_handler : DataHandler\n        The instance that controls all interactions with dataset\n    thread_list : List[Thread]\n        A list of all the possible running threads, used to ensure only 1 thread is\n        running at a time\n    preprocess_image_view : ImageViewModule\n        The image view for the preprocess tab\n    roi_image_view : ImageViewModule\n        The image view for the roi extraction tab\n    tab_widget : QTabWidget\n        Controls the main tabs of the application\n    console : ConsoleWidget\n        Widget for the console\n    tabs : List[Tabs]\n        A list of the currently active tabs not used until after init_w_data is run\n    '

    def __init__(self, parent, dev=False):
        """
        Initialize the main widget to load files
        Parameters
        ----------
        parent
        """
        super().__init__(parent)
        self.main_window = parent
        self.main_menu = self.main_window.main_menu
        self.layout = QVBoxLayout(self)
        self.data_handler = None
        self.thread_list = []
        self.preprocess_image_view = ImageViewModule(self, roi=False)
        self.roi_image_view = ImageViewModule(self, histogram=False, roi=False)
        self.tab_widget = QTabWidget()
        self.fileOpenTab = FileOpenTab(self)
        self.tab_widget.addTab(self.fileOpenTab, 'Open Dataset')
        self.tabs = [
         'Preprocessing', 'ROI Extraction', 'Analysis']
        for num, tab in enumerate(self.tabs):
            self.tab_widget.addTab(QWidget(), tab)
            self.tab_widget.setTabEnabled(num + 1, False)

        self.layout.addWidget(self.tab_widget)
        self.console = ConsoleWidget()
        self.console.setMaximumHeight(150)
        self.console.setMinimumHeight(150)
        self.layout.addWidget(self.console)
        self.setLayout(self.layout)
        fileMenu = self.main_menu.addMenu('&File')
        openFileAction = QAction('Open File', self)
        openFileAction.setStatusTip('Open a single file')
        openFileAction.triggered.connect(lambda : self.selectOpenFileTab(0))
        fileMenu.addAction(openFileAction)
        openFolderAction = QAction('Open Folder', self)
        openFolderAction.setStatusTip('Open a folder')
        openFolderAction.triggered.connect(lambda : self.selectOpenFileTab(1))
        fileMenu.addAction(openFolderAction)
        openPrevAction = QAction('Open Previous Session', self)
        openPrevAction.setStatusTip('Open a previous session')
        openPrevAction.triggered.connect(lambda : self.selectOpenFileTab(2))
        fileMenu.addAction(openPrevAction)
        if dev:
            self.data_handler = DataHandler('/Users/sschickler/Code Devel/LSSC-python/input_images/small_dataset.tif',
              '/Users/sschickler/Code Devel/LSSC-python/input_images/test31',
              trials=[''], save_dir_already_created=False)
            self.init_w_data()
        if False:
            if dev:
                self.data_handler = DataHandler('/Users/sschickler/Code Devel/LSSC-python/input_images/dataset_1',
                  '/Users/sschickler/Code Devel/LSSC-python/input_images/test3',
                  save_dir_already_created=False)
                self.init_w_data()

    def init_w_data(self):
        """
        Initialize main widget with data

        It activates the other tabs and helps load the data into image views
        Returns
        -------

        """
        for num, _ in enumerate(self.tabs):
            self.tab_widget.removeTab(1)

        self.tabs = [
         PreprocessingTab(self), ROIExtractionTab(self), AnalysisTab(self)]
        for tab in self.tabs:
            self.tab_widget.addTab(tab, tab.name)

        self.tab_widget.setCurrentIndex(1)
        self.tab_widget.currentChanged.connect(lambda x: self.tabs[1].set_background('', (self.tabs[1].background_chooser.current_state()), update_image=True))
        if not hasattr(self, 'export_menu'):
            self.export_menu = self.main_menu.addMenu('&Export')
            export_action = QAction('Export Time Traces/ROIs', self)
            export_action.setStatusTip('Export Time Traces/ROIs')
            export_action.triggered.connect(lambda : self.exportStuff())
            self.export_menu.addAction(export_action)

    def selectOpenFileTab(self, index):
        self.tab_widget.setCurrentIndex(0)
        self.fileOpenTab.tab_selector.setCurrentIndex(index)

    def exportStuff(self):
        msg = QMessageBox()
        msg.setWindowTitle('Export data')
        msg.setText('Data Exported to save directory')
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()


if __name__ == '__main__':
    LOG_FILENAME = 'log.out'
    logging.basicConfig(filename=LOG_FILENAME, level=(logging.DEBUG))
    logger = logging.getLogger('CIDAN')
    logger.debug('Program started')
    app = QApplication([])
    app.setApplicationName('CIDAN')
    widget = MainWindow(dev=True)
    sys.exit(app.exec_())