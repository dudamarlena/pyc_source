# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\Daq.py
# Compiled at: 2009-07-07 11:29:42
"""
Definition of data acquisition and triggering interfaces.

This module provides an interface to abstract data acquisition
devices.  To interface with real data acquisition devices, use a
module that subclasses the classes defined here.

*WARNING* This module has not been extensively tested or used, and should be
considered unstable.

"""
import VisionEgg, VisionEgg.ParameterTypes as ve_types
__version__ = VisionEgg.release_name

class Trigger(VisionEgg.ClassWithParameters):
    pass


class ChannelParameters(VisionEgg.ClassWithParameters):
    pass


class SignalType(ChannelParameters):
    constant_parameters_and_defaults = {'units': (
               'Unknown units',
               ve_types.String)}

    def __init__(self, **kw):
        if self.__class__ == SignalType:
            raise RuntimeError('Trying to instantiate abstract base class.')
        else:
            ChannelParameters.__init__(self, **kw)


class Analog(SignalType):
    constant_parameters_and_defaults = {'gain': (
              1.0,
              ve_types.Real), 
       'offset': (
                0.0,
                ve_types.Real)}


class Digital(SignalType):
    pass


class DaqMode(ChannelParameters):

    def __init__(self, **kw):
        if self.__class__ == DaqMode:
            raise RuntimeError('Trying to instantiate abstract base class.')
        else:
            ChannelParameters.__init__(self, **kw)


class Buffered(DaqMode):
    parameters_and_defaults = {'sample_rate_hz': (
                        5000.0,
                        ve_types.Real), 
       'duration_sec': (
                      5.0,
                      ve_types.Real), 
       'trigger': (
                 None,
                 ve_types.Instance(Trigger))}


class Immediate(DaqMode):
    pass


class Functionality(ChannelParameters):

    def __init__(self, **kw):
        if self.__class__ == Functionality:
            raise RuntimeError('Trying to instantiate abstract base class.')
        else:
            ChannelParameters.__init__(self, **kw)


class Input(Functionality):

    def get_data(self):
        raise RuntimeError('Must override get_data method with daq implementation!')


class Output(Functionality):

    def put_data(self, data):
        raise RuntimeError('Must override put_data method with daq implementation!')


class Channel(VisionEgg.ClassWithParameters):
    constant_parameters_and_defaults = {'signal_type': (
                     None,
                     ve_types.Instance(SignalType)), 
       'daq_mode': (
                  None,
                  ve_types.Instance(DaqMode)), 
       'functionality': (
                       None,
                       ve_types.Instance(Functionality))}

    def __init__(self, **kw):
        VisionEgg.ClassWithParameters.__init__(self, **kw)
        self.constant_parameters.signal_type.channel = self
        self.constant_parameters.daq_mode.channel = self
        self.constant_parameters.functionality.channel = self
        self.device = None
        return

    def arm_trigger(self):
        raise NotImpelemetedError('This method must be overridden.')


class Device:

    def __init__(self, channels=None):
        self.channels = []
        if channels is not None:
            if type(channels) is not types.ListType:
                raise ValueError('channels must be a list of channels')
            for channel in channels:
                self.add_channel(channel)

        return

    def add_channel(self, channel):
        if isinstance(channel, Channel):
            self.channels.append(channel)
        else:
            raise ValueError('%s not instance of VisionEgg.Daq.Channel' % channel)
        channel.device = self