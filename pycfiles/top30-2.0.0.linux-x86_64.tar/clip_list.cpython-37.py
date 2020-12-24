# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/projects/top30/pyenv/lib/python3.7/site-packages/top30/clip_list.py
# Compiled at: 2019-04-09 12:52:22
# Size of source mod 2**32: 6704 bytes
from PyQt5 import QtCore, QtWidgets, QtGui
from mutagen.id3 import COMM
import mutagen, top30

class ClipListModel(QtCore.QAbstractTableModel):

    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self, parent=None)
        self.horizontal_header = ['Type', 'Filename', 'Start']
        self.data = []

    def supportedDragActions(self):
        return QtCore.Qt.MoveAction

    def flags(self, index):
        flags = QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if index.isValid():
            if index.column() == self.columnCount() - 1:
                flags |= QtCore.Qt.ItemIsEditable
            flags |= QtCore.Qt.ItemIsDragEnabled
        return flags

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.data[index.row()][index.column()]

    def setData(self, index, value, role):
        if not (role != QtCore.Qt.EditRole or index.isValid)() or index.column() != self.columnCount() - 1:
            return False
        if value == '':
            self.data[index.row()][index.column()] = None
            self.data[index.row()][0] = 'Voice'
        else:
            self.data[index.row()][0] = 'Song'
            if ':' not in value:
                value = '00:' + value
            if value.count(':') > 1:
                return False
                minute = value.split(':')[0]
                second = value.split(':')[1]
                return minute.isdigit() and second.isdigit() or False
                value = '{0:02d}:{1:0>4.1f}'.format(int(minute), float(second))
                self.data[index.row()][index.column()] = value
            else:
                filename = self.data[index.row()][1]
                song_meta = mutagen.File(filename)
                tag = top30.SETTINGS.song_start_tag()
                if top30.get_format(filename) == 'mp3':
                    comment = COMM(3, 'eng', '', value)
                    song_meta['COMM:eng'] = comment
                else:
                    song_meta[tag] = value
            song_meta.save()
            return True

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return
        if orientation == QtCore.Qt.Horizontal:
            return self.horizontal_header[index]
        return str(index + 1)

    def appendRow(self, row):
        self.insertRows(self.rowCount(), [row])

    def insertRows(self, row, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row + len(rows) - 1)
        for i in range(len(rows)):
            row_i = row + i
            self.data.insert(row_i, rows[i])

        self.endInsertRows()

    def insertRow(self, row, row_data):
        self.insertRows(row, [row_data])

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            del self.data[row + count - 1]

        self.endRemoveRows()
        return True

    def removeRow(self, row):
        self.removeRows(row, 1)

    def moveRows(self, source_parent, source_first, source_last, destination_parent, destination):
        self.beginMoveRows(source_parent, source_first, source_last, destination_parent, destination)
        items = self.data[source_first:source_last + 1]
        self.data = self.data[:source_first] + self.data[source_last + 1:]
        for i in range(len(items)):
            self.data.insert(destination + i, items[i])

        self.endMoveRows()


class ClipListView(QtWidgets.QTableView):

    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent=None)
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if not event.mimeData().hasFormat('application/top30clip'):
            if event.mimeData().hasFormat('audio/ogg') or event.mimeData().hasFormat('audio/mp3'):
                event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid() or index.row() == self.source_index.row():
            return
        source = self.source_index.row()
        destination = index.row()
        if destination == source + 1:
            destination = source
            source += 1
        self.model().moveRows(QtCore.QModelIndex(), source, source, QtCore.QModelIndex(), destination)
        event.accept()

    def mousePressEvent(self, event):
        super(ClipListView, self).mousePressEvent(event)
        self.startDrag(event)

    def startDrag(self, event):
        self.source_index = self.indexAt(event.pos())
        if not self.source_index.isValid():
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setData('application/top30clip', b'')
        drag.setMimeData(mimeData)
        vis = self.source_index.sibling(self.source_index.row() + 1, self.source_index.column())
        pixmap = QtGui.QPixmap()
        pixmap = self.grab(self.visualRect(vis))
        drag.setPixmap(pixmap)
        result = drag.exec()


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False