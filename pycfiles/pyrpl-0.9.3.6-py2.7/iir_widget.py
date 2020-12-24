# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/module_widgets/iir_widget.py
# Compiled at: 2017-08-29 09:44:06
"""
The Iir widget allows to dynamically select zeros and poles of the iir filter
"""
from .base_module_widget import ModuleWidget
from collections import OrderedDict
from qtpy import QtCore, QtWidgets
import pyqtgraph as pg, numpy as np, sys
from ... import APP

class MyGraphicsWindow(pg.GraphicsWindow):

    def __init__(self, title, parent):
        super(MyGraphicsWindow, self).__init__(title)
        self.parent = parent
        self.setToolTip("IIR transfer function: \n----------------------\nCTRL + Left click: add one more pole. \nSHIFT + Left click: add one more zero\nLeft Click: select pole (other possibility: click on the '+j' labels below the graph)\nLeft/Right arrows: change imaginary part (frequency) of the current pole or zero\nUp/Down arrows; change the real part (width) of the current pole or zero. \nPoles are represented by 'X', zeros by 'O'")
        self.doubleclicked = False
        self.mouse_clicked_timer = QtCore.QTimer()
        self.mouse_clicked_timer.setSingleShot(True)
        self.mouse_clicked_timer.setInterval(APP.doubleClickInterval())
        self.mouse_clicked_timer.timeout.connect(self.mouse_clicked)

    def mousePressEvent(self, event):
        self.doubleclicked = False
        self.storeevent(event)
        if self.button == QtCore.Qt.LeftButton and self.modifier == 0:
            self.parent.module.select_pole_or_zero(self.x)
        if not self.mouse_clicked_timer.isActive():
            self.mouse_clicked_timer.start()
        return super(MyGraphicsWindow, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.doubleclicked = True
        self.storeevent(event)
        if self.mouse_clicked_timer.isActive():
            self.mouse_clicked_timer.stop()
            self.mouse_clicked()
        return super(MyGraphicsWindow, self).mouseDoubleClickEvent(event)

    def storeevent(self, event):
        self.button = event.button()
        self.modifier = int(event.modifiers())
        it = self.getItem(0, 0)
        pos = it.mapToScene(event.pos())
        point = it.vb.mapSceneToView(pos)
        self.x, self.y = point.x(), point.y()
        if self.parent.xlog:
            self.x = 10 ** self.x

    def mouse_clicked(self):
        default_damping = self.x / 10.0
        if self.button == QtCore.Qt.LeftButton:
            if self.doubleclicked:
                new = -default_damping - complex(0.0, 1.0) * self.x
                if self.modifier == QtCore.Qt.CTRL:
                    self.parent.module.complex_poles.append(new)
                if self.modifier == QtCore.Qt.SHIFT:
                    self.parent.module.complex_zeros.append(new)
            else:
                new = -self.x
                if self.modifier == 0:
                    pass
                if self.modifier == QtCore.Qt.CTRL:
                    self.parent.module.real_poles.append(new)
                if self.modifier == QtCore.Qt.SHIFT:
                    self.parent.module.real_zeros.append(new)

    def keyPressEvent(self, event):
        """ not working properly yet"""
        try:
            name = self.parent.module._selected_pole_or_zero
            index = self.parent.module._selected_index
            return self.parent.parent.attribute_widgets[name].widgets[index].keyPressEvent(event)
        except:
            return super(MyGraphicsWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """ not working properly yet"""

        def keyPressEvent(self, event):
            try:
                name = self.parent.module._selected_pole_or_zero
                index = self.parent.module._selected_index
                return self.parent.parent.attribute_widgets[name].widgets[index].keyReleaseEvent(event)
            except:
                return super(MyGraphicsWindow, self).keyReleaseEvent(event)


class IirGraphWidget(QtWidgets.QGroupBox):
    xlog = True

    def __init__(self, parent):
        self.name = 'Transfer functions'
        super(IirGraphWidget, self).__init__(parent)
        self.parent = parent
        self.module = self.parent.module
        self.layout = QtWidgets.QVBoxLayout(self)
        self.win = MyGraphicsWindow(title='Amplitude', parent=self)
        self.win_phase = MyGraphicsWindow(title='Phase', parent=self)
        self.mag = self.win.addPlot(title='Magnitude (dB)')
        self.phase = self.win_phase.addPlot(title='Phase (deg)')
        self.phase.setXLink(self.mag)
        self.plots = OrderedDict()
        for name, style in [('data', dict(pen='g')),
         (
          'filter_design', dict(pen='y')),
         (
          'data_x_design', dict(pen='r'))]:
            self.plots[name] = self.mag.plot(**style)
            self.plots[name + '_phase'] = self.phase.plot(**style)
            self.plots[name].setLogMode(xMode=self.xlog, yMode=None)
            self.plots[(name + '_phase')].setLogMode(xMode=self.xlog, yMode=None)

        for name, style in [
         ('filter_measurement',
          dict(symbol='o', size=10, pen='b')),
         (
          'zeros',
          dict(pen=pg.mkPen(None), symbol='o', size=10, brush=pg.mkBrush(255, 0, 255, 120))),
         (
          'poles',
          dict(size=15, symbol='x', pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 255, 120)))]:
            item = pg.ScatterPlotItem(**style)
            self.mag.addItem(item)
            self.plots[name] = item
            item = pg.ScatterPlotItem(**style)
            self.phase.addItem(item)
            self.plots[name + '_phase'] = item

        self.mag.setLogMode(x=self.xlog, y=None)
        self.phase.setLogMode(x=self.xlog, y=None)
        self.layout.addWidget(self.win)
        self.layout.addWidget(self.win_phase)
        return


class IirButtonWidget(QtWidgets.QGroupBox):
    BUTTONWIDTH = 100

    def __init__(self, parent):
        self.name = 'General settings'
        super(IirButtonWidget, self).__init__(parent)
        self.parent = parent
        self.module = self.parent.module
        self.layout = QtWidgets.QVBoxLayout(self)
        aws = self.parent.attribute_widgets
        for attr in ['input', 'inputfilter', 'output_direct', 'loops',
         'gain', 'on', 'bypass', 'overflow']:
            widget = aws[attr]
            widget.setFixedWidth(self.BUTTONWIDTH)
            self.layout.addWidget(widget)

        self.setFixedWidth(self.BUTTONWIDTH + 50)


class IirBottomWidget(QtWidgets.QGroupBox):
    BUTTONWIDTH = 300

    def __init__(self, parent):
        self.name = 'Filter poles and zeros'
        super(IirBottomWidget, self).__init__(parent)
        self.parent = parent
        self.module = self.parent.module
        self.layout = QtWidgets.QHBoxLayout(self)
        aws = self.parent.attribute_widgets
        for attr in ['complex_poles', 'complex_zeros',
         'real_poles', 'real_zeros']:
            widget = aws[attr]
            widget.setFixedWidth(self.BUTTONWIDTH)
            self.layout.addWidget(widget)


class IirWidget(ModuleWidget):

    def init_gui(self):
        self.module.setup()
        self.init_main_layout(orientation='vertical')
        self.init_attribute_layout()
        for widget in self.attribute_widgets.values():
            self.main_layout.removeWidget(widget)

        self.top_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.graph_widget = IirGraphWidget(self)
        self.top_layout.addWidget(self.graph_widget)
        self.button_widget = IirButtonWidget(self)
        self.top_layout.addWidget(self.button_widget)
        self.bottom_widget = IirBottomWidget(self)
        self.main_layout.addWidget(self.bottom_widget)
        self.attribute_widgets['data_curve'].setStyleSheet('color: green')
        self.update_plot()

    def select_pole(self, plot_item, spots):
        index = spots[0].data()
        self.attribute_widgets['poles'].set_selected(index)

    def select_zero(self, plot_item, spots):
        index = spots[0].data()
        self.attribute_widgets['zeros'].set_selected(index)

    @property
    def frequencies(self):
        try:
            f = self.module._data_curve_object.data.index.values
        except AttributeError:
            return np.logspace(1, np.log10(5000000.0), 2000)

        f[f <= 0] = sys.float_info.epsilon
        return np.asarray(f, dtype=float)

    def _magnitude(self, data):
        return 20.0 * np.log10(np.abs(np.asarray(data, dtype=np.complex)) + sys.float_info.epsilon)

    def _phase(self, data):
        return np.angle(np.asarray(data, dtype=np.complex), deg=True)

    def update_plot(self):
        tfargs = {}
        frequencies = self.frequencies
        plot = OrderedDict()
        try:
            plot['data'] = self.module._data_curve_object.data.values
        except AttributeError:
            plot['data'] = []

        plot['filter_design'] = self.module.transfer_function(frequencies, **tfargs)
        try:
            plot['data_x_design'] = plot['data'] / plot['filter_design']
        except ValueError:
            try:
                plot['data_x_design'] = 1.0 / plot['filter_design']
            except:
                plot['data_x_design'] = []

        for k, v in plot.items():
            self.graph_widget.plots[k].setData(frequencies[:len(v)], self._magnitude(v))
            self.graph_widget.plots[(k + '_phase')].setData(frequencies[:len(v)], self._phase(v))

        aws = self.attribute_widgets
        for end in ['poles', 'zeros']:
            mag, phase = [], []
            for start in ['complex', 'real']:
                key = start + '_' + end
                freq = getattr(self.module, key)
                if start == 'complex':
                    freq = np.imag(freq)
                freq = np.abs(freq)
                tf = self.module.transfer_function(freq, **tfargs)
                selected = aws[key].attribute_value.selected
                brush = [ pg.mkBrush(color='b') if num == selected else pg.mkBrush(color='y') for num in range(aws[key].number)
                        ]
                mag += [ {'pos': (fr, val), 'data': i, 'brush': br} for i, (fr, val, br) in enumerate(zip(list(np.log10(freq)), list(self._magnitude(tf)), brush))
                       ]
                phase += [ {'pos': (fr, val), 'data': i, 'brush': br} for i, (fr, val, br) in enumerate(zip(list(np.log10(freq)), list(self._phase(tf)), brush))
                         ]

            self.graph_widget.plots[end].setPoints(mag)
            self.graph_widget.plots[(end + '_phase')].setPoints(phase)

    def keyPressEvent(self, event):
        """ not working properly yet"""
        try:
            name = self.module._selected_pole_or_zero
            index = self.module._selected_index
            return self.attribute_widgets[name].widgets[index].keyPressEvent(event)
        except:
            return super(MyGraphicsWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """ not working properly yet"""

        def keyPressEvent(self, event):
            try:
                name = self.module._selected_pole_or_zero
                index = self.module._selected_index
                return self.attribute_widgets[name].widgets[index].keyReleaseEvent(event)
            except:
                return super(MyGraphicsWindow, self).keyReleaseEvent(event)