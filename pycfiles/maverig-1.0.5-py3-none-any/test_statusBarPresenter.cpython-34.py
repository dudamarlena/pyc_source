# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_statusBarPresenter.py
# Compiled at: 2015-02-17 04:36:04
# Size of source mod 2**32: 5205 bytes
import sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Model
from maverig.presenter.presenterManager import PresenterManager
from maverig.views.attributePanelView import AttributePanelView
from maverig.views.modePanelView import ModePanelView
from maverig.views.consolePanelView import ConsolePanelView
from maverig.views.progressView import ProgressView
from maverig.views.propertyPanelView import PropertyPanelView
from maverig.views.scenarioPanelView import ScenarioPanelView
from maverig.views.statusBarView import StatusBarView
from maverig.views.menuBarView import MenuBarView
from maverig.views.toolbarView import ToolbarView
from maverig.data import config
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestStatusBarPresenter(TestCase):

    def setUp(self):
        cfg = config.read_config()
        model = Model()
        self.presenter_manager = PresenterManager(model, cfg)
        attribute_panel_view = AttributePanelView()
        menu_bar_view = MenuBarView()
        property_panel_view = PropertyPanelView()
        tool_bar_view = ToolbarView()
        self.scenario_panel_view = ScenarioPanelView()
        status_bar_view = StatusBarView()
        mode_panel_view = ModePanelView()
        progress_view = ProgressView()
        console_panel_view = ConsolePanelView()
        self.presenter_manager.attribute_panel_presenter.view = attribute_panel_view
        self.presenter_manager.menu_bar_presenter.view = menu_bar_view
        self.presenter_manager.property_panel_presenter.view = property_panel_view
        self.presenter_manager.toolbar_presenter.view = tool_bar_view
        self.presenter_manager.scenario_panel_presenter.view = self.scenario_panel_view
        self.presenter_manager.status_bar_presenter.view = status_bar_view
        self.presenter_manager.mode_panel_presenter.view = mode_panel_view
        self.presenter_manager.progress_presenter.view = progress_view
        self.presenter_manager.console_panel_presenter.view = console_panel_view
        attribute_panel_view.associated_presenter = self.presenter_manager.attribute_panel_presenter
        menu_bar_view.associated_presenter = self.presenter_manager.menu_bar_presenter
        property_panel_view.associated_presenter = self.presenter_manager.property_panel_presenter
        tool_bar_view.associated_presenter = self.presenter_manager.toolbar_presenter
        self.scenario_panel_view.associated_presenter = self.presenter_manager.scenario_panel_presenter
        status_bar_view.associated_presenter = self.presenter_manager.status_bar_presenter
        mode_panel_view.associated_presenter = self.presenter_manager.mode_panel_presenter
        progress_view.associated_presenter = self.presenter_manager.progress_presenter
        console_panel_view.associated_presenter = self.presenter_manager.console_panel_presenter
        attribute_panel_view.init_ui()
        menu_bar_view.init_ui()
        property_panel_view.init_ui()
        tool_bar_view.init_ui()
        self.scenario_panel_view.init_ui()
        status_bar_view.init_ui()
        mode_panel_view.init_ui()
        progress_view.init_ui()
        console_panel_view.init_ui()
        self.status_bar_presenter = self.presenter_manager.status_bar_presenter

    def test_error(self):
        """Sets the given message in the status bar."""
        test_message = 'Test'
        self.status_bar_presenter.error(test_message)
        assert self.status_bar_presenter.view.status_message.text() == test_message

    def test_info(self):
        """Sets the given message in the status bar."""
        test_message = 'Test'
        self.status_bar_presenter.info(test_message)
        assert self.status_bar_presenter.view.status_message.text() == test_message

    def test_success(self):
        """Sets the given message in the status bar."""
        test_message = 'Test'
        self.status_bar_presenter.success(test_message)
        assert self.status_bar_presenter.view.status_message.text() == test_message

    def test_reset(self):
        """Resets the state of the status bar."""
        test_message = 'Nothing to report.'
        self.status_bar_presenter.reset()
        assert self.status_bar_presenter.view.status_message.text() == test_message

    def test_on_change_visibility_triggered(self):
        """Triggers the visibility of the status bar."""
        self.status_bar_presenter.on_change_visibility_triggered()

    def test_on_mode(self):
        """Set the current (Hand/Selection/Component) Mode for the Infopanel"""
        self.status_bar_presenter.model.mode = 'selection mode'
        assert self.status_bar_presenter.model.mode == 'selection mode'
        self.status_bar_presenter.model.mode = 'hand mode'
        assert self.status_bar_presenter.model.mode == 'hand mode'
        self.status_bar_presenter.model.mode = 'compornent mode'
        assert self.status_bar_presenter.model.mode == 'compornent mode'