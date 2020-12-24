# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/service/detect.py
# Compiled at: 2018-06-29 10:55:08
"""
Detection
"""
from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.core import deferred
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class DetectionMonitor:

    def __init__(self, algorithm, parameter, obj, prop, filter=None):
        if _debug:
            DetectionMonitor._debug('__init__ ...')
        self.algorithm = algorithm
        self.parameter = parameter
        self.obj = obj
        self.prop = prop
        self.filter = None
        return

    def property_change(self, old_value, new_value):
        if _debug:
            DetectionMonitor._debug('property_change %r %r', old_value, new_value)
        setattr(self.algorithm, self.parameter, new_value)
        if self.algorithm._triggered:
            if _debug:
                DetectionMonitor._debug('    - already triggered')
            return
        if self.filter:
            trigger = self.filter(old_value, new_value)
        else:
            trigger = old_value != new_value
        if _debug:
            DetectionMonitor._debug('    - trigger: %r', trigger)
        if trigger:
            deferred(self.algorithm._execute)
            if _debug:
                DetectionMonitor._debug('    - deferred: %r', self.algorithm._execute)
            self.algorithm._triggered = True


def monitor_filter(parameter):

    def transfer_filter_decorator(fn):
        fn._monitor_filter = parameter
        return fn

    return transfer_filter_decorator


@bacpypes_debugging
class DetectionAlgorithm:

    def __init__(self):
        if _debug:
            DetectionAlgorithm._debug('__init__')
        self._monitors = []
        self._triggered = False

    def bind(self, **kwargs):
        if _debug:
            DetectionAlgorithm._debug('bind %r', kwargs)
        monitor_filters = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_monitor_filter'):
                monitor_filters[attr._monitor_filter] = attr

        if _debug:
            DetectionAlgorithm._debug('    - monitor_filters: %r', monitor_filters)
        for parameter, (obj, prop) in kwargs.items():
            if not hasattr(self, parameter):
                if _debug:
                    DetectionAlgorithm._debug('    - no matching parameter: %r', parameter)
            monitor = DetectionMonitor(self, parameter, obj, prop)
            if _debug:
                DetectionAlgorithm._debug('    - monitor: %r', monitor)
            if parameter in monitor_filters:
                monitor.filter = monitor_filters[parameter]
            self._monitors.append(monitor)
            obj._property_monitors[prop].append(monitor.property_change)
            property_value = obj._values[prop]
            if property_value is not None:
                if _debug:
                    DetectionAlgorithm._debug('    - %s: %r', parameter, property_value)
                setattr(self, parameter, property_value)

        return

    def unbind(self):
        if _debug:
            DetectionAlgorithm._debug('unbind')
        for monitor in self._monitors:
            if _debug:
                DetectionAlgorithm._debug('    - monitor: %r', monitor)
            monitor.obj._property_monitors[monitor.prop].remove(monitor.property_change)

        self._monitors = []

    def _execute(self):
        if _debug:
            DetectionAlgorithm._debug('_execute')
        self.execute()
        self._triggered = False

    def execute(self):
        raise NotImplementedError('execute not implemented')