# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\template_cli\template_cli\Styles\CustomTitlebar\framelesswindow.py
# Compiled at: 2019-04-15 07:08:15
# Size of source mod 2**32: 11966 bytes
"""
Module implementing FramelessWindow.
"""
import sip, os
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QRect
from PyQt5.QtGui import QIcon, QCursor, QPainter, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QApplication, QMenu, QHBoxLayout, QWidget, QMainWindow
from .Ui_framelesswindow import Ui_FramelessWindow
PADDING = 4

class FramelessWindow(QWidget, Ui_FramelessWindow):
    subUI = None

    def __init__(self, title='python', parent=None, icon=''):
        super(FramelessWindow, self).__init__(parent, Qt.FramelessWindowHint)
        self.setupUi(self)
        self._icon = icon
        self.setTitle(title)
        self.icon = icon if icon != '' else ':/button_Ima/git.ico'
        self.contentLayout = QHBoxLayout(self.windowContent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.windowTitlebar.setAttribute(Qt.WA_StyledBackground, True)
        self.restoreButton.setVisible(False)
        self.tray_icon = QIcon(self.icon)
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.tray_icon)
        self.MaxAction = QAction('最大化 ', self, triggered=(lambda : self.setWindowState(Qt.WindowMaximized)))
        self.RestoreAction = QAction('还原 ', self, triggered=(self.show))
        self.QuitAction = QAction('退出 ', self, triggered=(self.close))
        self.tray_menu = QMenu(QApplication.desktop())
        self.tray_menu.addAction(self.MaxAction)
        self.tray_menu.addAction(self.RestoreAction)
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()
        self.setMouseTracking(True)
        self.SHADOW_WIDTH = 0
        self.isLeftPressDown = False
        self.dragPosition = 0
        self.Numbers = self.enum(UP=0,
          DOWN=1,
          LEFT=2,
          RIGHT=3,
          LEFTTOP=4,
          LEFTBOTTOM=5,
          RIGHTBOTTOM=6,
          RIGHTTOP=7,
          NONE=8)
        self.dir = self.Numbers.NONE

    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())
        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()
        if tl.x() + PADDING >= x:
            if tl.x() <= x:
                if tl.y() + PADDING >= y:
                    if tl.y() <= y:
                        self.dir = self.Numbers.LEFTTOP
                        self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif x >= rb.x() - PADDING:
            if x <= rb.x():
                if y >= rb.y() - PADDING:
                    if y <= rb.y():
                        self.dir = self.Numbers.RIGHTBOTTOM
                        self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif x <= tl.x() + PADDING:
            if x >= tl.x():
                if y >= rb.y() - PADDING:
                    if y <= rb.y():
                        self.dir = self.Numbers.LEFTBOTTOM
                        self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif x <= rb.x():
            if x >= rb.x() - PADDING:
                if y >= tl.y():
                    if y <= tl.y() + PADDING:
                        self.dir = self.Numbers.RIGHTTOP
                        self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif x <= tl.x() + PADDING:
            if x >= tl.x():
                self.dir = self.Numbers.LEFT
                self.setCursor(QCursor(Qt.SizeHorCursor))
        elif x <= rb.x():
            if x >= rb.x() - PADDING:
                self.dir = self.Numbers.RIGHT
                self.setCursor(QCursor(Qt.SizeHorCursor))
        elif y >= tl.y():
            if y <= tl.y() + PADDING:
                self.dir = self.Numbers.UP
                self.setCursor(QCursor(Qt.SizeVerCursor))
        elif y <= rb.y():
            if y >= rb.y() - PADDING:
                self.dir = self.Numbers.DOWN
                self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self.dir = self.Numbers.NONE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = False
            if self.dir != self.Numbers.NONE:
                QTimer.singleShot(300, self.releaseMouse)
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isLeftPressDown = True
            if self.dir != self.Numbers.NONE:
                QTimer.singleShot(300, self.mouseGrabber)
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())
        if not self.isLeftPressDown:
            self.region(gloPoint)
        else:
            if self.dir != self.Numbers.NONE:
                rmove = QRect(tl, rb)
                if self.dir == self.Numbers.LEFT:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                else:
                    if self.dir == self.Numbers.RIGHT:
                        rmove.setWidth(gloPoint.x() - tl.x())
                    else:
                        if self.dir == self.Numbers.UP:
                            if rb.y() - gloPoint.y() <= self.minimumHeight():
                                rmove.setY(tl.y())
                            else:
                                rmove.setY(gloPoint.y())
                        else:
                            if self.dir == self.Numbers.DOWN:
                                rmove.setHeight(gloPoint.y() - tl.y())
                            else:
                                if self.dir == self.Numbers.LEFTTOP:
                                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                                        rmove.setX(tl.x())
                                    else:
                                        rmove.setX(gloPoint.x())
                                    if rb.y() - gloPoint.y() <= self.minimumHeight():
                                        rmove.setY(tl.y())
                                    else:
                                        rmove.setY(gloPoint.y())
                                else:
                                    if self.dir == self.Numbers.RIGHTTOP:
                                        rmove.setWidth(gloPoint.x() - tl.x())
                                        rmove.setY(gloPoint.y())
                                    else:
                                        if self.dir == self.Numbers.LEFTBOTTOM:
                                            rmove.setX(gloPoint.x())
                                            rmove.setHeight(gloPoint.y() - tl.y())
                                        else:
                                            if self.dir == self.Numbers.RIGHTBOTTOM:
                                                rmove.setWidth(gloPoint.x() - tl.x())
                                                rmove.setHeight(gloPoint.y() - tl.y())
                    self.setGeometry(rmove)
            else:
                try:
                    self.move(event.globalPos() - self.dragPosition)
                except:
                    pass

                event.accept()

    @pyqtSlot()
    def on_applicationStateChanged(state):
        pass

    @pyqtSlot()
    def on_windowTitlebar_doubleClicked(self):
        if self.windowState() == Qt.WindowNoState:
            self.on_maximizeButton_clicked()
        elif self.windowState() == Qt.WindowMaximized:
            self.on_restoreButton_clicked()

    @pyqtSlot()
    def on_minimizeButton_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @pyqtSlot()
    def on_restoreButton_clicked(self):
        self.restoreButton.setVisible(False)
        self.maximizeButton.setVisible(True)
        self.setWindowState(Qt.WindowNoState)

    @pyqtSlot()
    def on_maximizeButton_clicked(self):
        self.restoreButton.setVisible(True)
        self.maximizeButton.setVisible(False)
        self.setWindowState(Qt.WindowMaximized)

    @pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()
        try:
            sip.delete(self.tray)
        except:
            pass

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = self.setIcon(value)

    def setIcon(self, icon: str):
        if isinstance(icon, QIcon):
            self.titleIconBtn.setIcon(icon)
            return icon
        if isinstance(icon, str):
            icon_ico = QIcon()
            icon_ico.addPixmap(QPixmap(icon), QIcon.Normal, QIcon.Off)
            self.titleIconBtn.setIcon(icon_ico)
            return icon_ico
        raise Exception('icon need type str or QIcon')

    def setTitle(self, text):
        self.titleText.setText(text)

    def paintEvent(self, e):
        """titlebar background color """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        hexcolor = os.getenv('border_color')
        painter.setBrush(QBrush(QColor(hexcolor)))
        painter.setPen(Qt.transparent)
        rect = self.rect()
        rect.setWidth(rect.width())
        rect.setHeight(rect.height())
        painter.drawRoundedRect(rect, 4, 4)

    def setContent(self, w):
        """
        add Window to self.contentLayout

        :param w:QWidget
        :return:
        """
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)
        self.contentLayout.addWidget(w)
        self.windowContent.setLayout(self.contentLayout)
        self.subUI = w
        self.subUI.origin_enterEvent = self.subUI.enterEvent
        self.subUI.enterEvent = self.m_enterEvent

    def m_enterEvent(self, e):
        """
        redirect to MainWindow's enterEvent
        重定向到 MainWindow's enterEvent
        """
        self.dir = self.Numbers.NONE
        self.setCursor(QCursor(Qt.ArrowCursor))
        return self.subUI.origin_enterEvent(e)

    def closeEvent(self, event):
        self.setWindowFlags(Qt.Widget)
        self.tray.setVisible(False)
        sip.delete(self.tray)
        return super(QWidget, self.subUI).closeEvent(event)