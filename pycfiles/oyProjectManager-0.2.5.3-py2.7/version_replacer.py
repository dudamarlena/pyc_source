# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/version_replacer.py
# Compiled at: 2013-02-05 13:32:42
import os, sys, logging, oyProjectManager
from oyProjectManager import config, utils, Asset, Project, Repository, Sequence
logger = logging.getLogger('beaker.container')
logger.setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
conf = config.Config()
qt_module_key = 'PREFERRED_QT_MODULE'
qt_module = 'PyQt4'
if os.environ.has_key(qt_module_key):
    qt_module = os.environ[qt_module_key]
if qt_module == 'PySide':
    from PySide import QtGui, QtCore
    from oyProjectManager.ui import version_replacer_UI_pyside as version_replacer_UI
elif qt_module == 'PyQt4':
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtGui, QtCore
    from oyProjectManager.ui import version_replacer_UI_pyqt4 as version_replacer_UI

def UI(environment=None, app_in=None, executor=None):
    """the UI to call the dialog by itself
    """
    global app
    global mainDialog
    self_quit = False
    if QtGui.QApplication.instance() is None:
        if not app_in:
            try:
                app = QtGui.QApplication(sys.argv)
            except AttributeError:
                app = QtGui.QApplication([])

        else:
            app = app_in
        self_quit = True
    else:
        app = QtGui.QApplication.instance()
    mainDialog = MainDialog(environment)
    mainDialog.show()
    if executor is None:
        app.exec_()
        if self_quit:
            app.connect(app, QtCore.SIGNAL('lastWindowClosed()'), app, QtCore.SLOT('quit()'))
    else:
        executor.exec_(app, mainDialog)
    return mainDialog


class MainDialog(QtGui.QDialog, version_replacer_UI.Ui_Dialog):
    """the main dialog of the script
    """

    def __init__(self, environment=None, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        window_title = 'Version Replacer | ' + 'oyProjectManager v' + oyProjectManager.__version__
        self.environment = environment
        if self.environment:
            window_title += ' | ' + environment.name
        else:
            window_title += ' | No Environment'
        self._centerWindow()
        self._horizontalLabels = [
         'Original Asset', 'Update To']
        self.numOfRefs = 0
        self.refData = []
        self.versionListBuffer = []

    def _centerWindow(self):
        """centers the window to the screen
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def update_references_from_environment(self):
        """gets the references from the environment
        """
        self.refData = self.environment.get_referenced_versions()
        self.numOfRefs = len(self.refData)

    def _fillUI(self):
        """fills the UI with values from environment
        """
        self.update_references_from_environment()
        self.assetList_tableWidget.clear()
        self.assetList_tableWidget.setRowCount(self.numOfRefs)
        self.assetList_tableWidget.setHorizontalHeaderLabels(self._horizontalLabels)
        for i, refData in enumerate(self.refData):
            assetObj = refData[0]
            assert isinstance(assetObj, Asset)
            assetName_tableWI = QtGui.QTableWidgetItem(assetObj.fileName)
            assetName_tableWI.setTextAlignment(129)
            self.assetList_tableWidget.setItem(i, 0, assetName_tableWI)
            self._assetsToReplaceList.append([refData, False, None])

        self.assetList_tableWidget.resizeColumnToContents(0)
        self.assetList_tableWidget.resizeColumnToContents(1)
        self.subName_comboBox.clear()
        self.subName_comboBox.addItem('MAIN')
        return

    def _updateProjectObject(self):
        """updates the project object if it is changed
        it is introduced to take advantage of the cache system
        """
        currentProjectName = self.getCurrentProjectName()
        if self._project is None or self._project.name != currentProjectName or currentProjectName != '' or currentProjectName is not None:
            self._project = Project(currentProjectName)
        return

    def _updateSequenceObject(self):
        """updates the sequence object if it is not
        """
        currentSequenceName = self.getCurrentSequenceName()
        if self._sequence is None or self._sequence.name != currentSequenceName and (currentSequenceName != '' or currentSequenceName is not None) or self._sequence.projectName != self._project.name:
            self._updateProjectObject()
            newSeq = Sequence(self._project, currentSequenceName)
            if newSeq._exists:
                self._sequence = newSeq
        return

    def update_project_list(self):
        """updates projects list
        """
        server_path = self._repo.server_path
        projectsList = self._repo.valid_projects
        projectsList.sort()
        self.server_comboBox.clear()
        self.project_comboBox.clear()
        self.server_comboBox.addItem(server_path)
        self.project_comboBox.addItems(projectsList)

    def updateSequenceList(self, *arg):
        """updates the sequence according to selected project
        """
        self._updateProjectObject()
        currentProject = self._project
        self.sequence_comboBox.clear()
        sequences = currentProject.sequenceNames()
        self.sequence_comboBox.addItems(sequences)
        self._updateSequenceObject()

    def getCurrentProjectName(self):
        """returns the current project name
        """
        return unicode(self.project_comboBox.currentText())

    def getCurrentSequenceName(self):
        """returns the current sequence name
        """
        return unicode(self.sequence_comboBox.currentText())

    def updateForNoSubName(self):
        """this method will be removed in later version, it is written just to support
        old types of assets those have no subName field
        """
        self._updateSequenceObject()
        currentSequence = self._sequence
        self.subName_comboBox.setEnabled(not currentSequence._noSubNameField)

    def updateAssetTypeList(self):
        """updates asset types
        """
        self._updateSequenceObject()
        currentSequence = self._sequence
        assetTypes = currentSequence.getAssetTypes(self._environment.name)
        assetTypeNames = [ assetType.name for assetType in assetTypes ]
        lastSelectedItem = self.assetType_comboBox1.currentText()
        self.assetType_comboBox1.clear()
        self.assetType_comboBox1.addItems(assetTypeNames)
        if lastSelectedItem != '':
            self.assetType_comboBox1.setCurrentIndex(self.assetType_comboBox1.findText(lastSelectedItem))

    def updateBaseNameField(self):
        """updates the baseName fields with current asset baseNames for selected
        type, if the type is not shot dependent
        """
        self._updateSequenceObject()
        currentSequence = self._sequence
        currentTypeName = self.getCurrentAssetType()
        if currentTypeName == None:
            return
        else:
            currentType = currentSequence.getAssetTypeWithName(currentTypeName)
            if currentType == None:
                return
            if currentType.isShotDependent:
                baseNamesList = [ currentSequence.convertToShotString(shotNumber) for shotNumber in currentSequence.shotList ]
            else:
                baseNamesList = sorted(currentSequence.getAssetBaseNamesForType(currentTypeName))
            self.baseName_comboBox.clear()
            self.baseName_comboBox.addItems(baseNamesList)
            return

    def updateSubNameField(self):
        """updates the subName field with current asset subNames for selected
        baseName, if the type is not shot dependent
        """
        self._updateSequenceObject()
        currentSequence = self._sequence
        if currentSequence.no_sub_name_field:
            self.subName_comboBox.clear()
            return
        else:
            currentAssetTypeName = self.getCurrentAssetType()
            assetTypeObj = currentSequence.getAssetTypeWithName(currentAssetTypeName)
            if assetTypeObj == None:
                self.subName_comboBox.clear()
                return
            currentBaseName = self.getCurrentBaseName()
            self.subName_comboBox.clear()
            if currentAssetTypeName == None or currentBaseName == None:
                return
            currentAssetType = currentSequence.getAssetTypeWithName(currentAssetTypeName)
            if currentAssetType == None:
                return
            allAssetFileNames = currentSequence.getAllAssetFileNamesForType(currentAssetTypeName)
            allAssetFileNamesFiltered = currentSequence.filterAssetNames(allAssetFileNames, baseName=currentBaseName, typeName=currentAssetTypeName)
            curSGFIV = currentSequence.generateFakeInfoVariables
            subNamesList = [ curSGFIV(assetFileName)['subName'] for assetFileName in allAssetFileNamesFiltered ]
            subNamesList.append('MAIN')
            subNamesList = utils.unique(subNamesList)
            self.subName_comboBox.addItems(sorted(subNamesList))
            return

    def getCurrentAssetType(self):
        """returns the current assetType from the UI
        """
        return unicode(self.assetType_comboBox1.currentText())

    def getCurrentBaseName(self):
        """returns the current baseName from the UI
        """
        return unicode(self.baseName_comboBox.currentText())

    def getCurrentSubName(self):
        """returns the current subName from the UI
        """
        return unicode(self.subName_comboBox.currentText())

    def updateVersionListBuffer(self):
        """updates the version list buffer
        """
        self._updateProjectObject()
        self._updateSequenceObject()
        currentProject = self._project
        currentSequence = self._sequence
        typeName = self.getCurrentAssetType()
        if typeName == '' or typeName == None:
            return
        baseName = self.getCurrentBaseName()
        if not currentSequence.no_sub_name_field:
            subName = self.getCurrentSubName()
        else:
            subName = ''
        assetInfo = dict()
        assetInfo['baseName'] = baseName
        assetInfo['subName'] = subName
        assetInfo['typeName'] = typeName
        allAssetFileNames = currentSequence.getAllAssetFileNamesForType(typeName)
        allAssetFileNamesFiltered = currentSequence.filterAssetNames(allAssetFileNames, **assetInfo)
        currSGFIV = currentSequence.generateFakeInfoVariables
        allVersionsList = [ currSGFIV(assetFileName)['fileName'] for assetFileName in allAssetFileNamesFiltered ]
        self.versionListBuffer = []
        if len(allVersionsList) > 0:
            self.versionListBuffer = sorted(filter(self._environment.hasValidExtension, allVersionsList))
        return

    def fullUpdateAssetFilesComboBox(self):
        """invokes a version list buffer update and a assets files comboBox update
        """
        self.updateVersionListBuffer()
        self.partialUpdateAssetFilesComboBox()

    def partialUpdateAssetFilesComboBox(self):
        """just updates if the number of maximum displayable entry is changed
        """
        _buffer = []
        _buffer = self.versionListBuffer
        self.fillAssetFilesComboBox(_buffer)

    def fillAssetFilesComboBox(self, assetFileNames):
        """fills the assets table widget with given assets
        """
        assetCount = len(assetFileNames)
        self.assetFile_comboBox.clear()
        data = []
        if assetCount == 0:
            return
        self.assetFile_comboBox.addItems(assetFileNames)

    def addAssetToReplaceList(self):
        """adds the asset to the replace list
        """
        index = self.assetList_tableWidget.currentIndex().row()
        assetFile = self.assetFile_comboBox.currentText()
        self._createAssetObjectFromOpenFields()
        tableItem = self.addItemToIndex(self.assetList_tableWidget, index, 1, assetFile)
        self._assetsToReplaceList[index][1] = True
        self._assetsToReplaceList[index][2] = self._asset

    def addItemToIndex(self, tableWidget, rowIndex, columnIndex, itemText):
        """adds new item to given index
        """
        item = QtGui.QTableWidgetItem(itemText)
        tableWidget.setItem(rowIndex, columnIndex, item)
        return item

    def _createAssetObjectFromOpenFields(self):
        """retriewes the file name from the open asset fields
        """
        assetFileName = unicode(self.assetFile_comboBox.currentText())
        self._asset = Asset(self._project, self._sequence, assetFileName)
        self._environment.asset = self._asset

    def removeReplacement(self):
        """removes the selected replacement
        """
        index = self.assetList_tableWidget.currentIndex().row()
        tableItem = self.addItemToIndex(self.assetList_tableWidget, index, 1, '')
        self._assetsToReplaceList[index][1] = False
        self._assetsToReplaceList[index][2] = None
        return

    def replaceAssets(self):
        """does the replace action
        """
        for repData in self._assetsToReplaceList:
            if repData[1] == True:
                self._environment.replaceAssets(repData[0][1], repData[2].full_path)

        self.close()

    def updateComboBoxesForAsset(self, cellRowId, cellColoumnId):
        """updates the comboboxes according to double clicked cell
        """
        if cellColoumnId == 0:
            assetObj = self._assetsToReplaceList[cellRowId][0][0]
            assert isinstance(assetObj, Asset)
            projectName = assetObj.sequence.project.name
            sequenceName = assetObj.sequence.name
            baseName = assetObj.baseName
            subName = assetObj.subName
            typeName = assetObj.typeName
            fileName = assetObj.fileName
            self.project_comboBox.setCurrentIndex(self.project_comboBox.findText(projectName))
            self.sequence_comboBox.setCurrentIndex(self.sequence_comboBox.findText(sequenceName))
            self.assetType_comboBox1.setCurrentIndex(self.assetType_comboBox1.findText(typeName))
            self.baseName_comboBox.setCurrentIndex(self.baseName_comboBox.findText(baseName))
            self.subName_comboBox.setCurrentIndex(self.subName_comboBox.findText(subName))
            self.assetFile_comboBox.setCurrentIndex(self.assetFile_comboBox.findText(fileName))
        elif cellColoumnId == 1:
            self.addAssetToReplaceList()