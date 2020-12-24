# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/extra/PyQt/treeview_example.py
# Compiled at: 2013-11-12 16:48:22
from PyQt4 import QtCore, QtGui
import sys, icons_rc

class Node(object):

    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)
        return

    def typeInfo(self):
        return 'NODE'

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        else:
            return

    def log(self, tabLevel=-1):
        output = ''
        tabLevel += 1
        for i in range(tabLevel):
            output += '\t'

        output += '|------' + self._name + '\n'
        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += '\n'
        return output

    def __repr__(self):
        return self.log()


class TransformNode(Node):

    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)

    def typeInfo(self):
        return 'TRANSFORM'


class CameraNode(Node):

    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)

    def typeInfo(self):
        return 'CAMERA'


class LightNode(Node):

    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)

    def typeInfo(self):
        return 'LIGHT'


class SceneGraphModel(QtCore.QAbstractItemModel):
    """INPUTS: Node, QObject"""

    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return
        else:
            node = index.internalPointer()
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                if index.column() == 0:
                    return node.name()
            if role == QtCore.Qt.DecorationRole:
                if index.column() == 0:
                    typeInfo = node.typeInfo()
                    if typeInfo == 'LIGHT':
                        return QtGui.QIcon(QtGui.QPixmap(':/Light.png'))
                    if typeInfo == 'TRANSFORM':
                        return QtGui.QIcon(QtGui.QPixmap(':/Transform.png'))
                    if typeInfo == 'CAMERA':
                        return QtGui.QIcon(QtGui.QPixmap(':/Camera.png'))
            return

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return 'Scenegraph'
            else:
                return 'Typeinfo'

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node('untitled' + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()
        return success

    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = LightNode('light' + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()
        return success


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle('plastique')
    rootNode = Node('Hips')
    childNode0 = TransformNode('RightPirateLeg', rootNode)
    childNode1 = Node('RightPirateLeg_END', childNode0)
    childNode2 = CameraNode('LeftFemur', rootNode)
    childNode3 = Node('LeftTibia', childNode2)
    childNode4 = Node('LeftFoot', childNode3)
    childNode5 = LightNode('LeftFoot_END', childNode4)
    print rootNode
    model = SceneGraphModel(rootNode)
    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)
    rightPirateLeg = model.index(0, 0, QtCore.QModelIndex())
    model.insertRows(1, 5, rightPirateLeg)
    model.insertLights(1, 5, rightPirateLeg)
    sys.exit(app.exec_())