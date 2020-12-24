# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtviews/htmldelegate.py
# Compiled at: 2012-06-23 10:05:01
from qtalchemy import *
from PySide import QtCore, QtGui

class HTMLDelegate(QtGui.QStyledItemDelegate):

    def paint(self, painter, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ''
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter)
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        textRect = options.rect
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
        painter.restore()
        return

    def sizeHint(self, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())