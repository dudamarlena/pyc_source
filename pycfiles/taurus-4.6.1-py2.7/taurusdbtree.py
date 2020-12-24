# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/tree/taurusdbtree.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides widgets that display the database in a tree format"""
from __future__ import absolute_import
from taurus.external.qt import Qt
from taurus.core.taurusbasetypes import TaurusElementType
from taurus.core.taurusauthority import TaurusAuthority
from taurus.qt.qtcore.model import *
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.qt.qtgui.icon import getElementTypeIcon, getElementTypeIconName
from .taurustree import TaurusBaseTreeWidget
__all__ = [
 'TaurusDbTreeWidget']
__docformat__ = 'restructuredtext'

class TaurusDbTreeWidget(TaurusBaseTreeWidget):
    """A class:`taurus.qt.qtgui.tree.TaurusBaseTreeWidget` that connects to a
    :class:`taurus.core.taurusauthority.TaurusAuthority` model. It can show the list of database
    elements in four different perspectives:

    - device : a three level hierarchy of devices (domain/family/name)
    - server : a server based perspective
    - class : a class based perspective

    Filters can be inserted into this widget to restrict the tree nodes that are
    seen.
    """
    KnownPerspectives = {TaurusElementType.Device: {'label': 'By device', 
                                  'icon': getElementTypeIconName(TaurusElementType.Device), 
                                  'tooltip': 'View by device tree', 
                                  'model': [
                                          TaurusDbDeviceProxyModel, TaurusDbDeviceModel]}, 
       'PlainDevice': {'label': 'By plain device', 
                       'icon': getElementTypeIconName(TaurusElementType.Device), 
                       'tooltip': 'View by plain device tree (it may take a long time if there are problems with the exported devices)', 
                       'model': [
                               TaurusDbDeviceProxyModel, TaurusDbPlainDeviceModel]}, 
       TaurusElementType.Server: {'label': 'By server', 
                                  'icon': getElementTypeIconName(TaurusElementType.Server), 
                                  'tooltip': 'View by server tree', 
                                  'model': [
                                          TaurusDbServerProxyModel, TaurusDbServerModel]}, 
       TaurusElementType.DeviceClass: {'label': 'By class', 
                                       'icon': getElementTypeIconName(TaurusElementType.DeviceClass), 
                                       'tooltip': 'View by class tree', 
                                       'model': [
                                               TaurusDbDeviceClassProxyModel, TaurusDbDeviceClassModel]}}
    DftPerspective = TaurusElementType.Device

    def getModelClass(self):
        return TaurusAuthority

    def sizeHint(self):
        return Qt.QSize(1024, 512)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.tree'
        ret['group'] = 'Taurus Views'
        ret['icon'] = 'designer:listview.png'
        return ret


class _TaurusTreePanel(Qt.QWidget, TaurusBaseWidget):
    """A demonstration panel to show how :class:`taurus.qt.qtcore.TaurusDbBaseModel`
    models can interact with several model view widgets like QTreeView,
    QTableView, QListView and QComboBox"""

    def __init__(self, parent=None, designMode=False):
        """doc please!"""
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QWidget, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        self.init(designMode)

    def init(self, designMode):
        l = Qt.QGridLayout()
        l.setContentsMargins(0, 0, 0, 0)
        self.setLayout(l)
        main_panel = Qt.QTabWidget()
        self._device_tree_view = TaurusDbTreeWidget(perspective=TaurusElementType.Device)
        self._device_table_view = Qt.QTableView()
        self._device_table_view.setModel(TaurusDbBaseModel())
        self._device_list_view = Qt.QListView()
        self._device_list_view.setModel(TaurusDbSimpleDeviceModel())
        self._server_tree_view = TaurusDbTreeWidget(perspective=TaurusElementType.Server)
        self._class_tree_view = TaurusDbTreeWidget(perspective=TaurusElementType.DeviceClass)
        self._device_combo_view = Qt.QWidget()
        combo_form = Qt.QFormLayout()
        self._device_combo_view.setLayout(combo_form)
        self._combo_dev_tree_widget = TaurusDbTreeWidget(perspective=TaurusElementType.Device)
        qmodel = self._combo_dev_tree_widget.getQModel()
        qmodel.setSelectables([TaurusElementType.Member])
        device_combo = Qt.QComboBox()
        device_combo.setModel(qmodel)
        device_combo.setMaxVisibleItems(20)
        device_combo.setView(self._combo_dev_tree_widget.treeView())
        combo_form.addRow('Device selector (by device hierarchy):', device_combo)
        self._combo_attr_tree_widget = TaurusDbTreeWidget(perspective=TaurusElementType.Device)
        qmodel = self._combo_attr_tree_widget.getQModel()
        device_combo = Qt.QComboBox()
        device_combo.setModel(qmodel)
        device_combo.setMaxVisibleItems(20)
        device_combo.setView(self._combo_attr_tree_widget.treeView())
        combo_form.addRow('Attribute selector (by device hierarchy):', device_combo)
        self._combo_dev_table_view = Qt.QTableView()
        self._combo_dev_table_view.setModel(TaurusDbBaseModel())
        qmodel = self._combo_dev_table_view.model()
        qmodel.setSelectables([TaurusElementType.Device])
        device_combo = Qt.QComboBox()
        device_combo.setModel(qmodel)
        device_combo.setMaxVisibleItems(20)
        device_combo.setView(self._combo_dev_table_view)
        combo_form.addRow('Device selector (by plain device):', device_combo)
        main_panel.addTab(self._device_tree_view, 'Device (Tree View)')
        main_panel.addTab(self._device_table_view, 'Device (Table View)')
        main_panel.addTab(self._device_list_view, 'Device (List View)')
        main_panel.addTab(self._server_tree_view, 'Server (Tree View)')
        main_panel.addTab(self._class_tree_view, 'Class (Tree View)')
        main_panel.addTab(self._device_combo_view, 'ComboBox Views')
        l.addWidget(main_panel, 1, 0)
        self._main_panel = main_panel

    def deviceTreeWidget(self):
        return self._device_tree_view

    def deviceTableWidget(self):
        return self._device_table_view

    def deviceListWidget(self):
        return self._device_list_view

    def serverTreeWidget(self):
        return self._server_tree_view

    def classTreeWidget(self):
        return self._class_tree_view

    def sizeHint(self):
        return Qt.QSize(1024, 512)

    def _updateTreeModels(self):
        db_name, db = self.getModel(), self.getModelObj()
        self._device_tree_view.setModel(db_name)
        model = self._device_table_view.model()
        if model is not None:
            model.setDataSource(db)
        model = self._device_list_view.model()
        if model is not None:
            model.setDataSource(db)
        self._server_tree_view.setModel(db_name)
        self._class_tree_view.setModel(db_name)
        self._combo_dev_tree_widget.setModel(db_name)
        self._combo_attr_tree_widget.setModel(db_name)
        model = self._combo_dev_table_view.model()
        if model is not None:
            model.setDataSource(db)
        return

    def refresh(self):
        db = self.getModelObj()
        if db is None:
            return
        else:
            db.refreshCache()
            self._device_tree_view.refresh()
            self._device_table_view.model().refresh()
            self._device_list_view.model().refresh()
            self._server_tree_view.refresh()
            self._class_tree_view.refresh()
            return

    def goIntoTree(self):
        index = self._device_tree_view.currentIndex()
        if index is None:
            return
        else:
            self._device_tree_view.setRootIndex(index)
            return

    def goUpTree(self):
        index = self._device_tree_view.rootIndex()
        if index is None:
            return
        else:
            index_parent = index.parent()
            if index_parent is None:
                return
            self._device_tree_view.setRootIndex(index_parent)
            return

    def getModelClass(self):
        return TaurusAuthority

    @Qt.pyqtSlot('QString')
    def setModel(self, model):
        """Sets/unsets the model name for this component

        :param model: (str) the new model name"""
        super(_TaurusTreePanel, self).setModel(model)
        self._updateTreeModels()

    model = Qt.pyqtProperty('QString', TaurusBaseWidget.getModel, TaurusBaseWidget.setModel, TaurusBaseWidget.resetModel)


def main_TaurusTreePanel(host):
    w = _TaurusTreePanel()
    w.setWindowIcon(getElementTypeIcon(TaurusElementType.Device))
    w.setWindowTitle('A Taurus Tree Example')
    w.setModel(host)
    w.show()
    return w


def main_TaurusDbTreeWidget(host, perspective=TaurusElementType.Device):
    w = TaurusDbTreeWidget(perspective=perspective)
    w.setWindowIcon(getElementTypeIcon(perspective))
    w.setWindowTitle('A Taurus Tree Example')
    w.setModel(host)
    w.show()
    return w


def demo():
    """DB panels"""
    import taurus
    db = taurus.Authority()
    host = db.getNormalName()
    w = main_TaurusTreePanel(host)
    return w


def main():
    import sys, taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    app = Application.instance()
    owns_app = app is None
    if owns_app:
        app = Application(app_name='DB model demo', app_version='1.0', org_domain='Taurus', org_name='Tango community')
    w = demo()
    w.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w
    return


if __name__ == '__main__':
    main()