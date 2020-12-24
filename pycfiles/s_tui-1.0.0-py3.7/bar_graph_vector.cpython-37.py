# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sturwid/bar_graph_vector.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 8375 bytes
from __future__ import absolute_import
from s_tui.sturwid.complex_bar_graph import LabeledBarGraphVector
from s_tui.sturwid.complex_bar_graph import ScalableBarGraph
import logging, math
logger = logging.getLogger(__name__)

class BarGraphVector(LabeledBarGraphVector):

    @staticmethod
    def append_latest_value(values, new_val):
        values.append(new_val)
        return values[1:]

    MAX_SAMPLES = 300
    SCALE_DENSITY = 5

    def __init__(self, source, regular_colors, graph_count, visible_graph_list, alert_colors=None, bar_width=1):
        self.source = source
        self.graph_count = graph_count
        self.graph_name = self.source.get_source_name()
        self.measurement_unit = self.source.get_measurement_unit()
        self.num_samples = self.MAX_SAMPLES
        self.graph_data = []
        for _ in range(graph_count):
            self.graph_data.append([0] * self.num_samples)

        self.graph_max = 1
        self.color_a = regular_colors[0]
        self.color_b = regular_colors[1]
        self.smooth_a = regular_colors[2]
        self.smooth_b = regular_colors[3]
        if alert_colors:
            self.alert_colors = alert_colors
        else:
            self.alert_colors = regular_colors
        self.regular_colors = regular_colors
        self.satt = None
        y_label = []
        graph_title = self.graph_name + ' [' + self.measurement_unit + ']'
        sub_title_list = self.source.get_sensor_list()
        w = []
        for _ in range(graph_count):
            graph = ScalableBarGraph(['bg background',
             self.color_a, self.color_b])
            w.append(graph)

        super(BarGraphVector, self).__init__(graph_title, sub_title_list, y_label, w, visible_graph_list)
        for graph in self.bar_graph_vector:
            graph.set_bar_width(bar_width)

        self.color_counter_vector = [0] * graph_count

    def _set_colors(self, colors):
        self.color_a = colors[0]
        self.color_b = colors[1]
        self.smooth_a = colors[2]
        self.smooth_b = colors[3]
        if self.satt:
            self.satt = {(1, 0):self.smooth_a, 
             (2, 0):self.smooth_b}
        for graph in self.bar_graph_vector:
            graph.set_segment_attributes([
             'bg background', self.color_a, self.color_b],
              satt=(self.satt))

    def get_graph_name(self):
        return self.graph_name

    def get_measurement_unit(self):
        return self.measurement_unit

    def get_is_available(self):
        return self.source.get_is_available()

    def get_label_scale(self, min_val, max_val, size):
        """Dynamically change the scale of the graph (y lable)"""
        if size < self.SCALE_DENSITY:
            label_cnt = 1
        else:
            label_cnt = int(size / self.SCALE_DENSITY)
        try:
            if max_val >= 100:
                label = [int(min_val + i * (max_val - min_val) / label_cnt) for i in range(label_cnt + 1)]
            else:
                label = [round(min_val + i * (max_val - min_val) / label_cnt, 1) for i in range(label_cnt + 1)]
            return label
        except ZeroDivisionError:
            logging.debug('Side label creation divided by 0')
            return ''

    def set_smooth_colors(self, smooth):
        if smooth:
            self.satt = {(1, 0):self.smooth_a, 
             (2, 0):self.smooth_b}
        else:
            self.satt = None
        for graph in self.bar_graph_vector:
            graph.set_segment_attributes([
             'bg background', self.color_a, self.color_b],
              satt=(self.satt))

    def update(self):
        if not self.get_is_available():
            return
        try:
            if self.source.get_edge_triggered():
                self._set_colors(self.alert_colors)
            else:
                self._set_colors(self.regular_colors)
        except NotImplementedError:
            pass

        current_reading = self.source.get_reading_list()
        logging.info('Reading %s', current_reading)
        y_label_size_max = 0
        local_top_value = []
        for graph_idx, graph in enumerate(self.bar_graph_vector):
            try:
                _ = self.visible_graph_list[graph_idx]
            except IndexError:
                self.visible_graph_list.append(True)

            bars = []
            if self.visible_graph_list[graph_idx]:
                self.graph_data[graph_idx] = self.append_latest_value(self.graph_data[graph_idx], current_reading[graph_idx])
                num_displayed_bars = graph.get_size()[1]
                visible_id = self.MAX_SAMPLES - num_displayed_bars - 1
                visible_graph_data = self.graph_data[graph_idx][visible_id:]
                local_top_value.append(max(visible_graph_data))

        update_max = False
        if self.graph_max == 1:
            self.graph_max = self.source.get_top()
            update_max = True
        local_max = math.ceil(max(local_top_value))
        if local_max > self.graph_max:
            update_max = True
            self.graph_max = local_max
        for graph_idx, graph in enumerate(self.bar_graph_vector):
            bars = []
            if self.visible_graph_list[graph_idx]:
                num_displayed_bars = graph.get_size()[1]
                if self.color_counter_vector[graph_idx] % 2 == 0:
                    for n in range(self.MAX_SAMPLES - num_displayed_bars, self.MAX_SAMPLES):
                        value = round(self.graph_data[graph_idx][n], 1)
                        if n & 1:
                            bars.append([0, value])
                        else:
                            bars.append([value, 0])

                else:
                    for n in range(self.MAX_SAMPLES - num_displayed_bars, self.MAX_SAMPLES):
                        value = round(self.graph_data[graph_idx][n], 1)
                        if n & 1:
                            bars.append([value, 0])
                        else:
                            bars.append([0, value])

                self.color_counter_vector[graph_idx] += 1
                graph.set_data(bars, float(self.graph_max))
                y_label_size_max = max(y_label_size_max, graph.get_size()[0])

        self.set_y_label(self.get_label_scale(0, self.graph_max, float(y_label_size_max)))
        if update_max:
            self.set_visible_graphs()

    def reset(self):
        self.graph_data = []
        for _ in range(self.graph_count):
            self.graph_data.append([0] * self.num_samples)

        self.graph_max = 1