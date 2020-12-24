# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/liteboxview.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtGui import QPainter, QGraphicsView, QGraphicsScene, QColor, QPixmap, QGraphicsPixmapItem
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
from camelot.view.art import Pixmap

def get_desktop():
    from PyQt4.QtCore import QCoreApplication
    return QCoreApplication.instance().desktop()


def get_desktop_pixmap():
    return QPixmap.grabWindow(get_desktop().winId())


def fit_to_screen(pixmap):
    d = get_desktop()
    dh = d.height()
    dw = d.width()
    if dh < pixmap.height() or dw < pixmap.width():
        fit = 0.95
        return pixmap.scaled(dw * fit, dh * fit, Qt.KeepAspectRatio)
    return pixmap


class CloseMark(QGraphicsPixmapItem):

    def __init__(self, pixmap=None, hover_pixmap=None, parent=None):
        super(CloseMark, self).__init__(parent)
        DEFAULT_PIXMAP = Pixmap('close_mark.png').getQPixmap()
        DEFAULT_HOVER_PIXMAP = Pixmap('close_mark_hover.png').getQPixmap()
        self._pixmap = pixmap or DEFAULT_PIXMAP
        self._hover_pixmap = hover_pixmap or DEFAULT_HOVER_PIXMAP
        self.setPixmap(self._pixmap)
        width = self.pixmap().width()
        height = self.pixmap().height()
        parent_width = self.parentItem().boundingRect().width()
        self.setPos(-width / 2 + parent_width, -height / 2)
        self.setAcceptsHoverEvents(True)
        self.setZValue(10)

    def hoverEnterEvent(self, event):
        self.setPixmap(self._hover_pixmap)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setPixmap(self._pixmap)
        self.update()

    def mousePressEvent(self, event):
        view = self.scene().views()[0]
        view.close()


class LiteBoxView(QGraphicsView):
    ALPHA = QColor(0, 0, 0, 192)
    closed_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LiteBoxView, self).__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        QtGui.QShortcut(Qt.Key_Escape, self, self.close)
        self.desktopshot = None
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        return

    def close(self):
        self.closed_signal.emit()
        super(LiteBoxView, self).close()

    def drawBackground(self, painter, rect):
        if self.desktopshot is None:
            self.desktopshot = get_desktop_pixmap()
        painter.drawPixmap(self.mapToScene(0, 0), self.desktopshot)
        painter.setBrush(LiteBoxView.ALPHA)
        painter.drawRect(rect)
        return

    def show_fullscreen_svg(self, path):
        """:param path: path to an svg file"""
        from PyQt4 import QtSvg
        item = QtSvg.QGraphicsSvgItem(path)
        self.show_fullscreen_item(item)

    def show_fullscreen_pixmap(self, pixmap):
        """:param pixmap: a QPixmap"""
        item = QGraphicsPixmapItem(pixmap)
        self.show_fullscreen_item(item)

    def show_fullscreen_image(self, image):
        """:param image: a QImage"""
        pixmap = QPixmap.fromImage(image)
        self.show_fullscreen_pixmap(pixmap)

    def show_fullscreen_item(self, item):
        """:param item: a QGraphicsItem to be shown fullscreen"""
        item.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.scene.clear()
        self.scene.addItem(item)
        CloseMark(parent=item)
        self.showFullScreen()
        self.setFocus()