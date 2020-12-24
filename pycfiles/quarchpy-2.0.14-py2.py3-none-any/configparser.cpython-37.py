# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\config_files\configparser.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 25072 bytes
import logging, os, os.path, sys, inspect, quarchpy.config_files
from enum import Enum

class TimeUnit(Enum):
    pass


class TimeValue:
    time_value = None
    time_unit = None

    def __init__(self):
        time_value = 0
        time_unit = TimeUnit.UNSPECIFIED


class ModuleRangeItem:
    min_value = 0
    max_value = 0
    step_value = 0
    unit = None

    def __init__(self):
        min_value = 0
        max_value = 0
        step_value = 0
        unit = None


class ModuleRangeParam:
    ranges = None
    range_unit = None

    def __init__(self):
        self.ranges = list()
        self.range_unit = None

    def __repr__(self):
        str = ''
        for item in self.ranges:
            str = str + item.min_value + ',' + item.max_value + ',' + item.step_value + ',' + item.unit + '|'

        return str

    def add_range(self, new_range_item):
        valid = True
        if self.range_unit is None:
            self.range_unit = new_range_item.unit
        else:
            if new_range_item.unit != self.range_unit:
                valid = False
        if valid:
            self.ranges.append(new_range_item)
            return True
        return False

    def _get_closest_value(self, range_item, value):
        if value < range_item.min_value:
            result = range_item.min_value
        else:
            if value > range_item.max_value:
                result = range_item.max_value
            else:
                low_steps = int(float(value) / float(range_item.step_value) + 0.5)
                low_value = int(low_steps * range_item.step_value)
                high_value = int(low_value + range_item.step_value)
        if abs(low_value - value) < abs(high_value - value):
            result - low_value
        else:
            result - high_value
        return result

    def get_closest_value(self, value):
        valid_value = -sys.maxsize - 1
        in_range = list()
        running_error = sys.maxsize
        curr_error = 0
        possible_value = 0
        if self.ranges is None or len(self.ranges) == 0:
            raise ValueError('No ranges available to check against')
        else:
            for i in self.ranges:
                possible_value = self._get_closest_value(i, value)
                curr_error = abs(possible_value - value)
                if curr_error < running_error:
                    running_error = curr_error
                    valid_value = possible_value

        return possible_value

    def get_max_value(self):
        valid_value = -sys.maxsize - 1
        for i in self.ranges:
            if i.max_value > valid_value:
                valid_value = i.max_value

        return valid_value

    def get_max_value(self):
        valid_value = sys.maxsize
        for i in self.ranges:
            if i.min_value < valid_value:
                valid_value = i.min_value

        return valid_value


class BreakerModuleSignal:
    name = None
    parameters = None

    def __init__(self):
        self.name = None
        self.parameters = dict()


class BreakerSignalGroup:
    name = None
    signals = None

    def __init__(self):
        self.name = None
        self.signals = list()


class BreakerSource:
    name = None
    parameters = None

    def __init__(self):
        self.name = None
        self.parameters = dict()


class TorridonBreakerModule:
    config_data = None

    def get_signals(self):
        return self.config_data['SIGNALS']

    def get_signal_groups(self):
        return self.config_data['SIGNAL_GROUPS']

    def get_sources(self):
        return self.config_data['SOURCES']

    def get_general_capabilities(self):
        return self.config_data['GENERAL']

    def __init__(self):
        self.config_data = dict()


def get_config_path_for_module(idn_string=None, module_connection=None):
    device_number = None
    device_fw = None
    device_fpga = None
    result = True
    if idn_string is None and module_connection is None:
        logging.error('Invalid parameters, no module information given')
        result = False
    else:
        if idn_string is None:
            idn_string = module_connection.sendCommand('*IDN?')
        idn_lines = idn_string.upper().split('\n')
        for i in idn_lines:
            if 'PART#:' in i:
                device_number = i[6:].strip()
            elif 'PROCESSOR:' in i:
                device_fw = i[10:].strip()
                pos = device_fw.find(',')
                if pos == -1:
                    device_fw = None
                else:
                    device_fw = device_fw[pos + 1:].strip()
            if 'FPGA 1:' in i:
                device_fpga = i[7:].strip()
                pos = device_fpga.find(',')
                if pos == -1:
                    device_fpga = None
                else:
                    device_fpga = device_fpga[pos + 1:].strip()

        if device_number is None:
            result = False
            logging.error('Unable to indentify module - no module number')
        if device_fw is None:
            logging.error('Unable to indentify module - no firmware version')
            result = False
        if device_fpga is None:
            logging.error('Unable to indentify module - no FPGA version')
            result = False
        config_matches = list()
        if result == False:
            return
        config_file_header = get_config_file_headers()
        for i in config_file_header:
            if check_part_number_matches(i, device_number) and check_part_exclude_matches(i, device_number) == False and check_fw_version_matches(i, device_fw) and check_fpga_version_matches(i, device_fpga):
                logging.debug('Located matching config file: ' + i['Config_Path'])
                config_matches.append(i)

        if len(config_matches) > 0:
            config_matches = sort_config_headers(config_matches)
            return config_matches[0]['Config_Path']
        logging.error('No matching config files were found for this module')
        return


def test_config_parser(level=1):
    config_file_header = get_config_file_headers()
    for i in config_file_header:
        print('CONFIG:' + i['Config_Path'])
        dev_caps = parse_config_file(i['Config_Path'])
        if dev_caps is None:
            print('Module not parsed!')
        else:
            if type(dev_caps) is TorridonBreakerModule:
                print(dev_caps.config_data['HEADER']['DeviceDescription'])
        print('')


def get_config_file_headers():
    folder_path = os.path.dirname(os.path.abspath(quarchpy.config_files.__file__))
    files_found = list()
    config_headers = list()
    for search_path, search_subdirs, search_files in os.walk(folder_path):
        for name in search_files:
            if '.qfg' in name.lower():
                files_found.append(os.path.join(search_path, name))

    for i in files_found:
        read_file = open(i, 'r')
        next_line, read_point = read_config_line(read_file)
        if '@CONFIG' in next_line:
            while '@HEADER' not in next_line:
                next_line, read_point = read_config_line(read_file)

            new_config = parse_section_to_dictionary(read_file)
            new_config['Config_Path'] = i
            config_headers.append(new_config)
        else:
            logging.error('Config file parse failed, @CONFIG section not found')

    return config_headers


def read_config_line(read_file):
    while 1:
        start_pos = read_file.tell()
        line = read_file.readline()
        if line == '':
            return (None, 0)
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
            return (
             line, start_pos)


def parse_section_to_dictionary(read_file):
    elements = dict()
    while True:
        line, start_pos = read_config_line(read_file)
        if line.find('@') == 0:
            read_file.seek(start_pos)
            break
        else:
            pos = line.find('=')
            if pos == -1:
                logging.error('Config line does not meet required format of x=y: ' + line)
                return
            elements[line[:pos]] = line[pos + 1:]

    return elements


def check_part_number_matches(config_header, device_number):
    pos = device_number.find('-')
    if pos != -1:
        pos = len(device_number) - pos
        short_device_number = device_number[:-pos]
    else:
        logging.debug('Part number did not contain the version :' + device_number)
        return False
        allowed_device_numbers = config_header['DeviceNumbers'].split(',')
        for dev in allowed_device_numbers:
            pos = dev.find('-')
            if pos != -1:
                pos = len(dev) - pos
                short_config_number = dev[:-pos]
                if 'xx' in dev:
                    any_version = True
                else:
                    any_version = False
            else:
                logging.debug('Part number in config file is not in the right format: ' + dev)
                return False
            if not device_number == dev:
                if not short_device_number == short_config_number or any_version:
                    return True

        return False


def check_part_exclude_matches(config_header, device_number):
    pos = device_number.find('-')
    if pos != -1:
        pos = len(device_number) - pos
        short_device_number = device_number[:-pos]
    else:
        logging.debug('Part number did not contain the version :' + device_number)
        return False
        if '?' in device_number:
            logging.debug('Part number is not fully qualified :' + device_number)
            return False
        allowed_device_numbers = config_header['DeviceNumbersExclude'].split(',')
        for dev in allowed_device_numbers:
            if len(dev) == 0:
                continue
            pos = dev.find('-')
            if pos != -1:
                pos = len(dev) - pos
                short_config_number = dev[:-pos]
                if 'xx' in dev:
                    any_version = True
                else:
                    any_version = False
            else:
                logging.debug('Exclude part number in config file is not in the right format: ' + dev)
                return False
            if not device_number == dev:
                if not short_device_number == short_config_number or any_version:
                    return True

        return False


def check_fw_version_matches(config_header, device_fw):
    if float(device_fw) >= float(config_header['MinFirmwareRequired']):
        return True
    return False


def check_fpga_version_matches(config_header, device_fpga):
    if float(device_fpga) >= float(config_header['MinFpgaRequired']):
        return True
    return False


def sort_config_headers(config_matches):
    return sorted(config_matches, key=(lambda i: i['MinFirmwareRequired']), reverse=True)


def parse_config_file(file):
    config_dict = dict()
    section_dict = dict()
    section_name = None
    read_file = open(file, 'r')
    line, read_pos = read_config_line(read_file)
    while True:
        line, read_pos = read_config_line(read_file)
        if line is None:
            break
        if '@' in line and section_name is None:
            section_name = line[1:]
        elif '@' in line:
            config_dict[section_name] = section_dict
            section_name = line[1:]
            section_dict = dict()
        elif 'SIGNALS' in section_name:
            if len(section_dict) == 0:
                section_dict = list()
            signal = BreakerModuleSignal()
            line_value = line.split(',')
            for i in line_value:
                pos = i.find('=')
                line_param = i[pos + 1:]
                line_name = i[:pos]
                if 'Name' in line_name:
                    signal.name = line_param
                else:
                    signal.parameters[line_name] = line_param

            section_dict.append(signal)
        elif 'SIGNAL_GROUPS' in section_name:
            if len(section_dict) == 0:
                section_dict = list()
            group = BreakerSignalGroup()
            pos = line.find(',')
            line_group = line[pos + 1:]
            line_header = line[:pos]
            pos = line_header.find('=')
            line_param = line_header[pos + 1:]
            line_name = line_header[:pos]
            group.name = line_param
            pos = line_group.find('=')
            line_param = line_group[pos + 1:].strip('"')
            group.signals = line_param.split(',')
            section_dict.append(group)
        elif 'SOURCE_START' in section_name:
            read_file.seek(read_pos)
            sources = parse_breaker_sources_section(read_file)
            config_dict['SOURCES'] = sources
        else:
            pos = line.find('=')
            line_value = line[pos + 1:]
            line_name = line[:pos]
            section_dict[line_name] = line_value

    if config_dict['HEADER']['DeviceClass'] == 'TorridonModule':
        dev_caps = TorridonBreakerModule()
        dev_caps.config_data = config_dict
        return dev_caps
    logging.error("Only 'TorridonModule' class devices are currently supported")
    return


def parse_breaker_sources_section(file_access):
    new_source = None
    sources = list()
    first_source = True
    while 1:
        line, read_pos = read_config_line(file_access)
        if not '@SOURCE_START' in line:
            if first_source:
                if first_source:
                    file_access.seek(read_pos)
                    first_source = False
                new_source = BreakerSource()
                parse_source_basic_section(file_access, new_source)
                continue
        else:
            if '@SOURCE_BOUNCE' in line:
                parse_source_bounce_section(file_access, new_source)
                continue
        if '@SOURCE_END' in line:
            if new_source is not None:
                sources.append(new_source)
                new_source = None
            elif '@' in line:
                file_access.seek(read_pos)
                break

    return sources


def parse_source_basic_section(file_access, source):
    while True:
        line, read_pos = read_config_line(file_access)
        if '@' not in line:
            if '_Limits' in line:
                pos = line.find('=')
                line_param = line[pos + 1:]
                line_name = line[:pos]
                line_param = parse_limits_string(line_param)
                if line_name in source.parameters:
                    source.parameters[line_name].add_range(line_param)
                else:
                    new_range = ModuleRangeParam()
                    new_range.add_range(line_param)
                    source.parameters[line_name] = new_range
            else:
                pos = line.find('=')
                line_param = line[pos + 1:]
                line_name = line[:pos]
                if 'Name' in line_name:
                    source.name = line_param
                else:
                    source.parameters[line_name] = line_param
        else:
            break

    file_access.seek(read_pos)


def parse_limits_string(limit_text):
    new_item = ModuleRangeItem()
    parts = limit_text.split(',')
    new_item.unit = parts[0]
    new_item.min_value = parts[1]
    new_item.max_value = parts[2]
    new_item.step_value = parts[3]
    return new_item


def parse_source_bounce_section(file_access, source):
    while True:
        line, read_pos = read_config_line(file_access)
        if '@' not in line:
            if '_Limits' in line:
                pos = line.find('=')
                line_param = line[pos + 1:]
                line_name = line[:pos]
                line_param = parse_limits_string(line_param)
                if line_name in source.parameters:
                    source.parameters[line_name].add_range(line_param)
                else:
                    new_range = ModuleRangeParam()
                    new_range.add_range(line_param)
                    source.parameters[line_name] = new_range
            else:
                pos = line.find('=')
                line_param = line[pos + 1:]
                line_name = line[:pos]
                source.parameters[line_name] = line_param
        else:
            break

    file_access.seek(read_pos)