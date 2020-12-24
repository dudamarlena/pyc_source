# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/OnlineMonitor.py
# Compiled at: 2018-07-05 04:39:41
# Size of source mod 2**32: 9098 bytes
import sys, logging
from PyQt5 import Qt
import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
from online_monitor.utils import utils, settings
from online_monitor.receiver.receiver import Receiver

class OnlineMonitorApplication(pg.Qt.QtGui.QMainWindow):
    app_name = 'Online Monitor'

    def __init__(self, config_file, loglevel='INFO'):
        super(OnlineMonitorApplication, self).__init__()
        utils.setup_logging(loglevel)
        logging.debug('Initialize online monitor with configuration in %s', config_file)
        self.configuration = utils.parse_config_file(config_file, expect_receiver=True)
        self.setup_style()
        self.setup_widgets()
        self.receivers = self.start_receivers()

    def closeEvent(self, event):
        super(OnlineMonitorApplication, self).closeEvent(event)
        self.stop_receivers()
        settings.set_window_geometry(self.geometry().getRect())

    def setup_style(self):
        self.setWindowTitle(self.app_name)
        stored_windows_geometry = settings.get_window_geometry()
        if stored_windows_geometry:
            self.setGeometry((pg.Qt.QtCore.QRect)(*stored_windows_geometry))
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(antialias=True)

    def start_receivers(self):
        receivers = []
        try:
            self.configuration['receiver']
        except KeyError:
            return receivers
        else:
            if self.configuration['receiver']:
                logging.info('Starting %d receivers', len(self.configuration['receiver']))
                for receiver_name, receiver_settings in self.configuration['receiver'].items():
                    receiver_settings['name'] = receiver_name
                    receiver = (utils.load_receiver)(receiver_settings['kind']), *(, base_class_type=Receiver, **receiver_settings)
                    receiver.setup_widgets((self.tab_widget), name=receiver_name)
                    receiver.start()
                    receivers.append(receiver)

                return receivers

    def on_tab_changed(self, value):
        for index, actual_receiver in enumerate((self.receivers), start=1):
            actual_receiver.active(True if index == value else False)

    def stop_receivers(self):
        if self.receivers:
            logging.info('Stopping %d receivers', len(self.receivers))
            for receiver in self.receivers:
                receiver.shutdown()

    def setup_widgets(self):
        self.tab_widget = Qt.QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.setup_status_widget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def setup_status_widget(self, parent):
        dock_area = DockArea()
        parent.addTab(dock_area, 'Status')
        self.status_dock = Dock('Status')
        dock_area.addDock(self.status_dock)
        status_graphics_widget = pg.GraphicsLayoutWidget()
        status_graphics_widget.show()
        self.status_dock.addWidget(status_graphics_widget)
        try:
            self.configuration['receiver']
        except KeyError:
            return
        else:
            for receiver_index, (receiver_name, receiver_settings) in enumerate(self.configuration['receiver'].items()):
                view = status_graphics_widget.addViewBox(row=receiver_index, col=5, lockAspect=True, enableMouse=False)
                text = pg.TextItem(('Receiver\n%s' % receiver_name), border='b', fill=(0,
                                                                                       0,
                                                                                       255,
                                                                                       100), anchor=(0.5,
                                                                                                     0.5), color=(0,
                                                                                                                  0,
                                                                                                                  0,
                                                                                                                  200))
                text.setPos(0.5, 0.5)
                view.addItem(text)
                try:
                    if self.configuration['converter']:
                        try:
                            actual_converter = self.configuration['converter'][receiver_name]
                            view = status_graphics_widget.addViewBox(row=receiver_index, col=1, lockAspect=True, enableMouse=False)
                            text = pg.TextItem(('Producer\n%s' % receiver_name), border='b', fill=(0,
                                                                                                   0,
                                                                                                   255,
                                                                                                   100), anchor=(0.5,
                                                                                                                 0.5), color=(0,
                                                                                                                              0,
                                                                                                                              0,
                                                                                                                              200))
                            text.setPos(0.5, 0.5)
                            view.addItem(text)
                            view = status_graphics_widget.addViewBox(row=receiver_index, col=3, lockAspect=True, enableMouse=False)
                            text = pg.TextItem(('Converter\n%s' % receiver_settings), border='b', fill=(0,
                                                                                                        0,
                                                                                                        255,
                                                                                                        100), anchor=(0.5,
                                                                                                                      0.5), color=(0,
                                                                                                                                   0,
                                                                                                                                   0,
                                                                                                                                   200))
                            text.setPos(0.5, 0.5)
                            view.addItem(text)
                        except KeyError:
                            pass

                except KeyError:
                    pass


def main():
    args = utils.parse_arguments()
    utils.setup_logging(args.log)
    app = Qt.QApplication(sys.argv)
    win = OnlineMonitorApplication(args.config_file)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()