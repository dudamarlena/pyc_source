# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/stage.py
# Compiled at: 2017-08-29 09:44:06
from __future__ import division
from . import LockboxModule
from ...attributes import SelectProperty, FloatProperty, BoolProperty, StringProperty
from ...module_attributes import *
from ...hardware_modules import InputSelectProperty
from ...widgets.module_widgets import ReducedModuleWidget, LockboxSequenceWidget, LockboxStageWidget, StageOutputWidget
from qtpy import QtCore
from collections import OrderedDict

class StageSignalLauncher(SignalLauncher):
    stage_created = QtCore.Signal(list)
    stage_deleted = QtCore.Signal(list)


class StageOutput(LockboxModule):
    _setup_attributes = [
     'lock_on',
     'reset_offset',
     'offset']
    _gui_attributes = _setup_attributes
    _widget_class = StageOutputWidget
    lock_on = BoolIgnoreProperty(default=False, call_setup=True)
    reset_offset = BoolProperty(default=False, call_setup=True)
    offset = FloatProperty(default=0, min=-1.0, max=1.0, increment=0.0001, call_setup=True)

    def _setup(self):
        self.parent._setup()


class StageInputSelectProperty(InputSelectProperty):
    pass


class Stage(LockboxModule):
    """
    A stage is a single step in the lock acquisition process
    """
    _gui_attributes = [
     'input',
     'setpoint',
     'duration',
     'gain_factor',
     'function_call']
    _setup_attributes = _gui_attributes + ['outputs']
    _widget_class = LockboxStageWidget
    _signal_launcher = StageSignalLauncher
    input = StageInputSelectProperty(ignore_errors=True, options=lambda stage: stage.lockbox.inputs.keys(), call_setup=True)
    setpoint = FloatProperty(default=0, min=-1000000.0, max=1000000.0, increment=0.1, call_setup=True)
    gain_factor = FloatProperty(default=1.0, min=-1000000.0, max=1000000.0, increment=0.1, call_setup=True)
    function_call = StringProperty(default='', call_setup=True)
    duration = FloatProperty(default=0, min=0, max=1000000.0, increment=0.1)
    outputs = ModuleDictProperty(module_cls=LockboxModule)

    def __init__(self, parent, name=None):
        super(Stage, self).__init__(parent, name=name)
        for output in self.lockbox.outputs:
            self.outputs[output.name] = StageOutput

        self._signal_launcher.stage_created.emit([self])
        self.parent._signal_launcher.stage_created.emit([self])
        self.lockbox._logger.debug('Stage %s initialized' % self.name)

    def _clear(self):
        self.lockbox._logger.debug('Deleting stage %s' % self.name)
        self._signal_launcher.stage_deleted.emit([self])
        self.parent._signal_launcher.stage_deleted.emit([self])
        super(Stage, self)._clear()

    @property
    def _states(self):
        """
        Returns the config file branch corresponding to the saved states of the module.
        """
        return

    def enable(self):
        """
        Setup the lockbox parameters according to this stage
        """
        for output in self.lockbox.outputs:
            setting = self.outputs[output.name]
            if setting.lock_on == 'ignore':
                pass
            if setting.lock_on == False:
                output.unlock()
            if setting.reset_offset:
                output._setup_offset(setting.offset)

        for output in self.lockbox.outputs:
            setting = self.outputs[output.name]
            if setting.lock_on == True:
                output.lock(input=self.input, setpoint=self.setpoint, offset=setting.offset if setting.reset_offset else None, gain_factor=self.gain_factor)

        if self.function_call != '':
            try:
                func = recursive_getattr(self.lockbox, self.function_call)
            except AttributeError:
                self._logger.warning("Could not find the function '%s' called in stage %s in the Lockbox class. Please specify a valid function name to call!", self.function_call, self.name)
            else:
                try:
                    func()
                except TypeError:
                    func(self)

        self.lockbox.current_state = self.name
        return

    def _setup(self):
        if hasattr(self.lockbox, '_sequence'):
            if self.lockbox.current_state == self.name:
                self.enable()
            elif self.lockbox.current_state == 'lock' and self == self.parent[(-1)]:
                self.lockbox.final_stage = self.setup_attributes