# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/swtch.py
# Compiled at: 2014-09-01 23:09:59
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
from . import ivi

class InvalidScanListException(ivi.IviException):
    pass


class InvalidSwitchPathException(ivi.IviException):
    pass


class EmptyScanListException(ivi.IviException):
    pass


class EmptySwitchPathException(ivi.IviException):
    pass


class ScanInProgressException(ivi.IviException):
    pass


class NoScanInProgressException(ivi.IviException):
    pass


class NoSuchPathException(ivi.IviException):
    pass


class IsConfigurationChannelException(ivi.IviException):
    pass


class NotAConfigurationChannelException(ivi.IviException):
    pass


class AttemptToConnectSourcesException(ivi.IviException):
    pass


class ExplicitConnectionExistsException(ivi.IviException):
    pass


class LegMissingFirstChannelException(ivi.IviException):
    pass


class LegMissingSecondChannelException(ivi.IviException):
    pass


class ChannelDuplicatedInLegException(ivi.IviException):
    pass


class ChannelDuplicatedInPathException(ivi.IviException):
    pass


class PathNotFoundException(ivi.IviException):
    pass


class DiscontinuousPathException(ivi.IviException):
    pass


class CannotConnectDirectlyException(ivi.IviException):
    pass


class ChannelsAlreadyConnectedException(ivi.IviException):
    pass


class CannotConnectToItselfException(ivi.IviException):
    pass


ScanMode = set(['none', 'break_before_make', 'break_after_make'])
ScanActionType = set(['connect_path', 'disconnect_path', 'wait_for_trigger'])
Path = set(['available', 'exists', 'unsupported', 'resource_in_use',
 'source_conflict', 'channel_not_available'])

class Base(ivi.IviContainer):
    """Base IVI methods for all switch modules"""

    def __init__(self, *args, **kwargs):
        self._channel_count = 1
        super(Base, self).__init__(*args, **kwargs)
        cls = 'IviSwtch'
        grp = 'Base'
        ivi.add_group_capability(self, cls + grp)
        self._channel_name = list()
        self._channel_characteristics_ac_current_carry_max = list()
        self._channel_characteristics_ac_current_switching_max = list()
        self._channel_characteristics_ac_power_carry_max = list()
        self._channel_characteristics_ac_power_switching_max = list()
        self._channel_characteristics_ac_voltage_max = list()
        self._channel_characteristics_bandwidth = list()
        self._channel_characteristics_impedance = list()
        self._channel_characteristics_dc_current_carry_max = list()
        self._channel_characteristics_dc_current_switching_max = list()
        self._channel_characteristics_dc_power_carry_max = list()
        self._channel_characteristics_dc_power_switching_max = list()
        self._channel_characteristics_dc_voltage_max = list()
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()
        self._path_is_debounced = False
        self._add_property('channels[].characteristics.ac_current_carry_max', self._get_channel_characteristics_ac_current_carry_max, None, None, ivi.Doc('\n                        The maximum AC current the channel can carry, in amperes RMS.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.1'))
        self._add_property('channels[].characteristics.ac_current_switching_max', self._get_channel_characteristics_ac_current_switching_max, None, None, ivi.Doc('\n                        The maximum AC current the channel can switch, in amperes RMS.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.2'))
        self._add_property('channels[].characteristics.ac_power_carry_max', self._get_channel_characteristics_ac_power_carry_max, None, None, ivi.Doc('\n                        The maximum AC power the channel can handle, in volt-amperes.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.3'))
        self._add_property('channels[].characteristics.ac_power_switching_max', self._get_channel_characteristics_ac_power_switching_max, None, None, ivi.Doc('\n                        The maximum AC power the channel can switch, in volt-amperes.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.4'))
        self._add_property('channels[].characteristics.ac_voltage_max', self._get_channel_characteristics_ac_voltage_max, None, None, ivi.Doc('\n                        The maximum AC voltage the channel can handle, in volts RMS.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.5'))
        self._add_property('channels[].characteristics.bandwidth', self._get_channel_characteristics_bandwidth, None, None, ivi.Doc('\n                        The maximum frequency signal, in Hertz, that can pass through the channel.\n                        without attenuating it by more than 3dB.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.6'))
        self._add_property('channels[].name', self._get_channel_name, None, None, ivi.Doc('\n                        This attribute returns the physical name identifier defined by the\n                        specific driver for the Channel that corresponds to the one-based index\n                        that the user specifies. If the driver defines a qualified channel name,\n                        this property returns the qualified name. If the value that the user\n                        passes for the Index parameter is less than one or greater than the value\n                        of the Channel Count, the attribute returns an empty string for the value\n                        and returns an error.\n                        ', cls, grp, '4.2.9'))
        self._add_property('channels[].characteristics.impedance', self._get_channel_characteristics_impedance, None, None, ivi.Doc('\n                        The characteristic impedance of the channel, in ohms.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.10'))
        self._add_property('channels[].characteristics.dc_current_carry_max', self._get_channel_characteristics_dc_current_carry_max, None, None, ivi.Doc('\n                        The maximum DC current the channel can carry, in amperes.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.11'))
        self._add_property('channels[].characteristics.dc_current_switching_max', self._get_channel_characteristics_dc_current_switching_max, None, None, ivi.Doc('\n                        The maximum DC current the channel can switch, in amperes\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.12'))
        self._add_property('channels[].characteristics.dc_power_carry_max', self._get_channel_characteristics_dc_power_carry_max, None, None, ivi.Doc('\n                        The maximum DC power the channel can handle, in watts.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.13'))
        self._add_property('channels[].characteristics.dc_power_switching_max', self._get_channel_characteristics_dc_power_switching_max, None, None, ivi.Doc('\n                        The maximum DC power the channel can switch, in watts.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.14'))
        self._add_property('channels[].characteristics.dc_voltage_max', self._get_channel_characteristics_dc_voltage_max, None, None, ivi.Doc('\n                        The maximum DC voltage the channel can handle, in volts.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        ', cls, grp, '4.2.15'))
        self._add_property('channels[].is_configuration_channel', self._get_channel_is_configuration_channel, self._set_channel_is_configuration_channel, None, ivi.Doc('\n                        Specifies whether the specific driver uses the channel for internal path\n                        creation. If set to True, the channel is no longer accessible to the user\n                        and can be used by the specific driver for path creation. If set to False,\n                        the channel is considered a standard channel and can be explicitly\n                        connected to another channel.\n                        \n                        For example, if the user specifies a column-to-column connection in a\n                        matrix, it typically must use at least one row channel to make the\n                        connection. Specifying a channel as a configuration channel allows the\n                        instrument driver to use it to create the path.\n                        \n                        Notice that once a channel has been configured as a configuration channel,\n                        then no operation can be performed on that channel, except for reading and\n                        writing the Is Configuration Channel attribute.\n                        ', cls, grp, '4.2.16'))
        self._add_property('path.is_debounced', self._get_path_is_debounced, None, None, ivi.Doc('\n                        This attribute indicates whether the switch module has settled from the\n                        switching commands and completed the debounce. If True, the switch module\n                        has settled from the switching commands and completed the debounce. It\n                        indicates that the signal going through the switch module is valid,\n                        assuming that the switches in the path have the correct characteristics.\n                        If False, the switch module has not settled.\n                        ', cls, grp, '4.2.17'))
        self._add_property('channels[].is_source_channel', self._get_channel_is_source_channel, self._set_channel_is_source_channel, None, ivi.Doc('\n                        Allows the user to declare a particular channel as a source channel. If\n                        set to True, the channel is a source channel. If set to False, the channel\n                        is not a source channel.\n                        \n                        If a user ever attempts to connect two channels that are either sources or\n                        have their own connections to sources, the path creation operation returns\n                        an error. Notice that the term source can be from either the instrument or\n                        the UUT perspective. This requires the driver to ensure with each\n                        connection that another connection within the switch module does not\n                        connect to another source.\n                        \n                        The intention of this attribute is to prevent channels from being\n                        connected that may cause damage to the channels, devices, or system.\n                        Notice that GROUND can be considered a source in some circumstances.\n                        ', cls, grp, '4.2.18'))
        self._add_property('channels[].characteristics.settling_time', self._get_channel_characteristics_settling_time, None, None, ivi.Doc('\n                        The maximum total settling time for the channel before the signal going\n                        through it is considered stable. This includes both the activation time\n                        for the channel as well as any debounce time.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        \n                        The units are seconds.\n                        ', cls, grp, '4.2.19'))
        self._add_property('channels[].characteristics.wire_mode', self._get_channel_characteristics_wire_mode, None, None, ivi.Doc('\n                        This attribute describes the number of conductors in the current channel.\n                        \n                        Notice that values for this attribute are on per-channel basis and may not\n                        take into account the other switches that make up a path to or from this\n                        channel.\n                        \n                        For example, this attribute returns 2 if the channel has two conductors.\n                        ', cls, grp, '4.2.20'))
        self._add_method('path.can_connect', self._path_can_connect, ivi.Doc('\n                        The purpose of this function is to allow the user to verify whether the\n                        switch module can create a given path without the switch module actually\n                        creating the path. In addition, the operation indicates whether the switch\n                        module can create the path at the moment based on the current paths in\n                        existence.\n                        \n                        Notice that while this operation is available for the end user, the\n                        primary purpose of this operation is to allow higher-level switch drivers\n                        to incorporate IviSwtch drivers into higher level switching systems.\n                        \n                        If the implicit connection exists between the two specified channels, this\n                        functions returns the warning Implicit Connection Exists.\n                        ', cls, grp, '4.3.1'))
        self._add_method('path.connect', self._path_connect, ivi.Doc('\n                        This function takes two channel names and, if possible, creates a path\n                        between the two channels. If the path already exists, the operation does\n                        not count the number of calls. For example, it does not remember that\n                        there were two calls to connect, thus requiring two calls to disconnect,\n                        but instead returns an error, regardless of whether the order of the two\n                        channels is the same or different on the two calls. This is true because\n                        paths are assumed to be bi-directional. This class does not handle\n                        unidirectional paths. Notice that the IVI spec does not specify the\n                        default names for the channels because this depends on the architecture\n                        of the switch module. The user can specify aliases for the vendor defined\n                        channel names in the IVI Configuration Store.\n                        \n                        This function returns as soon as the command is given to the switch module\n                        and the switch module is ready for another command. This may be before or\n                        after the switches involved settle. Use the Is Debounced function to\n                        determine if the switch module has settled. Use the Wait For Debounce\n                        function if you want to wait until the switch has debounced.\n                        \n                        If an explicit connection already exists between the two specified\n                        channels, this function returns the error Explicit Connection Exists\n                        without performing any connection operation.\n                        \n                        If one of the specified channels is a configuration channel, this function\n                        returns the error Is Configuration Channel without performing any\n                        connection operation.\n                        \n                        If the two specified channels are both connected to a different source,\n                        this function returns the error Attempt To Connect Sources without\n                        performing any connection operation.\n                        \n                        If the two specified channels are the same, this function returns the\n                        error Cannot Connect To Itself without performing any connection\n                        operation.\n                        \n                        If a path cannot be found between the two specified channels, this\n                        function returns the error Path Not Found without performing any\n                        connection operation.\n                        ', cls, grp, '4.3.2'))
        self._add_method('path.disconnect', self._path_disconnect, ivi.Doc('\n                        This function takes two channel names and, if possible, destroys the path\n                        between the two channels. The order of the two channels in the operation\n                        does not need to be the same as the connect operation. Notice that the IVI\n                        specification does not specify what the default names are for the channels\n                        as this depends on the architecture of the switch module. The user can\n                        specify aliases for the vendor defined channel names in the IVI\n                        Configuration Store.\n                        \n                        This function returns as soon as the command is given to the switch module\n                        and the switch module is ready for another command. This may be before or\n                        after the switches involved settle. Use the Is Debounced attribute to see\n                        if the switch has settled. Use the Wait For Debounce function if you want\n                        to wait until the switch has debounced.\n                        \n                        If some connections remain after disconnecting the two specified channels,\n                        this function returns the warning Path Remains.\n                        \n                        If no explicit path exists between the two specified channels, this\n                        function returns the error No Such Path without performing any\n                        disconnection operation.\n                        ', cls, grp, '4.3.3'))
        self._add_method('path.disconnect_all', self._path_disconnect_all, ivi.Doc('\n                        The purpose of this function is to allow the user to disconnect all paths\n                        created since Initialize or Reset have been called. This can be used as\n                        the test program goes from one sub-test to another to ensure there are no\n                        side effects in the switch module.\n                        \n                        Notice that some switch modules may not be able to disconnect all paths\n                        (such as a scanner that must keep at least one path). In these cases, this\n                        function returns the warning Path Remains.\n                        ', cls, grp, '4.3.4'))
        self._add_method('path.get_path', self._path_get_path, ivi.Doc('\n                        This function returns a list of channels (see the Set Path function for a\n                        description on the syntax of path list) that have been connected in order\n                        to create the path between the specified channels. The names of the\n                        switches as well as the internal configuration of the switch module are\n                        vendor specific. This function can be used to return the list of the\n                        switches in order to better understand the signal characteristics of the\n                        path and to provide the path list for the Set Path function.\n                        \n                        The first and last names in the list are the channel names of the path.\n                        All channels other than the first and the last channel in the path list\n                        are configuration channels. No other channel can be used to generate the\n                        path between the two channels.\n                        \n                        The only valid paths that can be returned are ones that have been\n                        explicitly set via Connect and Set Path functions.\n                        \n                        If no explicit path exists between the two specified channels, this\n                        function returns the error No Such Path.\n                        ', cls, grp, '4.3.6'))
        self._add_method('path.set_path', self._path_set_path, ivi.Doc("\n                        The IVI Switch is designed to provide automatic routing from channel to\n                        channel. However, due to such issues as calibration, it may be necessary\n                        to have deterministic control over the path that is created between two\n                        channels. This function allows the user to specify the exact path, in\n                        terms of the configuration channels used, to create. Notice that the end\n                        channel names are the first and last entries in the Path List parameter.\n                        \n                        The driver makes a connection between the channels using the configuration\n                        channels. The intermediary steps are called legs of the path.\n                        \n                        The path list syntax is a string array of channels. Path lists obey the\n                        following rules:\n\n                        * In the array, elements n and n+1 create a path leg.\n                        * Every channel in the path list other than the first and the last must be\n                          a configuration channel.\n                        * Driver channel strings as well as virtual channel names may be used to\n                          describe a path leg in a path list.\n                        \n                        An example of creating a path list is:\n                        \n                            path_list = ['ch1', 'conf1', 'ch2']\n                        \n                        It should be noticed that, even if users utilize virtual channel names,\n                        path_list is not interchangeable since the names of switches within the\n                        switch module are not required to be interchangeable and depend on the\n                        internal architecture of the switch module. However, it is possible to use\n                        the Connect and then Get Path functions to retrieve an already existing\n                        path. This allows the user to guarantee that the routing can be recreated\n                        exactly.\n                        \n                        If the specified path list is empty, this function returns the error Empty\n                        Switch Path without performing any connection operation.\n                        \n                        If one of the channels in the path list is a configuration channel that is\n                        currently in use, this function returns the error Resource In Use without\n                        performing any connection operation.\n                        \n                        If an explicit connection is made to a configuration channel, this\n                        function returns the error Is Configuration Channel without performing any\n                        connection operation.\n                        \n                        If one of the non-terminal channels in the path list is not a\n                        configuration channel, this function returns the error Not A Configuration\n                        Channel without performing any connection operation.\n                        \n                        If the path list attempts to connect between two different source\n                        channels, this function returns the error Attempt To Connect Sources\n                        without performing any connection operation.\n                        \n                        If the path list attempts to connect between channels that already have an\n                        explicit connection, this function returns the error Explicit Connection\n                        Exists without performing any connection operation.\n                        \n                        If the first and the second channels in the leg are the same, this\n                        function returns the error Channel Duplicated In Leg without performing\n                        any connection operation.\n                        \n                        If a channel name is duplicated in the path list, this function returns\n                        the error Channel Duplicated In Path without performing any connection\n                        operation.\n                        \n                        If the path list contains a leg with two channels that cannot be directly\n                        connected, this function returns the error Cannot Connect Directly without\n                        performing any connection operation. If a leg in the path contains two\n                        channels that are already directly connected, this function returns the\n                        error Channels Already Connected without performing any connection\n                        operation.\n                        ", cls, grp, '4.3.8'))
        self._add_method('path.wait_for_debounce', self._path_wait_for_debounce, ivi.Doc('\n                        The purpose of this function is to wait until the path through the switch\n                        is stable (debounced). If the signals did not settle within the time\n                        period the user specified with the maximum_time parameter, the function\n                        returns the Max Time Exceeded error.\n                        ', cls, grp, '4.3.9'))
        self._init_channels()
        return

    def _init_channels(self):
        try:
            super(Base, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_characteristics_ac_current_carry_max = list()
        self._channel_characteristics_ac_current_switching_max = list()
        self._channel_characteristics_ac_power_carry_max = list()
        self._channel_characteristics_ac_power_switching_max = list()
        self._channel_characteristics_ac_voltage_max = list()
        self._channel_characteristics_bandwidth = list()
        self._channel_characteristics_impedance = list()
        self._channel_characteristics_dc_current_carry_max = list()
        self._channel_characteristics_dc_current_switching_max = list()
        self._channel_characteristics_dc_power_carry_max = list()
        self._channel_characteristics_dc_power_switching_max = list()
        self._channel_characteristics_dc_voltage_max = list()
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()
        for i in range(self._channel_count):
            self._channel_name.append('channel%d' % (i + 1))
            self._channel_characteristics_ac_current_carry_max.append(0.1)
            self._channel_characteristics_ac_current_switching_max.append(0.1)
            self._channel_characteristics_ac_power_carry_max.append(1)
            self._channel_characteristics_ac_power_switching_max.append(1)
            self._channel_characteristics_ac_voltage_max.append(100)
            self._channel_characteristics_bandwidth.append(1000000.0)
            self._channel_characteristics_impedance.append(50)
            self._channel_characteristics_dc_current_carry_max.append(0.1)
            self._channel_characteristics_dc_current_switching_max.append(0.1)
            self._channel_characteristics_dc_power_carry_max.append(1)
            self._channel_characteristics_dc_power_switching_max.append(1)
            self._channel_characteristics_dc_voltage_max.append(100)
            self._channel_is_configuration_channel.append(False)
            self._channel_is_source_channel.append(False)
            self._channel_characteristics_settling_time.append(0.1)
            self._channel_characteristics_wire_mode.append(1)

        self.channels._set_list(self._channel_name)

    def _get_channel_characteristics_ac_current_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_current_carry_max[index]

    def _get_channel_characteristics_ac_current_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_current_switching_max[index]

    def _get_channel_characteristics_ac_power_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_power_carry_max[index]

    def _get_channel_characteristics_ac_power_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_power_switching_max[index]

    def _get_channel_characteristics_ac_voltage_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_ac_voltage_max[index]

    def _get_channel_characteristics_bandwidth(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_bandwidth[index]

    def _get_channel_name(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_name[index]

    def _get_channel_characteristics_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_impedance[index]

    def _get_channel_characteristics_dc_current_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_current_carry_max[index]

    def _get_channel_characteristics_dc_current_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_current_switching_max[index]

    def _get_channel_characteristics_dc_power_carry_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_power_carry_max[index]

    def _get_channel_characteristics_dc_power_switching_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_power_switching_max[index]

    def _get_channel_characteristics_dc_voltage_max(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_dc_voltage_max[index]

    def _get_channel_is_configuration_channel(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_is_configuration_channel[index]

    def _set_channel_is_configuration_channel(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_is_configuration_channel[index] = value

    def _get_path_is_debounced(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._path_is_debounced[index]

    def _get_channel_is_source_channel(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_is_source_channel[index]

    def _set_channel_is_source_channel(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = bool(value)
        self._channel_is_source_channel[index] = value

    def _get_channel_characteristics_settling_time(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_settling_time[index]

    def _get_channel_characteristics_wire_mode(self, index):
        index = ivi.get_index(self._channel_name, index)
        return self._channel_characteristics_wire_mode[index]

    def _path_can_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
        return False

    def _path_connect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)

    def _path_disconnect(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)

    def _path_disconnect_all(self):
        pass

    def _path_get_path(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
        return []

    def _path_set_path(self, path):
        pass

    def _path_wait_for_debounce(self, maximum_time):
        pass