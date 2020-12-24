# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/na_widget.py
# Compiled at: 2017-08-29 09:44:06
"""
A widget fot the network analyzer
"""
from .base_module_widget import ModuleWidget
from .acquisition_module_widget import AcquisitionModuleWidget
from qtpy import QtCore, QtWidgets
import pyqtgraph as pg
from time import time
import numpy as np, sys

class NaWidget(AcquisitionModuleWidget):
    """
    Network Analyzer Tab.
    """
    starting_update_rate = 0.2
    CHUNK_SIZE = 500

    def init_gui(self):
        """
        Sets up the gui
        """
        self.init_main_layout(orientation='vertical')
        self.init_attribute_layout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.setWindowTitle('NA')
        self.win = pg.GraphicsWindow(title='Magnitude')
        self.label_benchmark = pg.LabelItem(justify='right')
        self.win.addItem(self.label_benchmark, row=1, col=0)
        self._last_benchmark_value = np.nan
        self.win_phase = pg.GraphicsWindow(title='Phase')
        self.plot_item = self.win.addPlot(row=1, col=0, title='Magnitude (dB)')
        self.plot_item_phase = self.win_phase.addPlot(row=1, col=0, title='Phase (deg)')
        self.plot_item_phase.setXLink(self.plot_item)
        self.button_single = QtWidgets.QPushButton('Run single')
        self.button_single.my_label = 'Single'
        self.button_continuous = QtWidgets.QPushButton('Run continuous')
        self.button_continuous.my_label = 'Continuous'
        self.button_stop = QtWidgets.QPushButton('Stop')
        self.button_save = QtWidgets.QPushButton('Save curve')
        self.chunks = []
        self.chunks_phase = []
        self.main_layout.addWidget(self.win)
        self.main_layout.addWidget(self.win_phase)
        aws = self.attribute_widgets
        self.attribute_layout.removeWidget(aws['trace_average'])
        self.attribute_layout.removeWidget(aws['curve_name'])
        super(NaWidget, self).init_gui()
        self.arrow = pg.ArrowItem()
        self.arrow.setVisible(False)
        self.arrow_phase = pg.ArrowItem()
        self.arrow_phase.setVisible(False)
        self.plot_item.addItem(self.arrow)
        self.plot_item_phase.addItem(self.arrow_phase)
        self.last_updated_point = 0
        self.last_updated_time = 0
        self.update_running_buttons()
        self.update_period = self.starting_update_rate
        self.x_log_toggled()

    def autoscale(self):
        """
        log_mode = self.module.logscale
        self.plot_item.setLogMode(x=log_mod, y=None) # this seems also needed
        self.plot_item_phase.setLogMode(x=log_mod, y=None)
        """
        self.plot_item.setRange(xRange=[self.module.start_freq, self.module.stop_freq])
        self.plot_item_phase.setRange(xRange=[self.module.start_freq, self.module.stop_freq])

    def clear_curve(self):
        """
        Clear all chunks
        """
        self.update_period = self.starting_update_rate
        while True:
            try:
                chunk = self.chunks.pop()
                chunk_phase = self.chunks_phase.pop()
                chunk.clear()
                chunk_phase.clear()
            except IndexError:
                break

        self.label_benchmark.setText('')

    def x_log_toggled(self):
        """
        change x_log of axis
        """
        log_mod = self.module.logscale
        self.plot_item.setLogMode(x=log_mod, y=None)
        self.plot_item_phase.setLogMode(x=log_mod, y=None)
        for chunk, chunk_phase in zip(self.chunks, self.chunks_phase):
            chunk.setLogMode(xMode=log_mod, yMode=None)
            chunk_phase.setLogMode(xMode=log_mod, yMode=None)

        return

    def scan_finished(self):
        """
        if in run continuous, needs to redisplay the number of averages
        """
        self.update_current_average()
        self.update_point(self.module.points - 1, force=True)

    def set_benchmark_text(self, text):
        self.label_benchmark.setText(text)

    def update_point(self, index, force=False):
        """
        To speed things up, the curves are plotted by chunks of
        self.CHUNK_SIZE points. All points between last_updated_point and
        index will be redrawn.
        """
        last_chunk_index = self.last_updated_point // self.CHUNK_SIZE
        current_chunk_index = index // self.CHUNK_SIZE
        rate = self.module.measured_time_per_point
        if not np.isnan(rate) and self._last_benchmark_value != rate:
            theory = self.module.time_per_point
            self.set_benchmark_text('ms/pt: %.1f (theory: %.1f)' % (
             rate * 1000,
             theory * 1000))
        if force or time() - self.last_updated_time > self.update_period:
            for chunk_index in range(last_chunk_index, current_chunk_index + 1):
                self.update_chunk(chunk_index)

            self.last_updated_point = index
            self.last_updated_time = time()
            cur = self.module.current_point - 1
            visible = self.module.last_valid_point != cur + 1
            logscale = self.module.logscale
            freq = self.module.data_x[cur]
            xpos = np.log10(freq) if logscale else freq
            if cur > 0:
                self.arrow.setPos(xpos, self._magnitude(self.module.data_avg[cur]))
                self.arrow.setVisible(visible)
                self.arrow_phase.setPos(xpos, self._phase(self.module.data_avg[cur]))
                self.arrow_phase.setVisible(visible)

    def _magnitude(self, data):
        return 20.0 * np.log10(np.abs(data) + sys.float_info.epsilon)

    def _phase(self, data):
        return np.angle(data, deg=True)

    def update_attribute_by_name(self, name, new_value_list):
        super(NaWidget, self).update_attribute_by_name(name, new_value_list)
        if name == 'running_state':
            self.update_running_buttons()

    def update_chunk(self, chunk_index):
        """
        updates curve # chunk_index with the data from the module
        """
        while len(self.chunks) <= chunk_index:
            chunk = self.plot_item.plot(pen='y')
            chunk_phase = self.plot_item_phase.plot(pen=None, symbol='o')
            self.chunks.append(chunk)
            self.chunks_phase.append(chunk_phase)
            log_mod = self.module.logscale
            chunk.setLogMode(xMode=log_mod, yMode=None)
            chunk_phase.setLogMode(xMode=log_mod, yMode=None)

        sl = slice(max(0, self.CHUNK_SIZE * chunk_index - 1), min(self.CHUNK_SIZE * (chunk_index + 1), self.module.last_valid_point), 1)
        data = self.module.data_avg[sl]
        x = np.real(self.module.data_x[sl])
        self.chunks[chunk_index].setData(x, self._magnitude(data))
        self.chunks_phase[chunk_index].setData(x, self._phase(data))
        return

    def display_state(self, running_state):
        """
        Displays one of the possible states
        "running_continuous", "running_single", "paused_continuous", "paused_single", "stopped"
        """
        if running_state not in ('running_continuous', 'running_single', 'paused',
                                 'stopped'):
            raise ValueError('Na running_state should be either running_continuous, running_single, paused or stopped')
        if running_state == 'running_continuous':
            self.button_single.setEnabled(False)
            self.button_single.setText('Run single')
            self.button_continuous.setEnabled(True)
            self.button_continuous.setText('Pause')
            return
        if running_state == 'running_single':
            self.button_single.setEnabled(True)
            self.button_single.setText('Pause')
            self.button_continuous.setEnabled(False)
            self.button_continuous.setText('Run continuous')
            return
        if running_state == 'paused':
            self.button_continuous.setText('Resume continuous')
            self.button_single.setText('Run single')
            self.button_continuous.setEnabled(True)
            self.button_single.setEnabled(False)
            return
        if running_state == 'stopped':
            self.button_continuous.setText('Run continuous')
            self.button_single.setText('Run single')
            self.button_continuous.setEnabled(True)
            self.button_single.setEnabled(True)
            return


class MyGraphicsWindow(pg.GraphicsWindow):

    def __init__(self, title, parent_widget):
        super(MyGraphicsWindow, self).__init__(title)
        self.parent_widget = parent_widget
        self.setToolTip("IIR transfer function: \n----------------------\nCTRL + Left click: add one more pole. \nSHIFT + Left click: add one more zero\nLeft Click: select pole (other possibility: click on the '+j' labels below the graph)\nLeft/Right arrows: change imaginary part (frequency) of the current pole or zero\nUp/Down arrows; change the real part (width) of the current pole or zero. \nPoles are represented by 'X', zeros by 'O'")

    def mousePressEvent(self, *args, **kwds):
        event = args[0]
        try:
            try:
                modifier = int(event.modifiers())
                it = self.getItem(0, 0)
                pos = it.mapToScene(event.pos())
                point = it.vb.mapSceneToView(pos)
                x, y = (point.x(), point.y())
                x = 10 ** x
                new_z = -100 - complex(0.0, 1.0) * x
                if modifier == QtCore.Qt.CTRL:
                    self.parent_widget.module.poles += [new_z]
                    self.parent_widget.attribute_widgets['poles'].set_selected(-1)
                if modifier == QtCore.Qt.SHIFT:
                    self.parent_widget.module.zeros += [new_z]
                    self.parent_widget.attribute_widgets['zeros'].set_selected(-1)
            except BaseException as e:
                self.parent_widget.module._logger.error(e)

        finally:
            return super(MyGraphicsWindow, self).mousePressEvent(*args, **kwds)