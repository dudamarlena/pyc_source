# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sensors_menu.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 4659 bytes
"""
A class displaying all available sensors
"""
from __future__ import print_function
from __future__ import absolute_import
import copy, urwid
from s_tui.sturwid.ui_elements import ViListBox

class SensorsMenu:
    MAX_TITLE_LEN = 120

    def on_mode_button(self, button, state):
        pass

    def __init__(self, return_fn, source_list, default_source_conf):
        self.return_fn = return_fn
        cancel_button = urwid.Button('Cancel', on_press=(self.on_cancel))
        cancel_button._label.align = 'center'
        apply_button = urwid.Button('Apply', on_press=(self.on_apply))
        apply_button._label.align = 'center'
        if_buttons = urwid.Columns([apply_button, cancel_button])
        self.sensor_status_dict = {}
        sensor_column_list = []
        self.sensor_button_dict = {}
        self.active_sensors = {}
        for source in source_list:
            source_name = source.get_source_name()
            if default_source_conf[source_name]:
                self.sensor_status_dict[source_name] = copy.deepcopy(default_source_conf[source_name])
            else:
                self.sensor_status_dict[source_name] = [
                 True] * len(source.get_sensor_list())
            self.sensor_button_dict[source_name] = []
            self.active_sensors[source_name] = []
            sensor_title_str = source_name
            sensor_title = urwid.Text((
             'bold text', sensor_title_str), 'center')
            for sensor, s_tatus in zip(source.get_sensor_list(), self.sensor_status_dict[source_name]):
                cb = urwid.CheckBox(sensor, s_tatus)
                self.sensor_button_dict[source_name].append(cb)
                self.active_sensors[source_name].append(s_tatus)

            sensor_title_and_buttons = [
             sensor_title] + self.sensor_button_dict[source_name]
            listw = urwid.SimpleFocusListWalker(sensor_title_and_buttons)
            sensor_column_list.append(urwid.Pile(listw))

        sensor_select_widget = urwid.Columns(sensor_column_list)
        list_temp = [
         sensor_select_widget, if_buttons]
        listw = urwid.SimpleFocusListWalker(list_temp)
        self.main_window = urwid.LineBox(ViListBox(listw))
        max_height = 6
        for sensor, s_tatus in self.active_sensors.items():
            max_height = max(max_height, len(s_tatus) + 6)

        self.size = (max_height, self.MAX_TITLE_LEN)

    def get_size(self):
        return self.size

    def set_checkbox_value(self):
        for sensor, sensor_cb in self.sensor_button_dict.items():
            sensor_cb_next_state = self.active_sensors[sensor]
            for checkbox, state in zip(sensor_cb, sensor_cb_next_state):
                checkbox.set_state(state)

    def on_cancel(self, w):
        self.set_checkbox_value()
        self.return_fn(update=False)

    def on_apply(self, w):
        update_sensor_visibility = False
        for s_name, sensor_buttons in self.sensor_button_dict.items():
            cb_sensor_visibility = []
            for sensor_cb in sensor_buttons:
                cb_sensor_visibility.append(sensor_cb.get_state())
                changed_state = cb_sensor_visibility != self.active_sensors[s_name]
                update_sensor_visibility |= changed_state

            self.active_sensors[s_name] = cb_sensor_visibility

        self.set_checkbox_value()
        self.return_fn(update=update_sensor_visibility)