# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddmonitoring/utils/UI.py
# Compiled at: 2019-11-30 08:21:36
# Size of source mod 2**32: 6032 bytes
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, MultiColumnListBox, Widget, Label, TextBox, ListBox, Text, Button
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys, os
from asciimatics.scene import Scene
from collections import defaultdict
from ddmonitoring.utils.metrics_model import MetricsModel

class MonitorFrame(Frame):

    def __init__(self, screen, model):
        super(MonitorFrame, self).__init__(screen, (screen.height),
          (screen.width),
          has_border=True,
          title='DD-MONITORING')
        self._last_frame = 0
        self._model = model
        layout = Layout([1], fill_frame=False)
        layout2 = Layout([40, 40, 20], fill_frame=True)
        layout3 = Layout([1], fill_frame=False)
        self._alerts_header = TextBox(height=1, as_string=True)
        self._alerts_header.value = 'Alerts'
        self._alerts_header.disabled = True
        self._alerts_header.custom_colour = 'label'
        self._10min_header = TextBox(height=1, as_string=True)
        self._10min_header.value = 'Past 10 minutes'
        self._10min_header.disabled = True
        self._10min_header.custom_colour = 'label'
        self._1h_header = TextBox(height=1, as_string=True)
        self._1h_header.value = 'Past hour'
        self._1h_header.disabled = True
        self._1h_header.custom_colour = 'label'
        self._10m_metrics = MultiColumnListBox(height=(Widget.FILL_FRAME),
          columns=[
         15, 15, 10, 10, 10, 10],
          options=[],
          titles=[
         'URL', 'Availability', 'MAX.(ms)', 'AVG.(ms)', 'MIN.(ms)', 'CALLS'],
          name='Metrics')
        self._1h_metrics = MultiColumnListBox(height=(Widget.FILL_FRAME),
          columns=[
         15, 15, 10, 10, 10, 10],
          options=[],
          titles=[
         'URL', 'Availability', 'MAX.(ms)', 'AVG.(ms)', 'MIN.(ms)', 'CALLS'],
          name='Metrics')
        self._alerts = MultiColumnListBox(height=(Widget.FILL_FRAME),
          columns=[
         40],
          options=[],
          titles=[
         'Message'],
          name='Alerts')
        self.add_layout(layout)
        self.add_layout(layout2)
        layout2.add_widget(self._10min_header, 0)
        layout2.add_widget(self._1h_header, 1)
        layout2.add_widget(self._alerts_header, 2)
        layout2.add_widget(self._10m_metrics, 0)
        layout2.add_widget(self._1h_metrics, 1)
        layout2.add_widget(self._alerts, 2)
        self.add_layout(layout3)
        layout3.add_widget(Label('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C')))
        self.fix()
        self.palette = defaultdict(lambda : (
         Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK))
        for key in ('selected_focus_field', 'label'):
            self.palette[key] = (
             Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)

        self.palette['title'] = (
         Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)

    def get_metrics(self, data_interval):
        metrics = [([url, str(self._model.metrics[url][data_interval]['availability']), str(self._model.metrics[url][data_interval]['max_res_time']), str(self._model.metrics[url][data_interval]['avg_res_time']), str(self._model.metrics[url][data_interval]['min_res_time']), str(self._model.metrics[url][data_interval]['200_count'])], i) for i, url in enumerate(self._model.metrics)]
        alerts = [([alert], i) for i, alert in enumerate(self._model.alerts)]
        return (
         metrics, alerts)

    def _update(self, frame_no):
        if frame_no - self._last_frame >= self.frame_update_count or self._last_frame == 0:
            self._last_frame = frame_no
            last_start_10m = self._10m_metrics.start_line
            last_sel_10m = self._10m_metrics.value
            metrics_10m, alerts = self.get_metrics(30)
            last_start_1h = self._1h_metrics.start_line
            last_sel_1h = self._1h_metrics.value
            metrics_1h, _ = self.get_metrics(600)
            last_start_a = self._alerts.start_line
            last_sel_a = self._alerts.value
            self._10m_metrics.options = metrics_10m
            self._10m_metrics.value = last_sel_10m
            self._10m_metrics.start_line = last_start_10m
            self._1h_metrics.options = metrics_1h
            self._1h_metrics.value = last_sel_1h
            self._1h_metrics.start_line = last_start_1h
            self._alerts.options = alerts
            self._alerts.value = last_sel_a
            self._alerts.start_line = last_start_a
        super(MonitorFrame, self)._update(frame_no)

    @property
    def frame_update_count(self):
        return 20