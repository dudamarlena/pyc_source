# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/container/taurusmainwindow.py
# Compiled at: 2019-08-19 15:09:29
"""
mainwindow.py: a main window implementation with many added features by default
"""
from __future__ import absolute_import
from builtins import str
import os, sys
from functools import partial
from future.utils import string_types
from taurus import tauruscustomsettings
from taurus.core.util import deprecation_decorator
from taurus.external.qt import Qt, compat
from .taurusbasecontainer import TaurusBaseContainer
from taurus.qt.qtcore.configuration import BaseConfigurableClass
from taurus.qt.qtgui.util import ExternalAppAction
from taurus.qt.qtgui.dialog import protectTaurusMessageBox
__all__ = [
 'TaurusMainWindow']
__docformat__ = 'restructuredtext'

class CommandArgsLineEdit(Qt.QLineEdit):
    """ An specialized QLineEdit that can transform its text from/to command argument lists"""

    def __init__(self, extapp, *args):
        Qt.QLineEdit.__init__(self, *args)
        self._extapp = extapp
        self.textEdited.connect(self.setCmdText)

    def setCmdText(self, cmdargs):
        if not isinstance(cmdargs, string_types):
            cmdargs = (' ').join(cmdargs)
        self.setText(cmdargs)
        self._extapp.setCmdArgs(self.getCmdArgs(), False)

    def getCmdArgs(self):
        import shlex
        return shlex.split(str(self.text()))


class ConfigurationDialog(Qt.QDialog, BaseConfigurableClass):
    """ A Configuration Dialog"""

    def __init__(self, parent):
        Qt.QDialog.__init__(self, parent)
        BaseConfigurableClass.__init__(self)
        self._tabwidget = Qt.QTabWidget()
        self.setModal(True)
        self.externalAppsPage = None
        self.setLayout(Qt.QVBoxLayout())
        self.layout().addWidget(self._tabwidget)
        return

    def addExternalAppConfig(self, extapp):
        """
        Creates an entry in the "External Apps" tab of the configuration dialog

        :param extapp: (ExternalAppAction) the external application that is to
                       be included in the configuration menu.
        """
        if self.externalAppsPage is None:
            self.externalAppsPage = Qt.QScrollArea()
            w = Qt.QWidget()
            w.setLayout(Qt.QFormLayout())
            self.externalAppsPage.setWidget(w)
            self.externalAppsPage.setWidgetResizable(True)
            self._tabwidget.addTab(self.externalAppsPage, 'External Application Paths')
        label = 'Command line for %s' % str(extapp.text())
        editWidget = CommandArgsLineEdit(extapp, (' ').join(extapp.cmdArgs()))
        self.externalAppsPage.widget().layout().addRow(label, editWidget)
        extapp.cmdArgsChanged.connect(editWidget.setCmdText)
        return

    def deleteExternalAppConfig(self, extapp):
        """Remove the given external application configuration from
        the "External Apps" tab of the configuration dialog

        :param extapp: (ExternalAppAction) the external application that is to
                       be included in the configuration menu.
        """
        from taurus.external.qt import Qt
        layout = self.externalAppsPage.widget().layout()
        for cnt in reversed(range(layout.count())):
            widget = layout.itemAt(cnt).widget()
            if widget is not None:
                text = str(widget.text())
                if isinstance(widget, Qt.QLabel):
                    dialog_text = 'Command line for %s' % str(extapp.text())
                    if text == dialog_text:
                        layout.removeWidget(widget)
                        widget.close()
                else:
                    cmdargs = (' ').join(extapp.cmdArgs())
                    if text == cmdargs:
                        layout.removeWidget(widget)
                        widget.close()

        return

    def show(self):
        """ calls :meth:`Qt.QDialog.show` only if there is something to configure"""
        if self._tabwidget.count():
            Qt.QDialog.show(self)


class Rpdb2Thread(Qt.QThread):

    def run(self):
        dialog = Rpdb2WaitDialog(parent=self.parent())
        dialog.exec_()


class Rpdb2WaitDialog(Qt.QMessageBox):

    def __init__(self, title=None, text=None, parent=None):
        if text is None:
            text = 'Waitting for a debugger console to attach...'
        if title is None:
            title = 'Rpdb2 waitting...'
        Qt.QMessageBox.__init__(self)
        self.addButton(Qt.QMessageBox.Ok)
        self.setWindowTitle(title)
        self.setText(text)
        self.button(Qt.QMessageBox.Ok).setEnabled(False)
        parent.rpdb2Started.connect(self.onStarted)
        return

    def onStarted(self):
        self.setWindowTitle('Rpdb2 running!')
        self.setText('A rpdb2 debugger was started successfully!')
        self.button(Qt.QMessageBox.Ok).setEnabled(True)


class TaurusMainWindow(Qt.QMainWindow, TaurusBaseContainer):
    """
    A Taurus-aware QMainWindow with several customizations:

        - It takes care of (re)storing its geometry and state (see :meth:`loadSettings`)
        - Supports perspectives (programmatic access and, optionally,
          accessible by user), and allows defining a set of "factory settings"
        - It provides a customizable splashScreen (optional)
        - Supports spawning remote consoles and remote debugging
        - Supports full-screen mode toggling
        - Supports adding launchers to external applications
        - It provides a statusBar with an optional heart-beat LED
        - The following Menus are optionally provided and populated with basic actions:
            - File  (accessible by derived classes  as `self.fileMenu`)
            - View (accessible by derived classes  as `self.viewMenu`)
            - Taurus (accessible by derived classes  as `self.taurusMenu`)
            - Tools (accessible by derived classes  as `self.toolsMenu`)
            - Help (accessible by derived classes  as `self.helpMenu`)

    """
    modelChanged = Qt.pyqtSignal('const QString &')
    perspectiveChanged = Qt.pyqtSignal('QString')
    HEARTBEAT = 1500
    FILE_MENU_ENABLED = True
    VIEW_MENU_ENABLED = True
    TAURUS_MENU_ENABLED = True
    TOOLS_MENU_ENABLED = True
    HELP_MENU_ENABLED = True
    FULLSCREEN_TOOLBAR_ENABLED = True
    USER_PERSPECTIVES_ENABLED = True
    LOGGER_WIDGET_ENABLED = True
    SPLASH_LOGO_NAME = 'large:TaurusSplash.png'
    SPLASH_MESSAGE = 'Initializing Main window...'
    _old_options_api = {'_heartbeat': 'HEARTBEAT', 
       '_showFileMenu': 'FILE_MENU_ENABLED', 
       '_showViewMenu': 'VIEW_MENU_ENABLED', 
       '_showTaurusMenu': 'TAURUS_MENU_ENABLED', 
       '_showToolsMenu': 'TOOLS_MENU_ENABLED', 
       '_showHelpMenu': 'HELP_MENU_ENABLED', 
       '_showLogger': 'LOGGER_WIDGET_ENABLED', 
       '_supportUserPerspectives': 'USER_PERSPECTIVES_ENABLED', 
       '_splashLogo': 'SPLASH_LOGO_NAME', 
       '_splashMessage': 'SPLASH_MESSAGE'}

    def __init__(self, parent=None, designMode=False, splash=None):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QMainWindow, parent)
        self.call__init__(TaurusBaseContainer, name, designMode=designMode)
        for old, new in self._old_options_api.items():
            if hasattr(self, old):
                self.deprecated(dep=old, alt=new, rel='4.5.3a')
                setattr(self, new, getattr(self, old))

        if splash is None:
            splash = bool(self.SPLASH_LOGO_NAME)
        self.__splashScreen = None
        if splash and not designMode:
            self.__splashScreen = Qt.QSplashScreen(Qt.QPixmap(self.SPLASH_LOGO_NAME))
            self.__splashScreen.show()
            self.__splashScreen.showMessage(self.SPLASH_MESSAGE)
        self.__tangoHost = ''
        self.__settings = None
        self.extAppsBar = None
        self.helpManualDW = None
        self.helpManualBrowser = None
        if self.HELP_MENU_ENABLED:
            self.resetHelpManualURI()
        if self.HEARTBEAT is not None:
            from taurus.qt.qtgui.display import QLed
            self.heartbeatLed = QLed()
            self.heartbeatLed.setToolTip('Heartbeat: if it does not blink, the application is hung')
            self.statusBar().addPermanentWidget(self.heartbeatLed)
            self.resetHeartbeat()
        self.configurationDialog = ConfigurationDialog(self)
        self.__createActions()
        if self.LOGGER_WIDGET_ENABLED:
            self.addLoggerWidget()
        if self.FILE_MENU_ENABLED:
            self.createFileMenu()
        if self.VIEW_MENU_ENABLED:
            self.createViewMenu()
        if self.TAURUS_MENU_ENABLED:
            self.createTaurusMenu()
        if self.TOOLS_MENU_ENABLED:
            self.createToolsMenu()
        if self.HELP_MENU_ENABLED:
            self.createHelpMenu()
        if self.FULLSCREEN_TOOLBAR_ENABLED:
            self.viewToolBar = self.addToolBar('View')
            self.viewToolBar.setObjectName('viewToolBar')
            self.viewToolBar.addAction(self.toggleFullScreenAction)
        if self.USER_PERSPECTIVES_ENABLED:
            self.createPerspectivesToolBar()
        self.configurationAction.setEnabled(self.configurationDialog._tabwidget.count())
        return

    def __setattr__(self, key, value):
        super(TaurusMainWindow, self).__setattr__(key, value)
        if key in self._old_options_api:
            new = self._old_options_api[key]
            setattr(self, new, value)
            self.deprecated(dep=key, alt=new, rel='4.5.3a')

    def contextMenuEvent(self, event):
        """Reimplemented to avoid deprecation warning related to:
        https://github.com/taurus-org/taurus/issues/905
        """
        event.ignore()

    def addLoggerWidget(self, hidden=True):
        """adds a QLoggingWidget as a dockwidget of the main window (and hides it by default)"""
        from taurus.qt.qtgui.table import QLoggingWidget
        loggingWidget = QLoggingWidget()
        self.__loggerDW = Qt.QDockWidget('Taurus logs', self)
        self.__loggerDW.setWidget(loggingWidget)
        self.__loggerDW.setObjectName('loggerDW')
        self.addDockWidget(Qt.Qt.BottomDockWidgetArea, self.__loggerDW)
        if hidden:
            self.__loggerDW.hide()

    def createFileMenu(self):
        """adds a "File" Menu"""
        self.fileMenu = self.menuBar().addMenu('File')
        if self.USER_PERSPECTIVES_ENABLED:
            self.fileMenu.addAction(self.importSettingsFileAction)
            self.fileMenu.addAction(self.exportSettingsFileAction)
            self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitApplicationAction)

    def createViewMenu(self):
        """adds a "View" Menu"""
        self.viewMenu = self.menuBar().addMenu('View')
        if self.LOGGER_WIDGET_ENABLED:
            self.viewMenu.addAction(self.__loggerDW.toggleViewAction())
        self.viewToolBarsMenu = self.viewMenu.addMenu('Tool Bars')
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.toggleFullScreenAction)
        if self.USER_PERSPECTIVES_ENABLED:
            self.viewMenu.addSeparator()
            self.perspectivesMenu = Qt.QMenu('Load Perspectives', self)
            self.viewMenu.addMenu(self.perspectivesMenu)
            self.viewMenu.addAction(self.savePerspectiveAction)
            self.viewMenu.addAction(self.deletePerspectiveAction)

    def createTaurusMenu(self):
        """adds a "Taurus" Menu"""
        self.taurusMenu = self.menuBar().addMenu('Taurus')
        self.taurusMenu.addAction(self.changeTangoHostAction)

    def createToolsMenu(self):
        """adds a "Tools" Menu"""
        self.toolsMenu = self.menuBar().addMenu('Tools')
        self.externalAppsMenu = self.toolsMenu.addMenu('External Applications')
        self.toolsMenu.addAction(self.configurationAction)

    def createHelpMenu(self):
        """adds a "Help" Menu"""
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction('About ...', self.showHelpAbout)
        self.helpMenu.addAction(Qt.QIcon.fromTheme('help-browser'), 'Manual', self.onShowManual)

    def createPerspectivesToolBar(self):
        """adds a Perspectives ToolBar"""
        self.perspectivesToolBar = self.addToolBar('Perspectives')
        self.perspectivesToolBar.setObjectName('perspectivesToolBar')
        pbutton = Qt.QToolButton()
        if not hasattr(self, 'perspectivesMenu'):
            self.perspectivesMenu = Qt.QMenu('Load Perspectives', self)
        self.perspectivesMenu.setIcon(Qt.QIcon.fromTheme('document-open'))
        pbutton.setToolTip('Load Perspectives')
        pbutton.setText('Load Perspectives')
        pbutton.setPopupMode(Qt.QToolButton.InstantPopup)
        pbutton.setMenu(self.perspectivesMenu)
        self.perspectivesToolBar.addWidget(pbutton)
        self.perspectivesToolBar.addAction(self.savePerspectiveAction)
        if self.VIEW_MENU_ENABLED:
            self.viewToolBarsMenu.addAction(self.perspectivesToolBar.toggleViewAction())

    def updatePerspectivesMenu(self):
        """re-checks the perspectives available to update self.perspectivesMenu

        .. note:: This method may need be called by derived classes at the end
                  of their initialization.

        :return: (QMenu) the updated perspectives menu (or None if
                 self.USER_PERSPECTIVES_ENABLED is False)
        """
        if not self.USER_PERSPECTIVES_ENABLED:
            return None
        else:
            self.perspectivesMenu.clear()
            for pname in self.getPerspectivesList():
                a = self.perspectivesMenu.addAction(pname, self.__onPerspectiveSelected)
                a.perspective_name = pname

            return self.perspectivesMenu

    def __onPerspectiveSelected(self):
        """slot to be called by the actions in the perspectivesMenu"""
        pname = self.sender().perspective_name
        self.loadPerspective(name=pname)

    def splashScreen(self):
        """returns a the splashScreen

        :return: (QSplashScreen)
        """
        return self.__splashScreen

    def basicTaurusToolbar(self):
        """returns a QToolBar with few basic buttons (most important, the logo)

        :return: (QToolBar)
        """
        tb = Qt.QToolBar('Taurus Toolbar')
        tb.setObjectName('Taurus Toolbar')
        logo = getattr(tauruscustomsettings, 'ORGANIZATION_LOGO', 'logos:taurus.png')
        tb.addAction(Qt.QIcon(logo), Qt.qApp.organizationName())
        tb.setIconSize(Qt.QSize(50, 50))
        return tb

    def __createActions(self):
        """initializes the application-wide actions"""
        self.quitApplicationAction = Qt.QAction(Qt.QIcon.fromTheme('process-stop'), 'Exit Application', self)
        self.quitApplicationAction.triggered.connect(self.close)
        self.changeTangoHostAction = Qt.QAction(Qt.QIcon.fromTheme('network-server'), 'Change Tango Host ...', self)
        self.changeTangoHostAction.triggered.connect(self._onChangeTangoHostAction)
        self.changeTangoHostAction.setVisible(False)
        self.loadPerspectiveAction = Qt.QAction(Qt.QIcon.fromTheme('document-open'), 'Load Perspective ...', self)
        self.loadPerspectiveAction.triggered.connect(partial(self.loadPerspective, name=None, settings=None))
        self.savePerspectiveAction = Qt.QAction(Qt.QIcon.fromTheme('document-save'), 'Save Perspective ...', self)
        self.savePerspectiveAction.triggered.connect(partial(self.savePerspective, name=None))
        self.deletePerspectiveAction = Qt.QAction(Qt.QIcon('actions:edit-delete.svg'), 'Delete Perspective ...', self)
        self.deletePerspectiveAction.triggered.connect(partial(self.removePerspective, name=None, settings=None))
        self.exportSettingsFileAction = Qt.QAction(Qt.QIcon.fromTheme('document-save'), 'Export Settings ...', self)
        self.exportSettingsFileAction.triggered.connect(partial(self.exportSettingsFile, fname=None))
        self.importSettingsFileAction = Qt.QAction(Qt.QIcon.fromTheme('document-open'), 'Import Settings ...', self)
        self.importSettingsFileAction.triggered.connect(partial(self.importSettingsFile, fname=None))
        self.configurationAction = Qt.QAction(Qt.QIcon.fromTheme('preferences-system'), 'Configurations ...', self)
        self.configurationAction.triggered.connect(self.configurationDialog.show)
        self.spawnRpdb2Shortcut = Qt.QShortcut(self)
        self.spawnRpdb2Shortcut.setKey(Qt.QKeySequence(Qt.Qt.Key_F9))
        self.spawnRpdb2Shortcut.activated.connect(self._onSpawnRpdb2)
        self.spawnRpdb2Shortcut = Qt.QShortcut(self)
        rpdb2key = Qt.QKeySequence(Qt.Qt.CTRL + Qt.Qt.ALT + Qt.Qt.Key_0, Qt.Qt.Key_1)
        self.spawnRpdb2Shortcut.setKey(rpdb2key)
        self.spawnRpdb2Shortcut.activated.connect(self._onSpawnRpdb2)
        self.spawnRConsoleShortcut = Qt.QShortcut(self)
        rconsolekey = Qt.QKeySequence(Qt.Qt.CTRL + Qt.Qt.ALT + Qt.Qt.Key_0, Qt.Qt.Key_2)
        self.spawnRConsoleShortcut.setKey(rconsolekey)
        self.spawnRConsoleShortcut.activated.connect(self._onSpawnRConsole)
        self.toggleFullScreenAction = Qt.QAction(Qt.QIcon('actions:view-fullscreen.svg'), 'Show FullScreen', self)
        self.toggleFullScreenAction.setCheckable(True)
        self.toggleFullScreenAction.toggled.connect(self._onToggleFullScreen)
        self.fullScreenShortcut = Qt.QShortcut(self)
        self.fullScreenShortcut.setKey(Qt.QKeySequence(Qt.Qt.Key_F11))
        self.fullScreenShortcut.activated.connect(self._onToggleFullScreen)
        return

    @protectTaurusMessageBox
    def _onSpawnRpdb2(self):
        try:
            import rpdb2
        except ImportError:
            Qt.QMessageBox.warning(self, 'Rpdb2 not installed', 'Cannot spawn debugger: Rpdb2 is not installed on your system.')
            return

        if hasattr(self, '_rpdb2'):
            Qt.QMessageBox.information(self, 'Rpdb2 running', 'A rpdb2 debugger is already started')
            return
        pwd, ok = Qt.QInputDialog.getText(self, 'Rpdb2 password', 'Password:', Qt.QLineEdit.Password)
        if not ok:
            return
        Qt.QMessageBox.warning(self, 'Rpdb2 freeze', 'The application will freeze until a debugger attaches.')
        self._rpdb2 = rpdb2.start_embedded_debugger(str(pwd))
        Qt.QMessageBox.information(self, 'Rpdb2 running', 'rpdb2 debugger started successfully!')

    @protectTaurusMessageBox
    def _onSpawnRConsole(self):
        try:
            import rfoo.utils.rconsole
        except ImportError:
            Qt.QMessageBox.warning(self, 'rfoo not installed', 'Cannot spawn debugger: rfoo is not installed on your system.')
            return

        if hasattr(self, '_rconsole_port'):
            Qt.QMessageBox.information(self, 'rconsole running', 'A rconsole is already running on port %d' % self._rconsole_port)
            return
        port, ok = Qt.QInputDialog.getInteger(self, 'rconsole port', 'Port:', rfoo.utils.rconsole.PORT, 0, 65535)
        if not ok:
            return
        rfoo.utils.rconsole.spawn_server(port=port)
        self._rconsole_port = port
        Qt.QMessageBox.information(self, 'Rpdb2 running', '<html>rconsole started successfully!<br>Type:<p><b>rconsole -p %d</b></p>to connect to it' % port)

    def _onToggleFullScreen(self, yesno=None):
        if self.isFullScreen():
            self.showNormal()
            self._toggleToolBarsAndMenu(True)
        else:
            self._toggleToolBarsAndMenu(False)
            self.showFullScreen()

    def _toggleToolBarsAndMenu(self, visible, toolBarAreas=Qt.Qt.TopToolBarArea):
        for toolbar in self.findChildren(Qt.QToolBar):
            if bool(self.toolBarArea(toolbar) & toolBarAreas):
                toolbar.setVisible(visible)

    def setQSettings(self, settings):
        """sets the main window settings object

        :param settings: (QSettings or None)

        .. seealso:: :meth:`getQSettings`
        """
        self.__settings = settings

    def resetQSettings(self):
        """equivalent to setQSettings(None) """
        self.setQSettings(None)
        return

    def getQSettings(self):
        """Returns the main window settings object.
        If it was not previously set, it will create a new QSettings object
        following the Taurus convention i.e., it using Ini format and userScope)

        :return: (QSettings) the main window QSettings object
        """
        if self.__settings is None:
            self.__settings = self.newQSettings()
        return self.__settings

    def newQSettings(self):
        """Returns a settings taurus-specific QSettings object.
        The returned QSettings object will comply with the Taurus defaults for
        storing application settings (i.e., it uses Ini format and userScope)

        :return: (QSettings) a taurus-specific QSettings object
        """
        format = Qt.QSettings.IniFormat
        scope = Qt.QSettings.UserScope
        appname = Qt.QApplication.applicationName()
        orgname = Qt.QApplication.organizationName()
        return Qt.QSettings(format, scope, orgname, appname)

    def getFactorySettingsFileName(self):
        """returns the file name of the "factory settings" (the ini file with default settings).
        The default implementation returns "<path>/<appname>.ini", where <path>
        is the path of the module where the main window class is defined and
        <appname> is the application name (as obtained from QApplication).

        :return: (str) the absolute file name.
        """
        root, tail = os.path.split(os.path.abspath(sys.modules[self.__module__].__file__))
        basename = '%s.ini' % str(Qt.qApp.applicationName())
        return os.path.join(root, basename)

    def loadSettings(self, settings=None, group=None, ignoreGeometry=False, factorySettingsFileName=None):
        """restores the application settings previously saved with :meth:`saveSettings`.

        .. note:: This method should be called explicitly from derived classes after all
                  initialization is done

        :param settings: (QSettings or None) a QSettings object. If None given,
                         the default one returned by :meth:`getQSettings` will
                         be used
        :param group: (str) a prefix that will be added to the keys to be
                       loaded (no prefix by default)
        :param ignoreGeometry: (bool) if True, the geometry of the MainWindow
                               won't be restored
        :param factorySettingsFileName: (str) file name of a ini file containing the default
                                        settings to be used as a fallback in
                                        case the settings file is not found
                                        (e.g., the first time the application is
                                        launched after installation)
        """
        if settings is None:
            settings = self.getQSettings()
            if len(settings.allKeys()) == 0:
                fname = factorySettingsFileName or self.getFactorySettingsFileName()
                if os.path.exists(fname):
                    self.info('Importing factory settings from "%s"' % fname)
                    self.importSettingsFile(fname)
                return
        if group is not None:
            settings.beginGroup(group)
        if not ignoreGeometry:
            ba = settings.value('MainWindow/Geometry') or Qt.QByteArray()
            self.restoreGeometry(ba)
        try:
            ba = settings.value('TaurusConfig') or Qt.QByteArray()
            self.applyQConfig(ba)
        except Exception as e:
            msg = ('Problem loading configuration from "{}". ' + 'Some settings may not be restored.\n' + ' Reason: {}').format(str(settings.fileName()), e)
            self.error(msg)
            Qt.QMessageBox.warning(self, 'Error Loading settings', msg, Qt.QMessageBox.Ok)

        ba = settings.value('MainWindow/State') or Qt.QByteArray()
        self.restoreState(ba)
        dockwidgets = [ c for c in self.children() if isinstance(c, Qt.QDockWidget)
                      ]
        for d in dockwidgets:
            r = self.restoreDockWidget(d)
            d.hide()

        ba = settings.value('MainWindow/State') or Qt.QByteArray()
        self.restoreState(ba)
        if group is not None:
            settings.endGroup()
        self.updatePerspectivesMenu()
        self.info('MainWindow settings restored')
        return

    def saveSettings(self, group=None):
        """saves the application settings (so that they can be restored with :meth:`loadSettings`)

        .. note:: this method is automatically called by default when closing the
                  window, so in general there is no need to call it from derived classes

        :param group: (str) a prefix that will be added to the keys to be
                       saved (no prefix by default)
        """
        settings = self.getQSettings()
        if not settings.isWritable():
            self.info('Settings cannot be saved in "%s"', settings.fileName())
            return
        else:
            if group is not None:
                settings.beginGroup(group)
            settings.setValue('MainWindow/State', self.saveState())
            settings.setValue('MainWindow/Geometry', self.saveGeometry())
            settings.setValue('TaurusConfig', self.createQConfig())
            if group is not None:
                settings.endGroup()
            self.info('Settings saved in "%s"' % settings.fileName())
            return

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def savePerspective(self, name=None):
        """Stores current state of the application as a perspective with the given name

        :param name: (str) name of the perspective
        """
        perspectives = self.getPerspectivesList()
        if name is None:
            name, ok = Qt.QInputDialog.getItem(self, 'Save Perspective', 'Store current settings as the following perspective:', perspectives, 0, True)
            if not ok:
                return
        if name in perspectives:
            ans = Qt.QMessageBox.question(self, 'Overwrite perspective?', 'overwrite existing perspective %s?' % str(name), Qt.QMessageBox.Yes, Qt.QMessageBox.No)
            if ans != Qt.QMessageBox.Yes:
                return
        self.saveSettings(group='Perspectives/%s' % name)
        self.updatePerspectivesMenu()
        return

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def loadPerspective(self, name=None, settings=None):
        """Loads the settings saved for the given perspective.
        It emits a 'perspectiveChanged' signal with name as its parameter

        :param name: (str) name of the perspective
        :param settings: (QSettings or None) a QSettings object. If None given,
                         the default one returned by :meth:`getQSettings` will
                         be used
        """
        if name is None:
            perspectives = self.getPerspectivesList()
            if len(perspectives) == 0:
                return
            name, ok = Qt.QInputDialog.getItem(self, 'Load Perspective', 'Change perspective to:', perspectives, 0, False)
            if not ok:
                return
        self.loadSettings(settings=settings, group='Perspectives/%s' % name, ignoreGeometry=True)
        self.perspectiveChanged.emit(name)
        return

    def getPerspectivesList(self, settings=None):
        """Returns the list of saved perspectives

        :param settings: (QSettings or None) a QSettings object. If None given,
                         the default one returned by :meth:`getQSettings` will
                         be used

        :return: (QStringList) the list of the names of the currently saved
                 perspectives
        """
        if settings is None:
            settings = self.getQSettings()
        settings.beginGroup('Perspectives')
        names = settings.childGroups()
        settings.endGroup()
        return names

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def removePerspective(self, name=None, settings=None):
        """removes the given perspective from the settings

        :param name: (str) name of the perspective
        :param settings: (QSettings or None) a QSettings object. If None given,
                         the default one returned by :meth:`getQSettings` will
                         be used
        """
        if settings is None:
            settings = self.getQSettings()
        if name is None:
            perspectives = self.getPerspectivesList()
            if len(perspectives) == 0:
                return
            name, ok = Qt.QInputDialog.getItem(self, 'Delete Perspective', 'Choose perspective to be deleted:', perspectives, 0, False)
            if not ok:
                return
        if name not in perspectives:
            self.warning('Cannot remove perspective %s (not found)' % str(name))
            return
        else:
            settings.beginGroup('Perspectives')
            settings.remove(name)
            settings.endGroup()
            self.updatePerspectivesMenu()
            return

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def exportSettingsFile(self, fname=None):
        """copies the current settings file into the given file name.

        :param fname: (str) name of output file. If None given, a file dialog will be shown.
        """
        if fname is None:
            fname, _ = compat.getSaveFileName(self, 'Choose file where the current settings should be saved', '', 'Ini files (*.ini);;All files (*)')
            if not fname:
                return
        self.saveSettings()
        ok = Qt.QFile.copy(self.getQSettings().fileName(), fname)
        if ok:
            self.info('MainWindow settings saved in "%s"' % str(fname))
        else:
            msg = 'Settings could not be exported to %s' % str(fname)
            Qt.QMessageBox.warning(self, 'Export error', msg)
        return

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def importSettingsFile(self, fname=None):
        """
        loads settings (including importing all perspectives) from a given ini
        file. It warns before overwriting an existing perspective.

        :param fname: (str) name of ini file. If None given, a file dialog will be shown.
        """
        if fname is None:
            fname, _ = compat.getOpenFileName(self, 'Select a ini-format settings file', '', 'Ini files (*.ini);;All files (*)')
            if not fname:
                return
        s = Qt.QSettings(fname, Qt.QSettings.IniFormat)
        for p in self.getPerspectivesList(settings=s):
            self.loadPerspective(name=p, settings=s)
            self.savePerspective(name=p)

        self.loadSettings(settings=s)
        return

    def showEvent(self, event):
        """This event handler receives widget show events"""
        if self.__splashScreen is not None and not event.spontaneous():
            self.__splashScreen.finish(self)
        return

    def closeEvent(self, event):
        """This event handler receives widget close events"""
        self.saveSettings()
        if hasattr(self, 'socketServer'):
            self.socketServer.close()
        Qt.QMainWindow.closeEvent(self, event)
        TaurusBaseContainer.closeEvent(self, event)

    def addExternalAppLauncher(self, extapp, toToolBar=True, toMenu=True):
        """
        Adds launchers for an external application to the Tools Menu
        and/or to the Tools ToolBar.

        :param extapp: (ExternalAppAction or list<str>) the external application
                       to be launched passed as a :class:`ExternalAppAction`
                       (recommended because it allows to specify custom text and
                       icon) or, alternatively, as a list of strings (sys.argv-
                       like) that will be passed to :meth:`subprocess.Popen`.
        :param toToolBar: (bool) If True (default) a button will be added in the
                          Tools toolBar
        :param toMenu: (bool) If True (default) an entry will be added in the
                          Tools Menu, under the "External Applications" submenu

        .. seealso:: :class:`ExternalAppAction`
        """
        if not isinstance(extapp, ExternalAppAction):
            extapp = ExternalAppAction(extapp, parent=self)
        if extapp.parentWidget() is None:
            extapp.setParent(self)
        self.configurationDialog.addExternalAppConfig(extapp)
        self.configurationAction.setEnabled(True)
        if toToolBar:
            if self.extAppsBar is None:
                self.extAppsBar = self.addToolBar('External Applications')
                self.extAppsBar.setObjectName('External Applications')
                self.extAppsBar.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
                if self.VIEW_MENU_ENABLED:
                    self.viewToolBarsMenu.addAction(self.extAppsBar.toggleViewAction())
            self.extAppsBar.addAction(extapp)
        if toMenu and self.TOOLS_MENU_ENABLED:
            if self.toolsMenu is None:
                self.createToolsMenu()
            self.externalAppsMenu.addAction(extapp)
        self.registerConfigDelegate(extapp, '_extApp[%s]' % str(extapp.text()))
        return

    def deleteExternalAppLauncher(self, action):
        """
        Remove launchers for an external application to the Tools Menu
        and/or to the Tools ToolBar.

        :param extapp: (ExternalAppAction) the external application
                       to be removed passed as a :class:`ExternalAppAction`
        """
        self.configurationDialog.deleteExternalAppConfig(action)
        try:
            self.extAppsBar.removeAction(action)
            self.extAppsBar.update()
        except:
            pass

        try:
            self.externalAppsMenu.removeAction(action)
            self.externalAppsMenu.update
        except:
            pass

        self.unregisterConfigurableItem('_extApp[%s]' % str(action.text()), raiseOnError=False)

    @deprecation_decorator(dbg_msg='Change Tango Host action is TangoCentric', rel='4.1.2')
    def _onChangeTangoHostAction(self):
        """
        slot called when the Change Tango Host is triggered. It prompts for a
        Tango host name and calls :meth:`setTangoHost`
        """
        host, valid = Qt.QInputDialog.getText(self, 'Change Tango Host', 'New Tango Host', Qt.QLineEdit.Normal, str(self.getTangoHost()))
        if valid:
            self.setTangoHost(str(host))

    def setTangoHost(self, host):
        self.__tangoHost = host

    def getTangoHost(self):
        return self.__tangoHost

    def resetTangoHost(self):
        self.setTangoHost(None)
        return

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return

    def setHelpManualURI(self, uri):
        self.__helpManualURI = uri
        if self.helpManualBrowser is None:
            try:
                from taurus.external.qt.QtWebKit import QWebView
                self.helpManualBrowser = QWebView()
            except:
                self.helpManualBrowser = Qt.QLabel('QWebkit is not available')

                def dummyload(*args):
                    pass

                self.helpManualBrowser.load = dummyload
                return

        try:
            url = Qt.QUrl.fromUserInput(uri)
        except:
            url = Qt.QUrl(uri)

        self.helpManualBrowser.load(url)
        return

    def getHelpManualURI(self):
        return self.__helpManualURI

    def resetHelpManualURI(self):
        from taurus.core import release
        uri = getattr(self, 'MANUAL_URI', release.url)
        self.setHelpManualURI(uri)

    def showHelpAbout(self):
        appname = str(Qt.qApp.applicationName())
        appversion = str(Qt.qApp.applicationVersion())
        from taurus.core import release
        abouttext = '%s %s\n\nUsing %s %s' % (
         appname, appversion, release.name, release.version)
        Qt.QMessageBox.about(self, 'About', abouttext)

    def onShowManual(self, anchor=None):
        """Shows the User Manual in a dockwidget"""
        if self.helpManualDW is None:
            self.helpManualDW = Qt.QDockWidget('Manual', self)
            self.helpManualDW.setWidget(self.helpManualBrowser)
            self.helpManualDW.setObjectName('helpManualDW')
            self.addDockWidget(Qt.Qt.BottomDockWidgetArea, self.helpManualDW)
        else:
            self.helpManualDW.show()
        return

    def checkSingleInstance(self, key=None):
        """
        Tries to connect via a QLocalSocket to an existing application with the
        given key. If another instance already exists (i.e. the connection succeeds),
        it means that this application is not the only one
        """
        if key is None:
            from taurus.core.util.user import getSystemUserName
            username = getSystemUserName()
            appname = str(Qt.QApplication.applicationName())
            key = '__socket_%s-%s__' % (username, appname)
        from taurus.external.qt import QtNetwork
        socket = QtNetwork.QLocalSocket(self)
        socket.connectToServer(key)
        alive = socket.waitForConnected(3000)
        if alive:
            self.info('Another application with key "%s" is already running', key)
            return False
        else:
            self.socketServer = QtNetwork.QLocalServer(self)
            self.socketServer.newConnection.connect(self.onIncommingSocketConnection)
            ok = self.socketServer.listen(key)
            if not ok:
                AddressInUseError = QtNetwork.QAbstractSocket.AddressInUseError
                if self.socketServer.serverError() == AddressInUseError:
                    self.info('Resetting unresponsive socket with key "%s"', key)
                    if hasattr(self.socketServer, 'removeServer'):
                        self.socketServer.removeServer(key)
                    ok = self.socketServer.listen(key)
                if not ok:
                    self.warning('Cannot start local socket with key "%s". Reason: %s ', key, self.socketServer.errorString())
                    return False
            self.info('Registering as single instance with key "%s"', key)
            return True
            return

    def onIncommingSocketConnection(self):
        """
        Slot to be called when another application/instance with the same key
        checks if this application exists.

        .. note:: This is a dummy implementation which
                  just logs the connection and discards the associated socket
                  You may want to reimplement this if you want to act on such
                  connections
        """
        self.info('Incomming connection from application')
        socket = self.socketServer.nextPendingConnection()
        socket.deleteLater()
        self.raise_()
        self.activateWindow()

    def setHeartbeat(self, interval):
        """sets the interval of the heartbeat LED for the window.
        The heartbeat is displayed by a Led in the status bar unless
        it is disabled by setting the interval to 0

        :param interval: (int) heart beat interval in millisecs. Set to 0 to disable
        """
        self.heartbeatLed.setBlinkingInterval(interval)
        self.heartbeatLed.setVisible(interval > 0)

    def getHeartbeat(self):
        """returns the heart beat interval"""
        return self.heartbeatLed.getBlinkingInterval()

    def resetHeartbeat(self):
        """resets the heartbeat interval"""
        self.setHeartbeat(self.__class__.HEARTBEAT)

    @Qt.pyqtSlot()
    def applyPendingChanges(self):
        self.applyPendingOperations()

    @Qt.pyqtSlot()
    def resetPendingChanges(self):
        self.resetPendingOperations()

    model = Qt.pyqtProperty('QString', TaurusBaseContainer.getModel, TaurusBaseContainer.setModel, TaurusBaseContainer.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseContainer.getUseParentModel, TaurusBaseContainer.setUseParentModel, TaurusBaseContainer.resetUseParentModel)
    showQuality = Qt.pyqtProperty('bool', TaurusBaseContainer.getShowQuality, TaurusBaseContainer.setShowQuality, TaurusBaseContainer.resetShowQuality)
    tangoHost = Qt.pyqtProperty('QString', getTangoHost, setTangoHost, resetTangoHost)
    helpManualURI = Qt.pyqtProperty('QString', getHelpManualURI, setHelpManualURI, resetHelpManualURI)
    heartbeat = Qt.pyqtProperty('int', getHeartbeat, setHeartbeat, resetHeartbeat)


if __name__ == '__main__':
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    app.setApplicationName('TaurusMainWindow-test')
    app.setOrganizationName('ALBA')
    app.basicConfig()

    class MyMainWindow(TaurusMainWindow):
        HEARTBEAT = 300
        FILE_MENU_ENABLED = True
        VIEW_MENU_ENABLED = True
        TAURUS_MENU_ENABLED = False
        TOOLS_MENU_ENABLED = True
        HELP_MENU_ENABLED = True
        USER_PERSPECTIVES_ENABLED = True
        LOGGER_WIDGET_ENABLED = True
        SPLASH_LOGO_NAME = 'large:TaurusSplash.png'
        _splashMessage = 'Initializing Main window...'

        def __init__(self):
            TaurusMainWindow.__init__(self, parent=None, designMode=False, splash=None)
            import time
            for i in range(5):
                time.sleep(0.5)
                self.splashScreen().showMessage('starting: step %i/5' % (i + 1))

            return


    form = MyMainWindow()
    single = form.checkSingleInstance()
    if not single:
        sys.exit(1)
    form.loadSettings()
    form.show()
    sys.exit(app.exec_())