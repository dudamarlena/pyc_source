# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/models/custom_lockbox_example.py
# Compiled at: 2017-08-29 09:44:06
from pyrpl.software_modules.lockbox import *
from pyrpl.software_modules.loop import *

class CustomInputClass(InputSignal):
    """ A custom input signal for our customized lockbox. Please refer to the documentation on the default API of
    InputSignals"""

    def expected_signal(self, variable):
        return self.calibration_data.min + self.custom_gain_attribute * self.lockbox.custom_attribute * variable ** 2

    def expected_slope(self, variable):
        return 2.0 * self.custom_gain_attribute * self.lockbox.custom_attribute * variable

    _setup_attributes = [
     'custom_gain_attribute']
    _gui_attributes = ['custom_gain_attribute']
    custom_gain_attribute = FloatProperty(default=1.0, min=-10000000000.0, max=10000000000.0, increment=0.01, doc='custom factor for each input signal')

    def calibrate(self):
        """ This is a simplified calibration method. InputSignal.calibrate works better than this in most cases. """
        self.lockbox.sweep()
        curve = self.sweep_acquire()
        self.get_stats_from_curve(curve=curve)


class CustomLockbox(Lockbox):
    """ A custom lockbox class that can be used to implement customized feedback controllers"""
    inputs = LockboxModuleDictProperty(custom_input_name1=CustomInputClass, custom_input_name2=CustomInputClass)
    outputs = LockboxModuleDictProperty(slow_output=OutputSignal, fast_output=OutputSignal, pwm_output=OutputSignal)
    variable = 'displacement'
    custom_attribute = FloatProperty(default=1.0, increment=0.01, min=1e-05, max=100000.0)
    _setup_attributes = [
     'custom_attribute']
    _gui_attributes = [
     'custom_attribute']
    _mV_per_V = 1000.0
    _units = ['V', 'mV']

    def custom_function(self):
        self.calibrate_all()
        self.unlock()
        self.lock()


class ExampleLoop(LockboxPlotLoop):

    def __init__(self, parent, name=None):
        super(ExampleLoop, self).__init__(parent, name=name)
        self.c.n = 0
        self.last_texcess = 0
        self.result_ready = 'not ready'

    def loop(self):
        self.c.n += 1
        tact = time() - self.plot.plot_start_time
        tmin = self.interval * self.c.n
        texcess = tact - tmin
        dt = texcess - self.last_texcess
        self.last_texcess = texcess
        self.plot.append(green=np.sin(2.0 * np.pi * tact * 3), red=dt)
        if self.c.n == 100:
            self.result = 42
            self.result_ready = True
            self._clear()


class ExampleLoopLockbox(Lockbox):
    loop = None
    _gui_attributes = ['start', 'stop', 'interval']
    interval = FloatProperty(default=0.01, min=0)

    def start(self):
        self.stop()
        self.loop = ExampleLoop(parent=self, name='example_loop', interval=self.interval)

    def stop(self):
        if self.loop is not None:
            self.loop._clear()
            self.loop = None
        return


class GalvanicIsolationLoopLockbox(Lockbox):
    """ an example for a loop fully described in the lockbox class definition"""
    _gui_attributes = [
     'start_gi', 'stop_gi', 'gi_interval']
    gi_interval = FloatProperty(default=0.05, min=0, max=10000000000.0, doc='Minimum interval at which the loop updates the second redpitaya output')

    def start_gi(self):
        self.stop_gi()
        if not hasattr(self, 'second_pyrpl') or self.second_pyrpl is None:
            from pyrpl import Pyrpl
            self.second_pyrpl = Pyrpl('second_redpitaya', hostname='_FAKE_REDPITAYA_')
        self.galvanic_isolation_loop = LockboxLoop(parent=self, name='galvanic_isolation_loop', interval=self.gi_interval, loop_function=self.galvanic_isolation_loop_function)
        return

    def galvanic_isolation_loop_function(self):
        """ the loop function to be executed"""
        self.second_pyrpl.rp.asg0.offset = self.pyrpl.rp.sampler.pid0

    def stop_gi(self):
        if hasattr(self, 'galvanic_isolation_loop') and self.galvanic_isolation_loop is not None:
            self.galvanic_isolation_loop._clear()
        self.galvanic_isolation_loop = None
        return


class ShortLoopLockbox(Lockbox):
    """ an example for very short loop description"""

    def plot_sin_and_in1(lockbox_self, loop_self):
        """ if you pass an instance_method of the lockbox, it should take two arguments:
        the instance of the lockbox (self) and the instance of the loop"""
        loop_self.plot.append(green=np.sin(2 * np.pi * loop_self.time), red=lockbox_self.pyrpl.rp.sampler.in1)
        if loop_self.n > 100:
            loop_self._clear()

    loop = ModuleProperty(LockboxPlotLoop, interval=0.05, autostart=True, loop_function=plot_sin_and_in1)