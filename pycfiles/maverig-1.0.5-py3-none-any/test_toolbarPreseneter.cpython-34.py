# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_toolbarPreseneter.py
# Compiled at: 2015-02-10 09:13:11
# Size of source mod 2**32: 2426 bytes
import gettext, locale, sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Model
from maverig.presenter.presenterManager import PresenterManager
from maverig.data import dataHandler
from maverig.views.toolbarView import ToolbarView
from maverig.data import dataHandler, config
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestToolBarPresenter(TestCase):

    def setUp(self):
        cfg = config.read_config()
        model = Model()
        presenter_manager = PresenterManager(model, cfg)
        toolbar_view = ToolbarView()
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        presenter_manager.toolbar_presenter.view = toolbar_view
        toolbar_view.associated_presenter = presenter_manager.toolbar_presenter
        toolbar_view.init_ui()
        self.toolbar_presenter = presenter_manager.toolbar_presenter

    def test_on_pretty_painter_triggered(self):
        """Starts redrawing the scenario with ForceAtlas2."""
        self.toolbar_presenter.view.action_auto_layout.setDisabled(True)
        assert self.toolbar_presenter.view.action_auto_layout.isEnabled() == False

    def test_on_selection(self):
        """Reacts on model changes of the current selection and toggles the state of the delete action."""
        self.toolbar_presenter.model.mode = 'selection mode'
        if len(self.toolbar_presenter.model.selection) > 0:
            self.toolbar_presenter.view.action_delete.setEnabled(True)
            if not self.toolbar_presenter.view.action_delete.isEnabled() == True:
                raise AssertionError
        else:
            self.toolbar_presenter.view.action_delete.setDisabled(True)
        assert self.toolbar_presenter.view.action_delete.isEnabled() == False

    def test_on_drag(self):
        """Set the current mode"""
        self.toolbar_presenter.model.force_dragging = False
        self.toolbar_presenter.view.action_auto_layout.setEnabled(not self.toolbar_presenter.model.force_dragging)
        assert self.toolbar_presenter.view.action_auto_layout.isEnabled() == True