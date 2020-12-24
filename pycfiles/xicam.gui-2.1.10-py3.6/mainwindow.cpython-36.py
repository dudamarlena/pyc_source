# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\windows\mainwindow.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 13827 bytes
from functools import partial
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from xicam.plugins.GUIPlugin import PanelState
from yapsy import PluginInfo
from xicam.plugins import manager as pluginmanager
from xicam.plugins import observers as pluginobservers
from xicam.core import msg
from ..widgets import defaultstage
from .settings import ConfigDialog
from ..static import path

class XicamMainWindow(QMainWindow):
    __doc__ = '\n    The Xi-cam main window. Includes layout for various panels and mechanism to position GUIPlugin contents into panels.\n    '

    def __init__(self):
        super(XicamMainWindow, self).__init__()
        self.setWindowIcon(QIcon(QPixmap(str(path('icons/xicam.gif')))))
        self.setGeometry(0, 0, 1000, 600)
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.topwidget = self.leftwidget = self.rightwidget = self.bottomwidget = self.lefttopwidget = self.righttopwidget = self.leftbottomwidget = self.rightbottomwidget = None
        self.setWindowTitle('Xi-cam')
        ConfigDialog().restore()
        pluginmanager.collectPlugins()
        self.pluginmodewidget = pluginModeWidget()
        self.pluginmodewidget.sigSetStage.connect(self.setStage)
        self.pluginmodewidget.sigSetGUIPlugin.connect(self.setGUIPlugin)
        self.addToolBar(self.pluginmodewidget)
        self.setStatusBar(QStatusBar(self))
        msg.progressbar = QProgressBar(self)
        msg.progressbar.hide()
        msg.statusbar = self.statusBar()
        self.statusBar().addPermanentWidget(msg.progressbar)
        self.setCentralWidget(QStackedWidget())
        menubar = self.menuBar()
        file = QMenu('&File', parent=menubar)
        menubar.addMenu(file)
        file.addAction('Se&ttings', (self.showSettings), shortcut=(QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_S)))
        file.addAction('E&xit', self.close)
        help = QMenu('&Help', parent=menubar)
        menubar.addMenu(help)
        self._currentGUIPlugin = None
        self.build_layout()
        if pluginmanager.getPluginsOfCategory('GUIPlugin'):
            self.populate_layout()
        fkeys = [
         Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5, Qt.Key_F6,
         Qt.Key_F7, Qt.Key_F8, Qt.Key_F9, Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]
        self.Fshortcuts = [QShortcut(QKeySequence(key), self) for key in fkeys]
        for i in range(12):
            self.Fshortcuts[i].activated.connect(partial(self.setStage, i))

        defaultstage['left'].sigOpen.connect(self.open)
        defaultstage['left'].sigOpen.connect(print)
        defaultstage['left'].sigPreview.connect(defaultstage['lefttop'].preview_header)

    def open(self, header):
        self.currentGUIPlugin.plugin_object.appendHeader(header)

    def showSettings(self):
        self._configdialog = ConfigDialog()
        self._configdialog.show()

    @Slot(int)
    def setStage(self, i: int):
        """
        Set the current Stage/Layout/Plugin mode to number i in its sequence. Triggered by menu (TODO) or F keybindings.

        Parameters
        ----------
        i   : int
        """
        plugin = self.currentGUIPlugin.plugin_object
        if i < len(plugin.stages):
            plugin.stage = list(plugin.stages.values())[i]
            self.populate_layout()

    @Slot(int)
    def setGUIPlugin(self, i: int):
        self.currentGUIPlugin = pluginmanager.getPluginsOfCategory('GUIPlugin')[i]

    @property
    def currentGUIPlugin(self) -> PluginInfo:
        return self._currentGUIPlugin

    @currentGUIPlugin.setter
    def currentGUIPlugin(self, plugininfo: PluginInfo):
        if plugininfo != self._currentGUIPlugin:
            self._currentGUIPlugin = plugininfo
            self.populate_layout()

    def build_layout(self):
        for dockwidget in self.findChildren(QDockWidget):
            if dockwidget.parent() == self:
                self.removeDockWidget(dockwidget)

        self.topwidget = QDockWidget(parent=self)
        self.leftwidget = QDockWidget(parent=self)
        self.rightwidget = QDockWidget(parent=self)
        self.bottomwidget = QDockWidget(parent=self)
        self.lefttopwidget = QDockWidget(parent=self)
        self.righttopwidget = QDockWidget(parent=self)
        self.leftbottomwidget = QDockWidget(parent=self)
        self.rightbottomwidget = QDockWidget(parent=self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.lefttopwidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.righttopwidget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.topwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftwidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightwidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottomwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftbottomwidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightbottomwidget)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

    def populate_layout(self):
        if self.currentGUIPlugin:
            stage = self.currentGUIPlugin.plugin_object.stage
        else:
            stage = defaultstage
        self.centralWidget().addWidget(stage.centerwidget)
        self.centralWidget().setCurrentWidget(stage.centerwidget)
        for position in ('top', 'left', 'right', 'bottom', 'lefttop', 'righttop', 'leftbottom',
                         'rightbottom'):
            self.populate_hidden(stage, position)
            self.populate_position(stage, position)

    def populate_hidden(self, stage, position):
        getattr(self, position + 'widget').setHidden(stage[position] == PanelState.Disabled or stage[position] == PanelState.Defaulted and defaultstage[position] == PanelState.Defaulted)

    def populate_position(self, stage, position: str):
        if isinstance(stage[position], QWidget):
            getattr(self, position + 'widget').setWidget(stage[position])
        else:
            if stage[position] == PanelState.Defaulted:
                if not defaultstage[position] == PanelState.Defaulted:
                    getattr(self, position + 'widget').setWidget(defaultstage[position])
            elif isinstance(stage[position], type):
                raise TypeError(f"A type is not acceptable value for stages. You must instance this class: {stage[position]}, {position}")

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QSpinBox):
            focused_widget.clearFocus()
        super(XicamMainWindow, self).mousePressEvent(event)


class pluginModeWidget(QToolBar):
    __doc__ = '\n    A series of styled QPushButtons with pipe characters between them. Used to switch between plugin modes.\n    '
    sigSetStage = Signal(int)
    sigSetGUIPlugin = Signal(int)

    def __init__(self):
        super(pluginModeWidget, self).__init__()
        self.GUIPluginActionGroup = QActionGroup(self)
        self.font = QFont('Zero Threes')
        self.font.setPointSize(16)
        self.setLayoutDirection(Qt.RightToLeft)
        pluginobservers.append(self)
        self.pluginsChanged()

    def pluginsChanged(self):
        self.showGUIPlugins()

    def fadeOut(self, callback, distance=-20):
        duration = 200
        self._effects = []
        for action in self.actions():
            for widget in action.associatedWidgets():
                if widget is not self:
                    a = QPropertyAnimation(widget, b'pos', widget)
                    a.setStartValue(widget.pos())
                    a.setEndValue(widget.pos() + QPoint(0, distance))
                    self._effects.append(a)
                    a.setDuration(duration)
                    a.setEasingCurve(QEasingCurve.OutBack)
                    a.start(QPropertyAnimation.DeleteWhenStopped)
                    effect = QGraphicsOpacityEffect(self)
                    widget.setGraphicsEffect(effect)
                    self._effects.append(effect)
                    b = QPropertyAnimation(effect, b'opacity')
                    self._effects.append(b)
                    b.setDuration(duration)
                    b.setStartValue(1)
                    b.setEndValue(0)
                    b.setEasingCurve(QEasingCurve.OutBack)
                    b.start(QPropertyAnimation.DeleteWhenStopped)
                    b.finished.connect(partial(self.removeAction, action))
                    b.finished.connect(callback)

        if not self.actions():
            callback()

    def fadeIn(self):
        self._effects = []
        for action in self.actions():
            effect = QGraphicsOpacityEffect(self)
            self._effects.append(effect)
            for widget in action.associatedWidgets():
                if widget is not self:
                    widget.setGraphicsEffect(effect)

            a = QPropertyAnimation(effect, b'opacity')
            self._effects.append(a)
            a.setDuration(1000)
            a.setStartValue(0)
            a.setEndValue(1)
            a.setEasingCurve(QEasingCurve.OutBack)
            a.start(QPropertyAnimation.DeleteWhenStopped)

    def showStages(self, plugin):
        self.sigSetGUIPlugin.emit(plugin)
        if len(self.parent().currentGUIPlugin.plugin_object.stages) > 1:
            names = self.parent().currentGUIPlugin.plugin_object.stages.keys()
            self.fadeOut(callback=partial((self.mkButtons), names=names, callback=(self.sigSetStage.emit), parent=(self.parent().currentGUIPlugin.name)))

    def showGUIPlugins(self):
        plugins = pluginmanager.getPluginsOfCategory('GUIPlugin')
        names = [plugin.name for plugin in plugins if hasattr(plugin, 'is_activated') if plugin.is_activated or True]
        self.fadeOut(callback=partial((self.mkButtons), names=names, callback=(self.showStages)), distance=20)

    def mkButtons(self, names, callback, parent=None):
        layout = self.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        if parent:
            action = QAction('↑', self)
            action.setFont(self.font)
            action.triggered.connect(self.showGUIPlugins)
            action.setProperty('isMode', True)
            self.addAction(action)
            label = QAction('|', self)
            label.setFont(self.font)
            label.setDisabled(True)
            self.addAction(label)
        for i, name in zip(reversed(range(len(names))), reversed(list(names))):
            action = QAction(name, self)
            action.triggered.connect(partial(callback, i))
            action.setFont(self.font)
            action.setProperty('isMode', True)
            action.setCheckable(True)
            action.setActionGroup(self.GUIPluginActionGroup)
            self.addAction(action)
            label = QAction('|', self)
            label.setFont(self.font)
            label.setDisabled(True)
            self.addAction(label)

        if self.layout().count():
            self.layout().takeAt(self.layout().count() - 1).widget().deleteLater()
        if parent:
            label = QAction('>', self)
            label.setFont(self.font)
            label.setDisabled(True)
            self.addAction(label)
            action = QAction(parent, self)
            action.setFont(self.font)
            action.setProperty('isMode', True)
            action.setDisabled(True)
            action.setActionGroup(self.GUIPluginActionGroup)
            self.addAction(action)
        self.fadeIn()