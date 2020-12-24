# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/acquisition_module.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = '\nEverything involving asynchronicity in acquisition instruments is in this file.\n\nIn particular, this includes getting curves and continuously averaging curves.\n\nUsing the coroutine syntax introduced in python 3.4+ would make the code\nmore elegant, but it would not be compatible with python 2.7. Hence we have\nchosen to implement all asynchronous methods such that a promise is returned (a\nFuture-object in python). The promise implements the following methods:\n\n- await_result(): returns the acquisition result once it is ready.\n- add_done_callback(func): the function func(value) is used as "done-callback)\n\nAll asynchronous methods also have a blocking equivalent that directly\nreturns the result once it is ready:\n\n- curve_async  <---> curve\n- single_async <---> single\n\nFinally, this implmentation using standard python Futures makes it\npossible to use transparently pyrpl asynchronous methods inside python 3.x\ncoroutines.\n\nExample:\n\n    This example shows a typical acquisition use case where a sequence of\n    n aquisitions of simultaneous oscilloscope and network analyzer traces\n    are launched\n    ::\n\n        from asyncio import ensure_future, event_loop\n\n        async def my_acquisition_routine(n):\n            for i in range(n):\n                print("acquiring scope")\n                fut = ensure_future(p.rp.scope.run_single())\n                print("acquiring na")\n                data2 = await p.networkanalyzer.run_single()\n                # both acquisitions are carried out simultaneously\n                data1 = await fut\n                print("loop %i"%i, data1, data2)\n\n        ensure_future(my_acquisition_coroutine(10))\n        eventloop.run_until_complete()\n'
from copy import copy
from .module_attributes import *
from .async_utils import PyrplFuture, Future, MainThreadTimer, CancelledError

class AcquisitionError(ValueError):
    pass


class CurveFuture(PyrplFuture):
    """
    The basic acquisition of instruments is an asynchronous process:

    For instance, when the scope acquisition has been launched, we know
    that the curve won't be ready before duration(), but if the scope is
    waiting for a trigger event, this could take much longer. Of course,
    we want the event loop to stay alive while waiting for a pending curve.
    That's the purpose of this future object.

    After its creation, it will perform the following actions:

        1. stay inactive for a time given by instrument._remaining_time()
        2. after that, it will check every min_refresh_delay if a new curve is ready with instrument._data_ready()
        3. when data is ready, its result will be set with the instrument data, as returned by instrument._get_data()

    """

    def __init__(self, module, min_delay_ms=20):
        self._module = module
        self.min_delay_ms = min_delay_ms
        super(CurveFuture, self).__init__()
        self._init_timer()
        self._module._start_acquisition()

    def _init_timer(self):
        if self.min_delay_ms == 0:
            delay = self._module._remaining_time() * 1000 - 1
        else:
            delay = max(self.min_delay_ms, self._module._remaining_time() * 1000)
        self._timer = MainThreadTimer(max(0, delay))
        self._timer.timeout.connect(self._set_data_as_result)
        self._timer.start()

    def _get_one_curve(self):
        if self._module._data_ready():
            return self._module._get_curve()
        else:
            return
            return

    def _set_data_as_result(self):
        data = self._get_one_curve()
        if data is not None:
            self.set_result(data)
            if self._module.running_state in ('paused', 'stopped'):
                self._module._free_up_resources()
        else:
            self._timer.setInterval(self.min_delay_ms)
            self._timer.start()
        return

    def set_exception(self, exception):
        self._timer.stop()
        super(CurveFuture, self).set_exception(exception)

    def cancel(self):
        self._timer.stop()
        super(CurveFuture, self).cancel()


class RunFuture(PyrplFuture):
    """
    Uses several CurveFuture to perform an average.

    2 extra functions are provided to control the acquisition:

    pause(): stalls the acquisition

    start(): (re-)starts the acquisition (needs to be called at the beginning)

    The format for curves are:

    - Scope:
        - data_x  : self.times
        - data_avg: np.array((ch1, ch2))
    - Specan or NA:
        - data_x  : frequencies
        - data_avg: np.array(y_complex)
    """

    def __init__(self, module, min_delay_ms):
        self._run_continuous = False
        self._module = module
        self._min_delay_ms = min_delay_ms
        super(RunFuture, self).__init__()
        self.data_avg = None
        self.data_x = copy(self._module.data_x)
        self._fut = None
        self.current_avg = 0
        self._paused = True
        return

    def _new_curve_arrived(self, curve):
        try:
            result = curve.result()
        except (AcquisitionError, CancelledError):
            if self._module.running_state in ('running_continuous', 'running_single'):
                return
            self.cancel()

        if self._module.running_state in ('running_continuous', 'running_single'):
            self.current_avg = min(self.current_avg + 1, self._module.trace_average)
            if self.data_avg is None:
                self.data_avg = result
            else:
                self.data_avg = (self.data_avg * (self.current_avg - 1) + result) / self.current_avg
            self._module._emit_signal_by_name('display_curve', [
             self._module.data_x,
             self.data_avg])
            if self._is_run_over():
                if not self.done():
                    self.set_result(self.data_avg)
                    self._module.running_state = 'stopped'
            elif not self._paused:
                self.start()
        return

    def _is_run_over(self):
        if self._run_continuous:
            return False
        else:
            return self.current_avg >= self._module.trace_average

    def cancel(self):
        self.pause()
        super(RunFuture, self).cancel()

    def pause(self):
        self._paused = True
        self._module._free_up_resources()
        if self._fut is not None:
            self._fut.cancel()
        return

    def start(self):
        self._paused = False
        if self._fut is not None:
            self._fut.cancel()
        self._fut = self._module._curve_async(self._min_delay_ms)
        self._fut.add_done_callback(self._new_curve_arrived)
        return

    def _set_run_continuous(self):
        """
        Makes the RunFuture continuous (used when setting "running_continuous")
        """
        self._run_continuous = True
        self._min_delay_ms = self._module.MIN_DELAY_CONTINUOUS_MS


class RunningStateProperty(SelectProperty):

    def __init__(self, options=[
 'running_single', 'running_continuous', 'paused', 'stopped'], **kwargs):
        """
        A property to indicate whether the instrument is currently running or not.

        Changing the running_state performs the necessary actions to enable the
        selected state. The state can be one of the following:

        - 'running_single': takes a single acquisition (trace_average averages). Acquisitions are automatically restarted until the desired number of averages is acquired.
        - 'running_continuous': continuously takes a acquisitions, eternally averages and restarts automatically.
        - 'paused': acquisition interrupted, but no need to restart averaging at next call of running_continous.
        - 'stopped': acquisition interrupted, averaging will restart at next call of running_continuous.
        """
        super(RunningStateProperty, self).__init__(options=options, **kwargs)

    def set_value(self, obj, val):
        """
        This is the master property: changing this value triggers all the logic
        to change the acquisition mode
        """
        obj._curve_future.cancel()
        previous_state = obj.running_state
        SelectProperty.set_value(self, obj, val)
        if val == 'running_single':
            obj.setup()
        elif val == 'running_continuous':
            if previous_state == 'stopped':
                obj.setup()
            else:
                obj._run_future._set_run_continuous()
                obj._run_future.start()
        elif val in ('paused', 'stopped'):
            if hasattr(obj, '_run_future'):
                obj._run_future.cancel()


class SignalLauncherAcquisitionModule(SignalLauncher):
    """ class that takes care of emitting signals to update all possible
    displays"""
    display_curve = QtCore.Signal(list)
    autoscale_x = QtCore.Signal()
    update_point = QtCore.Signal(int)
    scan_finished = QtCore.Signal()
    clear_curve = QtCore.Signal()
    x_log_toggled = QtCore.Signal()
    unit_changed = QtCore.Signal()


class AcquisitionModule(Module):
    """
    The asynchronous mode is supported by a sub-object "run"
    of the module. When an asynchronous acquisition is running
    and the widget is visible, the current averaged data are
    automatically displayed. Also, the run object provides a
    function save_curve to store the current averaged curve
    on the hard-drive.

    The full API of the "run" object is the following.

    Methods:
        *(All methods return immediately)*
        single(): performs an asynchronous acquisition of trace_average curves.
            The function returns a promise of the result:
            an object with a ready() function, and a get() function that
            blocks until data is ready.
        continuous(): continuously acquires curves, and performs a
            moving average over the trace_average last ones.
        pause(): stops the current acquisition without restarting the
            averaging
        stop(): stops the current acquisition and restarts the averaging.
        save_curve(): saves the currently averaged curve (or curves for scope)
        curve(): the currently averaged curve

    Attributes:
        curve_name (str): name of the curve to create upon saving
        trace_average (int): number of averages in single (not to confuse with
            averaging per point)
        data_avg (array of numbers): array containing the current averaged curve
        current_avg (int): current number of averages
    """
    _gui_attributes = [
     'trace_average', 'curve_name']
    _setup_on_load = True
    _signal_launcher = SignalLauncherAcquisitionModule
    _setup_attributes = ['running_state', 'trace_average', 'curve_name']
    _run_future_cls = RunFuture
    _curve_future_cls = CurveFuture
    MIN_DELAY_SINGLE_MS = 0
    MIN_DELAY_CONTINUOUS_MS = 40
    running_state = RunningStateProperty(default='stopped', doc='Indicates whether the instrument is running acquisitions or not. See :class:`RunningStateProperty` for available options. ')
    trace_average = IntProperty(doc='number of curves to average in single mode. In continuous mode, a moving window average is performed.', default=1, min=1)
    curve_name = StringProperty(doc='name of the curve to save.')

    def __init__(self, parent, name=None):
        self._curve_future = Future()
        super(AcquisitionModule, self).__init__(parent, name=name)
        self.curve_name = self.name + ' curve'
        self._run_future = self._run_future_cls(self, min_delay_ms=self.MIN_DELAY_SINGLE_MS)

    def _new_curve_future(self, min_delay_ms):
        self._curve_future.cancel()
        self._curve_future = self._curve_future_cls(self, min_delay_ms=min_delay_ms)

    def _new_run_future(self):
        if hasattr(self, '_run_future'):
            self._run_future.cancel()
        if self.running_state == 'running_continuous':
            self._run_future = self._run_future_cls(self, min_delay_ms=self.MIN_DELAY_CONTINUOUS_MS)
            self._run_future._set_run_continuous()
        else:
            self._run_future = self._run_future_cls(self, min_delay_ms=self.MIN_DELAY_SINGLE_MS)

    def _emit_signal_by_name(self, signal_name, *args, **kwds):
        """Let's the module's signal_launcher emit signal name"""
        self._signal_launcher.emit_signal_by_name(signal_name, *args, **kwds)

    def _curve_async(self, min_delay_ms):
        """
        Same as curve_async except this function can be used in any
        running_state.
        """
        self._start_acquisition()
        self._new_curve_future(min_delay_ms=min_delay_ms)
        return self._curve_future

    def curve_async(self):
        """
        Launches the acquisition for one curve with the current parameters.

        - If running_state is not "stopped", stops the current acquisition.
        - If rolling_mode is True, raises an exception.
        - Immediately returns a future object representing the curve.
        - The curve can be retrieved by calling result(timeout) on the future object.
        - The future is cancelled if the instrument's state is changed before the end of the acquisition, or another call to curve_async() or curve() is made on the same instrument.
        """
        if self.running_state is not 'stopped':
            self.stop()
        return self._curve_async(0)

    def curve(self, timeout=None):
        """
        Same as curve_async, except:

        - the function will not return until the curve is ready or timeout occurs.
        - the function directly returns an array with the curve instead of a future object
        """
        return self.curve_async().await_result(timeout)

    def single_async(self):
        """
        Performs an asynchronous acquisition of trace_average curves.

        - If running_state is not stop, stops the current acquisition.
        - Immediately returns a future object representing the curve.
        - The curve can be retrieved by calling result(timeout) on the future object.
        - The future is cancelled if the instrument's state is changed before the end of the acquisition.
        """
        self.running_state = 'running_single'
        return self._run_future

    def single(self, timeout=None):
        """
        Same as single_async, except:
            - the function will not return until the averaged curve is ready or timeout occurs.
            - the function directly returns an array with the curve instead of a future object.
        """
        return self.single_async().await_result(timeout)

    def continuous(self):
        """
        continuously acquires curves, and performs a moving
        average over the trace_average last ones.
        """
        self.running_state = 'running_continuous'

    def pause(self):
        """
        Stops the current acquisition without restarting the averaging
        """
        self.running_state = 'paused'

    def stop(self):
        """
        Stops the current acquisition and averaging will be restarted
        at next run.
        """
        self.running_state = 'stopped'

    def save_curve(self):
        """
        Saves the curve(s) that is (are) currently displayed in the gui in
        the db_system. Also, returns the list [curve_ch1, curve_ch2]...
        """
        params = self.setup_attributes
        params.update(name=self.curve_name)
        curve = self._save_curve(self._run_future.data_x, self._run_future.data_avg, **params)
        return curve

    def _clear(self):
        super(AcquisitionModule, self)._clear()
        self._curve_future.cancel()
        self._run_future.cancel()

    def _setup(self):
        self._new_run_future()
        if self.running_state in ('running_single', 'running_continuous'):
            self._run_future.start()
            self._emit_signal_by_name('autoscale_x')

    def _remaining_time(self):
        """
        remaining time (in seconds) until the data has a chance to be ready.
        In the case of scope, where trigger might delay the acquisition,
        this is the minimum time to wait in the "best case scenario" where
        the acquisition would have started immediately after setup().
        """
        raise NotImplementedError('To implement in derived class')

    def _data_ready(self):
        """
        :return: True or False
        """
        raise NotImplementedError('To implement in derived class')

    def _get_curve(self):
        """
        get the curve from the instrument.
          a 1D array for single channel instruments
          a 2*n array for the scope
        """
        raise NotImplementedError

    @property
    def data_x(self):
        """
        x-axis of the curves to plot.
        :return:
        """
        raise NotImplementedError('To implement in derived class')

    def _start_acquisition(self):
        """
        If anything has to be communicated to the hardware (such as make
        trigger ready...) to start the acquisition, it should be done here.
        This function will be called only be called by the init-function of
        the _curve_future()
        Only non-blocking operations are allowed.
        """
        pass

    def _free_up_resources(self):
        pass

    @property
    def data_avg(self):
        return self._run_future.data_avg

    @property
    def current_avg(self):
        return self._run_future.current_avg