# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/utils/brpylib.py
# Compiled at: 2020-03-11 06:54:20
# Size of source mod 2**32: 71226 bytes
"""
Collection of classes used for reading headers and data from Blackrock files
current version: 1.3.2 --- 08/12/2016

@author: Mitch Frankel - Blackrock Microsystems
     Stephen Hou - v1.4.0 edits

Version History:
v1.0.0 - 07/05/2016 - initial release - requires brMiscFxns v1.0.0
v1.1.0 - 07/08/2016 - inclusion of NsxFile.savesubsetnsx() for saving subset of Nsx data to disk4
v1.1.1 - 07/09/2016 - update to NsxFile.savesubsetnsx() for option (not)overwriting subset files if already exist
                      bug fixes in NsxFile class as reported from beta user
v1.2.0 - 07/12/2016 - bug fixes in NsxFile.savesubsetnsx()
                      added version control and checking for brMiscFxns
                      requires brMiscFxns v1.1.0
v1.3.0 - 07/22/2016 - added 'samp_per_s' to NsxFile.getdata() output
                      added close() method to NsxFile and NevFile objects
                      NsxFile.getdata() now pre-allocates output['data'] as zeros - speed and safety
v1.3.1 - 08/02/2016 - bug fixes to NsxFile.getdata() for usability with Python 2.7 as reported from beta user
                      patch for use with multiple NSP sync (overwriting of initial null data from initial data packet)
                      __future__ import for use with Python 2.7 (division)
                      minor modifications to allow use of Python 2.6+
v1.3.2 - 08/12/2016 - bug fixes to NsXFile.getdata()
v1.4.0 - 06/22/2017 - inclusion of wave_read parameter to NevFile.getdata() for including/excluding waveform data

"""
import numpy as np
from collections import namedtuple
from datetime import datetime
from math import ceil
from os import path as ospath
from struct import calcsize, pack, unpack, unpack_from
brpylib_ver = '1.3.2'
brmiscfxns_ver_req = '1.2.0'
brmiscfxns_ver = '1.2.0'
if brmiscfxns_ver.split('.') < brmiscfxns_ver_req.split('.'):
    raise Exception('brpylib requires brMiscFxns ' + brmiscfxns_ver_req + ' or higher, please use latest version')
try:
    input = raw_input
except NameError:
    pass

WARNING_SLEEP_TIME = 5
DATA_PAGING_SIZE = 1073741824
DATA_FILE_SIZE_MIN = 10485760
STRING_TERMINUS = '\x00'
UNDEFINED = 0
ELEC_ID_DEF = 'all'
START_TIME_DEF = 0
DATA_TIME_DEF = 'all'
DOWNSAMPLE_DEF = 1
START_OFFSET_MIN = 0
STOP_OFFSET_MIN = 0
UV_PER_BIT_21 = 0.25
WAVEFORM_SAMPLES_21 = 48
NSX_BASIC_HEADER_BYTES_22 = 314
NSX_EXT_HEADER_BYTES_22 = 66
DATA_BYTE_SIZE = 2
TIMESTAMP_NULL_21 = 0
NO_FILTER = 0
BUTTER_FILTER = 1
SERIAL_MODE = 0
RB2D_MARKER = 1
RB2D_BLOB = 2
RB3D_MARKER = 3
BOUNDARY_2D = 4
MARKER_SIZE = 5
DIGITAL_PACKET_ID = 0
NEURAL_PACKET_ID_MIN = 1
NEURAL_PACKET_ID_MAX = 2048
COMMENT_PACKET_ID = 65535
VIDEO_SYNC_PACKET_ID = 65534
TRACKING_PACKET_ID = 65533
BUTTON_PACKET_ID = 65532
CONFIGURATION_PACKET_ID = 65531
PARALLEL_REASON = 1
PERIODIC_REASON = 64
SERIAL_REASON = 129
LOWER_BYTE_MASK = 255
FIRST_BIT_MASK = 1
SECOND_BIT_MASK = 2
CLASSIFIER_MIN = 1
CLASSIFIER_MAX = 16
CLASSIFIER_NOISE = 255
CHARSET_ANSI = 0
CHARSET_UTF = 1
CHARSET_ROI = 255
COMM_RGBA = 0
COMM_TIME = 1
BUTTON_PRESS = 1
BUTTON_RESET = 2
CHG_NORMAL = 0
CHG_CRITICAL = 1
ENTER_EVENT = 1
EXIT_EVENT = 2
FieldDef = namedtuple('FieldDef', ['name', 'formatStr', 'formatFnc'])

def processheaders(curr_file, packet_fields):
    """
    :param curr_file:      {file} the current BR datafile to be processed
    :param packet_fields : {named tuple} the specific binary fields for the given header
    :return:               a fully unpacked and formatted tuple set of header information

    Read a packet from a binary data file and return a list of fields
    The amount and format of data read will be specified by the
    packet_fields container
    """
    packet_format_str = '<' + ''.join([fmt for name, fmt, fun in packet_fields])
    bytes_in_packet = calcsize(packet_format_str)
    packet_binary = curr_file.read(bytes_in_packet)
    packet_unpacked = unpack(packet_format_str, packet_binary)
    data_iter = iter(packet_unpacked)
    packet_formatted = dict.fromkeys([name for name, fmt, fun in packet_fields])
    for name, fmt, fun in packet_fields:
        packet_formatted[name] = fun(data_iter)

    return packet_formatted


def format_filespec(header_list):
    return str(next(header_list)) + '.' + str(next(header_list))


def format_timeorigin(header_list):
    year = next(header_list)
    month = next(header_list)
    _ = next(header_list)
    day = next(header_list)
    hour = next(header_list)
    minute = next(header_list)
    second = next(header_list)
    millisecond = next(header_list)
    return datetime(year, month, day, hour, minute, second, millisecond * 1000)


def format_stripstring(header_list):
    string = bytes.decode(next(header_list), 'latin-1')
    return string.split(STRING_TERMINUS, 1)[0]


def format_none(header_list):
    return next(header_list)


def format_freq(header_list):
    return str(float(next(header_list)) / 1000) + ' Hz'


def format_filter(header_list):
    filter_type = next(header_list)
    if filter_type == NO_FILTER:
        return 'none'
    if filter_type == BUTTER_FILTER:
        return 'butterworth'


def format_charstring(header_list):
    return int(next(header_list))


def format_digconfig(header_list):
    config = next(header_list) & FIRST_BIT_MASK
    if config:
        return 'active'
    return 'ignored'


def format_anaconfig(header_list):
    config = next(header_list)
    if config & FIRST_BIT_MASK:
        return 'low_to_high'
    if config & SECOND_BIT_MASK:
        return 'high_to_low'
    return 'none'


def format_digmode(header_list):
    dig_mode = next(header_list)
    if dig_mode == SERIAL_MODE:
        return 'serial'
    return 'parallel'


def format_trackobjtype(header_list):
    trackobj_type = next(header_list)
    if trackobj_type == UNDEFINED:
        return 'undefined'
    if trackobj_type == RB2D_MARKER:
        return '2D RB markers'
    if trackobj_type == RB2D_BLOB:
        return '2D RB blob'
    if trackobj_type == RB3D_MARKER:
        return '3D RB markers'
    if trackobj_type == BOUNDARY_2D:
        return '2D boundary'
    if trackobj_type == MARKER_SIZE:
        return 'marker size'
    return 'error'


def getdigfactor(ext_headers, idx):
    max_analog = ext_headers[idx]['MaxAnalogValue']
    min_analog = ext_headers[idx]['MinAnalogValue']
    max_digital = ext_headers[idx]['MaxDigitalValue']
    min_digital = ext_headers[idx]['MinDigitalValue']
    return float(max_analog - min_analog) / float(max_digital - min_digital)


nev_header_dict = {'basic':[
  FieldDef('FileTypeID', '8s', format_stripstring),
  FieldDef('FileSpec', '2B', format_filespec),
  FieldDef('AddFlags', 'H', format_none),
  FieldDef('BytesInHeader', 'I', format_none),
  FieldDef('BytesInDataPackets', 'I', format_none),
  FieldDef('TimeStampResolution', 'I', format_none),
  FieldDef('SampleTimeResolution', 'I', format_none),
  FieldDef('TimeOrigin', '8H', format_timeorigin),
  FieldDef('CreatingApplication', '32s', format_stripstring),
  FieldDef('Comment', '256s', format_stripstring),
  FieldDef('NumExtendedHeaders', 'I', format_none)], 
 'ARRAYNME':FieldDef('ArrayName', '24s', format_stripstring), 
 'ECOMMENT':FieldDef('ExtraComment', '24s', format_stripstring), 
 'CCOMMENT':FieldDef('ContComment', '24s', format_stripstring), 
 'MAPFILE':FieldDef('MapFile', '24s', format_stripstring), 
 'NEUEVWAV':[
  FieldDef('ElectrodeID', 'H', format_none),
  FieldDef('PhysicalConnector', 'B', format_charstring),
  FieldDef('ConnectorPin', 'B', format_charstring),
  FieldDef('DigitizationFactor', 'H', format_none),
  FieldDef('EnergyThreshold', 'H', format_none),
  FieldDef('HighThreshold', 'h', format_none),
  FieldDef('LowThreshold', 'h', format_none),
  FieldDef('NumSortedUnits', 'B', format_charstring),
  FieldDef('BytesPerWaveform', 'B', format_charstring),
  FieldDef('SpikeWidthSamples', 'H', format_none),
  FieldDef('EmptyBytes', '8s', format_none)], 
 'NEUEVLBL':[
  FieldDef('ElectrodeID', 'H', format_none),
  FieldDef('Label', '16s', format_stripstring),
  FieldDef('EmptyBytes', '6s', format_none)], 
 'NEUEVFLT':[
  FieldDef('ElectrodeID', 'H', format_none),
  FieldDef('HighFreqCorner', 'I', format_freq),
  FieldDef('HighFreqOrder', 'I', format_none),
  FieldDef('HighFreqType', 'H', format_filter),
  FieldDef('LowFreqCorner', 'I', format_freq),
  FieldDef('LowFreqOrder', 'I', format_none),
  FieldDef('LowFreqType', 'H', format_filter),
  FieldDef('EmptyBytes', '2s', format_none)], 
 'DIGLABEL':[
  FieldDef('Label', '16s', format_stripstring),
  FieldDef('Mode', '?', format_digmode),
  FieldDef('EmptyBytes', '7s', format_none)], 
 'NSASEXEV':[
  FieldDef('Frequency', 'H', format_none),
  FieldDef('DigitalInputConfig', 'B', format_digconfig),
  FieldDef('AnalogCh1Config', 'B', format_anaconfig),
  FieldDef('AnalogCh1DetectVal', 'h', format_none),
  FieldDef('AnalogCh2Config', 'B', format_anaconfig),
  FieldDef('AnalogCh2DetectVal', 'h', format_none),
  FieldDef('AnalogCh3Config', 'B', format_anaconfig),
  FieldDef('AnalogCh3DetectVal', 'h', format_none),
  FieldDef('AnalogCh4Config', 'B', format_anaconfig),
  FieldDef('AnalogCh4DetectVal', 'h', format_none),
  FieldDef('AnalogCh5Config', 'B', format_anaconfig),
  FieldDef('AnalogCh5DetectVal', 'h', format_none),
  FieldDef('EmptyBytes', '6s', format_none)], 
 'VIDEOSYN':[
  FieldDef('VideoSourceID', 'H', format_none),
  FieldDef('VideoSource', '16s', format_stripstring),
  FieldDef('FrameRate', 'f', format_none),
  FieldDef('EmptyBytes', '2s', format_none)], 
 'TRACKOBJ':[
  FieldDef('TrackableType', 'H', format_trackobjtype),
  FieldDef('TrackableID', 'H', format_none),
  FieldDef('PointCount', 'H', format_none),
  FieldDef('VideoSource', '16s', format_stripstring),
  FieldDef('EmptyBytes', '2s', format_none)]}
nsx_header_dict = {'basic_21':[
  FieldDef('Label', '16s', format_stripstring),
  FieldDef('Period', 'I', format_none),
  FieldDef('ChannelCount', 'I', format_none)], 
 'basic':[
  FieldDef('FileSpec', '2B', format_filespec),
  FieldDef('BytesInHeader', 'I', format_none),
  FieldDef('Label', '16s', format_stripstring),
  FieldDef('Comment', '256s', format_stripstring),
  FieldDef('Period', 'I', format_none),
  FieldDef('TimeStampResolution', 'I', format_none),
  FieldDef('TimeOrigin', '8H', format_timeorigin),
  FieldDef('ChannelCount', 'I', format_none)], 
 'extended':[
  FieldDef('Type', '2s', format_stripstring),
  FieldDef('ElectrodeID', 'H', format_none),
  FieldDef('ElectrodeLabel', '16s', format_stripstring),
  FieldDef('PhysicalConnector', 'B', format_none),
  FieldDef('ConnectorPin', 'B', format_none),
  FieldDef('MinDigitalValue', 'h', format_none),
  FieldDef('MaxDigitalValue', 'h', format_none),
  FieldDef('MinAnalogValue', 'h', format_none),
  FieldDef('MaxAnalogValue', 'h', format_none),
  FieldDef('Units', '16s', format_stripstring),
  FieldDef('HighFreqCorner', 'I', format_freq),
  FieldDef('HighFreqOrder', 'I', format_none),
  FieldDef('HighFreqType', 'H', format_filter),
  FieldDef('LowFreqCorner', 'I', format_freq),
  FieldDef('LowFreqOrder', 'I', format_none),
  FieldDef('LowFreqType', 'H', format_filter)], 
 'data':[
  FieldDef('Header', 'B', format_none),
  FieldDef('Timestamp', 'I', format_none),
  FieldDef('NumDataPoints', 'I', format_none)]}

def check_elecid(elec_ids):
    if type(elec_ids) is str:
        if elec_ids != ELEC_ID_DEF:
            print("\n*** WARNING: Electrode IDs must be 'all', a single integer, or a list of integers.")
            print("      Setting elec_ids to 'all'")
            elec_ids = ELEC_ID_DEF
    elif elec_ids != ELEC_ID_DEF:
        if type(elec_ids) is not list:
            if type(elec_ids) == range:
                elec_ids = list(elec_ids)
            else:
                if type(elec_ids) == int:
                    elec_ids = [
                     elec_ids]
    return elec_ids


def check_starttime--- This code section failed: ---

 L. 366         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'start_time_s'
                4  LOAD_GLOBAL              int
                6  LOAD_GLOBAL              float
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_FALSE    36  'to 36'

 L. 367        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'start_time_s'
               18  LOAD_GLOBAL              int
               20  LOAD_GLOBAL              float
               22  BUILD_TUPLE_2         2 
               24  CALL_FUNCTION_2       2  '2 positional arguments'
               26  POP_JUMP_IF_FALSE    48  'to 48'
               28  LOAD_FAST                'start_time_s'
               30  LOAD_GLOBAL              START_TIME_DEF
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    48  'to 48'
             36_0  COME_FROM            12  '12'

 L. 368        36  LOAD_GLOBAL              print
               38  LOAD_STR                 '\n*** WARNING: Start time is not valid, setting start_time_s to 0'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  POP_TOP          

 L. 369        44  LOAD_GLOBAL              START_TIME_DEF
               46  STORE_FAST               'start_time_s'
             48_0  COME_FROM            34  '34'
             48_1  COME_FROM            26  '26'

 L. 370        48  LOAD_FAST                'start_time_s'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 50


def check_datatime(data_time_s):
    if type(data_time_s) is str and data_time_s != DATA_TIME_DEF or isinstance(data_time_s, (int, float)):
        if data_time_s < 0:
            print("\n*** WARNING: Data time is not valid, setting data_time_s to 'all'")
            data_time_s = DATA_TIME_DEF
    return data_time_s


def check_downsample(downsample):
    if not isinstance(downsample, int) or downsample < DOWNSAMPLE_DEF:
        print('\n*** WARNING: Downsample must be an integer value greater than 0.       Setting downsample to 1 (no downsampling)')
        downsample = DOWNSAMPLE_DEF
    return downsample


def check_dataelecid(elec_ids, all_elec_ids):
    unique_elec_ids = set(elec_ids)
    all_elec_ids = set(all_elec_ids)
    if not unique_elec_ids.issubset(all_elec_ids):
        if not unique_elec_ids & all_elec_ids:
            print('\nNone of the elec_ids passed exist in the data, returning None')
            return
        print('\n*** WARNING: Channels ' + str(sorted(list(unique_elec_ids - all_elec_ids))) + ' do not exist in the data')
        unique_elec_ids = unique_elec_ids & all_elec_ids
    return sorted(list(unique_elec_ids))


def check_filesize(file_size):
    if file_size < DATA_FILE_SIZE_MIN:
        print('\n file_size must be larger than 10 Mb, setting file_size=10 Mb')
        return DATA_FILE_SIZE_MIN
    return int(file_size)


def openfilecheck(open_mode, file_name='', file_ext='', file_type=''):
    """
    :param open_mode: {str} method to open the file (e.g., 'rb' for binary read only)
    :param file_name: [optional] {str} full path of file to open
    :param file_ext:  [optional] {str} file extension (e.g., '.nev')
    :param file_type: [optional] {str} file type for use when browsing for file (e.g., 'Blackrock NEV Files')
    :return: {file} opened file
    """
    while True:
        if not file_name:
            raise Exception('Invalid file name')
        if ospath.isfile(file_name):
            if file_ext:
                _, fext = ospath.splitext(file_name)
                if file_ext[(-1)] == '*':
                    test_extension = file_ext[:-1]
                else:
                    test_extension = file_ext
                if fext[0:len(test_extension)] != test_extension:
                    file_name = ''
                    print('\n*** File given is not a ' + file_ext + ' file, try again ***\n')
                    continue
            break
        else:
            file_name = ''
            print('\n*** File given does exist, try again ***\n')

    return open(file_name, open_mode)


def checkequal(iterator):
    try:
        iterator = iter(iterator)
        first = next(iterator)
        return all((first == rest for rest in iterator))
    except StopIteration:
        return True


class NevFile:
    __doc__ = '\n    attributes and methods for all BR event data files.  Initialization opens the file and extracts the\n    basic header information.\n    '

    def __init__(self, datafile=''):
        self.datafile = datafile
        self.basic_header = {}
        self.extended_headers = []
        self.datafile = openfilecheck('rb', file_name=(self.datafile), file_ext='.nev', file_type='Blackrock NEV Files')
        self.basic_header = processheaders(self.datafile, nev_header_dict['basic'])
        for i in range(self.basic_header['NumExtendedHeaders']):
            self.extended_headers.append({})
            header_string = bytes.decode(unpack('<8s', self.datafile.read(8))[0], 'latin-1')
            self.extended_headers[i]['PacketID'] = header_string.split(STRING_TERMINUS, 1)[0]
            self.extended_headers[i].update(processheaders(self.datafile, nev_header_dict[self.extended_headers[i]['PacketID']]))
            if header_string == 'NEUEVWAV' and float(self.basic_header['FileSpec']) < 2.3:
                self.extended_headers[i]['SpikeWidthSamples'] = WAVEFORM_SAMPLES_21

    def getdata(self, elec_ids='all', wave_read='read'):
        """
        This function is used to return a set of data from the NSx datafile.

        :param elec_ids: [optional] {list} User selection of elec_ids to extract specific spike waveforms (e.g., [13])
        :param wave_read: [optional] {STR} 'read' or 'no_read' - whether to read waveforms or not
        :return: output: {Dictionary} with one or more of the following dictionaries (all include TimeStamps)
                    dig_events:            Reason, Data, [for file spec 2.2 and below, AnalogData and AnalogDataUnits]
                    spike_events:          Units='nV', ChannelID, NEUEVWAV_HeaderIndices, Classification, Waveforms
                    comments:              CharSet, Flag, Data, Comment
                    video_sync_events:     VideoFileNum, VideoFrameNum, VideoElapsedTime_ms, VideoSourceID
                    tracking_events:       ParentID, NodeID, NodeCount, PointCount, TrackingPoints
                    button_trigger_events: TriggerType
                    configuration_events:  ConfigChangeType, ConfigChanged

        Note: For digital and neural data - TimeStamps, Classification, and Data can be lists of lists when more
        than one digital type or spike event exists for a channel
        """
        output = dict()
        self.datafile.seek(self.basic_header['BytesInHeader'], 0)
        elec_ids = check_elecid(elec_ids)
        while self.datafile.tell() != ospath.getsize(self.datafile.name):
            time_stamp = unpack('<I', self.datafile.read(4))[0]
            packet_id = unpack('<H', self.datafile.read(2))[0]
            if not elec_ids == 'all':
                if packet_id in elec_ids:
                    if not NEURAL_PACKET_ID_MIN <= packet_id <= NEURAL_PACKET_ID_MAX:
                        self.datafile.seek(self.basic_header['BytesInDataPackets'] - 6, 1)
                        continue
                else:
                    if packet_id == DIGITAL_PACKET_ID:
                        if 'dig_events' not in output:
                            output['dig_events'] = {'Reason':[],  'TimeStamps':[],  'Data':[]}
                        else:
                            reason = unpack('B', self.datafile.read(1))[0]
                            if reason == PARALLEL_REASON:
                                reason = 'parallel'
                            else:
                                if reason == PERIODIC_REASON:
                                    reason = 'periodic'
                                else:
                                    if reason == SERIAL_REASON:
                                        reason = 'serial'
                                    else:
                                        reason = 'unknown'
                        self.datafile.seek(1, 1)
                        if reason in output['dig_events']['Reason']:
                            idx = output['dig_events']['Reason'].index(reason)
                        else:
                            idx = -1
                            output['dig_events']['Reason'].append(reason)
                            output['dig_events']['TimeStamps'].append([])
                            output['dig_events']['Data'].append([])
                        output['dig_events']['TimeStamps'][idx].append(time_stamp)
                        output['dig_events']['Data'][idx].append(unpack('<H', self.datafile.read(2))[0])
                        if reason == 'serial':
                            output['dig_events']['Data'][idx][(-1)] &= LOWER_BYTE_MASK
                        if float(self.basic_header['FileSpec']) < 2.3:
                            if 'AnalogDataUnits' not in output['dig_events']:
                                output['dig_events']['AnalogDataUnits'] = 'mv'
                            output['dig_events']['AnalogData'].append([])
                            for j in range(5):
                                output['dig_events']['AnalogData'][(-1)].append(unpack('<h', self.datafile.read(2))[0])

                        else:
                            self.datafile.seek(self.basic_header['BytesInDataPackets'] - 10, 1)
                if NEURAL_PACKET_ID_MIN <= packet_id <= NEURAL_PACKET_ID_MAX:
                    if 'spike_events' not in output:
                        output['spike_events'] = {'Units':'nV', 
                         'ChannelID':[],  'TimeStamps':[],  'NEUEVWAV_HeaderIndices':[],  'Classification':[],  'Waveforms':[]}
                    else:
                        classifier = unpack('B', self.datafile.read(1))[0]
                        if classifier == UNDEFINED:
                            classifier = 'none'
                        else:
                            if CLASSIFIER_MIN <= classifier <= CLASSIFIER_MAX:
                                classifier = classifier
                            else:
                                if classifier == CLASSIFIER_NOISE:
                                    classifier = 'noise'
                                else:
                                    classifier = 'error'
                        self.datafile.seek(1, 1)
                        if packet_id in output['spike_events']['ChannelID']:
                            idx = output['spike_events']['ChannelID'].index(packet_id)
                        else:
                            idx = -1
                            output['spike_events']['ChannelID'].append(packet_id)
                            output['spike_events']['TimeStamps'].append([])
                            output['spike_events']['Classification'].append([])
                            output['spike_events']['NEUEVWAV_HeaderIndices'].append(next((item for item, d in enumerate(self.extended_headers) if d['ElectrodeID'] == packet_id if d['PacketID'] == 'NEUEVWAV')))
                        output['spike_events']['TimeStamps'][idx].append(time_stamp)
                        output['spike_events']['Classification'][idx].append(classifier)
                        ext_header_idx = output['spike_events']['NEUEVWAV_HeaderIndices'][idx]
                        samples = self.extended_headers[ext_header_idx]['SpikeWidthSamples']
                        dig_factor = self.extended_headers[ext_header_idx]['DigitizationFactor']
                        num_bytes = self.extended_headers[ext_header_idx]['BytesPerWaveform']
                        if num_bytes <= 1:
                            data_type = np.int8
                        else:
                            if num_bytes == 2:
                                data_type = np.int16
                    if wave_read == 'read':
                        if idx == -1:
                            output['spike_events']['Waveforms'].append([
                             np.fromfile(file=(self.datafile), dtype=data_type, count=samples).astype(np.int32) * dig_factor])
                        else:
                            output['spike_events']['Waveforms'][idx] = np.append((output['spike_events']['Waveforms'][idx]), [
                             np.fromfile(file=(self.datafile), dtype=data_type, count=samples).astype(np.int32) * dig_factor],
                              axis=0)
                    elif wave_read == 'noread':
                        if idx == -1:
                            self.datafile.seek(self.basic_header['BytesInDataPackets'] - 8, 1)
                else:
                    self.datafile.seek(self.basic_header['BytesInDataPackets'] - 8, 1)
            elif packet_id == COMMENT_PACKET_ID:
                if 'comments' not in output:
                    output['comments'] = {'TimeStamps':[],  'CharSet':[],  'Flag':[],  'Data':[],  'Comment':[]}
                else:
                    output['comments']['TimeStamps'].append(time_stamp)
                    char_set = unpack('B', self.datafile.read(1))[0]
                    if char_set == CHARSET_ANSI:
                        output['comments']['CharSet'].append('ANSI')
                    else:
                        if char_set == CHARSET_UTF:
                            output['comments']['CharSet'].append('UTF-16')
                        else:
                            if char_set == CHARSET_ROI:
                                output['comments']['CharSet'].append('NeuroMotive ROI')
                            else:
                                output['comments']['CharSet'].append('error')
                    comm_flag = unpack('B', self.datafile.read(1))[0]
                    if comm_flag == COMM_RGBA:
                        output['comments']['Flag'].append('RGBA color code')
                    else:
                        if comm_flag == COMM_TIME:
                            output['comments']['Flag'].append('timestamp')
                        else:
                            output['comments']['Flag'].append('error')
                output['comments']['Data'].append(unpack('<I', self.datafile.read(4))[0])
                samples = self.basic_header['BytesInDataPackets'] - 12
                comm_string = bytes.decode(self.datafile.read(samples), 'latin-1')
                output['comments']['Comment'].append(comm_string.split(STRING_TERMINUS, 1)[0])
            elif packet_id == VIDEO_SYNC_PACKET_ID:
                if 'video_sync_events' not in output:
                    output['video_sync_events'] = {'TimeStamps':[],  'VideoFileNum':[],  'VideoFrameNum':[],  'VideoElapsedTime_ms':[],  'VideoSourceID':[]}
                output['video_sync_events']['TimeStamps'].append(time_stamp)
                output['video_sync_events']['VideoFileNum'].append(unpack('<H', self.datafile.read(2))[0])
                output['video_sync_events']['VideoFrameNum'].append(unpack('<I', self.datafile.read(4))[0])
                output['video_sync_events']['VideoElapsedTime_ms'].append(unpack('<I', self.datafile.read(4))[0])
                output['video_sync_events']['VideoSourceID'].append(unpack('<I', self.datafile.read(4))[0])
                self.datafile.seek(self.basic_header['BytesInDataPackets'] - 20, 1)
            elif packet_id == TRACKING_PACKET_ID:
                if 'tracking_events' not in output:
                    output['tracking_events'] = {'TimeStamps':[],  'ParentID':[],  'NodeID':[],  'NodeCount':[],  'PointCount':[],  'TrackingPoints':[]}
                output['tracking_events']['TimeStamps'].append(time_stamp)
                output['tracking_events']['ParentID'].append(unpack('<H', self.datafile.read(2))[0])
                output['tracking_events']['NodeID'].append(unpack('<H', self.datafile.read(2))[0])
                output['tracking_events']['NodeCount'].append(unpack('<H', self.datafile.read(2))[0])
                output['tracking_events']['PointCount'].append(unpack('<H', self.datafile.read(2))[0])
                samples = (self.basic_header['BytesInDataPackets'] - 14) // 2
                output['tracking_events']['TrackingPoints'].append(np.fromfile(file=(self.datafile), dtype=(np.uint16), count=samples))
            elif packet_id == BUTTON_PACKET_ID:
                if 'button_trigger_events' not in output:
                    output['button_trigger_events'] = {'TimeStamps':[],  'TriggerType':[]}
                else:
                    output['button_trigger_events']['TimeStamps'].append(time_stamp)
                    trigger_type = unpack('<H', self.datafile.read(2))[0]
                    if trigger_type == UNDEFINED:
                        output['button_trigger_events']['TriggerType'].append('undefined')
                    else:
                        if trigger_type == BUTTON_PRESS:
                            output['button_trigger_events']['TriggerType'].append('button press')
                        else:
                            if trigger_type == BUTTON_RESET:
                                output['button_trigger_events']['TriggerType'].append('event reset')
                            else:
                                output['button_trigger_events']['TriggerType'].append('error')
                self.datafile.seek(self.basic_header['BytesInDataPackets'] - 8, 1)
            elif packet_id == CONFIGURATION_PACKET_ID:
                if 'configuration_events' not in output:
                    output['configuration_events'] = {'TimeStamps':[],  'ConfigChangeType':[],  'ConfigChanged':[]}
                else:
                    output['configuration_events']['TimeStamps'].append(time_stamp)
                    change_type = unpack('<H', self.datafile.read(2))[0]
                    if change_type == CHG_NORMAL:
                        output['configuration_events']['ConfigChangeType'].append('normal')
                    else:
                        if change_type == CHG_CRITICAL:
                            output['configuration_events']['ConfigChangeType'].append('critical')
                        else:
                            output['configuration_events']['ConfigChangeType'].append('error')
                samples = self.basic_header['BytesInDataPackets'] - 8
                output['configuration_events']['ConfigChanged'].append(unpack('<' + str(samples) + 's', self.datafile.read(samples))[0])
            else:
                self.datafile.seek(self.basic_header['BytesInDataPackets'] - 6, 1)

        return output

    def processroicomments(self, comments):
        """
        used to process the comment data packets associated with NeuroMotive region of interest enter/exit events.
        requires that read_data() has already been run.
        :return: roi_events:   a dictionary of regions, enter timestamps, and exit timestamps for each region
        """
        roi_events = {'Regions':[],  'EnterTimeStamps':[],  'ExitTimeStamps':[]}
        for i in range(len(comments['TimeStamps'])):
            if comments['CharSet'][i] == 'NeuroMotive ROI':
                temp_data = pack('<I', comments['Data'][i])
                roi = unpack_from('<B', temp_data)[0]
                event = unpack_from('<B', temp_data, 1)[0]
                source_label = next((d['VideoSource'] for d in self.extended_headers if d['TrackableID'] == roi))
                if source_label in roi_events['Regions']:
                    idx = roi_events['Regions'].index(source_label)
                else:
                    idx = -1
                    roi_events['Regions'].append(source_label)
                    roi_events['EnterTimeStamps'].append([])
                    roi_events['ExitTimeStamps'].append([])
                if event == ENTER_EVENT:
                    roi_events['EnterTimeStamps'][idx].append(comments['TimeStamp'][i])
                elif event == EXIT_EVENT:
                    roi_events['ExitTimeStamps'][idx].append(comments['TimeStamp'][i])

        return roi_events

    def close(self):
        name = self.datafile.name
        self.datafile.close()


class NsxFile:
    __doc__ = '\n    attributes and methods for all BR continuous data files.  Initialization opens the file and extracts the\n    basic header information.\n    '

    def __init__(self, datafile=''):
        self.datafile = datafile
        self.basic_header = {}
        self.extended_headers = []
        self.datafile = openfilecheck('rb', file_name=(self.datafile), file_ext='.ns*', file_type='Blackrock NSx Files')
        self.basic_header['FileTypeID'] = bytes.decode(self.datafile.read(8), 'latin-1')
        if self.basic_header['FileTypeID'] == 'NEURALSG':
            self.basic_header.update(processheaders(self.datafile, nsx_header_dict['basic_21']))
            self.basic_header['FileSpec'] = '2.1'
            self.basic_header['TimeStampResolution'] = 30000
            self.basic_header['BytesInHeader'] = 32 + 4 * self.basic_header['ChannelCount']
            shape = (1, self.basic_header['ChannelCount'])
            self.basic_header['ChannelID'] = list(np.fromfile(file=(self.datafile), dtype=(np.uint32), count=(self.basic_header['ChannelCount'])).reshape(shape)[0])
        else:
            self.basic_header.update(processheaders(self.datafile, nsx_header_dict['basic']))
            for i in range(self.basic_header['ChannelCount']):
                self.extended_headers.append(processheaders(self.datafile, nsx_header_dict['extended']))

    def getdata(self, elec_ids='all', start_time_s=0, data_time_s='all', downsample=1):
        """
        This function is used to return a set of data from the NSx datafile.

        :param elec_ids:      [optional] {list}  List of elec_ids to extract (e.g., [13])
        :param start_time_s:  [optional] {float} Starting time for data extraction (e.g., 1.0)
        :param data_time_s:   [optional] {float} Length of time of data to return (e.g., 30.0)
        :param downsample:    [optional] {int}   Downsampling factor (e.g., 2)
        :return: output:      {Dictionary} of:  data_headers: {list}        dictionaries of all data headers
                                                elec_ids:     {list}        elec_ids that were extracted (sorted)
                                                start_time_s: {float}       starting time for data extraction
                                                data_time_s:  {float}       length of time of data returned
                                                downsample:   {int}         data downsampling factor
                                                samp_per_s:   {float}       output data samples per second
                                                data:         {numpy array} continuous data in a 2D numpy array

        Parameters: elec_ids, start_time_s, data_time_s, and downsample are not mandatory.  Defaults will assume all
        electrodes and all data points starting at time(0) are to be read. Data is returned as a numpy 2d array
        with each row being the data set for each electrode (e.g. output['data'][0] for output['elec_ids'][0]).
        """
        start_time_s = check_starttime(start_time_s)
        data_time_s = check_datatime(data_time_s)
        downsample = check_downsample(downsample)
        elec_ids = check_elecid(elec_ids)
        output = dict()
        output['elec_ids'] = elec_ids
        output['start_time_s'] = float(start_time_s)
        output['data_time_s'] = data_time_s
        output['downsample'] = downsample
        output['data'] = []
        output['data_headers'] = []
        output['ExtendedHeaderIndices'] = []
        datafile_samp_per_sec = self.basic_header['TimeStampResolution'] / self.basic_header['Period']
        data_pt_size = self.basic_header['ChannelCount'] * DATA_BYTE_SIZE
        elec_id_indices = []
        front_end_idxs = []
        analog_input_idxs = []
        front_end_idx_cont = True
        analog_input_idx_cont = True
        hit_start = False
        hit_stop = False
        d_ptr = 0
        self.datafile.seek(self.basic_header['BytesInHeader'], 0)
        if self.basic_header['FileSpec'] == '2.1':
            output['elec_ids'] = self.basic_header['ChannelID']
            output['data_headers'].append({})
            output['data_headers'][0]['Timestamp'] = TIMESTAMP_NULL_21
            output['data_headers'][0]['NumDataPoints'] = (ospath.getsize(self.datafile.name) - self.datafile.tell()) // (DATA_BYTE_SIZE * self.basic_header['ChannelCount'])
        else:
            output['elec_ids'] = [d['ElectrodeID'] for d in self.extended_headers]
        if start_time_s == START_TIME_DEF:
            start_idx = START_OFFSET_MIN
        else:
            start_idx = int(round(start_time_s * datafile_samp_per_sec))
        if data_time_s == DATA_TIME_DEF:
            stop_idx = STOP_OFFSET_MIN
        else:
            stop_idx = int(round((start_time_s + data_time_s) * datafile_samp_per_sec))
        if elec_ids != ELEC_ID_DEF:
            elec_ids = check_dataelecid(elec_ids, output['elec_ids'])
            if not elec_ids:
                return output
            elec_id_indices = [output['elec_ids'].index(e) for e in elec_ids]
            output['elec_ids'] = elec_ids
        num_elecs = len(output['elec_ids'])
        if self.basic_header['FileSpec'] != '2.1':
            for i in range(num_elecs):
                idx = next((item for item, d in enumerate(self.extended_headers) if d['ElectrodeID'] == output['elec_ids'][i]))
                output['ExtendedHeaderIndices'].append(idx)
                if self.extended_headers[idx]['PhysicalConnector'] < 5:
                    front_end_idxs.append(i)
                else:
                    analog_input_idxs.append(i)

            if any(np.diff(np.array(front_end_idxs)) != 1):
                front_end_idx_cont = False
        else:
            if any(np.diff(np.array(analog_input_idxs)) != 1):
                analog_input_idx_cont = False
            if self.basic_header['FileSpec'] == '2.1':
                timestamp = TIMESTAMP_NULL_21
                num_data_pts = output['data_headers'][0]['NumDataPoints']
            else:
                while self.datafile.tell() != ospath.getsize(self.datafile.name):
                    self.datafile.seek(1, 1)
                    timestamp = unpack('<I', self.datafile.read(4))[0]
                    num_data_pts = unpack('<I', self.datafile.read(4))[0]
                    self.datafile.seek(num_data_pts * self.basic_header['ChannelCount'] * DATA_BYTE_SIZE, 1)

        stop_idx_output = ceil(timestamp / self.basic_header['Period']) + num_data_pts
        if data_time_s != DATA_TIME_DEF:
            if stop_idx < stop_idx_output:
                stop_idx_output = stop_idx
        total_samps = int(ceil((stop_idx_output - start_idx) / downsample))
        if total_samps * self.basic_header['ChannelCount'] * DATA_BYTE_SIZE > DATA_PAGING_SIZE:
            print('\nOutput data requested is larger than 1 GB, attempting to preallocate output now')
        try:
            output['data'] = np.zeros((total_samps, num_elecs), dtype=(np.float32))
        except MemoryError as err:
            try:
                err.args += (" Output data size requested is larger than available memory. Use the parameters\n              for getdata(), e.g., 'elec_ids', to request a subset of the data or use\n              NsxFile.savesubsetnsx() to create subsets of the main nsx file\n", )
                raise
            finally:
                err = None
                del err

        self.datafile.seek(self.basic_header['BytesInHeader'], 0)
        while (hit_stop or self.basic_header['FileSpec']) != '2.1':
            output['data_headers'].append(processheaders(self.datafile, nsx_header_dict['data']))
            if output['data_headers'][(-1)]['Header'] == 0:
                print('Invalid Header.  File may be corrupt')
            if output['data_headers'][(-1)]['NumDataPoints'] < downsample:
                self.datafile.seek(self.basic_header['ChannelCount'] * output['data_headers'][(-1)]['NumDataPoints'] * DATA_BYTE_SIZE, 1)
                continue
            timestamp_sample = int(round(output['data_headers'][(-1)]['Timestamp'] / self.basic_header['Period']))
            if timestamp_sample < d_ptr:
                d_ptr = 0
                hit_start = False
                output['data_headers'] = []
                self.datafile.seek(-9, 1)
                continue
            if len(output['data_headers']) == 1:
                if STOP_OFFSET_MIN < stop_idx < timestamp_sample:
                    print('\nData requested is before any data was saved, which starts at t = {0:.6f} s'.format(output['data_headers'][0]['Timestamp'] / self.basic_header['TimeStampResolution']))
                    return
            if not hit_start:
                start_offset = start_idx - timestamp_sample
                if start_offset > output['data_headers'][(-1)]['NumDataPoints']:
                    self.datafile.seek(output['data_headers'][(-1)]['NumDataPoints'] * data_pt_size, 1)
                    if self.datafile.tell() == ospath.getsize(self.datafile.name):
                        break
                    else:
                        continue
                else:
                    if start_offset < 0:
                        if STOP_OFFSET_MIN < stop_idx < timestamp_sample:
                            print('\nBecause of pausing, data section requested is during pause period')
                            return
                        print('\nFirst data packet requested begins at t = {0:.6f} s, initial section padded with zeros'.format(output['data_headers'][(-1)]['Timestamp'] / self.basic_header['TimeStampResolution']))
                        start_offset = START_OFFSET_MIN
                        d_ptr = (timestamp_sample - start_idx) // downsample
                    hit_start = True
            else:
                if STOP_OFFSET_MIN < stop_idx < timestamp_sample:
                    print('\nSection padded with zeros due to file pausing')
                    hit_stop = True
                    break
                else:
                    if timestamp_sample - start_idx > d_ptr:
                        print('\nSection padded with zeros due to file pausing')
                        start_offset = START_OFFSET_MIN
                        d_ptr = (timestamp_sample - start_idx) // downsample
                    if STOP_OFFSET_MIN < stop_idx <= timestamp_sample + output['data_headers'][(-1)]['NumDataPoints']:
                        total_pts = stop_idx - timestamp_sample - start_offset
                        hit_stop = True
                    else:
                        total_pts = output['data_headers'][(-1)]['NumDataPoints'] - start_offset
                    curr_file_pos = self.datafile.tell()
                    file_offset = int(curr_file_pos + start_offset * data_pt_size)
                    downsample_data_size = data_pt_size * downsample
                    max_length = DATA_PAGING_SIZE // downsample_data_size * downsample_data_size
                    num_loops = int(ceil(total_pts * data_pt_size / max_length))
                    for loop in range(num_loops):
                        if loop == 0:
                            if num_loops == 1:
                                num_pts = total_pts
                            else:
                                num_pts = max_length // data_pt_size
                        else:
                            file_offset += max_length
                            if loop == num_loops - 1:
                                num_pts = total_pts * data_pt_size % max_length // data_pt_size
                            else:
                                num_pts = max_length // data_pt_size
                        if num_loops != 1:
                            print('Data extraction requires paging: {0} of {1}'.format(loop + 1, num_loops))
                        else:
                            num_pts = int(num_pts)
                            shape = (num_pts, self.basic_header['ChannelCount'])
                            mm = np.memmap((self.datafile), dtype=(np.int16), mode='r', offset=file_offset, shape=shape)
                            if downsample != 1:
                                mm = mm[::downsample]
                            if elec_id_indices:
                                output['data'][d_ptr:d_ptr + mm.shape[0]] = np.array(mm[:, elec_id_indices]).astype(np.float32)
                            else:
                                output['data'][d_ptr:d_ptr + mm.shape[0]] = np.array(mm).astype(np.float32)
                        d_ptr += mm.shape[0]
                        del mm

                    curr_file_pos += self.basic_header['ChannelCount'] * output['data_headers'][(-1)]['NumDataPoints'] * DATA_BYTE_SIZE
                    self.datafile.seek(curr_file_pos, 0)
            if curr_file_pos == ospath.getsize(self.datafile.name):
                hit_stop = True

        if (hit_stop or start_idx) > START_OFFSET_MIN:
            raise Exception('Error: End of file found before start_time_s')
        else:
            if not hit_stop:
                if stop_idx:
                    print('\n*** WARNING: End of file found before stop_time_s, returning all data in file')
            output['data'] = output['data'].transpose()
        if self.basic_header['FileSpec'] == '2.1':
            output['data'] *= UV_PER_BIT_21
        else:
            if front_end_idxs:
                if front_end_idx_cont:
                    output['data'][front_end_idxs[0]:front_end_idxs[(-1)] + 1] *= getdigfactor(self.extended_headers, output['ExtendedHeaderIndices'][front_end_idxs[0]])
                else:
                    for i in front_end_idxs:
                        output['data'][i] *= getdigfactor(self.extended_headers, output['ExtendedHeaderIndices'][i])

            if analog_input_idxs:
                if analog_input_idx_cont:
                    output['data'][analog_input_idxs[0]:analog_input_idxs[(-1)] + 1] *= getdigfactor(self.extended_headers, output['ExtendedHeaderIndices'][analog_input_idxs[0]])
                else:
                    for i in analog_input_idxs:
                        output['data'][i] *= getdigfactor(self.extended_headers, output['ExtendedHeaderIndices'][i])

            output['samp_per_s'] = float(datafile_samp_per_sec / downsample)
            output['data_time_s'] = len(output['data'][0]) / output['samp_per_s']
            return output

    def savesubsetnsx(self, elec_ids='all', file_size=None, file_time_s=None, file_suffix=''):
        """
        This function is used to save a subset of data based on electrode IDs, file sizing, or file data time.  If
        both file_time_s and file_size are passed, it will default to file_time_s and determine sizing accordingly.

        :param elec_ids:    [optional] {list}  List of elec_ids to extract (e.g., [13])
        :param file_size:   [optional] {int}   Byte size of each subset file to save (e.g., 1024**3 = 1 Gb). If nothing
                                                   is passed, file_size will be all data points.
        :param file_time_s: [optional] {float} Time length of data for each subset file, in seconds (e.g. 60.0).  If
                                                   nothing is passed, file_size will be used as default.
        :param file_suffix: [optional] {str}   Suffix to append to NSx datafile name for subset files.  If nothing is
                                                   passed, default will be "_subset".
        :return: None - None of the electrodes requested exist in the data
                 SUCCESS - All file subsets extracted and saved
        """
        elec_id_indices = []
        file_num = 1
        pausing = False
        datafile_datapt_size = self.basic_header['ChannelCount'] * DATA_BYTE_SIZE
        self.datafile.seek(0, 0)
        elec_ids = check_elecid(elec_ids)
        if self.basic_header['FileSpec'] == '2.1':
            all_elec_ids = self.basic_header['ChannelID']
        else:
            all_elec_ids = [x['ElectrodeID'] for x in self.extended_headers]
        if elec_ids == ELEC_ID_DEF:
            elec_ids = all_elec_ids
        else:
            elec_ids = check_dataelecid(elec_ids, all_elec_ids)
            if not elec_ids:
                return
            elec_id_indices = [all_elec_ids.index(x) for x in elec_ids]
        num_elecs = len(elec_ids)
        if file_time_s:
            if file_time_s:
                if file_size:
                    print('\nWARNING: Only one of file_size or file_time_s can be passed, defaulting to file_time_s.')
            else:
                file_size = int(num_elecs * DATA_BYTE_SIZE * file_time_s * self.basic_header['TimeStampResolution'] / self.basic_header['Period'])
                if self.basic_header['FileSpec'] == '2.1':
                    file_size += 32 + 4 * num_elecs
                else:
                    file_size += NSX_BASIC_HEADER_BYTES_22 + NSX_EXT_HEADER_BYTES_22 * num_elecs + 5
            print('\nBased on timing request, file size will be {0:d} Mb'.format(int(file_size / 1048576)))
        else:
            if file_size:
                file_size = check_filesize(file_size)
            else:
                file_name, file_ext = ospath.splitext(self.datafile.name)
                if file_suffix:
                    file_name += '_' + file_suffix
                else:
                    file_name += '_subset'
                if ospath.isfile(file_name + '_000' + file_ext):
                    if 'y' != eval(input("\nFile '" + file_name.split('/')[(-1)] + '_xxx' + file_ext + "' already exists, overwrite [y/n]: ")):
                        print('\nExiting, no overwrite, returning None')
                        return
                    print('\n*** Overwriting existing subset files ***')
                subset_file = open(file_name + '_000' + file_ext, 'wb')
                print('\nWriting subset file: ' + ospath.split(subset_file.name)[1])
                if self.basic_header['FileSpec'] == '2.1':
                    subset_file.write(self.datafile.read(28))
                    subset_file.write(np.array(num_elecs).astype(np.uint32).tobytes())
                    subset_file.write(np.array(elec_ids).astype(np.uint32).tobytes())
                    self.datafile.seek(4 + 4 * self.basic_header['ChannelCount'], 1)
                else:
                    subset_file.write(self.datafile.read(10))
                    bytes_in_headers = NSX_BASIC_HEADER_BYTES_22 + NSX_EXT_HEADER_BYTES_22 * num_elecs
                    num_pts_header_pos = bytes_in_headers + 5
                    subset_file.write(np.array(bytes_in_headers).astype(np.uint32).tobytes())
                    self.datafile.seek(4, 1)
                    subset_file.write(self.datafile.read(296))
                    subset_file.write(np.array(num_elecs).astype(np.uint32).tobytes())
                    self.datafile.seek(4, 1)
                    for i in range(len(self.extended_headers)):
                        h_type = self.datafile.read(2)
                        chan_id = self.datafile.read(2)
                        if unpack('<H', chan_id)[0] in elec_ids:
                            subset_file.write(h_type)
                            subset_file.write(chan_id)
                            subset_file.write(self.datafile.read(62))
                        else:
                            self.datafile.seek(62, 1)

            while self.datafile.tell() != ospath.getsize(self.datafile.name):
                if self.basic_header['FileSpec'] == '2.1':
                    packet_pts = (ospath.getsize(self.datafile.name) - self.datafile.tell()) / (DATA_BYTE_SIZE * self.basic_header['ChannelCount'])
                else:
                    header_binary = self.datafile.read(1)
                    timestamp_binary = self.datafile.read(4)
                    packet_pts_binary = self.datafile.read(4)
                    packet_pts = unpack('<I', packet_pts_binary)[0]
                    if packet_pts == 0:
                        continue
                    subset_file.write(header_binary)
                    subset_file.write(timestamp_binary)
                    subset_file.write(packet_pts_binary)
                datafile_pos = self.datafile.tell()
                file_offset = datafile_pos
                mm_length = DATA_PAGING_SIZE // datafile_datapt_size * datafile_datapt_size
                num_loops = int(ceil(packet_pts * datafile_datapt_size / mm_length))
                packet_read_pts = 0
                subset_file_pkt_pts = 0
                for loop in range(num_loops):
                    if loop == 0:
                        if num_loops == 1:
                            num_pts = packet_pts
                        else:
                            num_pts = mm_length // datafile_datapt_size
                    else:
                        file_offset += mm_length
                        if loop == num_loops - 1:
                            num_pts = packet_pts * datafile_datapt_size % mm_length // datafile_datapt_size
                        else:
                            num_pts = mm_length // datafile_datapt_size
                    shape = (
                     int(num_pts), self.basic_header['ChannelCount'])
                    mm = np.memmap((self.datafile), dtype=(np.int16), mode='r', offset=file_offset, shape=shape)
                    if elec_id_indices:
                        mm = mm[:, elec_id_indices]
                    else:
                        start_idx = 0
                        if file_size:
                            if file_size - subset_file.tell() < DATA_PAGING_SIZE:
                                pts_can_add = int((file_size - subset_file.tell()) // (num_elecs * DATA_BYTE_SIZE)) + 1
                                stop_idx = start_idx + pts_can_add
                                while pts_can_add < num_pts:
                                    if elec_id_indices:
                                        subset_file.write(np.array(mm[start_idx:stop_idx]).tobytes())
                                    else:
                                        subset_file.write(mm[start_idx:stop_idx])
                                    prior_file_name = subset_file.name
                                    prior_file_pkt_pts = subset_file_pkt_pts + pts_can_add
                                    subset_file.close()
                                    prior_file = open(prior_file_name, 'rb+')
                                    if file_num < 10:
                                        numstr = '_00' + str(file_num)
                                    else:
                                        if 10 <= file_num < 100:
                                            numstr = '_0' + str(file_num)
                                        else:
                                            numstr = '_' + str(file_num)
                                    subset_file = open(file_name + numstr + file_ext, 'wb')
                                    print('Writing subset file: ' + ospath.split(subset_file.name)[1])
                                    if self.basic_header['FileSpec'] == '2.1':
                                        subset_file.write(prior_file.read(32 + 4 * num_elecs))
                                    else:
                                        subset_file.write(prior_file.read(bytes_in_headers))
                                        subset_file.write(header_binary)
                                        timestamp_new = unpack('<I', timestamp_binary)[0] + (packet_read_pts + pts_can_add) * self.basic_header['Period']
                                        subset_file.write(np.array(timestamp_new).astype(np.uint32).tobytes())
                                        subset_file.write(np.array(num_pts - pts_can_add).astype(np.uint32).tobytes())
                                        prior_file.seek(num_pts_header_pos, 0)
                                        prior_file.write(np.array(prior_file_pkt_pts).astype(np.uint32).tobytes())
                                        num_pts_header_pos = bytes_in_headers + 5
                                    prior_file.close()
                                    packet_read_pts += pts_can_add
                                    start_idx += pts_can_add
                                    num_pts -= pts_can_add
                                    file_num += 1
                                    subset_file_pkt_pts = 0
                                    pausing = False
                                    pts_can_add = int((file_size - subset_file.tell()) // (num_elecs * DATA_BYTE_SIZE)) + 1
                                    stop_idx = start_idx + pts_can_add

                            if elec_id_indices:
                                subset_file.write(np.array(mm[start_idx:]).tobytes())
                        else:
                            subset_file.write(mm[start_idx:])
                    packet_read_pts += num_pts
                    subset_file_pkt_pts += num_pts
                    del mm

                if self.basic_header['FileSpec'] != '2.1':
                    curr_hdr_num_pts_pos = num_pts_header_pos
                    num_pts_header_pos += 4 + subset_file_pkt_pts * num_elecs * DATA_BYTE_SIZE + 5
                datafile_pos += self.basic_header['ChannelCount'] * packet_pts * DATA_BYTE_SIZE
                self.datafile.seek(datafile_pos, 0)
                if file_time_s and not pausing:
                    if self.datafile.tell() != ospath.getsize(self.datafile.name):
                        pausing = True
                        print('\n*** Because of pausing in original datafile, this file may be slightly time shorter\n       than others, and will contain multiple data packets offset in time\n')
                    if self.basic_header['FileSpec'] != '2.1':
                        subset_file_pos = subset_file.tell()
                        subset_file.seek(curr_hdr_num_pts_pos, 0)
                        subset_file.write(np.array(subset_file_pkt_pts).astype(np.uint32).tobytes())
                        subset_file.seek(subset_file_pos, 0)

            subset_file.close()
            print('\n *** All subset files written to disk and closed ***')
            return 'SUCCESS'

    def close(self):
        name = self.datafile.name
        self.datafile.close()