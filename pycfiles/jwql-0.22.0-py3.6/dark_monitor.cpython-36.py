# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/apps/jwql/monitor_pages/dark_monitor.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 957 bytes
import os, numpy as np
from jwql.bokeh_templating import BokehTemplate
from jwql.utils.utils import get_config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class DarkMonitor(BokehTemplate):

    def pre_init(self):
        self._embed = True
        self.format_string = None
        self.interface_file = os.path.join(SCRIPT_DIR, 'dark_monitor_interface.yml')
        self.settings = get_config()
        self.output_dir = self.settings['outputs']
        self.load_data()
        self.timestamps = np.arange(10) / 10.0
        self.dark_current = np.arange(10)

    def post_init(self):
        self.refs['dark_current_yrange'].start = min(self.dark_current)
        self.refs['dark_current_yrange'].end = max(self.dark_current)

    def load_data(self):
        new_data = np.arange(10) / 20
        self.dark_current = new_data


DarkMonitor()