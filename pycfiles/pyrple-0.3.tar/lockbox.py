# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/lockbox.py
# Compiled at: 2017-08-29 09:44:06
from __future__ import division
from collections import OrderedDict
from qtpy import QtCore
import logging
from ...modules import SignalLauncher
from ...module_attributes import ModuleListProperty
from .input import *
from .output import *
from ...widgets.module_widgets import LockboxWidget
from ...pyrpl_utils import all_subclasses
from ...async_utils import sleep
from .stage import Stage
from . import LockboxModule, LockboxModuleDictProperty
from . import LockboxLoop, LockboxPlotLoop
from ...widgets.module_widgets.lockbox_widget import LockboxSequenceWidget

def all_classnames():
    return OrderedDict([ (subclass.__name__, subclass) for subclass in [
     Lockbox] + all_subclasses(Lockbox)
                       ])


class ClassnameProperty(SelectProperty):
    """
    Lots of lockbox attributes need to be updated when model is changed
    """

    def set_value(self, obj, val):
        super(ClassnameProperty, self).set_value(obj, val)
        if obj._autosave_active:
            self.save_attribute(obj, val)
        else:
            obj._logger.debug('Autosave of classname attribute of Lockbox is inactive. This may have severe impact on proper functionality.')
        obj._logger.debug('Lockbox classname changed to %s', val)
        obj._classname_changed()
        return val


class AutoLockProperty(BoolProperty):
    """ true if autolock is enabled"""

    def set_value(self, obj, val):
        super(AutoLockProperty, self).set_value(obj=obj, val=val)
        obj.relock(test_auto_lock=True)


class AutoLockIntervalProperty(FloatProperty):
    """ timeout for autolock timer """

    def set_value(self, obj, val):
        super(AutoLockIntervalProperty, self).set_value(obj=obj, val=val)
        obj._auto_lock_loop.interval = val


class LockstatusIntervalProperty(FloatProperty):
    """ timeout for lockstatus timer """

    def set_value(self, obj, val):
        super(LockstatusIntervalProperty, self).set_value(obj=obj, val=val)
        obj._lockstatus_loop.interval = val


class StateSelectProperty(SelectProperty):

    def set_value(self, obj, val):
        super(StateSelectProperty, self).set_value(obj, val)
        obj._state_change_time = time()
        obj._signal_launcher.state_changed.emit([val])


class SignalLauncherLockbox(SignalLauncher):
    """
    A SignalLauncher for the lockbox
    """
    output_created = QtCore.Signal(list)
    output_deleted = QtCore.Signal(list)
    output_renamed = QtCore.Signal()
    stage_created = QtCore.Signal(list)
    stage_deleted = QtCore.Signal(list)
    stage_renamed = QtCore.Signal()
    delete_widget = QtCore.Signal()
    state_changed = QtCore.Signal(list)
    add_input = QtCore.Signal(list)
    input_calibrated = QtCore.Signal(list)
    remove_input = QtCore.Signal(list)
    update_transfer_function = QtCore.Signal(list)
    update_lockstatus = QtCore.Signal(list)


class Lockbox(LockboxModule):
    """
    A Module that allows to perform feedback on systems that are well described
    by a physical model.
    """
    _widget_class = LockboxWidget
    _signal_launcher = SignalLauncherLockbox
    _gui_attributes = ['classname',
     'default_sweep_output',
     'auto_lock',
     'is_locked_threshold',
     'setpoint_unit']
    _setup_attributes = _gui_attributes + ['auto_lock_interval',
     'lockstatus_interval',
     '_auto_lock_timeout']
    classname = ClassnameProperty(options=lambda : list(all_classnames().keys()))

    def __init__(self, parent, name=None):
        super(Lockbox, self).__init__(parent=parent, name=name)
        self._state_change_time = -1

    setpoint_unit = SelectProperty(options=['V'], default='V', ignore_errors=True)
    _output_units = [
     'V', 'mV']

    def _unit1_in_unit2(self, unit1, unit2, try_prefix=True):
        """ helper function to convert unit2 to unit 1"""
        if unit1 == unit2:
            return 1.0
        try:
            return getattr(self, '_' + unit1 + '_in_' + unit2)
        except AttributeError:
            try:
                return 1.0 / getattr(self, '_' + unit2 + '_in_' + unit1)
            except AttributeError:
                if not try_prefix:
                    raise

        _unit_prefixes = OrderedDict([('', 1.0),
         ('m', 0.001),
         ('u', 1e-06),
         ('n', 1e-09),
         ('p', 1e-12),
         ('k', 1000.0),
         ('M', 1000000.0),
         ('G', 1000000000.0),
         ('T', 1000000000000.0)])
        for prefix2 in _unit_prefixes:
            if unit2.startswith(prefix2) and len(unit2) > len(prefix2):
                for prefix1 in _unit_prefixes:
                    if unit1.startswith(prefix1) and len(unit1) > len(prefix1):
                        try:
                            return self._unit1_in_unit2(unit1[len(prefix1):], unit2[len(prefix2):], try_prefix=False) * _unit_prefixes[prefix1] / _unit_prefixes[prefix2]
                        except AttributeError:
                            pass

        raise AttributeError('Could not find attribute %s in Lockbox class. ' % (unit1 + '_in_' + unit2))

    def _unit_in_setpoint_unit(self, unit):
        return self._unit1_in_unit2(unit, self.setpoint_unit)

    def _setpoint_unit_in_unit(self, unit):
        return self._unit1_in_unit2(self.setpoint_unit, unit)

    default_sweep_output = SelectProperty(options=lambda lb: lb.outputs.keys(), ignore_errors=True)
    is_locked_threshold = FloatProperty(default=1.0, min=-10000000000.0, max=10000000000.0, doc='Setpoint interval size to consider system in locked state')
    auto_lock = AutoLockProperty(default=False, doc='Turns on the autolock of the module.')
    auto_lock_interval = AutoLockIntervalProperty(default=1.0, min=0.001, max=10000000000.0)
    _auto_lock_loop = ModuleProperty(LockboxLoop, interval=1.0, autostart=True, loop_function=lambda obj: obj.relock(test_auto_lock=True))
    _auto_lock_timeout = FloatProperty(min=0, default=1000, doc='maximum time that a locking stage is allowed to take before a lock is considered as stalled. ')
    inputs = LockboxModuleDictProperty(input_from_output=InputFromOutput)
    outputs = LockboxModuleDictProperty(output1=OutputSignal, output2=OutputSignal)
    sequence = ModuleListProperty(Stage, default=[{}])
    sequence._widget_class = LockboxSequenceWidget
    current_state = StateSelectProperty(options=lambda inst: [
     'unlock', 'sweep', 'final_stage'] + list(range(len(inst.sequence))), default='unlock')

    @property
    def final_stage(self):
        """ temporary storage of the final lock stage"""
        if not hasattr(self, '_final_stage'):
            self._final_stage = Stage(self, name='final_stage')
            self.final_stage = {}
        return self._final_stage

    @final_stage.setter
    def final_stage(self, kwargs):
        setup_attributes = self.sequence[(-1)].setup_attributes
        setup_attributes.update(kwargs)
        setup_attributes['duration'] = 0
        self.final_stage.setup(**setup_attributes)

    def _current_stage(self, state=None):
        if state is None:
            state = self.current_state
        if isinstance(state, int):
            return self.sequence[self.current_state]
        else:
            if state == 'final_stage':
                return self.final_stage
            else:
                return state

            return

    @property
    def current_stage(self):
        return self._current_stage()

    @property
    def signals(self):
        """ a dict of all logical signals of the lockbox """
        signallist = []
        if hasattr(self, '_inputs'):
            signallist += self.inputs.items()
        if hasattr(self, '_outputs'):
            signallist += self.outputs.items()
        return OrderedDict(signallist)

    @property
    def asg(self):
        """ the asg being used for sweeps """
        if not hasattr(self, '_asg') or self._asg is None:
            self._asg = self.pyrpl.asgs.pop(self.name)
        return self._asg

    def calibrate_all(self, autosave=False):
        """
        Calibrates successively all inputs
        """
        curves = []
        for input in self.inputs:
            try:
                c = input.calibrate(autosave=autosave)
                if c is not None:
                    curves.append(c)
            except:
                pass

        return curves

    def get_analog_offsets(self, duration=1.0):
        """
        Measures and saves the analog offset for all inputs.

        This function is designed to measure the analog offsets of the redpitaya
        inputs and possibly the sensors connected to these inputs. Only call this
        function if you are sure about what you are doing and if all signal sources
        (lasers etc.) are turned off.

        The parameter duration specifies the time during which to average the
        input offsets.
        """
        for input in self.inputs:
            input.get_analog_offset(duration=duration)

    def unlock(self, reset_offset=True):
        """
        Unlocks all outputs.
        """
        if self._lock_loop is not None:
            self._lock_loop._clear()
            self._lock_loop = None
        for output in self.outputs:
            output.unlock(reset_offset=reset_offset)

        self.current_state = 'unlock'
        return

    def _sweep(self):
        """
        Performs a sweep of one of the output. No output default kwds to avoid
        problems when use as a slot.
        """
        self.unlock()
        self.outputs[self.default_sweep_output].sweep()
        self.current_state = 'sweep'

    def sweep(self):
        """
        Performs a sweep of one of the output. No output default kwds to avoid
        problems when use as a slot.
        """
        return self._sweep()

    _lock_loop = None

    def lock(self, **kwds):
        """
        Launches the full lock sequence, stage by stage until the end.
        optional kwds are stage attributes that are set after iteration through
        the sequence, e.g. a modified setpoint.
        """
        self.unlock()
        self.final_stage = kwds

        def lock_loop_function(lockbox, loop):
            if loop.n < len(lockbox.sequence):
                stage = lockbox.sequence[loop.n]
                stage.enable()
                loop.interval = stage.duration
            else:
                lockbox.final_stage.enable()
                loop._clear()
                lockbox._lock_loop = None
            return

        self._lock_loop = LockboxLoop(self, name='lock_loop', loop_function=lock_loop_function)

    def relock(self, test_auto_lock=False, **kwargs):
        """ locks the cavity if it is_locked is false. Returns the value of
        is_locked """
        if len(kwargs) > 0:
            self.final_stage.setup(**kwargs)
        if test_auto_lock and (not self.auto_lock or self._setup_ongoing):
            return
        if self.is_locking():
            return False
        else:
            if self.is_locked_and_final(loglevel=0):
                return True
            self._logger.info('Attempting to re-lock...')
            return self.lock(**kwargs)

    def relock_until_locked(self, **kwargs):
        """ blocks the command line until cavity is locked with kwargs """

        def relock_function(lockbox, loop):
            if lockbox.relock(**kwargs):
                loop._clear()

        self._relock_until_locked_loop = LockboxLoop(parent=self, name='relock_until_locked_loop', interval=1.0, autostart=True, loop_function=relock_function)
        while not self._relock_until_locked_loop._ended:
            sleep(1.0)

    def lock_until_locked(self, **kwargs):
        self.lock(**kwargs)
        return self.relock_until_locked(**kwargs)

    def sleep_while_locked(self, time_to_sleep):
        t0 = time()
        while time() < t0 + time_to_sleep:
            if self.is_locked_and_final(loglevel=0):
                sleep(0.1)
            else:
                self._logger.error('Error during measurement - cavity unlocked. Aborting sleep...')
                return False

        return True

    def is_locked(self, input=None, loglevel=logging.INFO):
        """ returns True if locked, else False. Also updates an internal
        dict that contains information about the current error signals. The
        state of lock is logged at loglevel """
        if self.current_stage not in self.sequence + [self.final_stage]:
            self._logger.log(loglevel, "Not locked: lockbox state '%s' does not correspond to a lock stage.", self.current_state)
            return False
        else:
            for o in self.outputs:
                if o.is_saturated:
                    self._logger.log(loglevel, 'Not locked: output %s is saturated.', o.name)
                    return False

            if input is None:
                if hasattr(self, '_default_is_locked_input') and self._default_is_locked_input is not None:
                    input = self._default_is_locked_input
                else:
                    input = self.current_stage.input
            if not isinstance(input, InputSignal):
                input = self.inputs[input]
            try:
                return input.is_locked(loglevel=loglevel)
            except TypeError:
                return input.is_locked()

            return

    def is_locked_and_final(self, loglevel=logging.INFO):
        return self.current_state == 'final_stage' and self.is_locked(loglevel=loglevel)

    def is_locking(self):
        return self._lock_loop is not None and self.current_stage in self.sequence and self._state_change_time + self._auto_lock_timeout > time()

    def _lockstatus(self):
        """ this function is a placeholder for periodic lockstatus
        diagnostics, such as calls to is_locked, logging means and rms
        values, and plotting measured setpoints etc."""
        self._signal_launcher.update_lockstatus.emit([None])
        try:
            self.log_lockstatus()
        except AttributeError:
            pass

        return

    _lockstatus_loop = ModuleProperty(LockboxLoop, interval=1.0, autostart=True, loop_function=_lockstatus)
    lockstatus_interval = LockstatusIntervalProperty(default=1.0, min=0.001, max=10000000000.0)

    @classmethod
    def _make_Lockbox(cls, parent, name):
        """ returns a new Lockbox object of the type defined by the classname
        variable in the config file"""
        try:
            classname = parent.c[name]['classname']
        except KeyError:
            classname = cls.__name__
            parent.logger.debug("No config file entry for classname found. Using class '%s'.", classname)

        parent.logger.debug('Making new Lockbox with class %s. ', classname)
        return all_classnames()[classname](parent, name)

    def _classname_changed(self):
        if self.classname == type(self).__name__:
            self._logger.debug('Lockbox classname not changed: - formerly: %s, now: %s.', type(self).__name__, self.classname)
            return
        self._logger.debug('Lockbox classname changed - formerly: %s, now: %s.', type(self).__name__, self.classname)
        pyrpl, name = self.pyrpl, self.name
        self._signal_launcher.delete_widget.emit()
        self._clear()
        new_lockbox = Lockbox._make_Lockbox(pyrpl, name)
        setattr(pyrpl, name, new_lockbox)
        pyrpl.software_modules.append(new_lockbox)
        for w in pyrpl.widgets:
            w.reload_dock_widget(name)

    def _clear(self):
        """ returns a new Lockbox object of the type defined by the classname
        variable in the config file"""
        pyrpl, name = self.pyrpl, self.name
        if self._lock_loop is not None:
            self._lock_loop._clear()
        super(Lockbox, self)._clear()
        setattr(pyrpl, name, None)
        try:
            self.parent.software_modules.remove(self)
        except ValueError:
            self._logger.warning('Could not find old Lockbox %s in the list of software modules. Duplicate lockbox objects may coexist. It is recommended to restart PyRPL. Existing software modules: \n%s', self.name, str(self.parent.software_modules))

        def getattribute_forwarder(obj, attribute):
            lockbox = getattr(pyrpl, name)
            return getattr(lockbox, attribute)

        self.__getattribute__ = getattribute_forwarder

        def setattribute_forwarder(obj, attribute, value):
            lockbox = getattr(pyrpl, name)
            return setattr(lockbox, attribute, value)

        self.__setattr__ = setattribute_forwarder
        return

    @property
    def _time(self):
        """ retrieves 'local' time of the lockbox """
        return time()

    @property
    def params(self):
        """
        returns a convenient dict with parameters that describe if and with
        which settings the lockbox was properly.

        params from different Pyrpl lockboxes can be merged together without
        problems if the names of the config files differ
        """
        d = dict(config=self.c._root._filename)
        for var in ['is_locked', 'is_locked_and_final', 'current_state',
         '_state_change_time', '_time', 'final_stage.setpoint',
         'setpoint_unit', 'final_stage.gain_factor',
         'final_stage.input']:
            val = recursive_getattr(self, var)
            if callable(val):
                val = val()
            d[var] = val

        for o in self.inputs:
            o.stats(t=1.0)
            d[o.name + '_mean'] = o.mean
            d[o.name + '_rms'] = o.rms
            d[o.name + '_calibration_data_min'] = o.calibration_data.min
            d[o.name + '_calibration_data_max'] = o.calibration_data.max
            if hasattr(o, 'quadrature_factor'):
                d[o.name + '_quadrature_factor'] = o.quadrature_factor

        for o in self.outputs:
            d[o.name + '_mean'] = o.mean
            d[o.name + '_rms'] = o.rms
            d[o.name + '_pid_setpoint'] = o.pid.setpoint
            d[o.name + '_pid_p'] = o.pid.p
            d[o.name + '_pid_i'] = o.pid.i
            d[o.name + '_pid_ival'] = o.pid.ival
            d[o.name + '_pid_input'] = o.pid.input

        dd = dict()
        for k in d:
            dd[self.pyrpl.name + '_' + k] = d[k]

        return dd