# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/taurusgui/paneldescriptionwizard.py
# Compiled at: 2019-08-19 15:09:30
"""
paneldescriptionwizard.py:
"""
from __future__ import print_function
from taurus.external.qt import Qt
import sys, weakref
from taurus.qt.qtgui.taurusgui.utils import PanelDescription
from taurus.qt.qtgui.icon import getCachedPixmap
from taurus.qt.qtgui.input import GraphicalChoiceWidget
from taurus.qt.qtgui.base import TaurusBaseComponent, TaurusBaseWidget
from taurus.qt.qtcore.communication import SharedDataManager
from taurus.qt.qtcore.mimetypes import TAURUS_MODEL_LIST_MIME_TYPE
from taurus.qt.qtgui.util import TaurusWidgetFactory
from taurus.core.util.log import Logger
import inspect, copy
__all__ = [
 'PanelDescriptionWizard']

class ExpertWidgetChooserDlg(Qt.QDialog):
    CHOOSE_TYPE_TXT = '(choose type)'
    memberSelected = Qt.pyqtSignal(dict)

    def __init__(self, parent=None):
        Qt.QDialog.__init__(self, parent)
        self.setWindowTitle('Advanced panel type selection')
        layout1 = Qt.QHBoxLayout()
        layout2 = Qt.QHBoxLayout()
        layout = Qt.QVBoxLayout()
        self.moduleNameLE = Qt.QLineEdit()
        self.moduleNameLE.setValidator(Qt.QRegExpValidator(Qt.QRegExp('[a-zA-Z0-9\\.\\_]*'), self.moduleNameLE))
        self.membersCB = Qt.QComboBox()
        self.dlgBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok | Qt.QDialogButtonBox.Cancel)
        self.dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(Qt.QLabel('Select the module and widget to use in the panel:'))
        layout1.addWidget(Qt.QLabel('Module'))
        layout1.addWidget(self.moduleNameLE)
        layout2.addWidget(Qt.QLabel('Class (or widget)'))
        layout2.addWidget(self.membersCB)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(self.dlgBox)
        self.setLayout(layout)
        self.moduleNameLE.editingFinished.connect(self.onModuleSelected)
        self.moduleNameLE.textEdited.connect(self.onModuleEdited)
        self.membersCB.activated.connect(self.onMemberSelected)
        self.dlgBox.accepted.connect(self.accept)
        self.dlgBox.rejected.connect(self.reject)

    def onModuleEdited(self):
        self.dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(False)
        self.module = None
        self.moduleNameLE.setStyleSheet('')
        self.membersCB.clear()
        return

    def onModuleSelected(self):
        modulename = str(self.moduleNameLE.text())
        try:
            __import__(modulename)
            self.module = sys.modules[modulename]
            self.moduleNameLE.setStyleSheet('QLineEdit {color: green}')
        except Exception as e:
            Logger().debug(repr(e))
            self.moduleNameLE.setStyleSheet('QLineEdit {color: red}')
            return

        members = inspect.getmembers(self.module)
        classnames = sorted([ n for n, m in members if inspect.isclass(m) and issubclass(m, Qt.QWidget) ])
        widgetnames = sorted([ n for n, m in members if isinstance(m, Qt.QWidget) ])
        self.membersCB.clear()
        self.membersCB.addItem(self.CHOOSE_TYPE_TXT)
        self.membersCB.addItems(classnames)
        if classnames and widgetnames:
            self.membersCB.InsertSeparator(self.membersCB.count())
        self.membersCB.addItems(classnames)

    def onMemberSelected(self, text):
        if str(text) == self.CHOOSE_TYPE_TXT:
            return
        self.dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(True)
        self.memberSelected.emit(self.getMemberDescription())

    def getMemberDescription(self):
        try:
            membername = str(self.membersCB.currentText())
            member = getattr(self.module, membername, None)
            result = {'modulename': self.module.__name__}
        except Exception as e:
            Logger().debug('Cannot get member description: %s', repr(e))
            return

        if inspect.isclass(member):
            result['classname'] = membername
        else:
            result['widgetname'] = membername
        return result

    @staticmethod
    def getDialog():
        dlg = ExpertWidgetChooserDlg()
        dlg.exec_()
        return (dlg.getMemberDescription(), dlg.result() == dlg.Accepted)


class BlackListValidator(Qt.QValidator):
    stateChanged = Qt.pyqtSignal(int, int)

    def __init__(self, blackList=None, parent=None):
        Qt.QValidator.__init__(self, parent)
        if blackList is None:
            blackList = []
        self.blackList = blackList
        self._previousState = None
        dummyValidator = Qt.QDoubleValidator(None)
        self._oldMode = len(dummyValidator.validate('', 0)) < 3
        return

    def validate(self, input, pos):
        if str(input) in self.blackList:
            state = self.Intermediate
        else:
            state = self.Acceptable
        if state != self._previousState:
            self.stateChanged.emit(state, self._previousState)
            self._previousState = state
        if self._oldMode:
            return (state, pos)
        else:
            return (
             state, input, pos)


class WidgetPage(Qt.QWizardPage, TaurusBaseWidget):
    OTHER_TXT = 'Other...'
    defaultCandidates = ['TaurusForm', 'TaurusTrend', 'TaurusPlot',
     'TaurusImageDialog', 'TaurusTrend2DDialog', 'TaurusNeXusBrowser',
     'TaurusDbTreeWidget', 'TaurusArrayEditor',
     'SardanaEditor', 'TaurusJDrawSynopticsView',
     'TaurusDevicePanel']

    def __init__(self, parent=None, designMode=False, extraWidgets=None):
        Qt.QWizardPage.__init__(self, parent)
        TaurusBaseWidget.__init__(self, 'WidgetPage')
        if extraWidgets:
            customWidgets, customWidgetScreenshots = list(zip(*extraWidgets))
            pixmaps = {}
            for k, s in extraWidgets:
                if s is None:
                    pixmaps[k] = None
                else:
                    try:
                        pixmaps[k] = getCachedPixmap(s)
                        if pixmaps[k].isNull():
                            raise Exception('Invalid Pixmap')
                    except:
                        self.warning('Could not create pixmap from %s' % s)
                        pixmaps[k] = None

        else:
            customWidgets, customWidgetScreenshots = [], []
            pixmaps = {}
        self.setFinalPage(True)
        self.setTitle('Panel type')
        self.setSubTitle('Choose a name and type for the new panel')
        self.setButtonText(Qt.QWizard.NextButton, 'Advanced settings...')
        self.widgetDescription = {'widgetname': None, 'modulename': None, 
           'classname': None}
        self.nameLE = Qt.QLineEdit()
        self.registerField('panelname*', self.nameLE)
        self.diagnosticLabel = Qt.QLabel('')
        nameLayout = Qt.QHBoxLayout()
        nameLayout.addWidget(Qt.QLabel('Panel Name'))
        nameLayout.addWidget(self.nameLE)
        nameLayout.addWidget(self.diagnosticLabel)
        available = TaurusWidgetFactory().getWidgetClassNames()
        choices = []
        row = []
        for cname in self.defaultCandidates + list(customWidgets):
            if cname in available or '.' in cname:
                row.append(cname)
                if cname not in pixmaps:
                    pixmaps[cname] = getCachedPixmap('snapshot:%s.png' % cname)
                if len(row) == 3:
                    choices.append(row)
                    row = []

        row.append(self.OTHER_TXT)
        choices.append(row)
        self.choiceWidget = GraphicalChoiceWidget(choices=choices, pixmaps=pixmaps)
        self.widgetTypeLB = Qt.QLabel('<b>Widget Type:</b>')
        self.choiceWidget.choiceMade.connect(self.onChoiceMade)
        layout = Qt.QVBoxLayout()
        layout.addLayout(nameLayout)
        layout.addWidget(self.choiceWidget)
        layout.addWidget(self.widgetTypeLB)
        self.setLayout(layout)
        return

    def initializePage(self):
        gui = self.wizard().getGui()
        if hasattr(gui, 'getPanelNames'):
            pnames = gui.getPanelNames()
            v = BlackListValidator(blackList=pnames, parent=self.nameLE)
            self.nameLE.setValidator(v)
            v.stateChanged.connect(self._onValidatorStateChanged)

    def validatePage(self):
        paneldesc = self.wizard().getPanelDescription()
        if paneldesc is None:
            Qt.QMessageBox.information(self, 'You must choose a panel type', 'Choose a panel type by clicking on one of the proposed types')
            return False
        else:
            try:
                w = paneldesc.getWidget()
                if not isinstance(w, Qt.QWidget):
                    raise ValueError
                paneldesc.name = self.field('panelname')
                return True
            except Exception as e:
                Qt.QMessageBox.warning(self, 'Invalid panel', 'The requested panel cannot be created. \nReason:\n%s' % repr(e))
                return False

            return

    def _onValidatorStateChanged(self, state, previous):
        if state == Qt.QValidator.Acceptable:
            self.diagnosticLabel.setText('')
        else:
            self.diagnosticLabel.setText('<b>(Name already exists)</b>')

    def onChoiceMade(self, choice):
        if choice == self.OTHER_TXT:
            wdesc, ok = ExpertWidgetChooserDlg.getDialog()
            if ok:
                self.widgetDescription.update(wdesc)
            else:
                return
        else:
            self.widgetDescription['classname'] = choice
        self.wizard().setPanelDescription(PanelDescription('', **self.widgetDescription))
        paneltype = str(self.widgetDescription['widgetname'] or self.widgetDescription['classname'])
        self.widgetTypeLB.setText('<b>Widget Type:</b> %s' % paneltype)


class AdvSettingsPage(Qt.QWizardPage):

    def __init__(self, parent=None):
        Qt.QWizardPage.__init__(self, parent)
        self.setTitle('Advanced settings')
        self.setSubTitle('Fine-tune the behavior of the panel by assigning a Taurus model ' + 'and/or defining the panel interactions with other parts of the GUI')
        self.setFinalPage(True)
        self.models = []
        layout = Qt.QVBoxLayout()
        self.modelGB = Qt.QGroupBox('Model')
        self.modelGB.setToolTip('Choose a Taurus model to be assigned to the panel')
        self.modelLE = Qt.QLineEdit()
        self.modelChooserBT = Qt.QToolButton()
        self.modelChooserBT.setIcon(Qt.QIcon('designer:devs_tree.png'))
        self.modelChooserBT.clicked.connect(self.showModelChooser)
        self.modelLE.editingFinished.connect(self.onModelEdited)
        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.modelLE)
        layout1.addWidget(self.modelChooserBT)
        self.modelGB.setLayout(layout1)
        self.commGB = Qt.QGroupBox('Communication')
        self.commGB.setToolTip('Define how the panel communicates with other panels and the GUI')
        self.commLV = Qt.QTableView()
        self.commModel = CommTableModel()
        self.commLV.setModel(self.commModel)
        self.commLV.setEditTriggers(self.commLV.AllEditTriggers)
        self.selectedComm = self.commLV.selectionModel().currentIndex()
        self.addBT = Qt.QToolButton()
        self.addBT.setIcon(Qt.QIcon.fromTheme('list-add'))
        self.removeBT = Qt.QToolButton()
        self.removeBT.setIcon(Qt.QIcon.fromTheme('list-remove'))
        self.removeBT.setEnabled(False)
        layout2 = Qt.QVBoxLayout()
        layout3 = Qt.QHBoxLayout()
        layout2.addWidget(self.commLV)
        layout3.addWidget(self.addBT)
        layout3.addWidget(self.removeBT)
        layout2.addLayout(layout3)
        self.commGB.setLayout(layout2)
        self.addBT.clicked.connect(self.commModel.insertRows)
        self.removeBT.clicked.connect(self.onRemoveRows)
        self.commLV.selectionModel().currentRowChanged.connect(self.onCommRowSelectionChanged)
        layout.addWidget(self.modelGB)
        layout.addWidget(self.commGB)
        self.setLayout(layout)

    def initializePage(self):
        try:
            widget = self.wizard().getPanelDescription().getWidget()
        except Exception as e:
            Logger().debug(repr(e))
            widget = None

        if isinstance(widget, TaurusBaseComponent) and widget.getModelName() != '':
            self.modelLE.setText('(already set by the chosen widget)')
            self.modelGB.setEnabled(False)
        try:
            if isinstance(Qt.qApp.SDM, SharedDataManager):
                sdm = Qt.qApp.SDM
        except Exception as e:
            Logger().debug(repr(e))
            sdm = None

        self.itemDelegate = CommItemDelegate(widget=widget, sdm=sdm)
        self.commLV.setItemDelegate(self.itemDelegate)
        return

    def showModelChooser(self):
        from taurus.qt.qtgui.panel import TaurusModelChooser
        models, ok = TaurusModelChooser.modelChooserDlg(parent=self, asMimeData=True)
        if not ok:
            return
        self.models = str(models.data(TAURUS_MODEL_LIST_MIME_TYPE))
        self.modelLE.setText(models.text())

    def onModelEdited(self):
        self.models = str(self.modelLE.text())

    def onRemoveRows(self):
        if self.selectedComm.isValid():
            self.commModel.removeRows(self.selectedComm.row())

    def onCommRowSelectionChanged(self, current, previous):
        self.selectedComm = current
        enable = current.isValid() and 0 <= current.row() < self.commModel.rowCount()
        self.removeBT.setEnabled(enable)

    def validatePage(self):
        desc = self.wizard().getPanelDescription()
        desc.model = self.models
        for uid, slotname, signalname in self.commModel.dumpData():
            if slotname:
                desc.sharedDataRead[uid] = slotname
            if signalname:
                desc.sharedDataWrite[uid] = signalname

        self.wizard().setPanelDescription(desc)
        return True


class CommTableModel(Qt.QAbstractTableModel):
    NUMCOLS = 3
    UID, R, W = list(range(NUMCOLS))
    dataChanged = Qt.pyqtSignal(int, int)

    def __init__(self, parent=None):
        Qt.QAbstractTableModel.__init__(self, parent)
        self.__table = []

    def dumpData(self):
        return copy.deepcopy(self.__table)

    def rowCount(self, index=Qt.QModelIndex()):
        return len(self.__table)

    def columnCount(self, index=Qt.QModelIndex()):
        return self.NUMCOLS

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.TextAlignmentRole:
            if orientation == Qt.Qt.Horizontal:
                return int(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
            return int(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        else:
            if role != Qt.Qt.DisplayRole:
                return
            else:
                if orientation == Qt.Qt.Horizontal:
                    if section == self.UID:
                        return 'Data UID'
                    if section == self.R:
                        return 'Reader (slot)'
                    if section == self.W:
                        return 'Writer (signal)'
                    return
                return str('%i' % (section + 1))

            return

    def data(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return
        row = index.row()
        column = index.column()
        if role == Qt.Qt.DisplayRole:
            text = self.__table[row][column]
            if text == '':
                if column == self.UID:
                    text = '(enter UID)'
                else:
                    text = '(not registered)'
            return str(text)
        else:
            return

    def flags(self, index):
        return Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsEditable | Qt.Qt.ItemIsDragEnabled | Qt.Qt.ItemIsDropEnabled | Qt.Qt.ItemIsSelectable

    def setData(self, index, value=None, role=Qt.Qt.EditRole):
        if index.isValid() and 0 <= index.row() < self.rowCount():
            row = index.row()
            column = index.column()
            self.__table[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position=None, rows=1, parentindex=None):
        if position is None:
            position = self.rowCount()
        if parentindex is None:
            parentindex = Qt.QModelIndex()
        self.beginInsertRows(parentindex, position, position + rows - 1)
        slice = [ self.rowModel() for i in range(rows) ]
        self.__table = self.__table[:position] + slice + self.__table[position:]
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, parentindex=None):
        if parentindex is None:
            parentindex = Qt.QModelIndex()
        self.beginResetModel()
        self.beginRemoveRows(parentindex, position, position + rows - 1)
        self.__table = self.__table[:position] + self.__table[position + rows:]
        self.endRemoveRows()
        self.endResetModel()
        return True

    @staticmethod
    def rowModel(uid='', slot='', signal=''):
        return [uid, slot, signal]


class CommItemDelegate(Qt.QStyledItemDelegate):
    NUMCOLS = 3
    UID, R, W = list(range(NUMCOLS))

    def __init__(self, parent=None, widget=None, sdm=None):
        super(CommItemDelegate, self).__init__(parent)
        if widget is not None:
            widget = weakref.proxy(widget)
        self._widget = widget
        if sdm is not None:
            sdm = weakref.proxy(sdm)
        self._sdm = sdm
        return

    def createEditor(self, parent, option, index):
        column = index.column()
        combobox = Qt.QComboBox(parent)
        combobox.setEditable(True)
        if column == self.UID and self._sdm is not None:
            combobox.addItems(self._sdm.activeDataUIDs())
        elif column == self.R and self._widget is not None:
            slotnames = [ n for n, o in inspect.getmembers(self._widget, inspect.ismethod) if not n.startswith('_') ]
            combobox.addItems(slotnames)
        return combobox

    def setEditorData(self, editor, index):
        editor.setEditText('')

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())


class PanelDescriptionWizard(Qt.QWizard, TaurusBaseWidget):
    """A wizard-style dialog for configuring a new TaurusGui panel.
    Use :meth:`getDialog` for launching it
    """

    def __init__(self, parent=None, designMode=False, gui=None, extraWidgets=None):
        Qt.QWizard.__init__(self, parent)
        name = 'PanelDescriptionWizard'
        TaurusBaseWidget.__init__(self, name)
        self._panelDescription = None
        if gui is None:
            gui = parent
        if gui is not None:
            self._gui = weakref.proxy(gui)
        self.widgetPG = WidgetPage(extraWidgets=extraWidgets)
        self.advSettingsPG = AdvSettingsPage()
        self.addPage(self.widgetPG)
        self.addPage(self.advSettingsPG)
        return

    def getGui(self):
        """returns a reference to the GUI to which the dialog is associated"""
        return self._gui

    def getPanelDescription(self):
        """Returns the panel description with the choices made so far

        :return: (PanelDescription) the panel description
        """
        return self._panelDescription

    def setPanelDescription(self, desc):
        """Sets the Panel description

        :param desc: (PanelDescription)
        """
        self._panelDescription = desc

    @staticmethod
    def getDialog(parent, extraWidgets=None):
        """Static method for launching a new Dialog.

        :param parent: parent widget for the new dialog

        :return: (tuple<PanelDescription,bool>) tuple of a description object
                 and a state flag. The state is True if the dialog was accepted
                 and False otherwise
        """
        dlg = PanelDescriptionWizard(parent, extraWidgets=extraWidgets)
        dlg.exec_()
        return (dlg.getPanelDescription(), dlg.result() == dlg.Accepted)


def test():
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    form = PanelDescriptionWizard()

    def kk(d):
        print(d)

    Qt.qApp.SDM = SharedDataManager(form)
    Qt.qApp.SDM.connectReader('111111', kk)
    Qt.qApp.SDM.connectWriter('222222', form, 'thisisasignalname')
    form.show()
    sys.exit(app.exec_())
    return


def test2():
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    print(ExpertWidgetChooserDlg.getDialog())
    sys.exit()
    return


def main():
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    from taurus.qt.qtgui.container import TaurusMainWindow
    form = Qt.QMainWindow()

    def kk(d):
        print(d)

    Qt.qApp.SDM = SharedDataManager(form)
    Qt.qApp.SDM.connectReader('someUID', kk)
    Qt.qApp.SDM.connectWriter('anotherUID', form, 'thisisasignalname')
    form.show()
    paneldesc, ok = PanelDescriptionWizard.getDialog(form, extraWidgets=[('PyQt4.Qt.QLineEdit', 'logos:taurus.png'),
     ('PyQt4.Qt.QTextEdit', None)])
    if ok:
        w = paneldesc.getWidget(sdm=Qt.qApp.SDM)
        form.setCentralWidget(w)
        form.setWindowTitle(paneldesc.name)
    print(Qt.qApp.SDM.info())
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    main()