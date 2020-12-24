# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\gui\MainWindow.py
# Compiled at: 2014-02-24 04:51:36
"""
Created on 30 Jan 2014

@author: Liam Deacon

@contact: liam.deacon@diamond.ac.uk

@copyright: 2014 Liam Deacon

@license: MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to 
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""
from __future__ import print_function, with_statement
import logging, ntpath, os, platform, sys
from collections import OrderedDict
import PyQt4
from PyQt4 import QtCore, QtGui, uic
import res_rc
__QT_TYPE__ = 'PyQt4'
from settings import Settings
from ImportDialog import ImportDialog
from phaseshifts.model import MTZ_model, Unitcell, Atom
__APP_AUTHOR__ = 'Liam Deacon'
__APP_COPYRIGHT__ = b'\xa9' + ('2013 {0}').format(__APP_AUTHOR__)
__APP_DESCRIPTION__ = 'A simple Python-based program \n for generation of phase shifts'
__APP_DISTRIBUTION__ = 'phaseshifts'
__APP_EMAIL__ = 'liam.m.deacon@diamond.ac.uk'
__APP_LICENSE__ = 'MIT License'
__APP_NAME__ = 'Phase Shifts'
__APP_VERSION__ = '0.1-alpha'
__PYTHON__ = ('{0}.{1}.{2}').format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro, sys.version_info.releaselevel)
__UPDATE_URL__ = ''
if platform.system() is 'Windows':
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(__APP_NAME__)

class MainWindow(QtGui.QMainWindow):
    """Class for main application widget"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uiFile = 'gui/MainWindow.ui'
        self.ui = uic.loadUi(uiFile, self)
        self.ui.show()
        self.init()
        self.initUi()

    def init(self):
        """Class to initialise logging and non-gui objects"""
        self.logger = logging.getLogger(__APP_NAME__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(os.path.join(os.environ['TEMP'], __APP_NAME__ + str('.log')))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        self.lastpath = ''
        self.settings = Settings()
        bulkTree = self.ui.treeWidgetBulk.invisibleRootItem()
        slabTree = self.ui.treeWidgetSlab.invisibleRootItem()

    def initUi(self):
        """Class to initialise the Qt Widget and setup slots and signals"""
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionAboutQt.triggered.connect(self.aboutQt)
        self.ui.actionContact.triggered.connect(self.contactDeveloper)
        self.ui.actionExport.triggered.connect(self.exportModel)
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionImport.triggered.connect(self.importModel)
        self.ui.actionModelBuilder.triggered.connect(self.modelBuilderDialog)
        self.ui.actionOpen.triggered.connect(self.importDialog)
        self.ui.actionSettings.triggered.connect(self.settingsDialog)
        self.ui.actionTextView.triggered.connect(self.changeModelView)
        self.ui.actionTreeView.triggered.connect(self.changeModelView)
        self.ui.actionUpdate.triggered.connect(self.getUpdate)
        self.ui.tabWidget.currentChanged.connect(self.changeMainTab)
        self.ui.stackedWidgetBulk.currentChanged.connect(self.changeModelView)
        self.ui.stackedWidgetSlab.currentChanged.connect(self.changeModelView)
        self.ui.pushBulkToText.pressed.connect(self.changeModelView)
        self.ui.pushBulkToTree.pressed.connect(self.changeModelView)
        self.ui.pushSlabToText.pressed.connect(self.changeModelView)
        self.ui.pushSlabToTree.pressed.connect(self.changeModelView)

    def about(self):
        """Display 'About' dialog"""
        text = __APP_DESCRIPTION__
        text += ('\n\nAuthor: {0} \nEmail: {1}').format(__APP_AUTHOR__, __APP_EMAIL__)
        text += ('\n\nApp version: {0}').format(__APP_VERSION__)
        text += ('\n{0}').format(__APP_COPYRIGHT__)
        text += '\n' + __APP_LICENSE__
        text += ('\n\nPython: {0}').format(__PYTHON__)
        text += ('\nGUI frontend: {0} {1}').format(__QT_TYPE__, QtCore.QT_VERSION_STR)
        msg = QtGui.QMessageBox.about(self, self.ui.windowTitle(), text)

    def aboutQt(self):
        """Display Qt dialog"""
        QtGui.QApplication.aboutQt()

    def contactDeveloper(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(str('mailto: {email}?subject={name} feedback&body=').format(email=__APP_EMAIL__, name=__APP_NAME__)))

    def getUpdate(self):
        """Check for app updates"""
        from UpdateDialog import UpdateDialog
        updateDialog = UpdateDialog(parent=self)
        updateDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        updateDialog.exec_()

    def changeMainTab(self):
        """Change main tab selection"""
        tabText = str(self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())).lower()
        if tabText == 'bulk':
            self.model = 'bulk'
        elif tabText == 'slab':
            self.model = 'slab'
        else:
            self.model = None
        return

    def changeModelView(self):
        """Change model view"""
        if self.sender() is self.ui.actionTreeView:
            self.ui.actionTextView.setChecked(False)
            self.ui.stackedWidgetBulk.setCurrentIndex(0)
            self.ui.stackedWidgetSlab.setCurrentIndex(0)
        elif self.sender() is self.ui.actionTextView:
            self.ui.actionTextView.setChecked(False)
            self.ui.stackedWidgetBulk.setCurrentIndex(1)
            self.ui.stackedWidgetSlab.setCurrentIndex(1)
        elif self.sender() is self.ui.pushBulkToText or self.sender() is self.ui.pushSlabToText:
            self.ui.actionTextView.setChecked(True)
            self.ui.actionTreeView.setChecked(False)
            self.ui.stackedWidgetBulk.setCurrentIndex(1)
            self.ui.stackedWidgetSlab.setCurrentIndex(1)
        elif self.sender() is self.ui.pushBulkToTree or self.sender() is self.ui.pushSlabToTree:
            self.ui.actionTextView.setChecked(False)
            self.ui.actionTreeView.setChecked(True)
            self.ui.stackedWidgetBulk.setCurrentIndex(0)
            self.ui.stackedWidgetSlab.setCurrentIndex(0)

    def exportModel(self):
        """Export model as text file"""
        pass

    def importDialog(self):
        """Open dialog and radio options"""
        importDialog = ImportDialog(parent=self, model=str(self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())).lower())
        importDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        importDialog.finished.connect(self.parseInput)
        importDialog.exec_()

    def importModel(self):
        """Import model from text file"""
        pass

    def help(self):
        """Display help"""
        try:
            helpDialog = Help.HelpWidget(parent=self)
            helpDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            helpDialog.exec_()
        except NameError:
            QtGui.QMessageBox.information(self, 'Help', 'Help is not currently available')
            self.logger.error('unable to create Help dialog')

    def modelBuilderDialog(self):
        """Start new instance of model builder wizard"""
        pass

    def getInputFile(self, startpath=str(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)), model=None):
        """returns file path of input"""
        if model == None:
            model = ''
        else:
            model += ' '
        model = model.capitalize()
        if os.path.exists(self.lastpath):
            if os.path.isfile(self.lastpath):
                startpath = os.path.dirname(self.lastpath)
            else:
                startpath = self.lastpath
        filepath = str(QtGui.QFileDialog.getOpenFileName(parent=None, caption='Open %sInput File' % model, directory=startpath))
        return filepath

    def parseInput(self):
        if isinstance(self.sender(), ImportDialog):
            if self.sender().action == 'cancel':
                print('cancel')
                return
            if self.sender().ui.radioBulk.isChecked():
                model = 'bulk'
            else:
                model = 'slab'
        else:
            tabText = str(self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())).lower()
            if tabText == 'bulk' or tabText == 'slab':
                model = tabText
            else:
                return self.importDialog()
            filename = self.getInputFile(model=model)
            if not os.path.exists(filename):
                return
            self.lastpath = filename
            try:
                atom = Atom('H')
                uc = Unitcell(1, 2, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                mtz = MTZ_model(uc, atoms=[atom])
                mtz.load_from_file(filename)
                exec 'self.%s = mtz' % model
                self.updateModelUi(model)
            except IOError:
                self.logger.error("IOError: Unable to open input file '%s'" % filename)

    def settingsDialog(self):
        """Launch settings dialog"""
        from SettingsDialog import SettingsDialog
        settingsDialog = SettingsDialog(parent=self)
        settingsDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        settingsDialog.finished.connect(self.updateSettings)
        settingsDialog.exec_()

    def updateModelUi(self, model=None):
        """Update model in gui"""
        if isinstance(model, str):
            model = model.lower()
            mtz = MTZ_model(Unitcell(1, 2, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]), atoms=[
             Atom('H')])
            if model == 'bulk':
                tree = self.ui.treeWidgetBulk
                mtz = eval('self.%s' % model)
            else:
                if model == 'slab':
                    tree = self.ui.treeWidgetSlab
                else:
                    return
                root = tree.invisibleRootItem()
                trunk = self.getChildItemsDict(tree)
                for branch in trunk:
                    branch = branch.replace(' ', '').split('=')[0]
                    item = root.child(self.treeRootDict.get(model).get(branch))
                    item.setText = mtz.header

    def updateSettings(self):
        """update the application settings"""
        self.settings = self.sender().settings
        print(self.settings.__dict__)

    def getChildItemsDict(self, obj):
        try:
            if isinstance(obj, QtGui.QTreeWidget):
                root = obj.invisibleRootItem()
            else:
                if isinstance(obj, QtGui.QTreeWidgetItem):
                    root = obj
                child_count = root.childCount()
                topLevelDict = {}
                for i in range(child_count):
                    item = root.child(i)
                    var = str(item.text(0))
                    exec '%s = i' % var
                    topLevelDict.update({var: eval(var)})

            return topLevelDict
        except any as e:
            self.logger.error(e.msg)

    def getChildItemHandle(self, obj, name=str):
        if isinstance(obj, QtGui.QTreeWidget):
            root = obj.invisibleRootItem()
        else:
            if isinstance(obj, QtGui.QTreeWidgetItem):
                root = obj
            if isinstance(name, int):
                return root.child(name)
        if isinstance(name, str):
            for i in range(root.childCount()):
                item = root.child(i)
                if str(item.text(0)) == name:
                    return item


def main(argv=None):
    """Entry point if executing as standalone"""
    if argv is None:
        argv = sys.argv
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    return app.exec_()


if __name__ == '__main__':
    main()