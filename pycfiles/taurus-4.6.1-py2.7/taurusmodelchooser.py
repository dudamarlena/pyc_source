# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/taurusmodelchooser.py
# Compiled at: 2019-08-19 15:09:30
"""
AttributeChooser.py: widget for choosing (a list of) attributes from a tango DB
"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import bytes, str
import sys, pkg_resources, taurus
from taurus.external.qt import Qt, QtCore
from taurus.external.qt.compat import PY_OBJECT
import taurus.core
from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.tree import TaurusDbTreeWidget
from taurus.core.util.containers import CaselessList
from .taurusmodellist import TaurusModelList
__all__ = [
 'TaurusModelSelectorTree', 'TaurusModelChooser',
 'TaurusModelSelector', 'TaurusModelSelectorItem']

class TaurusModelSelector(Qt.QTabWidget):
    """TaurusModelSelector is a QTabWidget container for
    TaurusModelSelectorItem.
    """
    modelsAdded = Qt.pyqtSignal(PY_OBJECT)

    def __init__(self, parent=None):
        Qt.QTabWidget.__init__(self, parent=parent)
        self.currentChanged.connect(self.__setTabItemModel)
        ep_name = 'taurus.qt.qtgui.panel.TaurusModelSelector.items'
        for ep in pkg_resources.iter_entry_points(ep_name):
            try:
                ms_class = ep.load()
                ms_item = ms_class(parent=self)
                self.__addItem(ms_item, ep.name)
            except Exception as e:
                err = ('Invalid TaurusModelSelectorItem plugin: {}\n{}').format(ep.module_name, e)
                taurus.warning(err)

    def __setTabItemModel(self):
        w = self.currentWidget()
        c = self.cursor()
        try:
            try:
                if not w.model:
                    self.setCursor(QtCore.Qt.WaitCursor)
                    w.setModel(w.default_model)
            except Exception as e:
                taurus.warning('Problem setting up selector: %r', e)

        finally:
            self.setCursor(c)

    def __addItem(self, widget, name, model=None):
        if model is not None:
            widget.default_model = model
        widget.modelsAdded.connect(self.modelsAdded)
        self.addTab(widget, name)
        return


class TaurusModelSelectorItem(TaurusWidget):
    """Base class for ModelSelectorItem.
    It defines the minimal API to be defined in the specialization
    """
    modelsAdded = Qt.pyqtSignal(PY_OBJECT)
    _dragEnabled = True

    def __init__(self, parent=None, **kwargs):
        TaurusWidget.__init__(self, parent)
        self._default_model = None
        return

    def getSelectedModels(self):
        raise NotImplementedError('getSelectedModels must be implemented' + ' in TaurusModelSelectorItem subclass')

    def getModelMimeData(self):
        """ Reimplemented from TaurusBaseComponent
        """
        models = self.getSelectedModels()
        md = Qt.QMimeData()
        md.setText((', ').join(models))
        models_bytes = [ bytes(m, encoding='utf-8') for m in models ]
        md.setData(taurus.qt.qtcore.mimetypes.TAURUS_MODEL_LIST_MIME_TYPE, ('\r\n').join(models_bytes))
        return md

    def _get_default_model(self):
        """
        Reimplement to return a default model to initialize the widget
        """
        raise NotImplementedError('default_model must be implemented' + ' in TaurusModelSelectorItem subclass')

    def _set_default_model(self, model):
        """
        Set default model to initialize the widget
        """
        self._default_model = model

    default_model = property(fget=_get_default_model, fset=_set_default_model)


class TaurusModelSelectorTree(TaurusModelSelectorItem):
    addModels = Qt.pyqtSignal('QStringList')

    def __init__(self, parent=None, selectables=None, buttonsPos=None, designMode=None):
        TaurusModelSelectorItem.__init__(self, parent)
        if selectables is None:
            selectables = [
             taurus.core.taurusbasetypes.TaurusElementType.Attribute, taurus.core.taurusbasetypes.TaurusElementType.Member,
             taurus.core.taurusbasetypes.TaurusElementType.Device]
        self._selectables = selectables
        self._deviceTree = TaurusDbTreeWidget(perspective=taurus.core.taurusbasetypes.TaurusElementType.Device)
        self._deviceTree.getQModel().setSelectables(self._selectables)
        self._toolbar = Qt.QToolBar('TangoSelector toolbar')
        self._toolbar.setIconSize(Qt.QSize(16, 16))
        self._toolbar.setFloatable(False)
        self._addSelectedAction = self._toolbar.addAction(Qt.QIcon.fromTheme('list-add'), 'Add selected', self.onAddSelected)
        self.setButtonsPos(buttonsPos)
        self.modelChanged.connect(self._deviceTree.setModel)
        return

    def setButtonsPos(self, buttonsPos):
        currlayout = self.layout()
        if currlayout is not None:
            currlayout.deleteLater()
            Qt.QCoreApplication.sendPostedEvents(currlayout, Qt.QEvent.DeferredDelete)
        if buttonsPos is None:
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.BottomToolBarArea:
            self._toolbar.setOrientation(Qt.Qt.Horizontal)
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self._deviceTree)
            self.layout().addWidget(self._toolbar)
        elif buttonsPos == Qt.Qt.TopToolBarArea:
            self._toolbar.setOrientation(Qt.Qt.Horizontal)
            self.setLayout(Qt.QVBoxLayout())
            self.layout().addWidget(self._toolbar)
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.LeftToolBarArea:
            self._toolbar.setOrientation(Qt.Qt.Vertical)
            self.setLayout(Qt.QHBoxLayout())
            self.layout().addWidget(self._toolbar)
            self.layout().addWidget(self._deviceTree)
        elif buttonsPos == Qt.Qt.RightToolBarArea:
            self._toolbar.setOrientation(Qt.Qt.Vertical)
            self.setLayout(Qt.QHBoxLayout())
            self.layout().addWidget(self._deviceTree)
            self.layout().addWidget(self._toolbar)
        else:
            raise ValueError('Invalid buttons position')
        return

    def getSelectedModels(self):
        selected = []
        try:
            from taurus.core.tango.tangodatabase import TangoDevInfo, TangoAttrInfo
        except:
            return selected

        for item in self._deviceTree.selectedItems():
            nfo = item.itemData()
            if isinstance(nfo, TangoDevInfo):
                selected.append(nfo.fullName())
            elif isinstance(nfo, TangoAttrInfo):
                selected.append('%s/%s' % (
                 nfo.device().fullName(), nfo.name()))
            else:
                self.info("Unknown item '%s' in selection" % repr(nfo))

        return selected

    def onAddSelected(self):
        self.addModels.emit(self.getSelectedModels())

    def treeView(self):
        return self._deviceTree.treeView()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.panel'
        ret['icon'] = 'designer:listview.png'
        ret['container'] = False
        ret['group'] = 'Taurus Views'
        return ret


class TangoModelSelectorItem(TaurusModelSelectorTree):
    """A taurus model selector item for Tango models
    """

    def __init__(self, parent=None, selectables=None, buttonsPos=Qt.Qt.RightToolBarArea, designMode=None):
        TaurusModelSelectorTree.__init__(self, parent=parent, selectables=selectables, buttonsPos=buttonsPos, designMode=designMode)

    def onAddSelected(self):
        """
        Reimplemented from TaurusModelSelectorTree to emit modelsAdded
        signal instead of addModels
        """
        self.modelsAdded.emit(self.getSelectedModels())

    def _get_default_model(self):
        """Reimplemented from TaurusModelSelectorItem"""
        if self._default_model is None:
            f = taurus.Factory('tango')
            self._default_model = f.getAuthority().getFullName()
        return self._default_model

    default_model = property(fget=_get_default_model, fset=TaurusModelSelectorTree._set_default_model)


class TaurusModelChooser(TaurusWidget):
    """A widget that allows the user to select a list of models from a tree representing
    devices and attributes from a Tango server.

    The user selects models and adds them to a list. Then the user should click on the
    update button to notify that the selection is ready.

    signals::
      - "updateModels"  emitted when the user clicks on the update button. It
        passes a list<str> of models that have been selected.
    """
    updateModels = Qt.pyqtSignal('QStringList')
    UpdateAttrs = Qt.pyqtSignal(['QStringList'], ['QMimeData'])

    def __init__(self, parent=None, selectables=None, host=None, designMode=None, singleModel=False):
        """Creator of TaurusModelChooser

        :param parent: (QObject) parent for the dialog
        :param selectables: (list<TaurusElementType>) if passed, only elements of the tree whose
                            type is in the list will be selectable.
        :param host: (QObject) Tango host to be explored by the chooser
        :param designMode: (bool) needed for taurusdesigner but ignored here
        :param singleModel: (bool) If True, the selection will be of just one
                            model. Otherwise (default) a list of models can be selected
        """
        TaurusWidget.__init__(self, parent)
        if host is None:
            try:
                host = taurus.Factory('tango').getAuthority().getFullName()
            except Exception as e:
                taurus.info('Cannot populate Tango Tree: %r', e)

        self._allowDuplicates = False
        self.setLayout(Qt.QVBoxLayout())
        self.tree = TaurusModelSelectorTree(selectables=selectables, buttonsPos=Qt.Qt.BottomToolBarArea)
        self.tree.setModel(host)
        self.list = TaurusModelList()
        self.list.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        applyBT = Qt.QToolButton()
        applyBT.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        applyBT.setText('Apply')
        applyBT.setIcon(Qt.QIcon('status:available.svg'))
        self.setSingleModelMode(singleModel)
        self._toolbar = self.tree._toolbar
        self._toolbar.addAction(self.list.removeSelectedAction)
        self._toolbar.addAction(self.list.removeAllAction)
        self._toolbar.addAction(self.list.moveUpAction)
        self._toolbar.addAction(self.list.moveDownAction)
        self._toolbar.addSeparator()
        self._toolbar.addWidget(applyBT)
        self.layout().addWidget(self.tree)
        self.layout().addWidget(self.list)
        self.modelChanged.connect(self.tree.setModel)
        self.tree.addModels.connect(self.addModels)
        applyBT.clicked.connect(self._onUpdateModels)
        return

    def getListedModels(self, asMimeData=False):
        """returns the list of models that have been added

        :param asMimeData: (bool) If False (default), the return value will be a
                           list of models. If True, the return value is a
                           `QMimeData` containing at least `TAURUS_MODEL_LIST_MIME_TYPE`
                           and `text/plain` MIME types. If only one model was selected,
                           the mime data also contains a TAURUS_MODEL_MIME_TYPE.

        :return: (list<str> or QMimeData) the type of return depends on the value of `asMimeData`"""
        models = self.list.getModelList()
        if self.isSingleModelMode():
            models = models[:1]
        if asMimeData:
            md = Qt.QMimeData()
            md.setData(taurus.qt.qtcore.mimetypes.TAURUS_MODEL_LIST_MIME_TYPE, str(('\r\n').join(models)))
            md.setText((', ').join(models))
            if len(models) == 1:
                md.setData(taurus.qt.qtcore.mimetypes.TAURUS_MODEL_MIME_TYPE, str(models[0]))
            return md
        return models

    def setListedModels(self, models):
        """adds the given list of models to the widget list
        """
        self.list.model().clearAll()
        self.list.addModels(models)

    def resetListedModels(self):
        """equivalent to setListedModels([])"""
        self.list.model().clearAll()

    def updateList(self, attrList):
        """for backwards compatibility with AttributeChooser only. Use :meth:`setListedModels` instead"""
        self.info('ModelChooser.updateList() is provided for backwards compatibility only. Use setListedModels() instead')
        self.setListedModels(attrList)

    def addModels(self, models):
        """ Add given models to the selected models list"""
        if len(models) == 0:
            models = [
             '']
        if self.isSingleModelMode():
            self.resetListedModels()
        if self._allowDuplicates:
            self.list.addModels(models)
        else:
            listedmodels = CaselessList(self.getListedModels())
            for m in models:
                if m not in listedmodels:
                    listedmodels.append(m)
                    self.list.addModels([m])

    def onRemoveSelected(self):
        """
        Remove the list-selected models from the list
        """
        self.list.removeSelected()

    def _onUpdateModels(self):
        models = self.getListedModels()
        self.updateModels.emit(models)
        if taurus.core.taurusbasetypes.TaurusElementType.Attribute in self.tree._selectables:
            self.UpdateAttrs.emit(models)

    def setSingleModelMode(self, single):
        """sets whether the selection should be limited to just one model
        (single=True) or not (single=False)"""
        if single:
            self.tree.treeView().setSelectionMode(Qt.QAbstractItemView.SingleSelection)
        else:
            self.tree.treeView().setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        self._singleModelMode = single

    def isSingleModelMode(self):
        """returns True if the selection is limited to just one model. Returns False otherwise.

        :return: (bool)"""
        return self._singleModelMode

    def resetSingleModelMode(self):
        """equivalent to setSingleModelMode(False)"""
        self.setSingleModelMode(self, False)

    @staticmethod
    def modelChooserDlg(parent=None, selectables=None, host=None, asMimeData=False, singleModel=False, windowTitle='Model Chooser', listedModels=None):
        """Static method that launches a modal dialog containing a TaurusModelChooser

        :param parent: (QObject) parent for the dialog
        :param selectables: (list<TaurusElementType>) if passed, only elements of the tree whose
                            type is in the list will be selectable.
        :param host: (QObject) Tango host to be explored by the chooser
        :param asMimeData: (bool) If False (default),  a list of models will be.
                           returned. If True, a `QMimeData` object will be
                           returned instead. See :meth:`getListedModels` for a
                           detailed description of this QMimeData object.
        :param singleModel: (bool) If True, the selection will be of just one
                            model. Otherwise (default) a list of models can be selected
        :param windowTitle: (str) Title of the dialog (default="Model Chooser")
        :param listedModels: (list<str>) List of model names for initializing the 
                             model list

        :return: (list,bool or QMimeData,bool) Returns a models,ok tuple. models can be
                 either a list of models or a QMimeData object, depending on
                 `asMimeData`. ok is True if the dialog was accepted (by
                 clicking on the "update" button) and False otherwise
        """
        dlg = Qt.QDialog(parent)
        dlg.setWindowTitle(windowTitle)
        dlg.setWindowIcon(Qt.QIcon('logos:taurus.png'))
        layout = Qt.QVBoxLayout()
        w = TaurusModelChooser(parent=parent, selectables=selectables, host=host, singleModel=singleModel)
        if listedModels is not None:
            w.setListedModels(listedModels)
        layout.addWidget(w)
        dlg.setLayout(layout)
        w.updateModels.connect(dlg.accept)
        dlg.exec_()
        return (w.getListedModels(asMimeData=asMimeData), dlg.result() == dlg.Accepted)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.panel'
        ret['icon'] = 'designer:listview.png'
        ret['container'] = False
        ret['group'] = 'Taurus Views'
        return ret

    singleModelMode = Qt.pyqtProperty('bool', isSingleModelMode, setSingleModelMode, resetSingleModelMode)


def main(args):
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = None
    app = Qt.QApplication(args)
    print(TaurusModelChooser.modelChooserDlg(host=host))
    sys.exit()
    return


if __name__ == '__main__':
    main(sys.argv)