# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/smartctl.py
# Compiled at: 2019-05-16 13:41:33
"""
SMARTctl - command ``/sbin/smartctl -a {device}``
=================================================
"""
from insights.core import CommandParser
from insights.core.plugins import parser
from insights.parsers import ParseException
import re
from insights.specs import Specs

@parser(Specs.smartctl)
class SMARTctl(CommandParser):
    """
    Parser for output of ``smartctl -a`` for each drive in system.

    This stores the information from the output of `smartctl` in the
    following properties:

     * ``device`` - the name of the device after /dev/ - e.g. sda
     * ``information`` - the -i info (vendor, product, etc)
     * ``health`` - overall health assessment (-H)
     * ``values`` - the SMART values (-c) - SMART config on drive firmware
     * ``attributes`` - the SMART attributes (-A) - run time data

    For legacy access, these are also available as values in the ``info``
    dictionary property, keyed to their name (i.e. info['device'])

    Each object contains a different device; the shared information for this
    parser in Insights will be one or more devices, so see the example below
    for how to iterate through the available SMARTctl information for each
    device.

    Sample (abbreviated) output::

        smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.10.0-267.el7.x86_64] (local build)
        Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

        === START OF INFORMATION SECTION ===
        Device Model:     ST500LM021-1KJ152
        Serial Number:    W620AT02
        LU WWN Device Id: 5 000c50 07817bb36
        ...

        === START OF READ SMART DATA SECTION ===
        SMART overall-health self-assessment test result: PASSED

        General SMART Values:
        Offline data collection status:  (0x00) Offline data collection activity
                            was never started.
                            Auto Offline Data Collection: Disabled.
        ...

        SMART Attributes Data Structure revision number: 10
        Vendor Specific SMART Attributes with Thresholds:
        ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
          1 Raw_Read_Error_Rate     0x000f   118   099   034    Pre-fail  Always       -       179599704
          3 Spin_Up_Time            0x0003   098   098   000    Pre-fail  Always       -       0
          4 Start_Stop_Count        0x0032   100   100   020    Old_age   Always       -       546
          5 Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Always       -       0
        ...

    Examples:
        >>> for drive in shared[SMARTctl]:
        ...     print "Device:", drive.device
        ...     print "Model:", drive.information['Device Model']
        ...     print "Health check:", drive.health
        ...     print "Last self-test status:", drive.values['Self-test execution status']
        ...     print "Raw read error rate:", drive.attributes['Raw_Read_Error_Rate']['RAW_VALUE']
        ...
        Device: /dev/sda
        Model: ST500LM021-1KJ152
        Health check: PASSED
        Last self-test status: 0
        Raw read error rate: 179599704

    """
    _INFO_LINE_STR = '(?P<key>\\w+(?:\\s\\w+)*):\\s+' + '(?P<value>\\S.*?)\\s*$'
    _INFO_LINE_RE = re.compile(_INFO_LINE_STR)
    _VALUE_LINE_STR = '(?P<key>\\w[A-Za-z _.-]+):\\s+' + '\\(\\s*(?P<value>\\S.*?)\\)'
    _VALUE_LINE_RE = re.compile(_VALUE_LINE_STR)
    _ATTR_LINE_STR = '^\\s*(?P<id>\\d+)\\s(?P<name>\\w+)\\s+' + '(?P<flag>0x[0-9a-fA-F]{4})\\s+(?P<value>\\d{3})\\s+' + '(?P<worst>\\d{3})\\s+(?P<threshold>\\d{3})\\s+' + '(?P<type>[A-Za-z_-]+)\\s+(?P<updated>[A-Za-z_-]+)\\s+' + '(?P<when_failed>\\S+)\\s+(?P<raw_value>\\S.*)$'
    _ATTR_LINE_RE = re.compile(_ATTR_LINE_STR)

    def __init__(self, context):
        filename_re = re.compile('smartctl_-a_\\.dev\\.(?P<device>\\w+)$')
        match = filename_re.search(context.path)
        if match:
            self.device = '/dev/' + match.group('device')
        else:
            raise ParseException(('Cannot parse device name from path {p}').format(p=context.path))
        super(SMARTctl, self).__init__(context)

    def parse_content(self, content):
        self.information = {}
        self.health = 'not parsed'
        self.values = {}
        self.attributes = {}
        self.full_line = ''
        PARSE_FORMATTED_INFO = 0
        PARSE_FREEFORM_INFO = 1
        PARSE_ATTRIBUTE_INFO = 2
        PARSE_COMPLETE = 3
        parse_state = PARSE_FORMATTED_INFO

        def parse_information(line):
            if line.startswith('=== START OF READ SMART DATA SECTION ==='):
                return PARSE_FREEFORM_INFO
            match = self._INFO_LINE_RE.search(line)
            if match:
                self.information[match.group('key')] = match.group('value')
            elif line == 'Device does not support SMART':
                self.information['SMART support is'] = 'Not supported'
            elif line == 'Device supports SMART and is Enabled':
                self.information['SMART support is'] = 'Enabled'
            elif line == 'Error Counter logging not supported':
                self.information['Error Counter logging'] = 'Not supported'
            elif line == 'Device does not support Self Test logging':
                self.information['Self Test logging'] = 'Not supported'
            elif line == 'Temperature Warning Disabled or Not Supported':
                self.information['Temperature Warning'] = 'Disabled or Not Supported'
            return PARSE_FORMATTED_INFO

        def parse_values(line):
            if line.startswith('Vendor Specific SMART Attributes with Thres'):
                return PARSE_ATTRIBUTE_INFO
            if line.startswith('SMART overall-health self-assessment test r'):
                self.health = ('').join(line.split(': ')[1:])
                return PARSE_FREEFORM_INFO
            if line.startswith('General SMART Values:'):
                return PARSE_FREEFORM_INFO
            if len(line) == 0 or line[0] == ' ' or line[0] == '\t':
                return PARSE_FREEFORM_INFO
            if self.full_line:
                self.full_line += ' '
            self.full_line += line.strip()
            match = self._VALUE_LINE_RE.search(self.full_line)
            if match:
                key, value = match.group('key', 'value')
                self.values[key] = value
                self.full_line = ''
            elif self.full_line.startswith('SMART Attributes Data Structure revision number: '):
                key, value = self.full_line.split(': ')
                self.values[key] = value
                self.full_line = ''
            return PARSE_FREEFORM_INFO

        def parse_attributes(line):
            if line.startswith('SMART Error Log Version:'):
                return PARSE_COMPLETE
            if len(line) == 0:
                return PARSE_ATTRIBUTE_INFO
            match = self._ATTR_LINE_RE.match(line)
            if match:
                name = match.group('name')
                self.attributes[name] = match.groupdict()
            return PARSE_ATTRIBUTE_INFO

        parse_for_state = [
         parse_information,
         parse_values,
         parse_attributes]
        for line in content:
            parse_state = parse_for_state[parse_state](line)
            if parse_state == PARSE_COMPLETE:
                break

        del self.full_line