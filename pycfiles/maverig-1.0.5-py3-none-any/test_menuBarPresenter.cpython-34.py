# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_menuBarPresenter.py
# Compiled at: 2015-02-17 04:36:04
# Size of source mod 2**32: 30019 bytes
import gettext, locale
from datetime import datetime
import sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Mode, ProgramMode, Model
from maverig.presenter.presenterManager import PresenterManager
from maverig.data import dataHandler, config
from maverig.views.attributePanelView import AttributePanelView
from maverig.views.modePanelView import ModePanelView
from maverig.views.consolePanelView import ConsolePanelView
from maverig.views.menuBarView import MenuBarView
from maverig.views.progressView import ProgressView
from maverig.views.propertyPanelView import PropertyPanelView
from maverig.views.scenarioPanelView import ScenarioPanelView
from maverig.views.settingsView import SettingsView
from maverig.views.statusBarView import StatusBarView
from maverig.views.toolbarView import ToolbarView
from maverig.data.config import ConfigKeys
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestMenusBarPresenter(TestCase):

    def setUp(self):
        self.model = Model()
        self.cfg = config.read_config()
        self.presenter_manager = PresenterManager(self.model, self.cfg)
        self.menu_bar_view = MenuBarView()
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        settings_view = SettingsView()
        attribute_panel_view = AttributePanelView()
        self.menu_bar_view = MenuBarView()
        property_panel_view = PropertyPanelView()
        tool_bar_view = ToolbarView()
        scenario_panel_view = ScenarioPanelView()
        status_bar_view = StatusBarView()
        mode_panel_view = ModePanelView()
        progress_view = ProgressView()
        console_panel_view = ConsolePanelView()
        self.menu_bar_presenter = self.presenter_manager.menu_bar_presenter
        self.presenter_manager.settings_presenter.view = settings_view
        self.presenter_manager.attribute_panel_presenter.view = attribute_panel_view
        self.presenter_manager.menu_bar_presenter.view = self.menu_bar_view
        self.presenter_manager.property_panel_presenter.view = property_panel_view
        self.presenter_manager.toolbar_presenter.view = tool_bar_view
        self.presenter_manager.scenario_panel_presenter.view = scenario_panel_view
        self.presenter_manager.status_bar_presenter.view = status_bar_view
        self.presenter_manager.mode_panel_presenter.view = mode_panel_view
        self.presenter_manager.progress_presenter.view = progress_view
        self.presenter_manager.console_panel_presenter.view = console_panel_view
        attribute_panel_view.associated_presenter = self.presenter_manager.attribute_panel_presenter
        self.menu_bar_view.associated_presenter = self.presenter_manager.menu_bar_presenter
        property_panel_view.associated_presenter = self.presenter_manager.property_panel_presenter
        tool_bar_view.associated_presenter = self.presenter_manager.toolbar_presenter
        scenario_panel_view.associated_presenter = self.presenter_manager.scenario_panel_presenter
        status_bar_view.associated_presenter = self.presenter_manager.status_bar_presenter
        mode_panel_view.associated_presenter = self.presenter_manager.mode_panel_presenter
        progress_view.associated_presenter = self.presenter_manager.progress_presenter
        console_panel_view.associated_presenter = self.presenter_manager.console_panel_presenter
        settings_view.associated_presenter = self.presenter_manager.settings_presenter
        attribute_panel_view.init_ui()
        self.menu_bar_view.init_ui()
        property_panel_view.init_ui()
        tool_bar_view.init_ui()
        scenario_panel_view.init_ui()
        status_bar_view.init_ui()
        mode_panel_view.init_ui()
        progress_view.init_ui()
        console_panel_view.init_ui()

    def test_on_file_new_triggered(self):
        pass

    def test_new_file(self):
        pass

    def test_on_file_open_triggered(self):
        """Opens a file dialog and loads a serialized scenario from the chosen file."""
        pass

    def test_open_file(self):
        pass

    def test_on_file_save_triggered(self):
        """Saves the serialized scenario. If the current scenario isn't saved within a file already a file dialog will
        be opened."""
        pass

    def test_on_file_save_as_triggered(self):
        """Opens a file dialog so that the serialized scenario can be saved within a named file."""
        pass

    def test_on_back_to_start_triggered(self):
        """Set simulated progress-visualisation to 0."""
        self.model.program_mode = ProgramMode.simulation_paused
        if self.model.program_mode == ProgramMode.simulation_paused:
            self.model.program_mode = ProgramMode.simulation
            assert self.model.program_mode == ProgramMode.simulation
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.sim_index = 0
        self.model.sim_event.demand()
        assert self.model.sim_index == 0
        assert self.model.sim_event.demanded

    def test_on_reduce_speed_triggered(self):
        """Set simulated progress-visualisation slower in speed."""
        self.model.vid_speed = 1000
        self.old_rel_speed = 1
        for i in range(4):
            if self.model.vid_speed < 2000:
                if self.model.vid_speed == 50:
                    self.model.vid_speed += 200
                    if not self.model.vid_speed == 250:
                        raise AssertionError
                else:
                    self.model.vid_speed += 250
                    assert self.model.vid_speed % 250 == 0
            old_rel_speed = self.model.vid_speed_rel
            self.menu_bar_presenter.change_rel_speed()
            if not self.model.vid_speed_rel != old_rel_speed:
                raise AssertionError

    def test_on_run_triggered(self):
        """Runs the simulation."""
        for i in range(3):
            if i == 0:
                self.model.program_mode == ProgramMode.composition
            else:
                if i == 1:
                    self.model.program_mode == ProgramMode.simulation
                else:
                    self.model.program_mode == ProgramMode.simulation
            if self.model.program_mode == ProgramMode.composition:
                assert self.model.program_mode == ProgramMode.composition
                if self.model.validate_scenario():
                    self.model.simulation.start()
                    assert self.model.sim_event.timer.isActive()
                    self.model.program_mode = ProgramMode.simulation
                    self.model.mode = Mode.sim
                    assert self.model.program_mode == ProgramMode.simulation
                    if not self.model.mode == Mode.sim:
                        raise AssertionError
            elif self.model.program_mode == ProgramMode.simulation_paused:
                self.model.program_mode = ProgramMode.simulation
                if not self.model.program_mode == ProgramMode.simulation:
                    raise AssertionError
            elif not self.model.program_mode == ProgramMode.simulation:
                raise AssertionError

    def test_on_stop_triggered(self):
        """Stops the simulation."""
        if self.model.validate_scenario():
            self.model.simulation.start()
            self.model.simulation.stop()
            assert not self.model.sim_event.timer.isActive()
        self.model.program_mode = ProgramMode.composition
        self.model.mode = Mode.selection
        assert self.model.program_mode == ProgramMode.composition
        assert self.model.mode == Mode.selection

    def test_on_pause_triggered(self):
        """Pauses the simulation."""
        self.model.program_mode = ProgramMode.simulation_paused
        assert self.model.program_mode == ProgramMode.simulation_paused

    def test_on_increase_speed_triggered(self):
        """Set simulated progress-visualisation faster in speed."""
        self.model.vid_speed = 1000
        self.old_rel_speed = 1
        for i in range(4):
            if self.model.vid_speed > 0:
                if self.model.vid_speed == 250:
                    self.model.vid_speed -= 200
                    if not self.model.vid_speed == 50:
                        raise AssertionError
                else:
                    self.model.vid_speed -= 250
                    assert self.model.vid_speed % 250 == 0
            old_rel_speed = self.model.vid_speed_rel
            self.menu_bar_presenter.change_rel_speed()
            if not self.model.vid_speed_rel != old_rel_speed:
                raise AssertionError

    def test_on_forward_to_end_triggered(self):
        """Set simulated progress-visualisation to the end of simulation."""
        self.model.sim_progress = 100
        if self.model.sim_progress == 100:
            self.model.program_mode = ProgramMode.simulation_paused
            assert self.model.program_mode == ProgramMode.simulation_paused
        self.model.sim_index = len(self.model.sim_timestamps) - 1
        self.model.sim_event.demand()
        assert self.model.sim_index == len(self.model.sim_timestamps) - 1
        assert self.model.sim_event.demanded

    def test_on_set_time_triggered(self):
        """Sets the start time and the duration of the simulation via a dialog."""
        sim_start = self.menu_bar_presenter.datetime_to_qdatetime(self.menu_bar_presenter.model.sim_start)
        sim_end = self.menu_bar_presenter.datetime_to_qdatetime(self.menu_bar_presenter.model.sim_end)
        sim_step_size = self.model.sim_step_size
        vid_speed = self.model.vid_speed
        vid_speed_rel = self.model.vid_speed_rel
        new_start_time = QtCore.QDateTime(2014, 10, 23, 18, 28, 21, 134, 0)
        new_end_time = QtCore.QDateTime(2014, 10, 26, 18, 28, 21, 134, 0)
        new_sim_step_size = 3600
        new_vid_speed = self.model.vid_speed - 250
        new_vid_speed_rel = self.menu_bar_presenter.change_rel_speed()
        self.menu_bar_presenter.model.sim_start = self.menu_bar_presenter.qdatetime_to_datetime(new_start_time)
        self.menu_bar_presenter.model.sim_end = self.menu_bar_presenter.qdatetime_to_datetime(new_end_time)
        self.menu_bar_presenter.model.sim_step_size = new_sim_step_size
        self.menu_bar_presenter.model.vid_speed = new_vid_speed
        self.menu_bar_presenter.model.vid_speed_rel = new_vid_speed_rel
        assert sim_start != self.menu_bar_presenter.model.sim_start
        assert sim_end != self.menu_bar_presenter.model.sim_end
        assert sim_step_size != self.menu_bar_presenter.model.sim_step_size
        assert vid_speed != self.menu_bar_presenter.model.vid_speed
        assert vid_speed_rel != self.menu_bar_presenter.model.vid_speed_rel

    def test_on_hand_mode_triggered(self):
        """Toggles the hand mode for shifting the scenario."""
        self.menu_bar_presenter.model.switch_modes(Mode.hand, Mode.comp)
        assert self.menu_bar_presenter.model.mode == 'hand mode'

    def test_on_selection_mode_triggered(self):
        """Toggles the hand mode for element selection."""
        self.menu_bar_presenter.model.mode = 'component mode'
        self.menu_bar_presenter.model.switch_modes(Mode.selection, Mode.comp)
        assert self.menu_bar_presenter.model.mode == 'selection mode'

    def test_on_raster_mode_triggered(self):
        """ Toggles raster mode for element snapping """
        self.menu_bar_presenter.model.raster_mode = self.menu_bar_view.action_raster_mode.triggered.connect(self.menu_bar_presenter.on_raster_mode_triggered)
        assert self.menu_bar_presenter.model.raster_mode == True

    def test_on_elements(self):
        self.menu_bar_presenter.model.elements = "{'Branch_7': <maverig.data.components.branch.Branch object at 0x04207BB0>}"
        if len(self.menu_bar_presenter.model.elements) > 0:
            self.menu_bar_view.action_select_all.setEnabled(True)
            if not self.menu_bar_view.action_select_all.isEnabled() == True:
                raise AssertionError
        else:
            self.menu_bar_view.action_select_all.setDisabled(True)
        assert self.menu_bar_view.action_select_all.isDisabled() == True

    def test_on_mode(self):
        """Reacts on model changes of the current mode and toggles the checked state of the selection mode and hand
        mode."""
        self.menu_bar_presenter.model.mode = 'selection mode'
        self.menu_bar_presenter.view.action_selection_mode.setChecked(self.menu_bar_presenter.model.mode == Mode.selection)
        assert self.menu_bar_presenter.view.action_selection_mode.isChecked() == True
        self.menu_bar_presenter.model.mode = 'hand mode'
        self.menu_bar_view.action_hand_mode.setChecked(self.menu_bar_presenter.model.mode == Mode.hand)
        assert self.menu_bar_view.action_hand_mode.isChecked() == True

    def test_on_go_to_triggered(self):
        """Go to an specific simulation time position"""
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 40, 0))
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 50, 0))
        current_time = 1
        self.model.sim_timestamp = self.model.sim_timestamps[current_time]
        assert self.model.sim_timestamp == datetime(2014, 10, 22, 4, 40, 0)

    def test_on_program_mode(self):
        """Reacts on model changes of the current program mode and adjust the ui to reflect the program mode
        composition, simulation or simulation paused."""
        for i in range(3):
            if i == 0:
                self.model.program_mode == ProgramMode.composition
            else:
                if i == 1:
                    self.model.program_mode == ProgramMode.simulation
                else:
                    self.model.program_mode == ProgramMode.simulation_paused
                if self.model.program_mode == ProgramMode.simulation:
                    self.menu_bar_view.action_new.setDisabled(True)
                    self.menu_bar_view.action_open.setDisabled(True)
                    assert self.menu_bar_view.action_new.isEnabled() is False
                    assert self.menu_bar_view.action_open.isEnabled() is False
                    self.menu_bar_view.action_undo.setDisabled(True)
                    self.menu_bar_view.action_redo.setDisabled(True)
                    self.menu_bar_view.action_auto_layout.setDisabled(True)
                    self.menu_bar_view.action_cut.setDisabled(True)
                    self.menu_bar_view.action_copy.setDisabled(True)
                    self.menu_bar_view.action_paste.setDisabled(True)
                    self.menu_bar_view.action_delete.setDisabled(True)
                    assert self.menu_bar_view.action_undo.isEnabled() is False
                    assert self.menu_bar_view.action_redo.isEnabled() is False
                    assert self.menu_bar_view.action_auto_layout.isEnabled() is False
                    assert self.menu_bar_view.action_cut.isEnabled() is False
                    assert self.menu_bar_view.action_copy.isEnabled() is False
                    assert self.menu_bar_view.action_paste.isEnabled() is False
                    assert self.menu_bar_view.action_delete.isEnabled() is False
                    self.menu_bar_view.action_back_to_start.setEnabled(True)
                    self.model.vid_speed_rel = 4
                    self.menu_bar_view.action_reduce_speed.setEnabled(self.model.vid_speed_rel > 0.5)
                    self.menu_bar_view.action_increase_speed.setEnabled(self.model.vid_speed_rel < 8)
                    self.menu_bar_view.action_forward_to_end.setEnabled(True)
                    self.menu_bar_view.action_stop.setEnabled(True)
                    self.menu_bar_view.action_run.setDisabled(True)
                    self.menu_bar_view.action_pause.setEnabled(self.model.sim_index < self.model.sim_end_index)
                    self.menu_bar_view.action_set_time.setDisabled(True)
                    self.menu_bar_view.action_go_to_time.setEnabled(True)
                    assert self.menu_bar_view.action_back_to_start.isEnabled()
                    assert self.menu_bar_view.action_reduce_speed.isEnabled()
                    assert self.menu_bar_view.action_increase_speed.isEnabled()
                    assert self.menu_bar_view.action_forward_to_end.isEnabled()
                    assert self.menu_bar_view.action_stop.isEnabled()
                    assert self.menu_bar_view.action_run.isEnabled() is False
                    assert self.menu_bar_view.action_pause.isEnabled()
                    assert self.menu_bar_view.action_set_time.isEnabled() is False
                    assert self.menu_bar_view.action_go_to_time.isEnabled() is False
                    self.menu_bar_view.action_hand_mode.setDisabled(True)
                    self.menu_bar_view.action_selection_mode.setDisabled(True)
                    self.menu_bar_view.action_raster_mode.setDisabled(True)
                    assert self.menu_bar_view.action_hand_mode.isEnabled() is False
                    assert self.menu_bar_view.action_selection_mode.isEnabled() is False
                    assert self.menu_bar_view.action_raster_mode.isEnabled() is False
                    self.model.raster_mode = False
                    assert self.model.raster_mode == False
                    self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_PROGRESS_BAR_VISIBLE] = False
                    self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_ATTRIBUTE_PANEL_VISIBLE] = False
                    self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_CONSOLE_PANEL_VISIBLE] = False
                    self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_STATUS_BAR_VISIBLE] = False
                    self.menu_bar_view.action_trigger_progress_bar.setEnabled(True)
                    self.menu_bar_view.action_trigger_attribute_panel.setEnabled(True)
                    self.menu_bar_view.action_trigger_progress_bar.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_PROGRESS_BAR_VISIBLE])
                    self.menu_bar_view.action_trigger_attribute_panel.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_ATTRIBUTE_PANEL_VISIBLE])
                    assert self.menu_bar_view.action_trigger_progress_bar.isEnabled()
                    assert self.menu_bar_view.action_trigger_attribute_panel.isEnabled()
                    assert self.menu_bar_view.action_trigger_progress_bar.isChecked(False)
                    assert self.menu_bar_view.action_trigger_attribute_panel.isChecked(False)
                    self.menu_bar_view.action_trigger_component_panel.setDisabled(True)
                    self.menu_bar_view.action_trigger_property_panel.setDisabled(True)
                    self.menu_bar_view.action_trigger_component_panel.setChecked(False)
                    self.menu_bar_view.action_trigger_property_panel.setChecked(False)
                    self.menu_bar_view.action_trigger_console.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_CONSOLE_PANEL_VISIBLE])
                    self.menu_bar_view.action_trigger_status_bar.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_STATUS_BAR_VISIBLE])
                    assert self.menu_bar_view.action_trigger_component_panel.isEnabled() is False
                    assert self.menu_bar_view.action_trigger_property_panel.isEnabled() is False
                    assert self.menu_bar_view.action_trigger_component_panel.isChecked(False)
                    assert self.menu_bar_view.action_trigger_property_panel.isChecked(False)
                    if not self.menu_bar_view.action_trigger_console.isChecked(False):
                        raise AssertionError
            if not self.menu_bar_view.action_trigger_status_bar.isChecked(False):
                raise AssertionError
            elif self.model.program_mode == ProgramMode.composition:
                self.menu_bar_view.action_new.setEnabled(True)
                self.menu_bar_view.action_open.setEnabled(True)
                assert self.menu_bar_view.action_new.isEnabled()
                assert self.menu_bar_view.action_open.isEnabled()
                self.elem_pos = QtCore.QPointF(213, 232)
                self.elem_id = self.model.create_element('PyPower.PQBus', self.elem_pos)
                self.menu_bar_presenter.model.clipboard_elements = '{PV : 12}'
                self.menu_bar_presenter.model.selection = '{PV : 12}'
                self.menu_bar_view.action_undo.setEnabled(True)
                self.menu_bar_view.action_redo.setEnabled(True)
                self.menu_bar_view.action_auto_layout.setEnabled(len(self.model.elements) > 0)
                self.menu_bar_view.action_cut.setEnabled(len(self.model.selection) > 0)
                self.menu_bar_view.action_copy.setEnabled(len(self.model.selection) > 0)
                self.menu_bar_view.action_paste.setEnabled(len(self.model.clipboard_elements) > 0)
                self.menu_bar_view.action_delete.setEnabled(len(self.model.selection) > 0)
                assert self.menu_bar_view.action_undo.isEnabled()
                assert self.menu_bar_view.action_redo.isEnabled()
                assert self.menu_bar_view.action_auto_layout.isEnabled()
                assert self.menu_bar_view.action_cut.isEnabled()
                assert self.menu_bar_view.action_copy.isEnabled()
                assert self.menu_bar_view.action_paste.isEnabled()
                assert self.menu_bar_view.action_delete.isEnabled()
                self.menu_bar_view.action_back_to_start.setDisabled(True)
                self.menu_bar_view.action_reduce_speed.setDisabled(True)
                self.menu_bar_view.action_increase_speed.setDisabled(True)
                self.menu_bar_view.action_forward_to_end.setDisabled(True)
                self.menu_bar_view.action_run.setEnabled(True)
                self.menu_bar_view.action_stop.setDisabled(True)
                self.menu_bar_view.action_pause.setDisabled(True)
                self.menu_bar_view.action_set_time.setEnabled(True)
                self.menu_bar_view.action_go_to_time.setDisabled(True)
                assert self.menu_bar_view.action_back_to_start.isEnabled() is False
                assert self.menu_bar_view.action_reduce_speed.isEnabled() is False
                assert self.menu_bar_view.action_increase_speed.isEnabled() is False
                assert self.menu_bar_view.action_forward_to_end.isEnabled() is False
                assert self.menu_bar_view.action_run.isEnabled()
                assert self.menu_bar_view.action_stop.isEnabled() is False
                assert self.menu_bar_view.action_pause.isEnabled() is False
                assert self.menu_bar_view.action_set_time.isEnabled()
                assert self.menu_bar_view.action_go_to_time.isEnabled() is False
                self.menu_bar_view.action_hand_mode.setEnabled(True)
                self.menu_bar_view.action_selection_mode.setEnabled(True)
                self.menu_bar_view.action_raster_mode.setEnabled(True)
                assert self.menu_bar_view.action_hand_mode.isEnabled()
                assert self.menu_bar_view.action_selection_mode.isEnabled()
                assert self.menu_bar_view.action_raster_mode.isEnabled()
                self.model.raster_mode = self.model.comp_raster
                assert self.model.raster_mode == self.model.comp_raster
                self.menu_bar_view.action_trigger_progress_bar.setDisabled(True)
                self.menu_bar_view.action_trigger_attribute_panel.setDisabled(True)
                self.menu_bar_view.action_trigger_progress_bar.setChecked(False)
                self.menu_bar_view.action_trigger_attribute_panel.setChecked(False)
                assert self.menu_bar_view.action_trigger_progress_bar.isEnabled() is False
                assert self.menu_bar_view.action_trigger_attribute_panel.isEnabled() is False
                assert self.menu_bar_view.action_trigger_progress_bar.isChecked() is False
                assert self.menu_bar_view.action_trigger_attribute_panel.isChecked() is False
                self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_COMPONENT_PANEL_VISIBLE] = False
                self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_PROPERTY_PANEL_VISIBLE] = False
                self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_CONSOLE_PANEL_VISIBLE] = False
                self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_STATUS_BAR_VISIBLE] = False
                self.menu_bar_view.action_trigger_component_panel.setEnabled(True)
                self.menu_bar_view.action_trigger_property_panel.setEnabled(True)
                self.menu_bar_view.action_trigger_component_panel.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_COMPONENT_PANEL_VISIBLE])
                self.menu_bar_view.action_trigger_property_panel.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_PROPERTY_PANEL_VISIBLE])
                self.presenter_manager.scenario_panel_presenter.view.refreshBg()
                self.menu_bar_view.action_trigger_console.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_CONSOLE_PANEL_VISIBLE])
                self.menu_bar_view.action_trigger_status_bar.setChecked(self.cfg[ConfigKeys.UI_STATE][ConfigKeys.IS_STATUS_BAR_VISIBLE])
                assert self.menu_bar_view.action_trigger_component_panel.isEnabled()
                assert self.menu_bar_view.action_trigger_property_panel.isEnabled()
                assert self.menu_bar_view.action_trigger_component_panel.isChecked() is False
                assert self.menu_bar_view.action_trigger_property_panel.isChecked() is False
                assert self.menu_bar_view.action_trigger_console.isChecked() is False
                if not self.menu_bar_view.action_trigger_status_bar.isChecked() is False:
                    raise AssertionError
            elif self.model.program_mode == ProgramMode.simulation_paused:
                self.menu_bar_view.action_stop.setEnabled(True)
                self.menu_bar_view.action_run.setEnabled(self.model.sim_index < self.model.sim_end_index)
                self.menu_bar_view.action_pause.setDisabled(True)
                assert self.menu_bar_view.action_stop.isEnabled()
                assert self.menu_bar_view.action_run.isEnabled()
                if not self.menu_bar_view.action_pause.isEnabled() is False:
                    raise AssertionError
                continue

    def test_on_selection(self):
        """Reacts on model changes of the current selection and toggles the state of the cut, copy and delete
        actions."""
        self.menu_bar_presenter.model.selection = '{PV : 12}'
        assert len(self.menu_bar_presenter.model.selection) > 0

    def test_on_clipboard(self):
        """Reacts on model changes of the clipboard and toggles the state of the paste action."""
        self.menu_bar_presenter.model.clipboard_elements = '{PV : 12}'
        assert len(self.menu_bar_presenter.model.clipboard_elements) > 0

    def test_change_rel_speed(self):
        self.menu_bar_presenter.model.vid_speed = 50
        self.menu_bar_presenter.model.update()
        for i in range(8):
            old_rel = self.menu_bar_presenter.model.vid_speed_rel
            self.menu_bar_presenter.on_reduce_speed_triggered()
            self.menu_bar_presenter.model.update()
            if not old_rel is not self.menu_bar_presenter.model.vid_speed_rel:
                raise AssertionError

    def test_on_drag(self):
        self.model.program_mode = ProgramMode.composition
        if self.model.program_mode == ProgramMode.composition:
            self.model.selection_dragging = False
            self.model.force_dragging = False
            self.menu_bar_view.action_auto_layout.setEnabled(not self.model.selection_dragging and not self.model.force_dragging and bool(self.model.graph.edges()))
            assert self.menu_bar_view.action_auto_layout.isEnabled() is False

    def test_on_vid_speed(self):
        self.model.program_mode = ProgramMode.composition
        for i in range(3):
            if i == 0:
                self.model.vid_speed_rel == 8
            if i == 1:
                self.model.vid_speed_rel == 0.5
            else:
                self.model.vid_speed_rel == 4
            if self.model.program_mode != ProgramMode.composition:
                if self.model.vid_speed_rel == 8:
                    self.view.action_increase_speed.setDisabled(True)
                    if not self.view.action_increase_speed.isEnabled():
                        raise AssertionError
                else:
                    if self.model.vid_speed_rel == 0.5:
                        self.view.action_reduce_speed.setDisabled(True)
                        if not self.view.action_increase_speed.isEnabled() is False:
                            raise AssertionError
                    else:
                        self.view.action_increase_speed.setEnabled(True)
                        self.view.action_reduce_speed.setEnabled(True)
                        assert self.view.action_increase_speed.isEnabled()
                        if not self.view.action_reduce_speed.isEnabled():
                            raise AssertionError
                        continue