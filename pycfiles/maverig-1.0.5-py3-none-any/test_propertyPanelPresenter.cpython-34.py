# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_propertyPanelPresenter.py
# Compiled at: 2015-02-17 04:36:04
# Size of source mod 2**32: 12559 bytes
import gettext, locale, sys
from unittest import TestCase
from PySide import QtCore, QtGui
from maverig.models.model import Model, ProgramMode
from maverig.data import dataHandler, config
from maverig.models.model import ElemPort
from maverig.presenter.presenterManager import PresenterManager
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

class TestPropertyPanelPresenter(TestCase):

    def setUp(self):
        self.model = Model()
        self.cfg = config.read_config()
        self.presenter_manager = PresenterManager(self.model, self.cfg)
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = dataHandler.get_lang_path()
        language = gettext.translation(current_locale, locale_path, [current_locale])
        language.install()
        self.widget_param_names = dict()
        settings_view = SettingsView()
        attribute_panel_view = AttributePanelView()
        menu_bar_view = MenuBarView()
        self.property_panel_view = PropertyPanelView()
        tool_bar_view = ToolbarView()
        scenario_panel_view = ScenarioPanelView()
        status_bar_view = StatusBarView()
        mode_panel_view = ModePanelView()
        progress_view = ProgressView()
        console_panel_view = ConsolePanelView()
        self.property_panel_presenter = self.presenter_manager.property_panel_presenter
        self.presenter_manager.settings_presenter.view = settings_view
        self.presenter_manager.attribute_panel_presenter.view = attribute_panel_view
        self.presenter_manager.menu_bar_presenter.view = menu_bar_view
        self.presenter_manager.property_panel_presenter.view = self.property_panel_view
        self.presenter_manager.toolbar_presenter.view = tool_bar_view
        self.presenter_manager.scenario_panel_presenter.view = scenario_panel_view
        self.presenter_manager.status_bar_presenter.view = status_bar_view
        self.presenter_manager.mode_panel_presenter.view = mode_panel_view
        self.presenter_manager.progress_presenter.view = progress_view
        self.presenter_manager.console_panel_presenter.view = console_panel_view
        attribute_panel_view.associated_presenter = self.presenter_manager.attribute_panel_presenter
        menu_bar_view.associated_presenter = self.presenter_manager.menu_bar_presenter
        self.property_panel_view.associated_presenter = self.presenter_manager.property_panel_presenter
        tool_bar_view.associated_presenter = self.presenter_manager.toolbar_presenter
        scenario_panel_view.associated_presenter = self.presenter_manager.scenario_panel_presenter
        status_bar_view.associated_presenter = self.presenter_manager.status_bar_presenter
        mode_panel_view.associated_presenter = self.presenter_manager.mode_panel_presenter
        progress_view.associated_presenter = self.presenter_manager.progress_presenter
        console_panel_view.associated_presenter = self.presenter_manager.console_panel_presenter
        settings_view.associated_presenter = self.presenter_manager.settings_presenter
        attribute_panel_view.init_ui()
        menu_bar_view.init_ui()
        self.property_panel_view.init_ui()
        tool_bar_view.init_ui()
        scenario_panel_view.init_ui()
        status_bar_view.init_ui()
        mode_panel_view.init_ui()
        progress_view.init_ui()
        console_panel_view.init_ui()

    def test_check_spinbox(self):
        """Check that the spinbox switch to the right value"""
        elem_id = self.property_panel_presenter.model.create_element('PyPower.PQBus', QtCore.QPointF(300, 60))
        self.property_panel_presenter.model.set_param_value(elem_id, 'base_kv', 110.0)
        self.property_panel_presenter.model.set_selected(elem_id, True)
        self.property_panel_presenter.model.update()
        for widget, param_name in self.property_panel_presenter.widget_param_names.items():
            if param_name == 'base_kv':
                widget.setValue(112.0)
                continue

        assert self.property_panel_presenter.model.get_param_value(elem_id, 'base_kv') == 220.0

    def test_value_changed(self):
        """Test if a wrong value für an element is set in the model"""
        elem_id = self.property_panel_presenter.model.create_element('PyPower.PQBus', QtCore.QPointF(300, 60))
        self.property_panel_presenter.model.set_param_value(elem_id, 'base_kv', 110.0)
        self.property_panel_presenter.model.set_selected(elem_id, True)
        self.property_panel_presenter.model.update()
        s_box = None
        for widget, param_name in self.property_panel_presenter.widget_param_names.items():
            if param_name == 'base_kv':
                s_box = widget
                continue

        s_box.setValue(0.23)
        assert self.property_panel_presenter.model.get_param_value(elem_id, 'base_kv') == 0.23
        s_box.setValue(2000)
        assert self.property_panel_presenter.model.get_param_value(elem_id, 'base_kv') == 0.23

    def test_on_change_visibility_triggered(self):
        """Test the hidden feature of the property panel"""
        self.property_panel_presenter.view.setHidden(False)
        if not self.property_panel_presenter.view.isHidden():
            self.property_panel_presenter.view.setHidden(True)
        else:
            self.property_panel_presenter.view.setHidden(False)
        assert self.property_panel_presenter.view.isHidden()

    def test_on_selection(self):
        """Check that the right widgets are placed in the property panel when selecting an element"""
        elem_id = self.property_panel_presenter.model.create_element('PyPower.Transformer', QtCore.QPointF(300, 60))
        self.property_panel_presenter.model.set_selected(elem_id, True)
        self.property_panel_presenter.model.update()
        transformer_type = None
        online = None
        transformer_tap = None
        for widget, param_name in self.property_panel_presenter.widget_param_names.items():
            if param_name == 'ttype':
                transformer_type = widget
            if param_name == 'online':
                online = widget
            if param_name == 'tap':
                transformer_tap = widget
                continue

        assert transformer_type and transformer_type.currentText() == 'TRAFO_31'
        assert online and online.isChecked()
        assert transformer_tap and transformer_tap.value() == 0

    def test_on_param(self):
        """Check that the right widgets are placed and up to date when changing a value of an element """
        elem_id = self.property_panel_presenter.model.create_element('PyPower.Transformer', QtCore.QPointF(300, 60))
        self.property_panel_presenter.model.set_param_value(elem_id, 'online', False)
        self.property_panel_presenter.model.set_param_value(elem_id, 'tap', 1)
        self.property_panel_presenter.model.set_selected(elem_id, True)
        self.property_panel_presenter.model.update()
        transformer_type = None
        online = None
        transformer_tap = None
        for widget, param_name in self.property_panel_presenter.widget_param_names.items():
            if param_name == 'ttype':
                transformer_type = widget
            if param_name == 'online':
                online = widget
            if param_name == 'tap':
                transformer_tap = widget
                continue

        assert transformer_type and transformer_type.currentText() == 'TRAFO_31'
        assert online and not online.isChecked()
        assert transformer_tap and transformer_tap.value() == 1

    def test_on_program_mode(self):
        """react on model program mode changes"""
        self.model.program_mode = ProgramMode.composition
        assert self.property_panel_presenter.view.isHidden() == True
        self.model.program_mode = ProgramMode.simulation
        assert self.property_panel_presenter.view.isHidden() == True

    def test_validate_set_param(self):
        """ validate if param can be set to value. elsewise send gui feedback """
        branch_1 = self.model.create_element('PyPower.Branch', QtCore.QPointF())
        self.model.set_param_value(branch_1, 'online', True)
        param_name = 'l'
        value = 0
        self.model.set_param_value(branch_1, param_name, value)
        comp = self.model.get_component(branch_1)
        data = comp['params'][param_name]
        if param_name is 'l' and value == 0:
            self.presenter_manager.status_bar_presenter.error(config.ZERO_KM_LENGTH())
            assert param_name is 'l'
            assert value is 0
            return False
        if data.get('accepted_values'):
            if value not in data['accepted_values']:
                assert data.get('accepted_values')
                assert value not in data['accepted_values']
        value = 2
        self.model.set_param_value(branch_1, param_name, value)
        if data.get('accepted_values'):
            if value in data['accepted_values']:
                assert data.get('accepted_values')
                assert value in data['accepted_values']

    def test_view_init_properties(self):
        """ init property panel GUI according to current params (self.params) """
        row = 0
        house_1 = self.model.create_element('CSV.House', QtCore.QPointF(120, 120))
        self.model.set_pos(ElemPort(house_1, '1'), QtCore.QPointF(150, 200))
        self.model.set_param_value(house_1, 'datafile', 'maverig/tests/data/household_1_2.small.csv')
        elem = self.model.elements[house_1]
        comp = self.model.get_component(house_1)
        branch_1 = self.model.create_element('PyPower.Branch', QtCore.QPointF())
        self.model.set_param_value(branch_1, 'online', True)
        self.model.set_param_value(branch_1, 'l', 10)
        if 'House' in comp['type']:
            self.property_panel_view.create_property_icon(dataHandler.get_component_icon(elem['icon']), row)
            widget = self.property_panel_view.create_household_cell(row, elem['params']['num_hh'])
            row += 1
        assert row == 1
        self.elem_ids = []
        self.elem_ids.append(house_1)
        if self.elem_ids:
            elem = self.model.elements[self.elem_ids[0]]
            comp = self.model.components[elem['sim_model']]
        for param_name in self.model.get_shared_published_params(self.elem_ids):
            data = comp['params'][param_name]
            value = elem['params'][param_name]
            accepted_values = data.get('accepted_values')
            self.property_panel_view.create_property_label(data['caption'], row)
            if data['datatype'] == 'int':
                pass
            if not data['datatype'] == 'int':
                raise AssertionError
            elif data['datatype'] == 'float':
                if not data['datatype'] == 'float':
                    raise AssertionError
            elif data['datatype'] == 'bool':
                if not data['datatype'] == 'bool':
                    raise AssertionError
            elif data['datatype'] == 'file (*.csv)':
                if not data['datatype'] == 'file (*.csv)':
                    raise AssertionError
            elif data['datatype'] == 'string':
                if not data['datatype'] == 'string':
                    raise AssertionError
                continue