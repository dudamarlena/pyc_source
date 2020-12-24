# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/examples/receiver/example_receiver.py
# Compiled at: 2018-07-05 04:39:41
from online_monitor.receiver.receiver import Receiver
from zmq.utils import jsonapi
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
from online_monitor.utils import utils

class ExampleReceiver(Receiver):

    def setup_widgets(self, parent, name):
        dock_area = DockArea()
        parent.addTab(dock_area, name)
        dock_position = Dock('Position')
        dock_area.addDock(dock_position)
        position_graphics = pg.GraphicsLayoutWidget()
        position_graphics.show()
        view = position_graphics.addViewBox()
        self.position_img = pg.ImageItem(border='w')
        view.addItem(self.position_img)
        dock_position.addWidget(position_graphics)

    def deserialize_data(self, data):
        return jsonapi.loads(data, object_hook=utils.json_numpy_obj_hook)

    def handle_data(self, data):
        for actual_data_type, actual_data in data.items():
            if 'time_stamp' not in actual_data_type:
                self.position_img.setImage(actual_data[:], autoDownsample=True)