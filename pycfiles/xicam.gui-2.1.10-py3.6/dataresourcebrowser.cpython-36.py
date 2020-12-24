# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\widgets\dataresourcebrowser.py
# Compiled at: 2018-05-17 17:08:05
# Size of source mod 2**32: 10646 bytes
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from ..clientonlymodels.LocalFileSystemResource import LocalFileSystemResourcePlugin
from xicam.gui.static import path
from xicam.core.data import NonDBHeader
from xicam.plugins import manager as pluginmanager
from xicam.plugins.DataResourcePlugin import DataSourceListModel
from .searchlineedit import SearchLineEdit
from urllib import parse
from pathlib import Path
from functools import partial
import os, webbrowser
from xicam.gui.widgets.tabview import ContextMenuTabBar

class BrowserTabWidget(QTabWidget):

    def __init__(self, parent=None):
        super(BrowserTabWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)


class DataBrowser(QWidget):
    sigOpen = Signal(NonDBHeader)
    sigPreview = Signal(NonDBHeader)

    def __init__(self, browserview):
        super(DataBrowser, self).__init__()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.browserview = browserview
        self.browserview.sigOpen.connect(self.sigOpen)
        self.browserview.sigPreview.connect(self.sigPreview)
        self.browserview.sigOpenExternally.connect(self.openExternally)
        self.browserview.sigURIChanged.connect(self.uri_to_text)
        self.toolbar = QToolBar()
        self.toolbar.addAction(QIcon(QPixmap(str(path('icons/up.png')))), 'Move up directory', self.moveUp)
        self.toolbar.addAction(QIcon(QPixmap(str(path('icons/refresh.png')))), 'Refresh', self.hardRefreshURI)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.URILineEdit = SearchLineEdit('', clearable=False)
        self.uri_to_text()
        hbox.addWidget(self.toolbar)
        hbox.addWidget(self.URILineEdit)
        vbox.addLayout(hbox)
        vbox.addWidget(self.browserview)
        self.setLayout(vbox)
        self.URILineEdit.textChanged.connect(self.softRefreshURI)
        self.URILineEdit.returnPressed.connect(self.softRefreshURI)
        self.URILineEdit.focusOutEvent = self.softRefreshURI
        self.hardRefreshURI()

    def text_to_uri(self):
        uri = parse.urlparse(self.URILineEdit.text())
        self.browserview.model.uri = uri
        print('uri:', uri)
        return uri

    def uri_to_text(self):
        uri = self.browserview.model.uri
        text = parse.urlunparse(uri)
        self.URILineEdit.setText(text)
        return text

    def hardRefreshURI(self, *_, **__):
        self.text_to_uri()
        self.browserview.refresh()

    def moveUp(self):
        self.browserview.model.uri = parse.urlparse(str(Path(self.URILineEdit.text()).parent))
        self.browserview.refresh()
        self.uri_to_text()

    def openExternally(self, uri):
        webbrowser.open(uri)

    softRefreshURI = hardRefreshURI


class BrowserTabBar(ContextMenuTabBar):
    sigAddBrowser = Signal(DataBrowser, str)

    def __init__(self, tabwidget):
        super(BrowserTabBar, self).__init__()
        self.tabwidget = tabwidget
        self.tabwidget.setTabBar(self)
        self.setExpanding(False)
        self.setTabsClosable(True)
        plusPixmap = QPixmap(str(path('icons/plus.png')))
        self.plusIcon = QIcon(plusPixmap)
        tab = self.addTab(self.plusIcon, '')
        try:
            self.tabButton(tab, QTabBar.RightSide).resize(0, 0)
            self.tabButton(tab, QTabBar.RightSide).hide()
        except AttributeError:
            self.tabButton(tab, QTabBar.LeftSide).resize(0, 0)
            self.tabButton(tab, QTabBar.LeftSide).hide()

        self.currentChanged.connect(self.tabwidget.setCurrentIndex)
        self.installEventFilter(self)

    def addTab(self, *args, **kwargs):
        return (self.insertTab)(self.count() - 1, *args, **kwargs)

    def eventFilter(self, object, event):
        try:
            if object == self:
                if event.type() in [QEvent.MouseButtonPress,
                 QEvent.MouseButtonRelease]:
                    if event.button() == Qt.LeftButton:
                        if event.type() == QEvent.MouseButtonPress:
                            tabIndex = object.tabAt(event.pos())
                            if tabIndex == self.count() - 1:
                                self.showMenu(self.mapToGlobal(event.pos()))
                                return True
            return False
        except Exception as e:
            print('Exception raised in eventfilter', e)

    def showMenu(self, pos):
        self.menu = QMenu()
        self.actions = {}
        for plugin in pluginmanager.getPluginsOfCategory('DataResourcePlugin'):
            self.actions[plugin.name] = QAction(plugin.name)
            self.actions[plugin.name].triggered.connect(partial(self._addBrowser, plugin))
            self.menu.addAction(self.actions[plugin.name])

        self.menu.popup(pos)

    def _addBrowser(self, plugin):
        self.sigAddBrowser.emit(DataBrowser(DataResourceList(DataSourceListModel(plugin.plugin_object))), plugin.name)


class DataResourceView(QObject):

    def __init__(self, model):
        super(DataResourceView, self).__init__()
        self.model = model
        self.setModel(self.model)
        self.doubleClicked.connect(self.open)
        self.setSelectionMode(self.ExtendedSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuRequested)
        self.menu = QMenu()
        standardActions = [QAction('Open', self),
         QAction('Open Externally', self),
         QAction('Enable/Disable Streaming', self),
         QAction('Delete', self)]
        self.menu.addActions(standardActions)
        standardActions[0].triggered.connect(self.open)
        standardActions[1].triggered.connect(self.openExternally)

    def menuRequested(self, position):
        self.menu.exec_(self.viewport().mapToGlobal(position))

    def open(self, index):
        pass

    def currentChanged(self, current, previous):
        pass

    def openExternally(self, uri: str):
        pass


class DataResourceTree(QTreeView, DataResourceView):
    sigOpen = Signal(NonDBHeader)
    sigOpenPath = Signal(str)
    sigOpenExternally = Signal(str)
    sigPreview = Signal(NonDBHeader)
    sigURIChanged = Signal()

    def __init__(self, *args):
        (super(DataResourceTree, self).__init__)(*args)

    def refresh(self):
        self.model.refresh()
        self.setRootIndex(self.model.index(self.model.path))


class DataResourceList(QListView, DataResourceView):
    sigOpen = Signal(NonDBHeader)
    sigOpenPath = Signal(str)
    sigOpenExternally = Signal(str)
    sigPreview = Signal(NonDBHeader)
    sigURIChanged = Signal()

    def refresh(self):
        self.model.refresh()


class LocalFileSystemTree(DataResourceTree):

    def __init__(self):
        self.model = LocalFileSystemResourcePlugin()
        super(LocalFileSystemTree, self).__init__(self.model)

    def open(self, _):
        indexes = self.selectionModel().selectedRows()
        if len(indexes) == 1:
            path = self.model.filePath(indexes[0])
            if os.path.isdir(path):
                self.model.path = path
                self.setRootIndex(indexes[0])
                self.sigURIChanged.emit()
                return
        self.sigOpen.emit(self.model.getHeader(indexes))

    def currentChanged(self, current, previous):
        if current.isValid():
            self.sigPreview.emit(self.model.getHeader([current]))

    def openExternally(self, uri: str):
        indexes = self.selectionModel().selectedRows()
        for index in indexes:
            self.sigOpenExternally.emit(self.model.filePath(index))


class DataResourceBrowser(QWidget):
    sigOpen = Signal(NonDBHeader)
    sigPreview = Signal(NonDBHeader)

    def __init__(self):
        super(DataResourceBrowser, self).__init__()
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(QSize(250, 400))
        self.browsertabwidget = BrowserTabWidget(self)
        self.browsertabbar = BrowserTabBar(self.browsertabwidget)
        self.browsertabbar.sigAddBrowser.connect(self.addBrowser)
        self.browsertabbar.tabCloseRequested.connect(self.closetab)
        self.addBrowser((DataBrowser(LocalFileSystemTree())), 'Local', closable=False)
        self.browsertabbar.setCurrentIndex(0)
        vbox.addWidget(self.browsertabwidget)
        self.setLayout(vbox)
        self.sigOpen.connect(print)

    def closetab(self, i):
        if hasattr(self.browsertabwidget.widget(i), 'closable'):
            if self.browsertabwidget.widget(i).closable:
                self.browsertabwidget.removeTab(i)

    def sizeHint(self):
        return QSize(250, 400)

    def addBrowser(self, databrowser: DataBrowser, text: str, closable: bool=True):
        databrowser.sigOpen.connect(self.sigOpen)
        databrowser.sigPreview.connect(self.sigPreview)
        databrowser.closable = closable
        tab = self.browsertabwidget.addTab(databrowser, text)
        if closable is False:
            try:
                self.browsertabbar.tabButton(tab, QTabBar.RightSide).resize(0, 0)
                self.browsertabbar.tabButton(tab, QTabBar.RightSide).hide()
            except AttributeError:
                self.browsertabbar.tabButton(tab, QTabBar.LeftSide).resize(0, 0)
                self.browsertabbar.tabButton(tab, QTabBar.LeftSide).hide()