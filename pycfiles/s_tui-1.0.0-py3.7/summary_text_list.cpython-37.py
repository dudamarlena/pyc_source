# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sturwid/summary_text_list.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2805 bytes
import urwid
from collections import OrderedDict

class SummaryTextList:
    MAX_LABEL_L = 12

    def __init__(self, source, visible_sensors_list):
        self.source = source
        self.visible_summaries = OrderedDict()
        keys = list(self.source.get_summary().keys())
        self.visible_summaries[keys[0]] = any(visible_sensors_list)
        for key, visible in zip(keys[1:], visible_sensors_list):
            self.visible_summaries[key] = visible

        self.summary_text_items = OrderedDict()

    def get_text_item_list(self):
        summery_text_list = []
        for key, val in self.source.get_summary().items():
            label_w = urwid.Text(str(key[0:self.MAX_LABEL_L]))
            value_w = urwid.Text((str(val)), align='right')
            self.summary_text_items[key] = value_w
            col_w = urwid.Columns([('weight', 1.5, label_w), value_w])
            try:
                _ = self.visible_summaries[key]
            except KeyError:
                self.visible_summaries[key] = True

            if self.visible_summaries[key]:
                summery_text_list.append(col_w)

        return summery_text_list

    def update_visibility(self, visible_sensors):
        keys = list(self.visible_summaries.keys())
        self.visible_summaries[keys[0]] = any(visible_sensors)
        for sensor, visible in zip(keys[1:], visible_sensors):
            self.visible_summaries[sensor] = visible

    def update(self):
        for key, val in self.source.get_summary().items():
            if key in self.summary_text_items:
                self.summary_text_items[key].set_text(str(val))

    def get_is_available(self):
        return self.source.get_is_available()