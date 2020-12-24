# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/util/tauruswidgettree.py
# Compiled at: 2019-08-19 15:09:30
"""
"""
__all__ = [
 'QObjectRepresentation', 'get_qobject_tree', 'get_qobject_tree_str',
 'TreeQObjectModel', 'TreeQObjectWidget']
__docformat__ = 'restructuredtext'
import weakref
from taurus.external.qt import Qt
from taurus.core.util.enumeration import Enumeration
QObjectRepresentation = Enumeration('QObjectRepresentation', ('ClassName', 'ObjectName',
                                                              'FullName'))

def _build_qobjects_as_dict(qobject, container):
    container[qobject] = childs = {}
    for child in qobject.children():
        if isinstance(child, Qt.QWidget):
            _build_qobjects_as_dict(child, childs)


def get_qobject_tree_as_dict(qobject=None):
    if qobject is None:
        app = Qt.QApplication.instance()
        qobjects = app.topLevelWidgets()
    else:
        qobjects = [
         qobject]
    tree = {}
    for qobject in qobjects:
        _build_qobjects_as_dict(qobject, tree)

    return tree


def _build_qobjects_as_list(qobject, container):
    children = qobject.children()
    node = (qobject, [])
    container.append(node)
    for child in children:
        if isinstance(child, Qt.QWidget):
            _build_qobjects_as_list(child, node[1])


def get_qobject_tree_as_list(qobject=None):
    if qobject is None:
        app = Qt.QApplication.instance()
        qobjects = app.topLevelWidgets()
    else:
        qobjects = [
         qobject]
    tree = []
    for qobject in qobjects:
        _build_qobjects_as_list(qobject, tree)

    return tree


get_qobject_tree = get_qobject_tree_as_list

def _get_qobject_str(qobject, representation):
    if representation == QObjectRepresentation.ClassName:
        return qobject.__class__.__name__
    if representation == QObjectRepresentation.ObjectName:
        return str(qobject.objectName())
    if representation == QObjectRepresentation.FullName:
        return ('{0}("{1}")').format(qobject.__class__.__name__, str(qobject.objectName()))
    return str(qobject)


def _build_qobject_str(node, str_tree, representation=QObjectRepresentation.ClassName):
    qobject, children = node
    str_node = _get_qobject_str(qobject, representation)
    str_children = []
    str_tree.append((str_node, str_children))
    for child in children:
        _build_qobject_str(child, str_children, representation=representation)


def get_qobject_tree_str(qobject=None, representation=QObjectRepresentation.ClassName):
    tree, str_tree = get_qobject_tree(qobject=qobject), []
    for e in tree:
        _build_qobject_str(e, str_tree, representation=representation)

    return str_tree


from taurus.qt.qtgui.tree.qtree import QBaseTreeWidget
from taurus.qt.qtcore.model import TaurusBaseModel, TaurusBaseTreeItem
QR = QObjectRepresentation

class TreeQObjecttItem(TaurusBaseTreeItem):

    def __init__(self, model, data, parent=None):
        TaurusBaseTreeItem.__init__(self, model, data, parent=parent)
        if data is not None:
            self.qobject = weakref.ref(data)
            dat = (_get_qobject_str(data, QR.ClassName),
             _get_qobject_str(data, QR.ObjectName))
            self.setData(0, dat)
        return


class TreeQObjectModel(TaurusBaseModel):
    ColumnNames = ('Class', 'Object name')
    ColumnRoles = ((QR.ClassName,), QR.ObjectName)

    def __init__(self, parent=None, data=None):
        TaurusBaseModel.__init__(self, parent=parent, data=data)

    def role(self, column, depth=0):
        if column == 0:
            return self.ColumnRoles[column][0]
        return self.ColumnRoles[column]

    def roleIcon(self, taurus_role):
        return Qt.QIcon()

    def roleSize(self, taurus_role):
        return Qt.QSize(300, 70)

    def roleToolTip(self, role):
        return 'widget information'

    @staticmethod
    def _build_qobject_item(model, parent, node):
        qobject, children = node
        item = TreeQObjecttItem(model, qobject, parent)
        parent.appendChild(item)
        for child in children:
            TreeQObjectModel._build_qobject_item(model, item, child)

    def setupModelData(self, data):
        if data is None:
            return
        else:
            rootItem = self._rootItem
            for node in data:
                TreeQObjectModel._build_qobject_item(self, rootItem, node)

            return


class TreeQObjectWidget(QBaseTreeWidget):
    KnownPerspectives = {'Default': {'label': 'Default perspecive', 
                   'tooltip': 'QObject tree view', 
                   'icon': '', 
                   'model': [
                           TreeQObjectModel]}}
    DftPerspective = 'Default'

    def __init__(self, parent=None, designMode=False, with_navigation_bar=True, with_filter_widget=True, perspective=None, proxy=None, qobject_root=None):
        QBaseTreeWidget.__init__(self, parent, designMode=designMode, with_navigation_bar=with_navigation_bar, with_filter_widget=with_filter_widget, perspective=perspective, proxy=proxy)
        qmodel = self.getQModel()
        qmodel.setDataSource(get_qobject_tree(qobject=qobject_root))


def build_gui():
    mw = Qt.QMainWindow()
    mw.setObjectName('main window')
    w = Qt.QWidget()
    w.setObjectName('central widget')
    mw.setCentralWidget(w)
    l = Qt.QVBoxLayout()
    w.setLayout(l)
    l1 = Qt.QLabel('H1')
    l1.setObjectName('label 1')
    l.addWidget(l1)
    l2 = Qt.QLabel('H2')
    l2.setObjectName('label 2')
    l.addWidget(l2)
    mw.show()
    return mw


def main():
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    w = build_gui()
    tree = TreeQObjectWidget(qobject_root=w)
    tree.show()
    w.dumpObjectTree()
    app.exec_()
    return


if __name__ == '__main__':
    main()