# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/imagedelegate.py
# Compiled at: 2013-04-11 17:47:52
from filedelegate import FileDelegate
from camelot.view.controls import editors
from camelot.view.proxy import ValueLoading
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class ImageDelegate(FileDelegate):
    """Delegate for :class:`camelot.types.Image` fields.  Expects values of type 
    :class:`camelot.core.files.storage.StoredImage`.

    .. image:: /_static/image.png
    """
    editor = editors.ImageEditor
    margin = 2

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        data = index.data(Qt.DisplayRole)
        if data not in (None, ValueLoading):
            pixmap = QtGui.QPixmap(index.data(Qt.DisplayRole))
            if pixmap.width() > 0 and pixmap.height() > 0:
                rect = option.rect
                w_margin = max(0, rect.width() - pixmap.width()) / 2 + self.margin
                h_margin = max(0, rect.height() - pixmap.height()) / 2 + self.margin
                rect = QtCore.QRect(rect.left() + w_margin, rect.top() + h_margin, rect.width() - w_margin * 2, rect.height() - h_margin * 2)
                painter.drawPixmap(rect, pixmap)
                pen = QtGui.QPen(Qt.darkGray)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawRect(rect)
        painter.restore()
        return