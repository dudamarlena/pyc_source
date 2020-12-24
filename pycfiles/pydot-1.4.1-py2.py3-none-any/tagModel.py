# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pydosh/models/tagModel.py
# Compiled at: 2014-02-11 15:20:57
import re
from PySide import QtCore, QtGui, QtSql
from pydosh import enum, currency
from pydosh.database import db
import pydosh.pydosh_rc

class TagModel(QtSql.QSqlTableModel):
    tagsChanged = QtCore.Signal()
    selectionChanged = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(TagModel, self).__init__(parent=parent)
        self.__selectedTagNames = set()
        self.setTable('tags')
        self.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        super(TagModel, self).select()

    def setRecordFilter(self, recordIds):
        """ List of record ids to limit tag data to display
                        If no record ids are given then we still need to set
                        "0" to ensure that no record ids are matched
                """
        self.setFilter((',').join([ str(rec) for rec in recordIds or [0] ]))

    def clearSelection(self):
        for row in xrange(self.rowCount()):
            index = self.index(row, enum.kTagsColumn_TagName)
            self.setData(index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """ Handle checkstate role changes
                """
        if index.column() == enum.kTagsColumn_TagName:
            if role == QtCore.Qt.CheckStateRole:
                tagName = index.data()
                if value == QtCore.Qt.Checked:
                    if tagName in self.__selectedTagNames:
                        return False
                    self.__selectedTagNames.add(tagName)
                else:
                    if tagName not in self.__selectedTagNames:
                        return False
                    self.__selectedTagNames.remove(tagName)
                self.dataChanged.emit(index, index)
                self.selectionChanged.emit(self.__selectedTagNames)
                return True
            if role == QtCore.Qt.EditRole:
                return super(TagModel, self).setData(index, value, role)
        return False

    def data(self, item, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if item.column() == enum.kTagsColumn_RecordIds:
                tags = set([ int(i) for i in super(TagModel, self).data(item).split(',') if i ])
                return tags
            if item.column() in (enum.kTagsColumn_Amount_in, enum.kTagsColumn_Amount_out):
                amount = super(TagModel, self).data(item)
                if amount:
                    return currency.formatCurrency(amount)
                return None
        elif role == QtCore.Qt.CheckStateRole and item.column() == enum.kTagsColumn_TagName:
            if item.data() in self.__selectedTagNames:
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

        elif role == QtCore.Qt.UserRole and item.column() in (enum.kTagsColumn_Amount_in, enum.kTagsColumn_Amount_out):
            return super(TagModel, self).data(item)
        return super(TagModel, self).data(item, role)

    def flags(self, index):
        flags = super(TagModel, self).flags(index)
        if index.column() == enum.kTagsColumn_TagName:
            flags |= QtCore.Qt.ItemIsUserCheckable
        if index.column() != enum.kTagsColumn_TagName:
            flags ^= QtCore.Qt.ItemIsEditable
        return flags

    def selectStatement(self):
        if not self.tableName():
            return None
        else:
            queryFilter = self.filter()
            queryFilter = 'AND r.recordid IN (%s)' % queryFilter if queryFilter else ''
            query = "\n\t\t\t   SELECT t.tagid, t.tagname,\n\t\t\t          ARRAY_TO_STRING(ARRAY_AGG(r.recordid), ',') AS recordids,\n\t\t\t          SUM(CASE WHEN r.amount > 0 THEN r.amount ELSE 0 END) AS amount_in,\n\t\t\t          ABS(SUM(CASE WHEN r.amount < 0 THEN r.amount ELSE 0 END)) AS amount_out\n\t\t\t          FROM tags t\n\t\t\tLEFT JOIN recordtags rt ON rt.tagid=t.tagid\n\t\t\tLEFT JOIN records r ON r.recordid=rt.recordid\n\t\t\t      %s\n\t\t\t    WHERE t.userid=%d\n\t\t\t GROUP BY t.tagid\n\t\t" % (queryFilter, db.userId)
            return query

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == enum.kTagsColumn_TagName:
                return 'tag'
            if section == enum.kTagsColumn_Amount_in:
                return 'in'
            if section == enum.kTagsColumn_Amount_out:
                return 'out'
        return

    def addTag(self, tagName):
        query = QtSql.QSqlQuery()
        query.prepare('\n\t\t\tINSERT INTO tags (tagname, userid)\n\t\t\t     VALUES (?, ?)\n\t\t\t  RETURNING tagid\n\t\t')
        query.addBindValue(tagName)
        query.addBindValue(db.userId)
        if not query.exec_():
            raise Exception(query.lastError().text())
        query.next()
        insertId = query.value(0)
        self.select()
        self.tagsChanged.emit()
        return insertId

    def removeTag(self, tagId):
        currentIndex = self.index(0, enum.kTagsColumn_TagId)
        match = self.match(currentIndex, QtCore.Qt.DisplayRole, tagId, 1, QtCore.Qt.MatchExactly)
        assert match
        match = match[0]
        self.setData(self.index(match.row(), enum.kTagsColumn_TagName), QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.removeRows(match.row(), 1, QtCore.QModelIndex())
        self.select()
        self.tagsChanged.emit()

    def addRecordTags(self, tagId, recordIds):
        if not recordIds:
            return False
        currentIndex = self.index(0, enum.kTagsColumn_TagId)
        match = self.match(currentIndex, QtCore.Qt.DisplayRole, tagId, 1, QtCore.Qt.MatchExactly)
        if match:
            existingRecordsForTag = self.index(match[0].row(), enum.kTagsColumn_RecordIds).data()
            recordIds = set(recordIds) - existingRecordsForTag
        query = QtSql.QSqlQuery()
        query.prepare('\n\t\t\tINSERT INTO recordtags (recordid, tagid)\n\t\t\t     VALUES (?, ?)\n\t\t')
        query.addBindValue(list(recordIds))
        query.addBindValue([tagId] * len(recordIds))
        if not query.execBatch():
            raise Exception(query.lastError().text())
        self.tagsChanged.emit()
        return self.select()

    def removeRecordTags(self, tagId, recordIds):
        if not recordIds:
            return False
        query = QtSql.QSqlQuery('\n\t\t\tDELETE FROM recordtags\n\t\t\t      WHERE recordid in (%s)\n\t\t\t        AND tagid=%s\n\t\t\t' % ((',').join([ str(i) for i in recordIds ]), tagId))
        if query.lastError().isValid():
            raise Exception(query.lastError().text())
        self.tagsChanged.emit()
        return self.select()


class TagProxyModel(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(TagProxyModel, self).__init__(parent=parent)

    def lessThan(self, left, right):
        """ Define the comparison to ensure column data is sorted correctly
                """
        if left.column() in (enum.kTagsColumn_Amount_in, enum.kTagsColumn_Amount_out):
            return left.data(QtCore.Qt.UserRole) > right.data(QtCore.Qt.UserRole)
        return super(TagProxyModel, self).lessThan(left, right)