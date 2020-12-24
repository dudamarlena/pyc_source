# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/taurusgui/taurusgui.py
# Compiled at: 2019-08-19 15:09:30
"""This package provides the TaurusGui class"""
from __future__ import absolute_import
from builtins import str
import os, sys, copy, click, weakref, inspect
from future.utils import string_types
from lxml import etree
import taurus
from taurus import tauruscustomsettings
from taurus.external.qt import Qt, compat
from taurus.qt.qtcore.configuration import BaseConfigurableClass
from taurus.qt.qtcore.communication import SharedDataManager
from taurus.qt.qtgui.util import TaurusWidgetFactory
from taurus.qt.qtgui.base import TaurusBaseWidget, TaurusBaseComponent
from taurus.qt.qtgui.container import TaurusMainWindow
from taurus.qt.qtgui.taurusgui.utils import ExternalApp, PanelDescription, ToolBarDescription, AppletDescription
from taurus.qt.qtgui.util.ui import UILoadable
from taurus.qt.qtgui.taurusgui.utils import ExternalAppAction
__all__ = [
 'DockWidgetPanel', 'TaurusGui']
__docformat__ = 'restructuredtext'

@UILoadable(with_ui='ui')
class AssociationDialog(Qt.QDialog):
    """A dialog for viewing and editing the associations between instruments
    and panels"""

    def __init__(self, parent, flags=None):
        if flags is None:
            flags = Qt.Qt.Widget
        Qt.QDialog.__init__(self, parent, flags)
        self.loadUi()
        self.refresh()
        self.ui.instrumentCB.activated.connect(self.onInstrumentChanged)
        self.ui.buttonBox.clicked.connect(self.onDialogButtonClicked)
        self.ui.refreshBT.clicked.connect(self.refresh)
        return

    def refresh(self):
        currentinstrument = self.ui.instrumentCB.currentText()
        mainwindow = self.parent()
        self.associations = mainwindow.getAllInstrumentAssociations()
        self.ui.instrumentCB.clear()
        self.ui.panelCB.clear()
        self.ui.instrumentCB.addItems(sorted(self.associations.keys()))
        self.ui.panelCB.addItems(['__[None]__'] + mainwindow.getPanelNames())
        idx = self.ui.instrumentCB.findText(currentinstrument)
        if idx == -1 and self.ui.instrumentCB.count() > 0:
            idx = 0
        self.ui.instrumentCB.setCurrentIndex(idx)
        self.onInstrumentChanged(self.ui.instrumentCB.currentText())

    def onInstrumentChanged(self, instrumentname):
        instrumentname = str(instrumentname)
        panelname = self.associations.get(instrumentname)
        if panelname is None:
            self.ui.panelCB.setCurrentIndex(0)
            return
        else:
            idx = self.ui.panelCB.findText(panelname)
            self.ui.panelCB.setCurrentIndex(idx)
            return

    def onDialogButtonClicked(self, button):
        role = self.ui.buttonBox.buttonRole(button)
        if role in (Qt.QDialogButtonBox.AcceptRole, Qt.QDialogButtonBox.ApplyRole):
            if self.ui.panelCB.currentIndex() > 0:
                panelname = str(self.ui.panelCB.currentText())
            else:
                panelname = None
            instrumentname = str(self.ui.instrumentCB.currentText())
            self.associations[instrumentname] = panelname
            self.parent().setInstrumentAssociation(instrumentname, panelname)
        return


class DockWidgetPanel(Qt.QDockWidget, TaurusBaseWidget):
    """
    This is an extended QDockWidget which provides some methods for being used
    as a "panel" of a TaurusGui application. Widgets of TaurusGui are inserted
    in the application by adding them to a DockWidgetPanel.
    """

    def __init__(self, parent, widget, name, mainwindow):
        Qt.QDockWidget.__init__(self, None)
        TaurusBaseWidget.__init__(self, name, parent=parent)
        self.setAllowedAreas(Qt.Qt.TopDockWidgetArea)
        self.setWidget(widget)
        name = str(name)
        self.setWindowTitle(name)
        self.setObjectName(name)
        self._custom = False
        self._mainwindow = weakref.proxy(mainwindow)
        return

    def isCustom(self):
        return self._custom

    def setCustom(self, custom):
        self._custom = custom

    def isPermanent(self):
        return self._permanent

    def setPermanent(self, permanent):
        self._permanent = permanent

    def setWidgetFromClassName(self, classname, modulename=None):
        if self.getWidgetClassName() != classname:
            try:
                klass = TaurusWidgetFactory().getWidgetClass(classname)
                w = klass()
            except:
                try:
                    if classname is not None and '.' in classname:
                        mn, classname = classname.rsplit('.', 1)
                        modulename = ('%s.%s' % (
                         modulename or '', mn)).strip('. ')
                    module = __import__(modulename, fromlist=[''])
                    klass = getattr(module, classname)
                    w = klass()
                except Exception as e:
                    raise RuntimeError('Cannot create widget from classname "%s". Reason: %s' % (classname, repr(e)))

            if hasattr(w, 'setCustomWidgetMap'):
                w.setCustomWidgetMap(self._mainwindow.getCustomWidgetMap())
            self.setWidget(w)
            wname = '%s-%s' % (str(self.objectName()), str(classname))
            w.setObjectName(wname)
        return

    def getWidgetModuleName(self):
        w = self.widget()
        if w is None:
            return ''
        else:
            return w.__module__

    def getWidgetClassName(self):
        w = self.widget()
        if w is None:
            return ''
        else:
            return w.__class__.__name__

    def applyConfig(self, configdict, depth=-1):
        try:
            self.setWidgetFromClassName(configdict.get('widgetClassName'), modulename=configdict.get('widgetModuleName', None))
            if isinstance(self.widget(), BaseConfigurableClass):
                self.widget().applyConfig(configdict['widget'])
        except Exception as e:
            self.info('Failed to set the widget for this panel. Reason: %s' % repr(e))
            self.traceback(self.Debug)
            return

        TaurusBaseWidget.applyConfig(self, configdict, depth)
        return

    def createConfig(self, *args, **kwargs):
        configdict = TaurusBaseWidget.createConfig(self, *args, **kwargs)
        configdict['widgetClassName'] = self.getWidgetClassName()
        configdict['widgetModuleName'] = self.getWidgetModuleName()
        if isinstance(self.widget(), BaseConfigurableClass):
            configdict['widget'] = self.widget().createConfig()
        return configdict

    def closeEvent(self, event):
        Qt.QDockWidget.closeEvent(self, event)
        TaurusBaseWidget.closeEvent(self, event)


class TaurusGui(TaurusMainWindow):
    """
    This is main class for constructing the dynamic GUIs. TaurusGui is a
    specialised TaurusMainWindow which is able to handle "panels" and load
    configuration files.
    There are several ways of using TaurusGui. In the following we will give
    3 examples on how to create a simple GUI called "MyGui" which contains one
    panel called "Foo" and consisting of a `QWidget`:

    **Example 1: use declarative configuration files.**

    You can create a purely declarative configuration file to be interpreted by
    the standard `taurusgui` script::

        from taurus.qt.qtgui.taurusgui.utils import PanelDescription

        GUI_NAME = 'MyGui'
        panel = PanelDescription('Foo',
                                 classname='taurus.external.qt.Qt.QWidget')

    Note that this just a very simple example. For a much richer one, see the
    :mod:`taurus.qt.qtgui.taurusgui.conf.tgconf_example01`

    **Example 2: do everything programmatically.**

    A stand-alone python script that launches the gui when executed. No
    configuration file is used here. Panels and other components are added
    programatically::

        if __name__ == '__main__':
            from taurus.qt.qtgui.application import TaurusApplication
            from taurus.qt.qtgui.taurusgui import TaurusGui
            from taurus.external.qt import Qt
            app = TaurusApplication(cmd_line_parser=None, app_name='MyGui')
            gui = TaurusGui()
            panel = Qt.QWidget()
            gui.createPanel(panel, 'Foo')
            gui.show()
            app.exec_()

    **Example 3: mixing declarative and programmatic ways**

    It is also possible to create a stand-alone python script which loads itself
    as a configuration file. In this way you can add things programmatically and
    at the same time use the declarative way::

        GUI_NAME = 'MyGui' # <-- declarative!
        if __name__ == '__main__':
            from taurus.qt.qtgui.application import TaurusApplication
            from taurus.qt.qtgui.taurusgui import TaurusGui
            from taurus.external.qt import Qt
            app = TaurusApplication(cmd_line_parser=None)
            gui = TaurusGui(confname=__file__)
            panel = Qt.QWidget()
            gui.createPanel(panel, 'Foo')  # <-- programmatic!
            gui.show()
            app.exec_()

    """
    SelectedInstrument = Qt.pyqtSignal('QString')
    doorNameChanged = Qt.pyqtSignal('QString')
    macroserverNameChanged = Qt.pyqtSignal('QString')
    newShortMessage = Qt.pyqtSignal('QString')
    IMPLICIT_ASSOCIATION = '__[IMPLICIT]__'
    PANELS_MENU_ENABLED = True
    APPLETS_TOOLBAR_ENABLED = True
    QUICK_ACCESS_TOOLBAR_ENABLED = True

    def __init__(self, parent=None, confname=None, configRecursionDepth=None, settingsname=None):
        TaurusMainWindow.__init__(self, parent, False, True)
        if configRecursionDepth is not None:
            self.defaultConfigRecursionDepth = configRecursionDepth
        self.__panels = {}
        self.__external_app = {}
        self.__external_app_actions = {}
        self._external_app_names = []
        self.__permanent_ext_apps = []
        self.__synoptics = []
        self.__instrumentToPanelMap = {}
        self.__panelToInstrumentMap = {}
        self.setDockNestingEnabled(True)
        self.registerConfigProperty(self._getPermanentExternalApps, self._setPermanentExternalApps, 'permanentexternalapps')
        self.registerConfigProperty(self._getPermanentCustomPanels, self._setPermanentCustomPanels, 'permanentCustomPanels')
        self.registerConfigProperty(self.getAllInstrumentAssociations, self.setAllInstrumentAssociations, 'instrumentAssociation')
        from taurus import tauruscustomsettings
        self.setCustomWidgetMap(getattr(tauruscustomsettings, 'T_FORM_CUSTOM_WIDGET_MAP', {}))
        Qt.qApp.SDM = SharedDataManager(self)
        if self.PANELS_MENU_ENABLED:
            self.__initPanelsMenu()
            self.__initPanelsToolBar()
        if self.QUICK_ACCESS_TOOLBAR_ENABLED:
            self.__initQuickAccessToolBar()
        if self.APPLETS_TOOLBAR_ENABLED:
            self.__initJorgBar()
        self.__initSharedDataConnections()
        if self.TOOLS_MENU_ENABLED:
            self.__initToolsMenu()
        self._lockviewAction = Qt.QAction(Qt.QIcon.fromTheme('system-lock-screen'), 'Lock View', self)
        self._lockviewAction.setCheckable(True)
        self._lockviewAction.toggled.connect(self.setLockView)
        self._lockviewAction.setChecked(not self.isModifiableByUser())
        if self.VIEW_MENU_ENABLED:
            self.__initViewMenu()
        if settingsname:
            self.resetQSettings()
            _s = Qt.QSettings(settingsname, Qt.QSettings.IniFormat)
            self.setQSettings(_s)
        self.loadConfiguration(confname)
        Qt.qApp.SDM.connectReader('shortMessage', self.onShortMessage)
        Qt.qApp.SDM.connectWriter('shortMessage', self, 'newShortMessage')
        msg = '%s is ready' % Qt.qApp.applicationName()
        self.newShortMessage.emit(msg)
        if self.defaultConfigRecursionDepth >= 0:
            Qt.QMessageBox.information(self, 'Fail-proof mode', 'Running in fail-proof mode.' + '\nLoading of potentially problematic settings is disabled.' + '\nSome panels may not be loaded or may ignore previous user configuration' + '\nThis will also apply when loading perspectives', Qt.QMessageBox.Ok, Qt.QMessageBox.NoButton)
        return

    def closeEvent(self, event):
        try:
            self.__macroBroker.removeTemporaryPanels()
        except:
            pass

        TaurusMainWindow.closeEvent(self, event)
        for n, panel in self.__panels.items():
            panel.closeEvent(event)
            panel.widget().closeEvent(event)
            if not event.isAccepted():
                result = Qt.QMessageBox.question(self, 'Closing error', "Panel '%s' cannot be closed. Proceed closing?" % n, Qt.QMessageBox.Yes | Qt.QMessageBox.No)
                if result == Qt.QMessageBox.Yes:
                    event.accept()
                else:
                    break

    def __updatePanelsMenu(self):
        """dynamically fill the panels menus"""
        panelsmenu = self.sender()
        permanent = panelsmenu == self.__permPanelsMenu
        panelsmenu.clear()
        panelnames = sorted([ n for n, p in self.__panels.items() if p.isPermanent() == permanent ])
        for name in panelnames:
            panelsmenu.addAction(self.__panels[name].toggleViewAction())

    def __initPanelsMenu(self):
        self.__panelsMenu = Qt.QMenu('Panels', self)
        try:
            self.menuBar().insertMenu(self.helpMenu.menuAction(), self.__panelsMenu)
        except AttributeError:
            self.menuBar().addMenu(self.__panelsMenu)

        self.hideAllPanelsAction = self.__panelsMenu.addAction(Qt.QIcon('actions:hide.svg'), 'Hide all panels', self.hideAllPanels)
        self.showAllPanelsAction = self.__panelsMenu.addAction(Qt.QIcon('actions:show.svg'), 'Show all panels', self.showAllPanels)
        self.newPanelAction = self.__panelsMenu.addAction(Qt.QIcon.fromTheme('window-new'), 'New Panel...', self.createCustomPanel)
        self.removePanelAction = self.__panelsMenu.addAction(Qt.QIcon.fromTheme('edit-clear'), 'Remove Panel...', self.removePanel)
        self.__panelsMenu.addAction(Qt.QIcon.fromTheme('preferences-desktop-personal'), 'Switch temporary/permanent status...', self.updatePermanentCustomPanels)
        self.__panelsMenu.addSeparator()
        self.__permPanelsMenu = Qt.QMenu('Permanent Panels', self)
        self.__panelsMenu.addMenu(self.__permPanelsMenu)
        self.__permPanelsMenu.aboutToShow.connect(self.__updatePanelsMenu)
        self.__tempPanelsMenu = Qt.QMenu('Temporary Panels', self)
        self.__panelsMenu.addMenu(self.__tempPanelsMenu)
        self.__tempPanelsMenu.aboutToShow.connect(self.__updatePanelsMenu)
        self.__panelsMenu.addSeparator()

    def __initViewMenu(self):
        self.viewMenu.addSeparator()
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self._lockviewAction)

    def __initPanelsToolBar(self):
        self.panelsToolBar = self.addToolBar('Panels')
        self.panelsToolBar.setObjectName('PanelsToolbar')
        self.panelsToolBar.addAction(self.newPanelAction)
        if self.VIEW_MENU_ENABLED:
            self.viewToolBarsMenu.addAction(self.panelsToolBar.toggleViewAction())

    def __initQuickAccessToolBar(self):
        self.quickAccessToolBar = self.addToolBar('Quick Access')
        self.quickAccessToolBar.setObjectName('quickAccessToolbar')
        self.quickAccessToolBar.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        if self.VIEW_MENU_ENABLED:
            self.viewToolBarsMenu.addAction(self.quickAccessToolBar.toggleViewAction())

    def __initJorgBar(self):
        self.jorgsBar = Qt.QToolBar('Fancy ToolBar')
        self.jorgsBar.setObjectName('jorgsToolBar')
        self.addToolBar(Qt.Qt.RightToolBarArea, self.jorgsBar)
        self.jorgsBar.setIconSize(Qt.QSize(60, 60))
        self.jorgsBar.setMovable(False)

    def __initSharedDataConnections(self):
        splashScreen = self.splashScreen()
        if splashScreen is not None:
            self.splashScreen().showMessage('setting up shared data connections')
        Qt.qApp.SDM.connectWriter('macroserverName', self, 'macroserverNameChanged')
        Qt.qApp.SDM.connectWriter('doorName', self, 'doorNameChanged')
        Qt.qApp.SDM.connectReader('SelectedInstrument', self.onSelectedInstrument)
        Qt.qApp.SDM.connectWriter('SelectedInstrument', self, 'SelectedInstrument')
        Qt.qApp.SDM.connectReader('executionStarted', self.setFocusToPanel)
        Qt.qApp.SDM.connectReader('selectedPerspective', self.loadPerspective)
        Qt.qApp.SDM.connectWriter('perspectiveChanged', self, 'perspectiveChanged')
        return

    def __initToolsMenu(self):
        if self.toolsMenu is None:
            self.toolsMenu = Qt.QMenu('Tools')
        tm = self.toolsMenu
        tm.addAction(Qt.QIcon('apps:preferences-system-session.svg'), 'manage instrument-panel associations', self.onShowAssociationDialog)
        tm.addAction(Qt.QIcon.fromTheme('document-save'), 'Export current Panel configuration to XML', self.onExportCurrentPanelConfiguration)
        tm.addAction(Qt.QIcon('actions:data-transfer.svg'), 'Show Shared Data Manager connections', self.showSDMInfo)
        self.addExternalApplicationAction = self.externalAppsMenu.addAction(Qt.QIcon.fromTheme('list-add'), 'Add external application launcher...', self.createExternalApp)
        self.removeExternalApplicationAction = self.externalAppsMenu.addAction(Qt.QIcon.fromTheme('list-remove'), 'Remove external appication launcher...', self.removeExternalApp)
        self.externalAppsMenu.addSeparator()
        return

    def createExternalApp(self):
        """Add a new external application on execution time"""
        from .appsettingswizard import ExternalAppEditor
        app_editor = ExternalAppEditor(self)
        name, xml, ok = app_editor.getDialog()
        if name in self._external_app_names:
            msg = 'The "%s" external application exists in your GUI. If you want to create a new one, please use other text label' % name
            taurus.warning(msg)
            return
        if ok:
            extapp = ExternalApp.fromXml(xml)
            action = extapp.getAction()
            action_name = str(action.text())
            self.__external_app[action_name] = extapp
            self._addExternalAppLauncher(name, action)

    def _addExternalAppLauncher(self, name, action):
        action_name = str(action.text())
        self.__external_app_actions[action_name] = action
        self.addExternalAppLauncher(action)
        self._external_app_names.append(name)

    def removeExternalApp(self, name=None):
        """Remove the given external application from the GUI.

        :param name: (str or None) the name of the external application to be
                     removed
                     If None given, the user will be prompted
        """
        apps = list(self.__external_app.keys()) + self.__permanent_ext_apps
        if name is None:
            items = sorted(apps)
            msg1 = 'Remove External application'
            msg2 = 'External application to be removed (only custom external applications can be removed).'
            name, ok = Qt.QInputDialog.getItem(self, msg1, msg2, items, 0, False)
            if not ok:
                return
        name = str(name)
        if name not in apps:
            msg = 'Cannot remove the external application "%s" (not found)' % name
            self.debug(msg)
            return
        else:
            if name in list(self.__external_app.keys()):
                self.__external_app.pop(name)
            else:
                self.__permanent_ext_apps.remove(name)
            action = self.__external_app_actions.pop(name)
            self._external_app_names.remove(name)
            self.deleteExternalAppLauncher(action)
            self.debug('External application "%s" removed' % name)
            return

    def setCustomWidgetMap(self, map):
        """
        Sets the widget map that is used application-wide. This widget map will
        be used by default in all TaurusForm Panels belonging to this gui.

        :param map: (dict<str,Qt.QWidget>) a dictionary whose keys are device
                    type strings (e.g. see :class:`PyTango.DeviceInfo`) and
                    whose values are widgets to be used

        .. seealso:: :meth:`TaurusForm.setCustomWidgetMap`, :meth:`getCustomWidgetMap`
        """
        self._customWidgetMap = map

    def getCustomWidgetMap(self):
        """
        Returns the default map used to create custom widgets by the TaurusForms
        belonging to this GUI

        :return: (dict<str,Qt.QWidget>) a dictionary whose keys are device
                 type strings (i.e. see :class:`PyTango.DeviceInfo`) and whose
                 values are widgets to be used

        .. seealso:: :meth:`setCustomWidgetMap`
        """
        return self._customWidgetMap

    def createConfig(self, *args, **kwargs):
        """reimplemented from TaurusMainWindow.createConfig"""
        self.updatePermanentCustomPanels(showAlways=False)
        self.updatePermanentExternalApplications(showAlways=False)
        cfg = TaurusMainWindow.createConfig(self, *args, **kwargs)
        return cfg

    def removePanel(self, name=None):
        """ remove the given panel from the GUI.

        .. note:: The panel; is actually removed from the current perspective.
                  If the panel is saved in other perspectives, it should be removed from
                  them as well.

        :param name: (str or None) the name of the panel to be removed
                     If None given, the user will be prompted
        """
        if name is None:
            items = sorted([ n for n, p in self.__panels.items() if p.isCustom() ])
            name, ok = Qt.QInputDialog.getItem(self, 'Remove Panel', 'Panel to be removed (only custom panels can be removed).\n Important: you may want to save the perspective afterwards,\n and maybe remove the panel from other perspectives as well', items, 0, False)
            if not ok:
                return
        name = str(name)
        if name not in self.__panels:
            self.debug('Cannot remove panel "%s" (not found)' % name)
            return
        else:
            panel = self.__panels.pop(name)
            try:
                panel.widget().setModel(None)
            except:
                pass

            self.unregisterConfigurableItem(name, raiseOnError=False)
            self.removeDockWidget(panel)
            panel.setParent(None)
            panel.setAttribute(Qt.Qt.WA_DeleteOnClose)
            panel.close()
            self.debug('Panel "%s" removed' % name)
            return

    def createPanel(self, widget, name, floating=False, registerconfig=True, custom=False, permanent=False, icon=None, instrumentkey=None):
        """
        Creates a panel containing the given widget.

        :param wiget: (QWidget) the widget to be contained in the panel
        :param name: (str) the name of the panel. It will be used in tabs as well as for configuration
        :param floating: (bool) whether the panel should be docked or floating. (see note below)
        :param registerconfig: (bool) if True, the panel will be registered as a delegate for configuration
        :param custom: (bool) if True the panel is to be considered a "custom panel"
        :param permanent: (bool) set this to True for panels that need to be recreated when restoring the app
        :param icon: (QIcon) icon for the panel
        :param instrumentkey: (str) name of an instrument to which this panel is to be associated

        :return: (DockWidgetPanel) the created panel

        .. note:: On a previous version, there was a mandatory parameter called
                  `area` (which accepted a Qt.DockWidgetArea or None as values)
                  this parameter has now been substituted by the keyword
                  argument `floating`. In order to provide backwards
                  compatibility, the "floating" keyword argument stays at the
                  same position as the old `area` argument and if a Qt.DockWidgetArea
                  value is given, it will be interpreted as floating=True (while if
                  `None` is passed, it will be interpreted as floating=False.
        """
        if not isinstance(floating, bool):
            self.info('Deprecation warning: please note that the "area" argument is deprecated. See TaurusGui.createPanel doc')
            floating = not floating
        name = str(name)
        if name in self.__panels:
            self.info('Panel with name "%s" already exists. Reusing.' % name)
            return self.__panels[name]
        else:
            panel = DockWidgetPanel(None, widget, name, self)
            self.addDockWidget(Qt.Qt.TopDockWidgetArea, panel)
            if len(self.__panels) != 0:
                self.tabifyDockWidget(list(self.__panels.values())[(-1)], panel)
            panel.setFloating(floating)
            if instrumentkey is not None:
                if instrumentkey == self.IMPLICIT_ASSOCIATION:
                    for syn in self.__synoptics:
                        if name in syn.get_item_list():
                            self.setInstrumentAssociation(name, name)
                            break

                else:
                    self.setInstrumentAssociation(instrumentkey, name)
            if icon is not None:
                panel.toggleViewAction().setIcon(icon)
            panel.setCustom(custom)
            panel.setPermanent(permanent)
            if registerconfig:
                self.registerConfigDelegate(panel, name=name)
            self.__panels[name] = panel
            panel.visibilityChanged.connect(self._onPanelVisibilityChanged)
            return panel

    def getPanel(self, name):
        """get a panel object by name

        :return: (DockWidgetPanel)
        """
        return self.__panels[str(name)]

    def getPanelNames(self):
        """returns the names of existing panels

        :return: (list<str>)
        """
        return copy.deepcopy(list(self.__panels.keys()))

    def _setPermanentExternalApps(self, permExternalApps):
        """creates empty panels for restoring custom panels.

        :param permCustomPanels: (list<str>) list of names of custom panels
        """
        for name in permExternalApps:
            if name not in self._external_app_names:
                self.__permanent_ext_apps.append(name)
                action = ExternalAppAction('', name)
                self._addExternalAppLauncher(name, action)

    def _getPermanentExternalApps(self):
        return self.__permanent_ext_apps

    def _setPermanentCustomPanels(self, permCustomPanels):
        """creates empty panels for restoring custom panels.

        :param permCustomPanels: (list<str>) list of names of custom panels
        """
        for name in permCustomPanels:
            if name not in self.__panels:
                self.createPanel(None, name, custom=True, permanent=True)

        return

    def _getPermanentCustomPanels(self):
        """
        returns a list of panel names for which the custom and permanent flags
        are True (i.e., those custom panels that should be stored in
        configuration and/or perspectives)

        :return: (list<str>)
        """
        return [ n for n, p in self.__panels.items() if p.isCustom() and p.isPermanent() ]

    def updatePermanentCustomPanels(self, showAlways=True):
        """
        Shows a dialog for selecting which custom panels should be permanently
        stored in the configuration.

        :param showAlways: (bool) forces showing the dialog even if there are no new custom Panels
        """
        perm = self._getPermanentCustomPanels()
        temp = [ n for n, p in self.__panels.items() if p.isCustom() and not p.isPermanent()
               ]
        if len(temp) > 0 or showAlways:
            from taurus.qt.qtgui.panel import QDoubleListDlg
            dlg = QDoubleListDlg(winTitle='Stored panels', mainLabel='Select which of the panels should be stored', label1='Temporary (to be discarded)', label2='Permanent (to be stored)', list1=temp, list2=perm)
            result = dlg.exec_()
            if result == Qt.QDialog.Accepted:
                registered = self.getConfigurableItemNames()
                for name in dlg.getAll2():
                    if name not in registered:
                        self.__panels[name].setPermanent(True)
                        self.registerConfigDelegate(self.__panels[name], name)

                for name in dlg.getAll1():
                    self.__panels[name].setPermanent(False)
                    self.unregisterConfigurableItem(name, raiseOnError=False)

    def updatePermanentExternalApplications(self, showAlways=True):
        """
        Shows a dialog for selecting which new externals applications
        should be permanently stored in the configuration.

        :param showAlways: (bool) forces showing the dialog
        """
        if len(self.__external_app) > 0 or showAlways:
            from taurus.qt.qtgui.panel import QDoubleListDlg
            msg = 'Select which of the external applications should be stored'
            dlg = QDoubleListDlg(winTitle='Stored external applications', mainLabel=msg, label1='Temporary (to be discarded)', label2='Permanent (to be stored)', list1=list(self.__external_app.keys()), list2=self.__permanent_ext_apps)
            result = dlg.exec_()
            if result == Qt.QDialog.Accepted:
                for name in dlg.getAll2():
                    self.__permanent_ext_apps.append(str(name))
                    if name in self.__external_app:
                        self.__external_app.pop(str(name))

                for name in dlg.getAll1():
                    self.unregisterConfigurableItem('_extApp[%s]' % str(name), raiseOnError=False)

    def createCustomPanel(self, paneldesc=None):
        """
        Creates a panel from a Panel Description and sets it as "custom panel".

        :param paneldesc: (PanelDescription) description of the panel to be created

        .. seealso:: :meth:`createPanel`
        """
        if paneldesc is None:
            from taurus.qt.qtgui.taurusgui import PanelDescriptionWizard
            paneldesc, ok = PanelDescriptionWizard.getDialog(self, extraWidgets=self._extraCatalogWidgets)
            if not ok:
                return
        w = paneldesc.getWidget(sdm=Qt.qApp.SDM, setModel=False)
        if hasattr(w, 'setCustomWidgetMap'):
            w.setCustomWidgetMap(self.getCustomWidgetMap())
        if paneldesc.model is not None:
            w.setModel(paneldesc.model)
        if isinstance(w, TaurusBaseComponent):
            w.setModifiableByUser(True)
            w.setModelInConfig(True)
        self.createPanel(w, paneldesc.name, floating=paneldesc.floating, custom=True, registerconfig=False, instrumentkey=paneldesc.instrumentkey, permanent=False)
        msg = 'Panel %s created. Drag items to it or use the context menu to customize it' % w.name
        self.newShortMessage.emit(msg)
        return

    def createMainSynoptic(self, synopticname):
        """
        Creates a synoptic panel and registers it as "SelectedInstrument"
        reader and writer (allowing  selecting instruments from synoptic
        """
        try:
            jdwFileName = os.path.join(self._confDirectory, synopticname)
            from taurus.qt.qtgui.graphic import TaurusJDrawSynopticsView
            synoptic = TaurusJDrawSynopticsView()
            synoptic.setModel(jdwFileName)
            self.__synoptics.append(synoptic)
        except Exception as e:
            msg = 'Error loading synoptic file "%s".\nSynoptic won\'t be available' % jdwFileName
            self.error(msg)
            self.traceback(level=taurus.Info)
            result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\n\n%s' % (
             msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
            if result == Qt.QMessageBox.Abort:
                sys.exit()

        Qt.qApp.SDM.connectWriter('SelectedInstrument', synoptic, 'graphicItemSelected')
        Qt.qApp.SDM.connectReader('SelectedInstrument', synoptic.selectGraphicItem)
        name = os.path.splitext(os.path.basename(synopticname))[0]
        if len(name) > 10:
            name = 'Syn'
        i = 2
        prefix = name
        while name in self.__panels:
            name = '%s_%i' % (prefix, i)
            i += 1

        synopticpanel = self.createPanel(synoptic, name, permanent=True, icon=Qt.QIcon.fromTheme('image-x-generic'))
        if self.QUICK_ACCESS_TOOLBAR_ENABLED:
            toggleSynopticAction = synopticpanel.toggleViewAction()
            self.quickAccessToolBar.addAction(toggleSynopticAction)

    def createConsole(self, kernels):
        msg = 'createConsole() and the "CONSOLE" configuration key are ' + 'deprecated since 4.0.4. Add a panel with a ' + 'silx.gui.console.IPythonWidget  widdget instead'
        self.deprecated(msg)
        try:
            from silx.gui.console import IPythonWidget
        except ImportError:
            self.warning('Cannot import taurus.qt.qtgui.console. ' + 'The Console Panel will not be available')
            return

        console = IPythonWidget()
        self.createPanel(console, 'Console', permanent=True, icon=Qt.QIcon.fromTheme('utilities-terminal'))

    def createInstrumentsFromPool(self, macroservername):
        """
        Creates a list of instrument panel descriptions by gathering the info
        from the Pool. Each panel is a TaurusForm grouping together all those
        elements that belong to the same instrument according to the Pool info

        :return: (list<PanelDescription>)
        """
        instrument_dict = {}
        try:
            ms = taurus.Device(macroservername)
            instruments = ms.getElementsOfType('Instrument')
            if instruments is None:
                raise Exception()
        except Exception as e:
            msg = 'Could not fetch Instrument list from "%s"' % macroservername
            self.error(msg)
            result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\n\n%s' % (
             msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
            if result == Qt.QMessageBox.Abort:
                sys.exit()
            return []

        for i in instruments.values():
            i_name = i.full_name
            i_view = PanelDescription(i_name, classname='TaurusForm', floating=False, model=[])
            instrument_dict[i_name] = i_view

        from operator import attrgetter
        pool_elements = sorted(ms.getElementsWithInterface('Moveable').values(), key=attrgetter('name'))
        pool_elements += sorted(ms.getElementsWithInterface('ExpChannel').values(), key=attrgetter('name'))
        pool_elements += sorted(ms.getElementsWithInterface('IORegister').values(), key=attrgetter('name'))
        for elem in pool_elements:
            instrument = elem.instrument
            if instrument:
                i_name = instrument
                e_name = elem.full_name
                if not e_name.startswith('tango://'):
                    e_name = 'tango://%s' % e_name
                instrument_dict[i_name].model.append(e_name)

        ret = [ instrument for instrument in instrument_dict.values() if len(instrument.model) > 0 ]
        return ret

    def __getVarFromXML(self, root, nodename, default=None):
        name = root.find(nodename)
        if name is None or name.text is None:
            return default
        return name.text
        return

    def _importConfiguration(self, confname):
        """returns the module corresponding to `confname` or to
        `tgconf_<confname>`. Note: the `conf` subdirectory of the directory in
        which taurusgui.py file is installed is temporally prepended to sys.path
        """
        confsubdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf')
        oldpath = sys.path
        try:
            try:
                sys.path = [
                 confsubdir] + sys.path
                conf = __import__(confname)
            except ImportError:
                altconfname = 'tgconf_%s' % confname
                try:
                    conf = __import__(altconfname)
                except ImportError:
                    msg = 'cannot import %s or %s' % (confname, altconfname)
                    self.error(msg)
                    Qt.QMessageBox.critical(self, 'Initialization error', msg, Qt.QMessageBox.Abort)
                    sys.exit()

        finally:
            sys.path = oldpath

        return conf

    def loadConfiguration(self, confname):
        """Reads a configuration file

        :param confname: (str or None) the  name of module located in the
                         PYTHONPATH or in the conf subdirectory of the directory
                         in which taurusgui.py file is installed.
                         This method will try to import <confname>.
                         If that fails, it will try to import
                         `tgconf_<confname>`.
                         Alternatively, `confname` can be the path to the
                         configuration module (not necessarily in the
                         PYTHONPATH).
                         `confname` can also be None, in which case a dummy
                         empty module will be used.
        """
        try:
            if confname is None:
                import types
                conf = types.ModuleType('__dummy_conf_module__')
                confname = str(Qt.qApp.applicationName())
                self._confDirectory = ''
            elif os.path.exists(confname):
                import imp
                path, name = os.path.split(confname)
                name, _ = os.path.splitext(name)
                try:
                    f, filename, data = imp.find_module(name, [path])
                    conf = imp.load_module(name, f, filename, data)
                    confname = name
                except ImportError:
                    conf = self._importConfiguration(confname)

                self._confDirectory = os.path.dirname(conf.__file__)
            else:
                conf = self._importConfiguration(confname)
                self._confDirectory = os.path.dirname(conf.__file__)
        except Exception:
            import traceback
            msg = 'Error loading configuration: %s' % traceback.format_exc()
            self.error(msg)
            Qt.QMessageBox.critical(self, 'Initialization error', msg, Qt.QMessageBox.Abort)
            sys.exit()

        xmlroot = self._loadXmlConfig(conf)
        self._loadAppName(conf, confname, xmlroot)
        self._loadOrgName(conf, xmlroot)
        self._loadCustomLogo(conf, xmlroot)
        Qt.QApplication.instance().basicConfig()
        self._loadOrgLogo(conf, xmlroot)
        self._loadSingleInstance(conf, xmlroot)
        self._loadExtraCatalogWidgets(conf, xmlroot)
        self._loadManualUri(conf, xmlroot)
        POOLINSTRUMENTS = self._loadSardanaOptions(conf, xmlroot)
        self._loadSynoptic(conf, xmlroot)
        self._loadConsole(conf, xmlroot)
        self._loadCustomPanels(conf, xmlroot, POOLINSTRUMENTS)
        self._loadCustomToolBars(conf, xmlroot)
        self._loadCustomApplets(conf, xmlroot)
        self._loadExternalApps(conf, xmlroot)
        self._loadIniFile(conf, xmlroot)
        return

    def _loadXmlConfig(self, conf):
        """
        Get the xml root node from the xml configuration file
        """
        xml_config = getattr(conf, 'XML_CONFIG', None)
        if xml_config is None:
            self._xmlConfigFileName = None
        else:
            self._xmlConfigFileName = os.path.join(self._confDirectory, xml_config)
        xmlroot = etree.fromstring('<root></root>')
        if xml_config is not None:
            try:
                xmlfname = os.path.join(self._confDirectory, xml_config)
                xmlFile = open(xmlfname, 'r')
                xmlstring = xmlFile.read()
                xmlFile.close()
                xmlroot = etree.fromstring(xmlstring)
            except Exception as e:
                msg = 'Error reading the XML file: "%s"' % xmlfname
                self.error(msg)
                self.traceback(level=taurus.Info)
                result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\nReason:"%s"' % (
                 msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
                if result == Qt.QMessageBox.Abort:
                    sys.exit()

        return xmlroot

    def _loadAppName(self, conf, confname, xmlroot):
        appname = getattr(conf, 'GUI_NAME', self.__getVarFromXML(xmlroot, 'GUI_NAME', confname))
        Qt.qApp.setApplicationName(appname)
        self.setWindowTitle(appname)

    def _loadOrgName(self, conf, xmlroot):
        orgname = getattr(conf, 'ORGANIZATION', self.__getVarFromXML(xmlroot, 'ORGANIZATION', str(Qt.qApp.organizationName()) or 'Taurus'))
        Qt.qApp.setOrganizationName(orgname)

    def _loadCustomLogo(self, conf, xmlroot):
        custom_logo = getattr(conf, 'CUSTOM_LOGO', getattr(conf, 'LOGO', self.__getVarFromXML(xmlroot, 'CUSTOM_LOGO', 'logos:taurus.png')))
        if Qt.QFile.exists(custom_logo):
            custom_icon = Qt.QIcon(custom_logo)
        else:
            custom_icon = Qt.QIcon(os.path.join(self._confDirectory, custom_logo))
        self.setWindowIcon(custom_icon)
        if self.APPLETS_TOOLBAR_ENABLED:
            self.jorgsBar.addAction(custom_icon, Qt.qApp.applicationName())

    def _loadOrgLogo(self, conf, xmlroot):
        logo = getattr(tauruscustomsettings, 'ORGANIZATION_LOGO', 'logos:taurus.png')
        org_logo = getattr(conf, 'ORGANIZATION_LOGO', self.__getVarFromXML(xmlroot, 'ORGANIZATION_LOGO', logo))
        if Qt.QFile.exists(org_logo):
            org_icon = Qt.QIcon(org_logo)
        else:
            org_icon = Qt.QIcon(os.path.join(self._confDirectory, org_logo))
        if self.APPLETS_TOOLBAR_ENABLED:
            self.jorgsBar.addAction(org_icon, Qt.qApp.organizationName())

    def _loadSingleInstance(self, conf, xmlroot):
        """
        if required, enforce that only one instance of this GUI can be run
        """
        single_inst = getattr(conf, 'SINGLE_INSTANCE', self.__getVarFromXML(xmlroot, 'SINGLE_INSTANCE', 'True').lower() == 'true')
        if single_inst:
            if not self.checkSingleInstance():
                msg = 'Only one instance of %s is allowed to run the same time' % Qt.qApp.applicationName()
                self.error(msg)
                Qt.QMessageBox.critical(self, 'Multiple copies', msg, Qt.QMessageBox.Abort)
                sys.exit(1)

    def _loadExtraCatalogWidgets(self, conf, xmlroot):
        """
        get custom widget catalog entries
        """
        extra_catalog_widgets = getattr(conf, 'EXTRA_CATALOG_WIDGETS', [])
        self._extraCatalogWidgets = []
        for class_name, pix_map_name in extra_catalog_widgets:
            if pix_map_name and not Qt.QFile.exists(pix_map_name):
                pix_map_name = os.path.join(self._confDirectory, pix_map_name)
            self._extraCatalogWidgets.append((class_name, pix_map_name))

    def _loadManualUri(self, conf, xmlroot):
        """
        manual panel
        """
        manual_uri = getattr(conf, 'MANUAL_URI', self.__getVarFromXML(xmlroot, 'MANUAL_URI', taurus.Release.url))
        self.setHelpManualURI(manual_uri)
        if self.HELP_MENU_ENABLED:
            self.createPanel(self.helpManualBrowser, 'Manual', permanent=True, icon=Qt.QIcon.fromTheme('help-browser'))

    def _loadSardanaOptions(self, conf, xmlroot):
        """configure macro infrastructure"""
        ms = self._loadMacroServerName(conf, xmlroot)
        mp = self._loadMacroPanels(conf, xmlroot)
        if ms is not None and mp is True:
            from sardana.taurus.qt.qtgui.macrolistener import MacroBroker
            self.__macroBroker = MacroBroker(self)
        self._loadDoorName(conf, xmlroot)
        self._loadMacroEditorsPath(conf, xmlroot)
        pool_instruments = self._loadInstrumentsFromPool(conf, xmlroot, ms)
        return pool_instruments

    def _loadMacroServerName(self, conf, xmlroot):
        macro_server_name = getattr(conf, 'MACROSERVER_NAME', self.__getVarFromXML(xmlroot, 'MACROSERVER_NAME', None))
        if macro_server_name:
            self.macroserverNameChanged.emit(macro_server_name)
        return macro_server_name

    def _loadMacroPanels(self, conf, xmlroot):
        macro_panels = getattr(conf, 'MACRO_PANELS', self.__getVarFromXML(xmlroot, 'MACRO_PANELS', True))
        return macro_panels

    def _loadDoorName(self, conf, xmlroot):
        door_name = getattr(conf, 'DOOR_NAME', self.__getVarFromXML(xmlroot, 'DOOR_NAME', ''))
        if door_name:
            self.doorNameChanged.emit(door_name)

    def _loadMacroEditorsPath(self, conf, xmlroot):
        macro_editors_path = getattr(conf, 'MACROEDITORS_PATH', self.__getVarFromXML(xmlroot, 'MACROEDITORS_PATH', ''))
        if macro_editors_path:
            from sardana.taurus.qt.qtgui.extra_macroexecutor.macroparameterseditor.macroparameterseditor import ParamEditorManager
            ParamEditorManager().parsePaths(macro_editors_path)
            ParamEditorManager().browsePaths()

    def _loadInstrumentsFromPool(self, conf, xmlroot, macro_server_name):
        """
        Get panel descriptions from pool if required
        """
        instruments_from_pool = getattr(conf, 'INSTRUMENTS_FROM_POOL', self.__getVarFromXML(xmlroot, 'INSTRUMENTS_FROM_POOL', 'False').lower() == 'true')
        if instruments_from_pool:
            try:
                self.splashScreen().showMessage('Gathering Instrument info from Pool')
            except AttributeError:
                pass

            pool_instruments = self.createInstrumentsFromPool(macro_server_name)
        else:
            pool_instruments = []
        return pool_instruments

    def _loadSynoptic(self, conf, xmlroot):
        synoptic = getattr(conf, 'SYNOPTIC', None)
        if isinstance(synoptic, string_types):
            self.warning('Deprecated usage of synoptic keyword (now it expects a list of paths). Please update your configuration file to: "synoptic=[\'%s\']".' % synoptic)
            synoptic = [synoptic]
        if synoptic is None:
            synoptic = []
            node = xmlroot.find('SYNOPTIC')
            if node is not None and node.text is not None:
                for child in node:
                    s = child.get('str')
                    if s is not None and len(s):
                        synoptic.append(s)

        for s in synoptic:
            self.createMainSynoptic(s)

        return

    def _loadConsole(self, conf, xmlroot):
        """
        Deprecated CONSOLE command (if you need a IPython Console, just add a
        Panel with a `silx.gui.console.IPythonWidget`
        """
        console = getattr(conf, 'CONSOLE', self.__getVarFromXML(xmlroot, 'CONSOLE', []))
        if console:
            self.createConsole([])

    def _loadCustomPanels(self, conf, xmlroot, poolinstruments=None):
        """
        get custom panel descriptions from the python config file, xml config and
        create panels based on the panel descriptions
        """
        custom_panels = [ obj for name, obj in inspect.getmembers(conf) if isinstance(obj, PanelDescription)
                        ]
        panel_descriptions = xmlroot.find('PanelDescriptions')
        if panel_descriptions is not None:
            for child in panel_descriptions:
                if child.tag == 'PanelDescription':
                    child_str = etree.tostring(child, encoding='unicode')
                    pd = PanelDescription.fromXml(child_str)
                    if pd is not None:
                        custom_panels.append(pd)

        for p in custom_panels + poolinstruments:
            try:
                try:
                    self.splashScreen().showMessage('Creating panel %s' % p.name)
                except AttributeError:
                    pass

                w = p.getWidget(sdm=Qt.qApp.SDM, setModel=False)
                if hasattr(w, 'setCustomWidgetMap'):
                    w.setCustomWidgetMap(self.getCustomWidgetMap())
                if p.model is not None:
                    w.setModel(p.model)
                if p.instrumentkey is None:
                    instrumentkey = self.IMPLICIT_ASSOCIATION
                registerconfig = p not in poolinstruments
                self.createPanel(w, p.name, floating=p.floating, registerconfig=registerconfig, instrumentkey=instrumentkey, permanent=True)
            except Exception as e:
                msg = 'Cannot create panel %s' % getattr(p, 'name', '__Unknown__')
                self.error(msg)
                self.traceback(level=taurus.Info)
                result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\n\n%s' % (
                 msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
                if result == Qt.QMessageBox.Abort:
                    sys.exit()

        return

    def _loadCustomToolBars(self, conf, xmlroot):
        """
        get custom toolbars descriptions from the python config file, xml config and
        create toolbars based on the descriptions
        """
        custom_toolbars = [ obj for name, obj in inspect.getmembers(conf) if isinstance(obj, ToolBarDescription)
                          ]
        tool_bar_descriptions = xmlroot.find('ToolBarDescriptions')
        if tool_bar_descriptions is not None:
            for child in tool_bar_descriptions:
                if child.tag == 'ToolBarDescription':
                    child_str = etree.tostring(child, encoding='unicode')
                    d = ToolBarDescription.fromXml(child_str)
                    if d is not None:
                        custom_toolbars.append(d)

        for d in custom_toolbars:
            try:
                try:
                    self.splashScreen().showMessage('Creating Toolbar %s' % d.name)
                except AttributeError:
                    pass

                w = d.getWidget(sdm=Qt.qApp.SDM, setModel=False)
                if d.model is not None:
                    w.setModel(d.model)
                w.setWindowTitle(d.name)
                self.addToolBar(w)
                self.viewToolBarsMenu.addAction(w.toggleViewAction())
                if isinstance(w, BaseConfigurableClass):
                    self.registerConfigDelegate(w, d.name)
            except Exception as e:
                msg = 'Cannot add toolbar %s' % getattr(d, 'name', '__Unknown__')
                self.error(msg)
                self.traceback(level=taurus.Info)
                result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\n\n%s' % (
                 msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
                if result == Qt.QMessageBox.Abort:
                    sys.exit()

        return

    def _loadCustomApplets(self, conf, xmlroot):
        """
        get custom applet descriptions from the python config file, xml config and
        create applet based on the descriptions
        """
        custom_applets = []
        MONITOR = getattr(conf, 'MONITOR', self.__getVarFromXML(xmlroot, 'MONITOR', []))
        if MONITOR:
            custom_applets.append(AppletDescription('monitor', classname='TaurusMonitorTiny', model=MONITOR))
        custom_applets += [ obj for name, obj in inspect.getmembers(conf) if isinstance(obj, AppletDescription)
                          ]
        applet_descriptions = xmlroot.find('AppletDescriptions')
        if applet_descriptions is not None:
            for child in applet_descriptions:
                if child.tag == 'AppletDescription':
                    child_str = etree.tostring(child, encoding='unicode')
                    d = AppletDescription.fromXml(child_str)
                    if d is not None:
                        custom_applets.append(d)

        for d in custom_applets:
            try:
                try:
                    self.splashScreen().showMessage('Creating applet %s' % d.name)
                except AttributeError:
                    pass

                w = d.getWidget(sdm=Qt.qApp.SDM, setModel=False)
                if d.model is not None:
                    w.setModel(d.model)
                self.jorgsBar.addWidget(w)
                if isinstance(w, BaseConfigurableClass):
                    self.registerConfigDelegate(w, d.name)
            except Exception as e:
                msg = 'Cannot add applet %s' % getattr(d, 'name', '__Unknown__')
                self.error(msg)
                self.traceback(level=taurus.Info)
                result = Qt.QMessageBox.critical(self, 'Initialization error', '%s\n\n%s' % (
                 msg, repr(e)), Qt.QMessageBox.Abort | Qt.QMessageBox.Ignore)
                if result == Qt.QMessageBox.Abort:
                    sys.exit()

        return

    def _loadExternalApps(self, conf, xmlroot):
        """
        add external applications from both the python and the xml config files
        """
        external_apps = [ obj for name, obj in inspect.getmembers(conf) if isinstance(obj, ExternalApp)
                        ]
        ext_apps_node = xmlroot.find('ExternalApps')
        if ext_apps_node is not None:
            for child in ext_apps_node:
                if child.tag == 'ExternalApp':
                    child_str = etree.tostring(child, encoding='unicode')
                    ea = ExternalApp.fromXml(child_str)
                    if ea is not None:
                        external_apps.append(ea)

        for a in external_apps:
            self._external_app_names.append(str(a.getAction().text()))
            self.addExternalAppLauncher(a.getAction())

        return

    def _loadIniFile(self, conf, xmlroot):
        """
        get the "factory settings" filename. By default, it is called
        "default.ini" and resides in the configuration dir
        """
        ini_file = getattr(conf, 'INIFILE', self.__getVarFromXML(xmlroot, 'INIFILE', 'default.ini'))
        ini_file_name = os.path.join(self._confDirectory, ini_file)
        msg = 'Loading previous state'
        if self.defaultConfigRecursionDepth >= 0:
            msg += ' in Fail Proof mode'
        try:
            self.splashScreen().showMessage(msg)
        except AttributeError:
            pass

        self.loadSettings(factorySettingsFileName=ini_file_name)

    def setLockView(self, locked):
        self.setModifiableByUser(not locked)

    def setModifiableByUser(self, modifiable):
        if modifiable:
            dwfeat = Qt.QDockWidget.AllDockWidgetFeatures
        else:
            dwfeat = Qt.QDockWidget.NoDockWidgetFeatures
        for panel in self.__panels.values():
            panel.toggleViewAction().setEnabled(modifiable)
            panel.setFeatures(dwfeat)

        if self.PANELS_MENU_ENABLED:
            for action in (self.newPanelAction, self.showAllPanelsAction, self.hideAllPanelsAction):
                action.setEnabled(modifiable)

        if self.TOOLS_MENU_ENABLED:
            for action in (self.addExternalApplicationAction, self.removeExternalApplicationAction):
                action.setEnabled(modifiable)

        self._lockviewAction.setChecked(not modifiable)
        TaurusMainWindow.setModifiableByUser(self, modifiable)

    def onShortMessage(self, msg):
        """ Slot to be called when there is a new short message. Currently, the only action
        taken when there is a new message is to display it in the main window status bar.

        :param msg: (str) the short descriptive message to be handled
        """
        self.statusBar().showMessage(msg)

    def hideAllPanels(self):
        """hides all current panels"""
        for panel in self.__panels.values():
            panel.hide()

    def showAllPanels(self):
        """shows all current panels"""
        for panel in self.__panels.values():
            panel.show()

    def onShowAssociationDialog(self):
        """launches the instrument-panel association dialog (modal)"""
        dlg = AssociationDialog(self)
        Qt.qApp.SDM.connectWriter('SelectedInstrument', dlg.ui.instrumentCB, 'activated(QString)')
        dlg.exec_()
        Qt.qApp.SDM.disconnectWriter('SelectedInstrument', dlg.ui.instrumentCB, 'activated(QString)')

    def getInstrumentAssociation(self, instrumentname):
        """
        Returns the panel name associated to an instrument name

        :param instrumentname: (str or None) The name of the instrument whose associated panel is wanted

        :return: (str or None) the associated panel name (or None).
        """
        return self.__instrumentToPanelMap.get(instrumentname, None)

    def setInstrumentAssociation(self, instrumentname, panelname):
        """
        Sets the panel name associated to an instrument

        :param instrumentname: (str) The name of the instrument
        :param panelname: (str or None) The name of the associated
                          panel or None to remove the association
                          for this instrument.
        """
        instrumentname = str(instrumentname)
        oldpanelname = self.__instrumentToPanelMap.get(instrumentname, None)
        self.__panelToInstrumentMap.pop(oldpanelname, None)
        self.__instrumentToPanelMap[instrumentname] = panelname
        if panelname is not None:
            self.__panelToInstrumentMap[panelname] = instrumentname
        return

    def getAllInstrumentAssociations(self):
        """
        Returns the dictionary of instrument-panel associations

        :return: (dict<str,str>) a dict whose keys are the instruments known to the gui
                 and whose values are the corresponding associated panels (or None).
        """
        return copy.deepcopy(self.__instrumentToPanelMap)

    def setAllInstrumentAssociations(self, associationsdict, clearExisting=False):
        """
        Sets the dictionary of instrument-panel associations.
        By default, it keeps any existing association not present in the associationsdict.

        :param associationsdict: (dict<str,str>) a dict whose keys are the instruments names
                                 and whose values are the corresponding associated panels (or None)
        :param clearExisting: (bool) if True, the the existing asociations are cleared.
                              If False (default) existing associations are
                              updated with those in associationsdict
        """
        if clearExisting:
            self.__instrumentToPanelMap = copy.deepcopy(associationsdict)
        else:
            self.__instrumentToPanelMap.update(copy.deepcopy(associationsdict))
        self.__panelToInstrumentMap = {}
        for k, v in self.__instrumentToPanelMap.items():
            self.__panelToInstrumentMap[v] = k

    def _onPanelVisibilityChanged(self, visible):
        if visible:
            panelname = str(self.sender().objectName())
            instrumentname = self.__panelToInstrumentMap.get(panelname)
            if instrumentname is not None:
                self.SelectedInstrument.emit(instrumentname)
        return

    def onSelectedInstrument(self, instrumentname):
        """ Slot to be called when the selected instrument has changed (e.g. by user
        clicking in the synoptic)

        :param instrumentname: (str) The name that identifies the instrument.
        """
        instrumentname = str(instrumentname)
        panelname = self.getInstrumentAssociation(instrumentname)
        self.setFocusToPanel(panelname)

    def setFocusToPanel(self, panelname):
        """ Method that sets a focus for panel passed via an argument

        :param panelname: (str) The name that identifies the panel.
                               This name must be unique within the panels in the GUI.
        """
        panelname = str(panelname)
        try:
            panel = self.__panels[panelname]
            panel.show()
            panel.setFocus()
            panel.raise_()
        except KeyError:
            pass

    def tabifyArea(self, area):
        """ tabifies all panels in a given area.

        :param area: (Qt.DockWidgetArea)

        .. warning:: This method is deprecated
        """
        raise DeprecationWarning('tabifyArea is no longer supported (now all panels reside in the same DockWidget Area)')
        panels = self.findPanelsInArea(area)
        if len(panels) < 2:
            return
        p0 = panels[0]
        for p in panels[1:]:
            self.tabifyDockWidget(p0, p)

    def findPanelsInArea(self, area):
        """ returns all panels in the given area

        :param area: (QMdiArea, Qt.DockWidgetArea, 'FLOATING' or None). If
                     area=='FLOATING', the dockwidgets that are floating will be
                     returned.
        :param area:  (Qt.DockWidgetArea or str )

        .. warning:: This method is deprecated
        """
        raise DeprecationWarning('findPanelsInArea is no longer supported (now all panels reside in the same DockWidget Area)')
        if area == 'FLOATING':
            return [ p for p in self.__panels.values() if p.isFloating() ]
        else:
            return [ p for p in self.__panels.values() if self.dockWidgetArea(p) == area ]

    @classmethod
    def getQtDesignerPluginInfo(cls):
        """TaurusGui is not to be in designer """
        return

    def onShowManual(self, anchor=None):
        """reimplemented from :class:`TaurusMainWindow` to show the manual in a panel (not just a dockwidget)"""
        self.setFocusToPanel('Manual')

    def onExportCurrentPanelConfiguration(self, fname=None):
        if fname is None:
            fname = self._xmlConfigFileName
        if self._xmlConfigFileName is None:
            xmlroot = etree.Element('taurusgui_config')
        else:
            try:
                f = open(self._xmlConfigFileName, 'r')
                xmlroot = etree.fromstring(f.read())
                f.close()
            except Exception as e:
                self.error('Cannot parse file "%s": %s', self._xmlConfigFileName, str(e))
                return

        panelDescriptionsNode = xmlroot.find('PanelDescriptions')
        if panelDescriptionsNode is None:
            panelDescriptionsNode = etree.SubElement(xmlroot, 'PanelDescriptions')
        from taurus.qt.qtgui.panel import QDoubleListDlg
        dlg = QDoubleListDlg(winTitle='Export Panels to XML', mainLabel='Select which of the custom panels you want to export as xml configuration', label1='Not Exported', label2='Exported', list1=[ n for n, p in self.__panels.items() if p.isCustom() ], list2=[])
        result = dlg.exec_()
        if result != Qt.QDialog.Accepted:
            return
        else:
            exportlist = dlg.getAll2()
            registered = self.getConfigurableItemNames()
            for name in exportlist:
                panel = self.__panels[name]
                if name not in registered:
                    panel.setPermanent(True)
                    self.registerConfigDelegate(panel, name)
                panelxml = PanelDescription.fromPanel(panel).toXml()
                panelDescriptionsNode.append(etree.fromstring(panelxml))

            xml = etree.tostring(xmlroot, pretty_print=True, encoding='unicode')
            while True:
                if fname is None:
                    fname, _ = compat.getSaveFileName(self, 'Open File', self._confDirectory, self.tr('XML files (*.xml)'))
                    if not fname:
                        return
                fname = str(fname)
                if os.path.exists(fname):
                    import shutil
                    try:
                        bckname = '%s.orig' % fname
                        shutil.copy(fname, bckname)
                    except:
                        self.warning('%s will be overwritten but I could not create a backup in %s', fname, bckname)

                try:
                    f = open(fname, 'w')
                    f.write(xml)
                    f.close()
                    break
                except Exception as e:
                    msg = 'Cannot write to %s: %s' % (fname, str(e))
                    self.error(msg)
                    Qt.QMessageBox.warning(self, 'I/O problem', msg + '\nChoose a different location.', Qt.QMessageBox.Ok, Qt.QMessageBox.NoButton)
                    fname = None

            hint = "XML_CONFIG = '%s'" % os.path.relpath(fname, self._confDirectory)
            msg = 'Configuration written in %s' % fname
            self.info(msg)
            Qt.QMessageBox.information(self, 'Configuration updated', msg + '\nMake sure that the .py configuration file in %s contains\n%s' % (
             self._confDirectory, hint), Qt.QMessageBox.Ok, Qt.QMessageBox.NoButton)
            return

    def showSDMInfo(self):
        """pops up a dialog showing the current information from the Shared Data Manager"""
        text = 'Currently managing %i shared data objects:\n%s' % (
         len(Qt.qApp.SDM.activeDataUIDs()), (', ').join(Qt.qApp.SDM.activeDataUIDs()))
        nfo = Qt.qApp.SDM.info()
        w = Qt.QMessageBox(Qt.QMessageBox.Information, 'Shared Data Manager Information', text, buttons=Qt.QMessageBox.Close, parent=self)
        w.setDetailedText(nfo)
        w.show()
        self.info(nfo)


@click.command('gui')
@click.argument('confname', nargs=1, required=True)
@click.option('--safe-mode', 'safe_mode', is_flag=True, default=False, help='launch in safe mode (it prevents potentially problematic ' + 'configs from being loaded)')
@click.option('--ini', type=click.Path(exists=True), metavar='INIFILE', help='settings file (.ini) to be loaded (defaults to ' + '<user_config_dir>/<appname>.ini)', default=None)
def gui_cmd(confname, safe_mode, ini):
    """Launch a TaurusGUI using the given CONF"""
    import sys, taurus
    from taurus.qt.qtgui.application import TaurusApplication
    taurus.info('Starting execution of TaurusGui')
    app = TaurusApplication(cmd_line_parser=None, app_name='taurusgui')
    if safe_mode:
        configRecursionDepth = 0
    else:
        configRecursionDepth = None
    gui = TaurusGui(None, confname=confname, settingsname=ini, configRecursionDepth=configRecursionDepth)
    gui.show()
    ret = app.exec_()
    taurus.info('Finished execution of TaurusGui')
    sys.exit(ret)
    return


@click.command('newgui')
def newgui_cmd():
    """Create a new TaurusGui"""
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None, app_name='newgui')
    from taurus.qt.qtgui.taurusgui import AppSettingsWizard
    wizard = AppSettingsWizard()
    wizard.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    gui_cmd()