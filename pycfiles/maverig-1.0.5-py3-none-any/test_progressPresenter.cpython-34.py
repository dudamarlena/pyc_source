# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_progressPresenter.py
# Compiled at: 2015-02-17 04:45:15
# Size of source mod 2**32: 12957 bytes
import gettext, locale, time
from datetime import datetime
import sys
from unittest import TestCase
from maverig.models.model import ProgramMode
from PySide import QtCore, QtGui
from maverig.models.model import Model
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
try:
    app = QtGui.QApplication(sys.argv)
except RuntimeError:
    app = QtCore.QCoreApplication.instance()

class TestProgressPresenter(TestCase):

    def setUp(self):
        self.model = Model()
        cfg = config.read_config()
        self.presenter_manager = PresenterManager(self.model, cfg)
        self.progress_view = ProgressView()
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        settings_view = SettingsView()
        attribute_panel_view = AttributePanelView()
        menu_bar_view = MenuBarView()
        property_panel_view = PropertyPanelView()
        tool_bar_view = ToolbarView()
        scenario_panel_view = ScenarioPanelView()
        status_bar_view = StatusBarView()
        mode_panel_view = ModePanelView()
        self.progress_view = ProgressView()
        console_panel_view = ConsolePanelView()
        self.presenter_manager.settings_presenter.view = settings_view
        self.presenter_manager.attribute_panel_presenter.view = attribute_panel_view
        self.presenter_manager.menu_bar_presenter.view = menu_bar_view
        self.presenter_manager.property_panel_presenter.view = property_panel_view
        self.presenter_manager.toolbar_presenter.view = tool_bar_view
        self.presenter_manager.scenario_panel_presenter.view = scenario_panel_view
        self.presenter_manager.status_bar_presenter.view = status_bar_view
        self.presenter_manager.mode_panel_presenter.view = mode_panel_view
        self.presenter_manager.progress_presenter.view = self.progress_view
        self.presenter_manager.console_panel_presenter.view = console_panel_view
        attribute_panel_view.associated_presenter = self.presenter_manager.attribute_panel_presenter
        menu_bar_view.associated_presenter = self.presenter_manager.menu_bar_presenter
        property_panel_view.associated_presenter = self.presenter_manager.property_panel_presenter
        tool_bar_view.associated_presenter = self.presenter_manager.toolbar_presenter
        scenario_panel_view.associated_presenter = self.presenter_manager.scenario_panel_presenter
        status_bar_view.associated_presenter = self.presenter_manager.status_bar_presenter
        mode_panel_view.associated_presenter = self.presenter_manager.mode_panel_presenter
        self.progress_view.associated_presenter = self.presenter_manager.progress_presenter
        console_panel_view.associated_presenter = self.presenter_manager.console_panel_presenter
        settings_view.associated_presenter = self.presenter_manager.settings_presenter
        attribute_panel_view.init_ui()
        menu_bar_view.init_ui()
        property_panel_view.init_ui()
        tool_bar_view.init_ui()
        scenario_panel_view.init_ui()
        status_bar_view.init_ui()
        mode_panel_view.init_ui()
        self.progress_view.init_ui()
        console_panel_view.init_ui()
        self.timer = QtCore.QTimer()
        self.refresh = QtCore.QTimer()

    def test_show_video(self):
        """Trigged when sim_video_start in toolbar is pressed and move the slider"""
        self.timer.timeout.connect(self.test_run_iteration)
        self.timer.start(200)
        millis = start_time = int(round(time.time() * 1000))
        while start_time + 1100 > millis:
            millis = int(round(time.time() * 1000))
            QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

        assert self.timer.isActive()
        assert self.model.sim_index == 5

    def test_stop_video(self):
        """Trigged when sim_video_stop in toolbar is pressed and stops the slider"""
        self.timer.start(200)
        assert self.timer.isActive()
        self.timer.stop()
        assert not self.timer.isActive()

    def test_run_iteration(self):
        """Connected to timer, which is responsible for moving the slider"""
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        old = self.model.sim_index
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.sim_index += 1
        assert old == self.model.sim_index - 1

    def test_run_refresh(self):
        """Connected to timer, which is responsible for modelupdates"""
        self.model.test_event.demand()
        assert self.model.test_event.demanded
        self.model.update()
        assert not self.model.test_event.demanded
        self.model.test_event.demand()

    def test_on_slider_moved(self):
        """ set simulation position in model and keep slider in valid simulated area.
        But model updates GUI later through refresh_timer due to speed and smooth graph animation issues. """
        position = 1
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.sim_index = position
        assert self.model.sim_index == position
        self.model.sim_index = 1
        position = 10
        self.progress_view.slider.setValue(position)
        assert self.progress_view.slider.value() != position
        assert self.progress_view.slider.value() == self.model.sim_index

    def test_on_change_visibility_triggered(self):
        """Triggers the visibility of the progress panel"""
        self.progress_view.setHidden(False)
        if not self.progress_view.isHidden():
            self.progress_view.setHidden(True)
        else:
            self.progress_view.setHidden(False)
        assert self.progress_view.isHidden() == True

    def on_screen_dateformat(self):
        """Show a date in normal or in countdown-perspective"""
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.update()
        for i in range(2):
            if i == 0:
                date_format = True
            else:
                date_format = False
            if date_format:
                end_date = str(self.model.sim_end - self.model.sim_timestamp)
                end_date = end_date.split(',')
                start_date = str(self.model.sim_timestamp - self.model.sim_start)
                start_date = start_date.split(' ')
                self.progress_view.end_date.setText('-' + end_date[0])
                self.progress_view.end_time.setText(end_date[1])
                self.progress_view.actual_date.setText(start_date[0])
                self.progress_view.actual_time.setText(start_date[1])
            else:
                end_date = str(self.model.sim_end)
                end_date = end_date.split(' ')
                start_date = str(self.model.sim_timestamp)
                start_date = start_date.split(' ')
                self.progress_view.end_date.setText(end_date[0])
                self.progress_view.end_time.setText(end_date[1])
                self.progress_view.actual_date.setText(start_date[0])
                self.progress_view.actual_time.setText(start_date[1])
            assert self.progress_view.end_date.text() is not None
            assert self.progress_view.end_time.text() is not None
            assert self.progress_view.actual_date.text() is not None
            if not self.progress_view.actual_time.text() is not None:
                raise AssertionError

    def test_on_change_dateformat(self):
        """Change between the visibility of a date in normal or in countdown-perspective"""
        self.date_format = True
        assert self.date_format == True
        self.date_format = False
        assert self.date_format == False

    def test_on_progress(self):
        """Applies the current progress to the progress bar."""
        self.progress_view.progress.setValue(50)
        assert self.progress_view.progress.value() == 50
        self.model.sim_progress = 90
        self.model.update()
        if self.model.sim_progress >= 100:
            self.model.output_event('Progress: 100.00%', new_line=False)
            self.model.output_event('Simulation finished.', new_line=True)
            self.model.test_event.demand()
        assert not self.model.test_event.demanded
        self.model.sim_progress = 100
        self.model.update()
        if self.model.sim_progress >= 100:
            self.model.output_event('Progress: 100.00%', new_line=False)
            self.model.output_event('Simulation finished.', new_line=True)
            self.model.test_event.demand()
        assert self.model.test_event.demanded

    def test_on_sim(self):
        """Update of slider and date-values for new data"""
        self.progress_view.slider.setMaximum(80)
        for i in range(self.model.sim_end_index):
            self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))

        self.model.sim_index = 10
        if self.progress_view.slider.maximum() != self.model.sim_end_index:
            self.progress_view.slider.setMaximum(self.model.sim_end_index)
        assert self.progress_view.slider.maximum() == self.model.sim_end_index
        self.progress_view.slider.blockSignals(True)
        self.progress_view.slider.setValue(self.model.sim_index)
        self.progress_view.slider.blockSignals(False)
        assert self.progress_view.slider.value() == self.model.sim_index
        date_format = None
        self.model.sim_timestamps.append(datetime(2014, 10, 22, 4, 30, 0))
        self.model.update()
        self.model.program_mode = ProgramMode.simulation
        self.model.sim_index = self.model.sim_end_index
        self.model.update()
        if self.model.program_mode != ProgramMode.composition:
            if self.model.sim_index == self.model.sim_end_index:
                self.model.program_mode = ProgramMode.simulation_paused
                self.model.update()
        assert self.model.program_mode == ProgramMode.simulation_paused

    def test_on_vid_speed(self):
        """Trigged when sim_video changes in speed"""
        self.timer.start(100)
        assert self.timer.isActive()
        assert self.timer.interval() == 100
        if self.timer.isActive():
            self.timer.stop()
            assert not self.timer.isActive()
            self.timer.start(500)
        assert self.timer.isActive()
        assert self.timer.interval() == 500

    def test_on_program_mode(self):
        """react on model program mode changes"""
        self.model.program_mode = ProgramMode.composition
        self.progress_view.progress.setValue(0)
        self.progress_view.slider.setValue(0)
        self.progress_view.setHidden(True)
        assert self.progress_view.isHidden() == True
        assert self.progress_view.progress.value() == 0
        assert self.progress_view.slider.value() == 0
        for i in range(2):
            if i == 0:
                self.model.program_mode = ProgramMode.simulation
            else:
                self.model.program_mode = ProgramMode.simulation_paused
            self.progress_view.setHidden(False)
            self.refresh.timeout.connect(self.test_run_refresh)
            self.refresh.start(40)
            self.index = 0
            millis = start_time = int(round(time.time() * 1000))
            while start_time + 100 > millis:
                millis = int(round(time.time() * 1000))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

            assert self.refresh.isActive()
            assert self.model.test_event.demanded
            if not self.progress_view.isHidden() == False:
                raise AssertionError