# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/TimerOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3849 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/07/2018'
from silx.gui import qt
from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Input, Output
from tomwer.core.process.timer import Timer
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.log import TomwerLogger
import functools
_logger = TomwerLogger(__name__)

class _TimerWidget(qt.QWidget):

    def __init__(self, parent, _time=None):
        if _time is not None:
            assert type(_time) is int
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.layout().addWidget(qt.QLabel('time to wait (in sec):', parent=self), 0, 0)
        self._timeLE = qt.QSpinBox(parent=self)
        self._timeLE.setMinimum(0)
        self._timeLE.setValue(_time or 1)
        self.layout().addWidget(self._timeLE, 0, 1)
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 1, 0)
        self.timeChanged = self._timeLE.valueChanged


class TimerOW(widget.OWWidget, Timer):
    name = 'timer'
    id = 'orange.widgets.tomwer.filterow'
    description = 'Simple widget which wait for a defined amont of time andrelease the data'
    icon = 'icons/time.png'
    priority = 200
    category = 'esrfWidgets'
    keywords = ['control', 'timer', 'wait', 'data']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    _waiting_time = Setting(int(1))

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    class Outputs:
        data_out = Output(name='data', type=TomoBase)

    def __init__(self, parent=None):
        """
        """
        widget.OWWidget.__init__(self, parent)
        Timer.__init__(self, wait=(self._waiting_time))
        self._widget = _TimerWidget(parent=self, _time=(self._waiting_time))
        self._widget.setContentsMargins(0, 0, 0, 0)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self._widget)
        self._widget.timeChanged.connect(self._updateTime)

    @Inputs.data_in
    def process(self, scan):
        if scan is None:
            return
        callback = functools.partial(self.Outputs.data_out.send, scan)
        _timer = qt.QTimer(self)
        _timer.singleShot(self._waiting_time * 1000, callback)

    def _updateTime(self, newTime):
        self._waiting_time = newTime