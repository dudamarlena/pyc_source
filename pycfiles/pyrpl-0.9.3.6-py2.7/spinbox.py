# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/spinbox.py
# Compiled at: 2017-08-29 09:44:06
from qtpy import QtCore, QtWidgets, QtGui
import numpy as np, time, sys
if sys.version_info < (3,):
    integer_types = (
     int, long)
else:
    integer_types = (
     int,)

class NumberSpinBox(QtWidgets.QWidget):
    """
    Base class for spinbox with numerical value.

    The button can be either in log_increment mode, or linear increment.
       - In log_increment: the halflife_seconds value determines how long it
         takes when the user keeps clicking on the "*"/"/" buttons to change
         the value by a factor 2. Since the underlying register is assumed to
         be represented by an int, its values are separated by a minimal
         separation, called "increment". The time to wait before refreshing
         the value is adjusted automatically so that the log behavior is still
         correct, even when the value becomes comparable to the increment.
       - In linear increment, the value is immediately incremented by the
        increment, then, nothing happens during a time given by
        timer_initial_latency. Only after that the value is incremented by
        "increment" every timer_min_interval.
    """
    MOUSE_WHEEL_ACTIVATED = False
    value_changed = QtCore.Signal()
    selected = QtCore.Signal(list)
    change_interval = 0.02
    _change_initial_latency = 0.1

    @property
    def change_initial_latency(self):
        """ latency for continuous update when a button is pressed """
        if self.singleStep != 0:
            return self._change_initial_latency
        else:
            return 0

    def forward_to_subspinboxes(func):
        """
        a decorator that forwards function calls to subspinboxes
        """

        def func_wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        return func_wrapper

    def __init__(self, label='', min=-1, max=1, increment=0.0001220703125, log_increment=False, halflife_seconds=0.5, per_second=0.2):
        """
        :param label: label of the button
        :param min: min value
        :param max: max value
        :param increment: increment of the underlying register
        :param log_increment: boolean: when buttons up/down are pressed, should the value change linearly or log
        :param halflife_seconds: when button is in log, how long to change the value by a factor 2.
        :param per_second: when button is in lin, how long to change the value by 1 unit.
        """
        super(NumberSpinBox, self).__init__(None)
        self._val = 0
        self.labeltext = label
        self.log_increment = log_increment
        self.minimum = min
        self.maximum = max
        self.halflife_seconds = halflife_seconds
        self.per_second = per_second
        self.singleStep = increment
        self.change_timer = QtCore.QTimer()
        self.change_timer.setSingleShot(True)
        self.change_timer.setInterval(int(np.ceil(self.change_interval * 1000)))
        self.change_timer.timeout.connect(self.continue_step)
        self.make_layout()
        self.update_tooltip()
        self.set_min_size()
        self.val = 0
        return

    def make_layout(self):
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        self.setLayout(self.lay)
        if self.labeltext is not None:
            self.label = QtWidgets.QLabel(self.labeltext)
            self.lay.addWidget(self.label)
        if self.log_increment:
            self.up = QtWidgets.QPushButton('*')
            self.down = QtWidgets.QPushButton('/')
        else:
            self.up = QtWidgets.QPushButton('+')
            self.down = QtWidgets.QPushButton('-')
        self.line = QtWidgets.QLineEdit()
        self.line.setStyleSheet('QLineEdit { qproperty-cursorPosition: 0; }')
        self.lay.addWidget(self.down)
        self.lay.addWidget(self.line)
        self.lay.addWidget(self.up)
        self.up.setMaximumWidth(15)
        self.down.setMaximumWidth(15)
        self.up.pressed.connect(self.first_step)
        self.down.pressed.connect(self.first_step)
        self.up.released.connect(self.finish_step)
        self.down.released.connect(self.finish_step)
        self.line.editingFinished.connect(self.validate)
        self._button_up_down = False
        self._button_down_down = False
        return

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Right]:
                self._button_up_down = True
                self._button_down_down = False
                self.first_step()
            elif event.key() in [QtCore.Qt.Key_Down, QtCore.Qt.Key_Left]:
                self._button_down_down = True
                self._button_up_down = False
                self.first_step()
            else:
                return super(NumberSpinBox, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            if event.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Right]:
                self._button_up_down = False
                self.finish_step()
            elif event.key() in [QtCore.Qt.Key_Down, QtCore.Qt.Key_Left]:
                self._button_down_down = False
                self.finish_step()
            else:
                return super(NumberSpinBox, self).keyReleaseEvent(event)

    @property
    def is_increasing(self):
        return self.up.isDown() or self._button_up_down

    @property
    def is_decreasing(self):
        return self.down.isDown() or self._button_down_down

    @property
    def change_sign(self):
        if self.is_increasing:
            return 1.0
        else:
            if self.is_decreasing:
                return -1.0
            return 0.0

    def wheelEvent(self, event):
        """
        Handle mouse wheel event. No distinction between linear and log.
        :param event:
        :return:
        """
        if self.MOUSE_WHEEL_ACTIVATED:
            nsteps = int(event.delta() / 120)
            func = self.step_up if nsteps > 0 else self.step_down
            for i in range(abs(nsteps)):
                func(single_increment=True)

    def set_min_size(self):
        """
        sets the min size for content to fit.
        """
        font = QtGui.QFont('', 0)
        font_metric = QtGui.QFontMetrics(font)
        pixel_wide = font_metric.width('0' * self.max_num_letter)
        self.line.setFixedWidth(pixel_wide)

    @property
    def max_num_letter(self):
        """
        Returns the maximum number of letters
        """
        return 5

    def set_log_increment(self):
        self.up.setText('↑')
        self.down.setText('↓')
        self.log_increment = True

    def update_tooltip(self):
        """
        The tooltip uses the values of min/max/increment...
        """
        string = 'Increment is %.5e\nmin value: %.1e\nmax value: %.1e\n' % (
         self.singleStep, self.minimum, self.maximum)
        string += 'Press up/down to tune.'
        self.setToolTip(string)

    def setDecimals(self, val):
        self.decimals = val
        self.set_min_size()

    def validate(self):
        """ make sure a new value is inside the allowed bounds after a
        manual change of the value """
        if self.line.isModified():
            self.setValue(self.saturate(self.val))
            self.value_changed.emit()

    def saturate(self, val):
        if val > self.maximum:
            return self.maximum
        else:
            if val < self.minimum:
                return self.minimum
            return val

    def setMaximum(self, val):
        self.maximum = val
        self.update_tooltip()

    def setMinimum(self, val):
        self.minimum = val
        self.update_tooltip()

    def setSingleStep(self, val):
        self.singleStep = val

    def set_per_second(self, val):
        self.per_second = val

    def setValue(self, val):
        """ replace this function with something useful in derived classes """
        self.val = val

    def value(self):
        """ replace this function with something useful in derived classes """
        return self.val

    def first_step(self):
        """
        Once +/- pressed for timer_initial_latency ms, start to update continuously
        """
        self.start_time = time.time()
        self.start_value = self.value()
        value = self.start_value + self.singleStep * self.change_sign
        if np.sign(value) * np.sign(self.start_value) < 0:
            value = 0
        self.setValue(self.saturate(value))
        if self.log_increment and self.start_value == 0:
            self.start_value = self.value()
        self.change_timer.start()

    def continue_step(self):
        dt = time.time() - self.start_time
        if dt > self.change_initial_latency:
            if self.log_increment:
                if self.start_value == 0:
                    return self.first_step()
                sign = self.change_sign * np.sign(self.start_value)
                halflifes = dt / self.halflife_seconds * sign
                value = self.start_value * 2 ** halflifes
                if abs(value) <= self.singleStep / 2.0 and sign < 0:
                    self.start_value = 0
                    value = 0
                    self.start_time = time.time()
            else:
                value = self.start_value + self.per_second * dt * self.change_sign
                if np.sign(value) * np.sign(self.start_value) < 0:
                    self.start_value = 0
                    value = 0
                    self.start_time = time.time()
            if abs(self.val - value) > self.singleStep:
                self.setValue(self.saturate(value))
        self.change_timer.start()

    def finish_step(self):
        self.change_timer.stop()
        if hasattr(self, 'start_time'):
            dt = time.time() - self.start_time
        else:
            dt = 0
        if dt > self.change_initial_latency:
            self.validate()


class IntSpinBox(NumberSpinBox):
    """
    Number spin box for integer values
    """

    def __init__(self, label, min=-8192, max=8192, increment=1, per_second=10, **kwargs):
        super(IntSpinBox, self).__init__(label=label, min=min, max=max, increment=increment, per_second=per_second, **kwargs)

    @property
    def val(self):
        return int(str(self.line.text()))

    @val.setter
    def val(self, new_val):
        self.line.setText('%.i' % round(new_val))
        self.value_changed.emit()
        return new_val

    @property
    def max_num_letter(self):
        """
        Maximum number of letters in line
        """
        if np.isinf(self.maximum):
            return super(IntSpinBox, self).max_num_letter
        else:
            return int(np.log10(np.abs(self.maximum)) + 1)

    def setMaximum(self, val):
        super(IntSpinBox, self).setMaximum(val)
        self.set_min_size()


class FloatSpinBox(NumberSpinBox):
    """
    Number spin box for float values
    """

    def __init__(self, label, decimals=4, min=-1, max=1, increment=0.0001220703125, **kwargs):
        self.decimals = decimals
        super(FloatSpinBox, self).__init__(label=label, min=min, max=max, increment=increment, **kwargs)

    @property
    def val(self):
        if str(self.line.text()) != ('%.' + str(self.decimals) + 'e') % self._val:
            return float(str(self.line.text()))
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = self.saturate(new_val)
        self.line.blockSignals(True)
        self.line.setText(('{:.' + str(self.decimals) + 'e}').format(float(new_val)))
        self.line.blockSignals(False)
        self.value_changed.emit()
        return new_val

    @property
    def max_num_letter(self):
        """
        Returns the maximum number of letters
        """
        return self.decimals + 7


class ComplexSpinBox(FloatSpinBox):
    """
    Two spinboxes representing a complex number, with the right keyboard
    shortcuts (up down for imag, left/right for real).
    """

    def forward_to_subspinboxes(func):
        """
        a decorator that forwards function calls to subspinboxes
        """

        def func_wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        return func_wrapper

    def __init__(self, *args, **kwargs):
        super(ComplexSpinBox, self).__init__(*args, **kwargs)

    def make_layout(self):
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.real = FloatSpinBox(label=self.labeltext, min=self.minimum, max=self.maximum, increment=self.singleStep, log_increment=self.log_increment, halflife_seconds=self.halflife_seconds, decimals=self.decimals)
        self.imag = FloatSpinBox(label=self.labeltext, min=self.minimum, max=self.maximum, increment=self.singleStep, log_increment=self.log_increment, halflife_seconds=self.halflife_seconds, decimals=self.decimals)
        self.real.value_changed.connect(self.value_changed)
        self.lay.addWidget(self.real)
        self.label = QtWidgets.QLabel(' + j')
        self.lay.addWidget(self.label)
        self.imag.value_changed.connect(self.value_changed)
        self.lay.addWidget(self.imag)
        self.setLayout(self.lay)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    @property
    def val(self):
        return complex(self.real.val, self.imag.val)

    @val.setter
    def val(self, new_val):
        self.real.val = np.real(new_val)
        self.imag.val = np.imag(new_val)
        return new_val

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left]:
            return self.imag.keyPressEvent(event)
        else:
            return self.real.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left]:
            return self.imag.keyReleaseEvent(event)
        else:
            return self.real.keyReleaseEvent(event)

    def wheelEvent(self, event):
        return self.imag.wheelEvent(event)

    def setFixedWidth(self, *args, **kwargs):
        self.real.setFixedWidth(*args, **kwargs)
        return self.imag.setFixedWidth(*args, **kwargs)

    def set_min_size(self, *args, **kwargs):
        self.real.set_min_size(*args, **kwargs)
        return self.imag.set_min_size(*args, **kwargs)

    def update_tooltip(self, *args, **kwargs):
        self.real.update_tooltip(*args, **kwargs)
        return self.imag.update_tooltip(*args, **kwargs)

    def setDecimals(self, *args, **kwargs):
        self.real.setDecimals(*args, **kwargs)
        return self.imag.setDecimals(*args, **kwargs)

    def set_per_second(self, *args, **kwargs):
        self.real.set_per_second(*args, **kwargs)
        return self.imag.set_per_second(*args, **kwargs)

    def setMaximum(self, *args, **kwargs):
        self.real.setMaximum(*args, **kwargs)
        return self.imag.setMaximum(*args, **kwargs)

    def setMinimum(self, *args, **kwargs):
        self.real.setMinimum(*args, **kwargs)
        return self.imag.setMinimum(*args, **kwargs)

    def setSingleStep(self, *args, **kwargs):
        self.real.setSingleStep(*args, **kwargs)
        return self.imag.setSingleStep(*args, **kwargs)

    def set_log_increment(self, *args, **kwargs):
        self.real.set_log_increment(*args, **kwargs)
        self.imag.set_log_increment(*args, **kwargs)
        self.imag.up.setText('→')
        self.imag.down.setText('←')