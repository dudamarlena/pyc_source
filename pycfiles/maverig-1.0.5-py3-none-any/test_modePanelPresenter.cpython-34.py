# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_modePanelPresenter.py
# Compiled at: 2015-02-17 04:45:55
# Size of source mod 2**32: 4596 bytes
import gettext, locale, sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Mode, Model, ProgramMode
from maverig.presenter.presenterManager import PresenterManager
from maverig.data import dataHandler
from maverig.views.modePanelView import ModePanelView
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestModePanelPresenter(TestCase):

    def setUp(self):
        self.model = Model()
        self.presenter_manager = PresenterManager(self.model, None)
        self.mode_panel_view = ModePanelView()
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        self.presenter_manager.mode_panel_presenter.view = self.mode_panel_view
        self.mode_panel_view.associated_presenter = self.presenter_manager.mode_panel_presenter
        self.mode_panel_view.init_ui()

    def test_selection_mode_btn_clicked(self):
        """Switches the mode between Selection Mode and Component Mode, if the Selection Mode Button is clicked"""
        self.model.mode = 'component mode'
        self.model.switch_modes(Mode.selection, Mode.comp)
        assert self.model.mode == 'selection mode'

    def test_hand_mode_btn_clicked(self):
        """Switches the mode between Hand Mode and Component Mode, if the Hand Mode Button is clicked"""
        self.model.mode = 'component mode'
        self.model.switch_modes(Mode.hand, Mode.comp)
        assert self.model.mode == 'hand mode'

    def test_comp_btn_clicked(self):
        """Switches the mode between Component Mode and Selection Mode, if one Component Button is clicked"""
        self.model.mode = 'component mode'
        comp_name = 'RefBus'
        if self.model.mode != Mode.comp or self.model.comp != comp_name:
            self.model.mode = Mode.comp
        else:
            self.model.mode = Mode.selection
        assert self.model.mode == 'component mode'

    def test_on_change_visibility_triggered(self):
        """Triggers the visibility of the component panel"""
        self.mode_panel_view.setHidden(False)
        if not self.mode_panel_view.isHidden():
            self.mode_panel_view.setHidden(True)
        else:
            self.mode_panel_view.setHidden(False)
        assert self.mode_panel_view.isHidden() == True

    def test_on_mode(self):
        """ react on model mode changes and update the view buttons accordingly """
        self.model.mode = 'selection mode'
        if self.model.mode == Mode.selection:
            self.mode_panel_view.btn_selection_mode.setChecked(True)
            self.mode_panel_view.hover_component_button(self.mode_panel_view.btn_selection_mode)
            self.mode_panel_view.unhover_component_button(self.mode_panel_view.btn_hand_mode)
        else:
            if self.model.mode == Mode.hand:
                self.mode_panel_view.btn_hand_mode.setChecked(True)
                self.mode_panel_view.hover_component_button(self.mode_panel_view.btn_hand_mode)
                self.mode_panel_view.unhover_component_button(self.mode_panel_view.btn_selection_mode)
            if self.model.comp:
                btn = self.buttons[self.model.comp]
                if self.model.mode == Mode.comp:
                    btn.setChecked(True)
                    self.mode_panel_view.hover_component_button(btn)
                else:
                    btn.setChecked(False)
                    self.mode_panel_view.unhover_component_button(btn)
            if not (self.mode_panel_view.btn_selection_mode.isChecked() == True and self.mode_panel_view.btn_selection_mode.width() == 55):
                raise AssertionError

    def test_program_mode(self):
        """react on model program mode changes"""
        self.model.program_mode = ProgramMode.composition
        assert self.mode_panel_view.isHidden() == True
        self.model.program_mode = ProgramMode.simulation
        assert self.mode_panel_view.isHidden() == True