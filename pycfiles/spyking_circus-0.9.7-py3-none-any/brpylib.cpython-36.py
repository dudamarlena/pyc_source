# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/utils/brpylib.py
# Compiled at: 2019-11-21 11:07:33
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
    else:
        return 'ignored'


def format_anaconfig(header_list):
    config = next(header_list)
    if config & FIRST_BIT_MASK:
        return 'low_to_high'
    else:
        if config & SECOND_BIT_MASK:
            return 'high_to_low'
        return 'none'


def format_digmode(header_list):
    dig_mode = next(header_list)
    if dig_mode == SERIAL_MODE:
        return 'serial'
    else:
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
    else:
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
    if elec_ids != ELEC_ID_DEF:
        if type(elec_ids) is not list:
            if type(elec_ids) == range:
                elec_ids = list(elec_ids)
            elif type(elec_ids) == int:
                elec_ids = [
                 elec_ids]
    return elec_ids


def check_starttime(start_time_s):
    if not isinstance(start_time_s, (int, float)) or isinstance(start_time_s, (int, float)) and start_time_s < START_TIME_DEF:
        print('\n*** WARNING: Start time is not valid, setting start_time_s to 0')
        start_time_s = START_TIME_DEF
    return start_time_s


def check_datatime(data_time_s):
    if type(data_time_s) is str and data_time_s != DATA_TIME_DEF or isinstance(data_time_s, (int, float)) and data_time_s < 0:
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
    else:
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
        return all(first == rest for rest in iterator)
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

    def getdata--- This code section failed: ---

 L. 515         0  LOAD_GLOBAL              dict
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'output'

 L. 516         6  LOAD_FAST                'self'
                8  LOAD_ATTR                datafile
               10  LOAD_ATTR                seek
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                basic_header
               16  LOAD_STR                 'BytesInHeader'
               18  BINARY_SUBSCR    
               20  LOAD_CONST               0
               22  CALL_FUNCTION_2       2  '2 positional arguments'
               24  POP_TOP          

 L. 519        26  LOAD_GLOBAL              check_elecid
               28  LOAD_FAST                'elec_ids'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  STORE_FAST               'elec_ids'

 L. 522        34  SETUP_LOOP         2622  'to 2622'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                datafile
               42  LOAD_ATTR                tell
               44  CALL_FUNCTION_0       0  '0 positional arguments'
               46  LOAD_GLOBAL              ospath
               48  LOAD_ATTR                getsize
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                datafile
               54  LOAD_ATTR                name
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 524        64  LOAD_GLOBAL              unpack
               66  LOAD_STR                 '<I'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                datafile
               72  LOAD_ATTR                read
               74  LOAD_CONST               4
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  CALL_FUNCTION_2       2  '2 positional arguments'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  STORE_FAST               'time_stamp'

 L. 525        86  LOAD_GLOBAL              unpack
               88  LOAD_STR                 '<H'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                datafile
               94  LOAD_ATTR                read
               96  LOAD_CONST               2
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  STORE_DEREF              'packet_id'

 L. 528       108  LOAD_FAST                'elec_ids'
              110  LOAD_STR                 'all'
              112  COMPARE_OP               ==
              114  JUMP_IF_TRUE_OR_POP   146  'to 146'
              116  LOAD_DEREF               'packet_id'
              118  LOAD_FAST                'elec_ids'
              120  COMPARE_OP               in
              122  JUMP_IF_FALSE_OR_POP   146  'to 146'

 L. 529       124  LOAD_GLOBAL              NEURAL_PACKET_ID_MIN
              126  LOAD_DEREF               'packet_id'
              128  DUP_TOP          
              130  ROT_THREE        
              132  COMPARE_OP               <=
              134  JUMP_IF_FALSE_OR_POP   142  'to 142'
              136  LOAD_GLOBAL              NEURAL_PACKET_ID_MAX
              138  COMPARE_OP               <=
            140_0  COME_FROM           122  '122'
            140_1  COME_FROM           114  '114'
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM           134  '134'
              142  ROT_TWO          
              144  POP_TOP          
            146_0  COME_FROM           140  '140'
              146  POP_JUMP_IF_TRUE    174  'to 174'

 L. 530       148  LOAD_FAST                'self'
              150  LOAD_ATTR                datafile
              152  LOAD_ATTR                seek
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                basic_header
              158  LOAD_STR                 'BytesInDataPackets'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               6
              164  BINARY_SUBTRACT  
              166  LOAD_CONST               1
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  POP_TOP          

 L. 531       172  CONTINUE             38  'to 38'

 L. 535       174  LOAD_DEREF               'packet_id'
              176  LOAD_GLOBAL              DIGITAL_PACKET_ID
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   642  'to 642'

 L. 538       184  LOAD_STR                 'dig_events'
              186  LOAD_FAST                'output'
              188  COMPARE_OP               not-in
              190  POP_JUMP_IF_FALSE   208  'to 208'

 L. 539       192  BUILD_LIST_0          0 
              194  BUILD_LIST_0          0 
              196  BUILD_LIST_0          0 
              198  LOAD_CONST               ('Reason', 'TimeStamps', 'Data')
              200  BUILD_CONST_KEY_MAP_3     3 
              202  LOAD_FAST                'output'
              204  LOAD_STR                 'dig_events'
              206  STORE_SUBSCR     
            208_0  COME_FROM           190  '190'

 L. 541       208  LOAD_GLOBAL              unpack
              210  LOAD_STR                 'B'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                datafile
              216  LOAD_ATTR                read
              218  LOAD_CONST               1
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  CALL_FUNCTION_2       2  '2 positional arguments'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  STORE_FAST               'reason'

 L. 542       230  LOAD_FAST                'reason'
              232  LOAD_GLOBAL              PARALLEL_REASON
              234  COMPARE_OP               ==
              236  POP_JUMP_IF_FALSE   244  'to 244'

 L. 542       238  LOAD_STR                 'parallel'
              240  STORE_FAST               'reason'
              242  JUMP_FORWARD        280  'to 280'
              244  ELSE                     '280'

 L. 543       244  LOAD_FAST                'reason'
              246  LOAD_GLOBAL              PERIODIC_REASON
              248  COMPARE_OP               ==
              250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 543       254  LOAD_STR                 'periodic'
              256  STORE_FAST               'reason'
              258  JUMP_FORWARD        280  'to 280'
              260  ELSE                     '280'

 L. 544       260  LOAD_FAST                'reason'
              262  LOAD_GLOBAL              SERIAL_REASON
              264  COMPARE_OP               ==
              266  POP_JUMP_IF_FALSE   276  'to 276'

 L. 544       270  LOAD_STR                 'serial'
              272  STORE_FAST               'reason'
              274  JUMP_FORWARD        280  'to 280'
              276  ELSE                     '280'

 L. 545       276  LOAD_STR                 'unknown'
              278  STORE_FAST               'reason'
            280_0  COME_FROM           274  '274'
            280_1  COME_FROM           258  '258'
            280_2  COME_FROM           242  '242'

 L. 546       280  LOAD_FAST                'self'
              282  LOAD_ATTR                datafile
              284  LOAD_ATTR                seek
              286  LOAD_CONST               1
              288  LOAD_CONST               1
              290  CALL_FUNCTION_2       2  '2 positional arguments'
              292  POP_TOP          

 L. 549       294  LOAD_FAST                'reason'
              296  LOAD_FAST                'output'
              298  LOAD_STR                 'dig_events'
              300  BINARY_SUBSCR    
              302  LOAD_STR                 'Reason'
              304  BINARY_SUBSCR    
              306  COMPARE_OP               in
              308  POP_JUMP_IF_FALSE   332  'to 332'

 L. 550       312  LOAD_FAST                'output'
              314  LOAD_STR                 'dig_events'
              316  BINARY_SUBSCR    
              318  LOAD_STR                 'Reason'
              320  BINARY_SUBSCR    
              322  LOAD_ATTR                index
              324  LOAD_FAST                'reason'
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  STORE_FAST               'idx'
              330  JUMP_FORWARD        390  'to 390'
              332  ELSE                     '390'

 L. 552       332  LOAD_CONST               -1
              334  STORE_FAST               'idx'

 L. 553       336  LOAD_FAST                'output'
              338  LOAD_STR                 'dig_events'
              340  BINARY_SUBSCR    
              342  LOAD_STR                 'Reason'
              344  BINARY_SUBSCR    
              346  LOAD_ATTR                append
              348  LOAD_FAST                'reason'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  POP_TOP          

 L. 554       354  LOAD_FAST                'output'
              356  LOAD_STR                 'dig_events'
              358  BINARY_SUBSCR    
              360  LOAD_STR                 'TimeStamps'
              362  BINARY_SUBSCR    
              364  LOAD_ATTR                append
              366  BUILD_LIST_0          0 
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  POP_TOP          

 L. 555       372  LOAD_FAST                'output'
              374  LOAD_STR                 'dig_events'
              376  BINARY_SUBSCR    
              378  LOAD_STR                 'Data'
              380  BINARY_SUBSCR    
              382  LOAD_ATTR                append
              384  BUILD_LIST_0          0 
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  POP_TOP          
            390_0  COME_FROM           330  '330'

 L. 557       390  LOAD_FAST                'output'
              392  LOAD_STR                 'dig_events'
              394  BINARY_SUBSCR    
              396  LOAD_STR                 'TimeStamps'
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'idx'
              402  BINARY_SUBSCR    
              404  LOAD_ATTR                append
              406  LOAD_FAST                'time_stamp'
              408  CALL_FUNCTION_1       1  '1 positional argument'
              410  POP_TOP          

 L. 558       412  LOAD_FAST                'output'
              414  LOAD_STR                 'dig_events'
              416  BINARY_SUBSCR    
              418  LOAD_STR                 'Data'
              420  BINARY_SUBSCR    
              422  LOAD_FAST                'idx'
              424  BINARY_SUBSCR    
              426  LOAD_ATTR                append
              428  LOAD_GLOBAL              unpack
              430  LOAD_STR                 '<H'
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                datafile
              436  LOAD_ATTR                read
              438  LOAD_CONST               2
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  CALL_FUNCTION_2       2  '2 positional arguments'
              444  LOAD_CONST               0
              446  BINARY_SUBSCR    
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  POP_TOP          

 L. 561       452  LOAD_FAST                'reason'
              454  LOAD_STR                 'serial'
              456  COMPARE_OP               ==
              458  POP_JUMP_IF_FALSE   490  'to 490'

 L. 562       462  LOAD_FAST                'output'
              464  LOAD_STR                 'dig_events'
              466  BINARY_SUBSCR    
              468  LOAD_STR                 'Data'
              470  BINARY_SUBSCR    
              472  LOAD_FAST                'idx'
              474  BINARY_SUBSCR    
              476  LOAD_CONST               -1
              478  DUP_TOP_TWO      
              480  BINARY_SUBSCR    
              482  LOAD_GLOBAL              LOWER_BYTE_MASK
              484  INPLACE_AND      
              486  ROT_THREE        
              488  STORE_SUBSCR     
            490_0  COME_FROM           458  '458'

 L. 565       490  LOAD_GLOBAL              float
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                basic_header
              496  LOAD_STR                 'FileSpec'
              498  BINARY_SUBSCR    
              500  CALL_FUNCTION_1       1  '1 positional argument'
              502  LOAD_CONST               2.3
              504  COMPARE_OP               <
              506  POP_JUMP_IF_FALSE   616  'to 616'

 L. 566       510  LOAD_STR                 'AnalogDataUnits'
              512  LOAD_FAST                'output'
              514  LOAD_STR                 'dig_events'
              516  BINARY_SUBSCR    
              518  COMPARE_OP               not-in
              520  POP_JUMP_IF_FALSE   536  'to 536'

 L. 567       524  LOAD_STR                 'mv'
              526  LOAD_FAST                'output'
              528  LOAD_STR                 'dig_events'
              530  BINARY_SUBSCR    
              532  LOAD_STR                 'AnalogDataUnits'
              534  STORE_SUBSCR     
            536_0  COME_FROM           520  '520'

 L. 569       536  LOAD_FAST                'output'
              538  LOAD_STR                 'dig_events'
              540  BINARY_SUBSCR    
              542  LOAD_STR                 'AnalogData'
              544  BINARY_SUBSCR    
              546  LOAD_ATTR                append
              548  BUILD_LIST_0          0 
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  POP_TOP          

 L. 570       554  SETUP_LOOP          640  'to 640'
              556  LOAD_GLOBAL              range
              558  LOAD_CONST               5
              560  CALL_FUNCTION_1       1  '1 positional argument'
              562  GET_ITER         
              564  FOR_ITER            612  'to 612'
              566  STORE_FAST               'j'

 L. 571       568  LOAD_FAST                'output'
              570  LOAD_STR                 'dig_events'
              572  BINARY_SUBSCR    
              574  LOAD_STR                 'AnalogData'
              576  BINARY_SUBSCR    
              578  LOAD_CONST               -1
              580  BINARY_SUBSCR    
              582  LOAD_ATTR                append
              584  LOAD_GLOBAL              unpack
              586  LOAD_STR                 '<h'
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                datafile
              592  LOAD_ATTR                read
              594  LOAD_CONST               2
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  CALL_FUNCTION_2       2  '2 positional arguments'
              600  LOAD_CONST               0
              602  BINARY_SUBSCR    
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  POP_TOP          
              608  JUMP_BACK           564  'to 564'
              612  POP_BLOCK        
            614_0  COME_FROM_LOOP      554  '554'
              614  JUMP_FORWARD        640  'to 640'
              616  ELSE                     '640'

 L. 573       616  LOAD_FAST                'self'
              618  LOAD_ATTR                datafile
              620  LOAD_ATTR                seek
              622  LOAD_FAST                'self'
              624  LOAD_ATTR                basic_header
              626  LOAD_STR                 'BytesInDataPackets'
              628  BINARY_SUBSCR    
              630  LOAD_CONST               10
              632  BINARY_SUBTRACT  
              634  LOAD_CONST               1
              636  CALL_FUNCTION_2       2  '2 positional arguments'
              638  POP_TOP          
            640_0  COME_FROM           614  '614'
              640  JUMP_BACK            38  'to 38'
              642  ELSE                     '2618'

 L. 576       642  LOAD_GLOBAL              NEURAL_PACKET_ID_MIN
              644  LOAD_DEREF               'packet_id'
              646  DUP_TOP          
              648  ROT_THREE        
              650  COMPARE_OP               <=
              652  JUMP_IF_FALSE_OR_POP   662  'to 662'
              656  LOAD_GLOBAL              NEURAL_PACKET_ID_MAX
              658  COMPARE_OP               <=
              660  JUMP_FORWARD        666  'to 666'
            662_0  COME_FROM           652  '652'
              662  ROT_TWO          
              664  POP_TOP          
            666_0  COME_FROM           660  '660'
              666  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 579       670  LOAD_STR                 'spike_events'
              672  LOAD_FAST                'output'
              674  COMPARE_OP               not-in
              676  POP_JUMP_IF_FALSE   702  'to 702'

 L. 580       680  LOAD_STR                 'nV'
              682  BUILD_LIST_0          0 
              684  BUILD_LIST_0          0 

 L. 581       686  BUILD_LIST_0          0 
              688  BUILD_LIST_0          0 
              690  BUILD_LIST_0          0 
              692  LOAD_CONST               ('Units', 'ChannelID', 'TimeStamps', 'NEUEVWAV_HeaderIndices', 'Classification', 'Waveforms')
              694  BUILD_CONST_KEY_MAP_6     6 
              696  LOAD_FAST                'output'
              698  LOAD_STR                 'spike_events'
              700  STORE_SUBSCR     
            702_0  COME_FROM           676  '676'

 L. 583       702  LOAD_GLOBAL              unpack
              704  LOAD_STR                 'B'
              706  LOAD_FAST                'self'
              708  LOAD_ATTR                datafile
              710  LOAD_ATTR                read
              712  LOAD_CONST               1
              714  CALL_FUNCTION_1       1  '1 positional argument'
              716  CALL_FUNCTION_2       2  '2 positional arguments'
              718  LOAD_CONST               0
              720  BINARY_SUBSCR    
              722  STORE_FAST               'classifier'

 L. 584       724  LOAD_FAST                'classifier'
              726  LOAD_GLOBAL              UNDEFINED
              728  COMPARE_OP               ==
              730  POP_JUMP_IF_FALSE   740  'to 740'

 L. 584       734  LOAD_STR                 'none'
              736  STORE_FAST               'classifier'
              738  JUMP_FORWARD        794  'to 794'
              740  ELSE                     '794'

 L. 585       740  LOAD_GLOBAL              CLASSIFIER_MIN
              742  LOAD_FAST                'classifier'
              744  DUP_TOP          
              746  ROT_THREE        
              748  COMPARE_OP               <=
              750  JUMP_IF_FALSE_OR_POP   760  'to 760'
              754  LOAD_GLOBAL              CLASSIFIER_MAX
              756  COMPARE_OP               <=
              758  JUMP_FORWARD        764  'to 764'
            760_0  COME_FROM           750  '750'
              760  ROT_TWO          
              762  POP_TOP          
            764_0  COME_FROM           758  '758'
              764  POP_JUMP_IF_FALSE   774  'to 774'

 L. 585       768  LOAD_FAST                'classifier'
              770  STORE_FAST               'classifier'
              772  JUMP_FORWARD        794  'to 794'
              774  ELSE                     '794'

 L. 586       774  LOAD_FAST                'classifier'
              776  LOAD_GLOBAL              CLASSIFIER_NOISE
              778  COMPARE_OP               ==
              780  POP_JUMP_IF_FALSE   790  'to 790'

 L. 586       784  LOAD_STR                 'noise'
              786  STORE_FAST               'classifier'
              788  JUMP_FORWARD        794  'to 794'
              790  ELSE                     '794'

 L. 587       790  LOAD_STR                 'error'
              792  STORE_FAST               'classifier'
            794_0  COME_FROM           788  '788'
            794_1  COME_FROM           772  '772'
            794_2  COME_FROM           738  '738'

 L. 588       794  LOAD_FAST                'self'
              796  LOAD_ATTR                datafile
              798  LOAD_ATTR                seek
              800  LOAD_CONST               1
              802  LOAD_CONST               1
              804  CALL_FUNCTION_2       2  '2 positional arguments'
              806  POP_TOP          

 L. 591       808  LOAD_DEREF               'packet_id'
              810  LOAD_FAST                'output'
              812  LOAD_STR                 'spike_events'
              814  BINARY_SUBSCR    
              816  LOAD_STR                 'ChannelID'
              818  BINARY_SUBSCR    
              820  COMPARE_OP               in
              822  POP_JUMP_IF_FALSE   846  'to 846'

 L. 592       826  LOAD_FAST                'output'
              828  LOAD_STR                 'spike_events'
              830  BINARY_SUBSCR    
              832  LOAD_STR                 'ChannelID'
              834  BINARY_SUBSCR    
              836  LOAD_ATTR                index
              838  LOAD_DEREF               'packet_id'
              840  CALL_FUNCTION_1       1  '1 positional argument'
              842  STORE_FAST               'idx'
              844  JUMP_FORWARD        946  'to 946'
              846  ELSE                     '946'

 L. 594       846  LOAD_CONST               -1
              848  STORE_FAST               'idx'

 L. 595       850  LOAD_FAST                'output'
              852  LOAD_STR                 'spike_events'
              854  BINARY_SUBSCR    
              856  LOAD_STR                 'ChannelID'
              858  BINARY_SUBSCR    
              860  LOAD_ATTR                append
              862  LOAD_DEREF               'packet_id'
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  POP_TOP          

 L. 596       868  LOAD_FAST                'output'
              870  LOAD_STR                 'spike_events'
              872  BINARY_SUBSCR    
              874  LOAD_STR                 'TimeStamps'
              876  BINARY_SUBSCR    
              878  LOAD_ATTR                append
              880  BUILD_LIST_0          0 
              882  CALL_FUNCTION_1       1  '1 positional argument'
              884  POP_TOP          

 L. 597       886  LOAD_FAST                'output'
              888  LOAD_STR                 'spike_events'
              890  BINARY_SUBSCR    
              892  LOAD_STR                 'Classification'
              894  BINARY_SUBSCR    
              896  LOAD_ATTR                append
              898  BUILD_LIST_0          0 
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  POP_TOP          

 L. 600       904  LOAD_FAST                'output'
              906  LOAD_STR                 'spike_events'
              908  BINARY_SUBSCR    
              910  LOAD_STR                 'NEUEVWAV_HeaderIndices'
              912  BINARY_SUBSCR    
              914  LOAD_ATTR                append

 L. 601       916  LOAD_GLOBAL              next
              918  LOAD_CLOSURE             'packet_id'
              920  BUILD_TUPLE_1         1 
              922  LOAD_GENEXPR             '<code_object <genexpr>>'
              924  LOAD_STR                 'NevFile.getdata.<locals>.<genexpr>'
              926  MAKE_FUNCTION_8          'closure'
              928  LOAD_GLOBAL              enumerate
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                extended_headers
              934  CALL_FUNCTION_1       1  '1 positional argument'
              936  GET_ITER         
              938  CALL_FUNCTION_1       1  '1 positional argument'
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  POP_TOP          
            946_0  COME_FROM           844  '844'

 L. 604       946  LOAD_FAST                'output'
              948  LOAD_STR                 'spike_events'
              950  BINARY_SUBSCR    
              952  LOAD_STR                 'TimeStamps'
              954  BINARY_SUBSCR    
              956  LOAD_FAST                'idx'
              958  BINARY_SUBSCR    
              960  LOAD_ATTR                append
              962  LOAD_FAST                'time_stamp'
              964  CALL_FUNCTION_1       1  '1 positional argument'
              966  POP_TOP          

 L. 605       968  LOAD_FAST                'output'
              970  LOAD_STR                 'spike_events'
              972  BINARY_SUBSCR    
              974  LOAD_STR                 'Classification'
              976  BINARY_SUBSCR    
              978  LOAD_FAST                'idx'
              980  BINARY_SUBSCR    
              982  LOAD_ATTR                append
              984  LOAD_FAST                'classifier'
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  POP_TOP          

 L. 608       990  LOAD_FAST                'output'
              992  LOAD_STR                 'spike_events'
              994  BINARY_SUBSCR    
              996  LOAD_STR                 'NEUEVWAV_HeaderIndices'
              998  BINARY_SUBSCR    
             1000  LOAD_FAST                'idx'
             1002  BINARY_SUBSCR    
             1004  STORE_FAST               'ext_header_idx'

 L. 609      1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                extended_headers
             1010  LOAD_FAST                'ext_header_idx'
             1012  BINARY_SUBSCR    
             1014  LOAD_STR                 'SpikeWidthSamples'
             1016  BINARY_SUBSCR    
             1018  STORE_FAST               'samples'

 L. 610      1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                extended_headers
             1024  LOAD_FAST                'ext_header_idx'
             1026  BINARY_SUBSCR    
             1028  LOAD_STR                 'DigitizationFactor'
             1030  BINARY_SUBSCR    
             1032  STORE_FAST               'dig_factor'

 L. 611      1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                extended_headers
             1038  LOAD_FAST                'ext_header_idx'
             1040  BINARY_SUBSCR    
             1042  LOAD_STR                 'BytesPerWaveform'
             1044  BINARY_SUBSCR    
             1046  STORE_FAST               'num_bytes'

 L. 612      1048  LOAD_FAST                'num_bytes'
             1050  LOAD_CONST               1
             1052  COMPARE_OP               <=
             1054  POP_JUMP_IF_FALSE  1066  'to 1066'

 L. 612      1058  LOAD_GLOBAL              np
             1060  LOAD_ATTR                int8
             1062  STORE_FAST               'data_type'
             1064  JUMP_FORWARD       1082  'to 1082'
             1066  ELSE                     '1082'

 L. 613      1066  LOAD_FAST                'num_bytes'
             1068  LOAD_CONST               2
             1070  COMPARE_OP               ==
             1072  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 613      1076  LOAD_GLOBAL              np
             1078  LOAD_ATTR                int16
             1080  STORE_FAST               'data_type'
           1082_0  COME_FROM          1072  '1072'
           1082_1  COME_FROM          1064  '1064'

 L. 616      1082  LOAD_FAST                'wave_read'
             1084  LOAD_STR                 'read'
             1086  COMPARE_OP               ==
             1088  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 617      1092  LOAD_FAST                'idx'
             1094  LOAD_CONST               -1
             1096  COMPARE_OP               ==
             1098  POP_JUMP_IF_FALSE  1150  'to 1150'

 L. 618      1102  LOAD_FAST                'output'
             1104  LOAD_STR                 'spike_events'
             1106  BINARY_SUBSCR    
             1108  LOAD_STR                 'Waveforms'
             1110  BINARY_SUBSCR    
             1112  LOAD_ATTR                append

 L. 619      1114  LOAD_GLOBAL              np
             1116  LOAD_ATTR                fromfile
             1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                datafile
             1122  LOAD_FAST                'data_type'
             1124  LOAD_FAST                'samples'
             1126  LOAD_CONST               ('file', 'dtype', 'count')
             1128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1130  LOAD_ATTR                astype
             1132  LOAD_GLOBAL              np
             1134  LOAD_ATTR                int32
             1136  CALL_FUNCTION_1       1  '1 positional argument'
             1138  LOAD_FAST                'dig_factor'
             1140  BINARY_MULTIPLY  
             1142  BUILD_LIST_1          1 
             1144  CALL_FUNCTION_1       1  '1 positional argument'
             1146  POP_TOP          
             1148  JUMP_FORWARD       1218  'to 1218'
             1150  ELSE                     '1218'

 L. 622      1150  LOAD_GLOBAL              np
             1152  LOAD_ATTR                append
             1154  LOAD_FAST                'output'
             1156  LOAD_STR                 'spike_events'
             1158  BINARY_SUBSCR    
             1160  LOAD_STR                 'Waveforms'
             1162  BINARY_SUBSCR    
             1164  LOAD_FAST                'idx'
             1166  BINARY_SUBSCR    

 L. 623      1168  LOAD_GLOBAL              np
             1170  LOAD_ATTR                fromfile
             1172  LOAD_FAST                'self'
             1174  LOAD_ATTR                datafile
             1176  LOAD_FAST                'data_type'
             1178  LOAD_FAST                'samples'
             1180  LOAD_CONST               ('file', 'dtype', 'count')
             1182  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1184  LOAD_ATTR                astype
             1186  LOAD_GLOBAL              np
             1188  LOAD_ATTR                int32
             1190  CALL_FUNCTION_1       1  '1 positional argument'

 L. 624      1192  LOAD_FAST                'dig_factor'
             1194  BINARY_MULTIPLY  
             1196  BUILD_LIST_1          1 
             1198  LOAD_CONST               0
             1200  LOAD_CONST               ('axis',)
             1202  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1204  LOAD_FAST                'output'
             1206  LOAD_STR                 'spike_events'
             1208  BINARY_SUBSCR    
             1210  LOAD_STR                 'Waveforms'
             1212  BINARY_SUBSCR    
             1214  LOAD_FAST                'idx'
             1216  STORE_SUBSCR     
           1218_0  COME_FROM          1148  '1148'
             1218  JUMP_FORWARD       1290  'to 1290'
             1220  ELSE                     '1290'

 L. 626      1220  LOAD_FAST                'wave_read'
             1222  LOAD_STR                 'noread'
             1224  COMPARE_OP               ==
             1226  POP_JUMP_IF_FALSE  2618  'to 2618'

 L. 627      1230  LOAD_FAST                'idx'
             1232  LOAD_CONST               -1
             1234  COMPARE_OP               ==
             1236  POP_JUMP_IF_FALSE  1266  'to 1266'

 L. 628      1240  LOAD_FAST                'self'
             1242  LOAD_ATTR                datafile
             1244  LOAD_ATTR                seek
             1246  LOAD_FAST                'self'
             1248  LOAD_ATTR                basic_header
             1250  LOAD_STR                 'BytesInDataPackets'
             1252  BINARY_SUBSCR    
             1254  LOAD_CONST               8
             1256  BINARY_SUBTRACT  
             1258  LOAD_CONST               1
             1260  CALL_FUNCTION_2       2  '2 positional arguments'
             1262  POP_TOP          
             1264  JUMP_FORWARD       1290  'to 1290'
             1266  ELSE                     '1290'

 L. 630      1266  LOAD_FAST                'self'
             1268  LOAD_ATTR                datafile
             1270  LOAD_ATTR                seek
             1272  LOAD_FAST                'self'
             1274  LOAD_ATTR                basic_header
             1276  LOAD_STR                 'BytesInDataPackets'
             1278  BINARY_SUBSCR    
             1280  LOAD_CONST               8
             1282  BINARY_SUBTRACT  
             1284  LOAD_CONST               1
             1286  CALL_FUNCTION_2       2  '2 positional arguments'
             1288  POP_TOP          
           1290_0  COME_FROM          1264  '1264'
           1290_1  COME_FROM          1218  '1218'
             1290  JUMP_BACK            38  'to 38'
             1292  ELSE                     '2618'

 L. 633      1292  LOAD_DEREF               'packet_id'
             1294  LOAD_GLOBAL              COMMENT_PACKET_ID
             1296  COMPARE_OP               ==
             1298  POP_JUMP_IF_FALSE  1682  'to 1682'

 L. 636      1302  LOAD_STR                 'comments'
             1304  LOAD_FAST                'output'
             1306  COMPARE_OP               not-in
             1308  POP_JUMP_IF_FALSE  1332  'to 1332'

 L. 637      1312  BUILD_LIST_0          0 
             1314  BUILD_LIST_0          0 
             1316  BUILD_LIST_0          0 
             1318  BUILD_LIST_0          0 
             1320  BUILD_LIST_0          0 
             1322  LOAD_CONST               ('TimeStamps', 'CharSet', 'Flag', 'Data', 'Comment')
             1324  BUILD_CONST_KEY_MAP_5     5 
             1326  LOAD_FAST                'output'
             1328  LOAD_STR                 'comments'
             1330  STORE_SUBSCR     
           1332_0  COME_FROM          1308  '1308'

 L. 639      1332  LOAD_FAST                'output'
             1334  LOAD_STR                 'comments'
             1336  BINARY_SUBSCR    
             1338  LOAD_STR                 'TimeStamps'
             1340  BINARY_SUBSCR    
             1342  LOAD_ATTR                append
             1344  LOAD_FAST                'time_stamp'
             1346  CALL_FUNCTION_1       1  '1 positional argument'
             1348  POP_TOP          

 L. 641      1350  LOAD_GLOBAL              unpack
             1352  LOAD_STR                 'B'
             1354  LOAD_FAST                'self'
             1356  LOAD_ATTR                datafile
             1358  LOAD_ATTR                read
             1360  LOAD_CONST               1
             1362  CALL_FUNCTION_1       1  '1 positional argument'
             1364  CALL_FUNCTION_2       2  '2 positional arguments'
             1366  LOAD_CONST               0
             1368  BINARY_SUBSCR    
             1370  STORE_FAST               'char_set'

 L. 642      1372  LOAD_FAST                'char_set'
             1374  LOAD_GLOBAL              CHARSET_ANSI
             1376  COMPARE_OP               ==
             1378  POP_JUMP_IF_FALSE  1402  'to 1402'

 L. 642      1382  LOAD_FAST                'output'
             1384  LOAD_STR                 'comments'
             1386  BINARY_SUBSCR    
             1388  LOAD_STR                 'CharSet'
             1390  BINARY_SUBSCR    
             1392  LOAD_ATTR                append
             1394  LOAD_STR                 'ANSI'
             1396  CALL_FUNCTION_1       1  '1 positional argument'
             1398  POP_TOP          
             1400  JUMP_FORWARD       1480  'to 1480'
             1402  ELSE                     '1480'

 L. 643      1402  LOAD_FAST                'char_set'
             1404  LOAD_GLOBAL              CHARSET_UTF
             1406  COMPARE_OP               ==
             1408  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 643      1412  LOAD_FAST                'output'
             1414  LOAD_STR                 'comments'
             1416  BINARY_SUBSCR    
             1418  LOAD_STR                 'CharSet'
             1420  BINARY_SUBSCR    
             1422  LOAD_ATTR                append
             1424  LOAD_STR                 'UTF-16'
             1426  CALL_FUNCTION_1       1  '1 positional argument'
             1428  POP_TOP          
             1430  JUMP_FORWARD       1480  'to 1480'
             1432  ELSE                     '1480'

 L. 644      1432  LOAD_FAST                'char_set'
             1434  LOAD_GLOBAL              CHARSET_ROI
             1436  COMPARE_OP               ==
             1438  POP_JUMP_IF_FALSE  1462  'to 1462'

 L. 644      1442  LOAD_FAST                'output'
             1444  LOAD_STR                 'comments'
             1446  BINARY_SUBSCR    
             1448  LOAD_STR                 'CharSet'
             1450  BINARY_SUBSCR    
             1452  LOAD_ATTR                append
             1454  LOAD_STR                 'NeuroMotive ROI'
             1456  CALL_FUNCTION_1       1  '1 positional argument'
             1458  POP_TOP          
             1460  JUMP_FORWARD       1480  'to 1480'
             1462  ELSE                     '1480'

 L. 645      1462  LOAD_FAST                'output'
             1464  LOAD_STR                 'comments'
             1466  BINARY_SUBSCR    
             1468  LOAD_STR                 'CharSet'
             1470  BINARY_SUBSCR    
             1472  LOAD_ATTR                append
             1474  LOAD_STR                 'error'
             1476  CALL_FUNCTION_1       1  '1 positional argument'
             1478  POP_TOP          
           1480_0  COME_FROM          1460  '1460'
           1480_1  COME_FROM          1430  '1430'
           1480_2  COME_FROM          1400  '1400'

 L. 647      1480  LOAD_GLOBAL              unpack
             1482  LOAD_STR                 'B'
             1484  LOAD_FAST                'self'
             1486  LOAD_ATTR                datafile
             1488  LOAD_ATTR                read
             1490  LOAD_CONST               1
             1492  CALL_FUNCTION_1       1  '1 positional argument'
             1494  CALL_FUNCTION_2       2  '2 positional arguments'
             1496  LOAD_CONST               0
             1498  BINARY_SUBSCR    
             1500  STORE_FAST               'comm_flag'

 L. 648      1502  LOAD_FAST                'comm_flag'
             1504  LOAD_GLOBAL              COMM_RGBA
             1506  COMPARE_OP               ==
             1508  POP_JUMP_IF_FALSE  1532  'to 1532'

 L. 648      1512  LOAD_FAST                'output'
             1514  LOAD_STR                 'comments'
             1516  BINARY_SUBSCR    
             1518  LOAD_STR                 'Flag'
             1520  BINARY_SUBSCR    
             1522  LOAD_ATTR                append
             1524  LOAD_STR                 'RGBA color code'
             1526  CALL_FUNCTION_1       1  '1 positional argument'
             1528  POP_TOP          
             1530  JUMP_FORWARD       1580  'to 1580'
             1532  ELSE                     '1580'

 L. 649      1532  LOAD_FAST                'comm_flag'
             1534  LOAD_GLOBAL              COMM_TIME
             1536  COMPARE_OP               ==
             1538  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 649      1542  LOAD_FAST                'output'
             1544  LOAD_STR                 'comments'
             1546  BINARY_SUBSCR    
             1548  LOAD_STR                 'Flag'
             1550  BINARY_SUBSCR    
             1552  LOAD_ATTR                append
             1554  LOAD_STR                 'timestamp'
             1556  CALL_FUNCTION_1       1  '1 positional argument'
             1558  POP_TOP          
             1560  JUMP_FORWARD       1580  'to 1580'
             1562  ELSE                     '1580'

 L. 650      1562  LOAD_FAST                'output'
             1564  LOAD_STR                 'comments'
             1566  BINARY_SUBSCR    
             1568  LOAD_STR                 'Flag'
             1570  BINARY_SUBSCR    
             1572  LOAD_ATTR                append
             1574  LOAD_STR                 'error'
             1576  CALL_FUNCTION_1       1  '1 positional argument'
             1578  POP_TOP          
           1580_0  COME_FROM          1560  '1560'
           1580_1  COME_FROM          1530  '1530'

 L. 652      1580  LOAD_FAST                'output'
             1582  LOAD_STR                 'comments'
             1584  BINARY_SUBSCR    
             1586  LOAD_STR                 'Data'
             1588  BINARY_SUBSCR    
             1590  LOAD_ATTR                append
             1592  LOAD_GLOBAL              unpack
             1594  LOAD_STR                 '<I'
             1596  LOAD_FAST                'self'
             1598  LOAD_ATTR                datafile
             1600  LOAD_ATTR                read
             1602  LOAD_CONST               4
             1604  CALL_FUNCTION_1       1  '1 positional argument'
             1606  CALL_FUNCTION_2       2  '2 positional arguments'
             1608  LOAD_CONST               0
             1610  BINARY_SUBSCR    
             1612  CALL_FUNCTION_1       1  '1 positional argument'
             1614  POP_TOP          

 L. 654      1616  LOAD_FAST                'self'
             1618  LOAD_ATTR                basic_header
             1620  LOAD_STR                 'BytesInDataPackets'
             1622  BINARY_SUBSCR    
             1624  LOAD_CONST               12
             1626  BINARY_SUBTRACT  
             1628  STORE_FAST               'samples'

 L. 655      1630  LOAD_GLOBAL              bytes
             1632  LOAD_ATTR                decode
             1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                datafile
             1638  LOAD_ATTR                read
             1640  LOAD_FAST                'samples'
             1642  CALL_FUNCTION_1       1  '1 positional argument'
             1644  LOAD_STR                 'latin-1'
             1646  CALL_FUNCTION_2       2  '2 positional arguments'
             1648  STORE_FAST               'comm_string'

 L. 656      1650  LOAD_FAST                'output'
             1652  LOAD_STR                 'comments'
             1654  BINARY_SUBSCR    
             1656  LOAD_STR                 'Comment'
             1658  BINARY_SUBSCR    
             1660  LOAD_ATTR                append
             1662  LOAD_FAST                'comm_string'
             1664  LOAD_ATTR                split
             1666  LOAD_GLOBAL              STRING_TERMINUS
             1668  LOAD_CONST               1
             1670  CALL_FUNCTION_2       2  '2 positional arguments'
             1672  LOAD_CONST               0
             1674  BINARY_SUBSCR    
             1676  CALL_FUNCTION_1       1  '1 positional argument'
             1678  POP_TOP          
             1680  JUMP_BACK            38  'to 38'
             1682  ELSE                     '2618'

 L. 659      1682  LOAD_DEREF               'packet_id'
             1684  LOAD_GLOBAL              VIDEO_SYNC_PACKET_ID
             1686  COMPARE_OP               ==
             1688  POP_JUMP_IF_FALSE  1910  'to 1910'

 L. 662      1692  LOAD_STR                 'video_sync_events'
             1694  LOAD_FAST                'output'
             1696  COMPARE_OP               not-in
             1698  POP_JUMP_IF_FALSE  1722  'to 1722'

 L. 663      1702  BUILD_LIST_0          0 
             1704  BUILD_LIST_0          0 
             1706  BUILD_LIST_0          0 

 L. 664      1708  BUILD_LIST_0          0 
             1710  BUILD_LIST_0          0 
             1712  LOAD_CONST               ('TimeStamps', 'VideoFileNum', 'VideoFrameNum', 'VideoElapsedTime_ms', 'VideoSourceID')
             1714  BUILD_CONST_KEY_MAP_5     5 
             1716  LOAD_FAST                'output'
             1718  LOAD_STR                 'video_sync_events'
             1720  STORE_SUBSCR     
           1722_0  COME_FROM          1698  '1698'

 L. 666      1722  LOAD_FAST                'output'
             1724  LOAD_STR                 'video_sync_events'
             1726  BINARY_SUBSCR    
             1728  LOAD_STR                 'TimeStamps'
             1730  BINARY_SUBSCR    
             1732  LOAD_ATTR                append
             1734  LOAD_FAST                'time_stamp'
             1736  CALL_FUNCTION_1       1  '1 positional argument'
             1738  POP_TOP          

 L. 667      1740  LOAD_FAST                'output'
             1742  LOAD_STR                 'video_sync_events'
             1744  BINARY_SUBSCR    
             1746  LOAD_STR                 'VideoFileNum'
             1748  BINARY_SUBSCR    
             1750  LOAD_ATTR                append
             1752  LOAD_GLOBAL              unpack
             1754  LOAD_STR                 '<H'
             1756  LOAD_FAST                'self'
             1758  LOAD_ATTR                datafile
             1760  LOAD_ATTR                read
             1762  LOAD_CONST               2
             1764  CALL_FUNCTION_1       1  '1 positional argument'
             1766  CALL_FUNCTION_2       2  '2 positional arguments'
             1768  LOAD_CONST               0
             1770  BINARY_SUBSCR    
             1772  CALL_FUNCTION_1       1  '1 positional argument'
             1774  POP_TOP          

 L. 668      1776  LOAD_FAST                'output'
             1778  LOAD_STR                 'video_sync_events'
             1780  BINARY_SUBSCR    
             1782  LOAD_STR                 'VideoFrameNum'
             1784  BINARY_SUBSCR    
             1786  LOAD_ATTR                append
             1788  LOAD_GLOBAL              unpack
             1790  LOAD_STR                 '<I'
             1792  LOAD_FAST                'self'
             1794  LOAD_ATTR                datafile
             1796  LOAD_ATTR                read
             1798  LOAD_CONST               4
             1800  CALL_FUNCTION_1       1  '1 positional argument'
             1802  CALL_FUNCTION_2       2  '2 positional arguments'
             1804  LOAD_CONST               0
             1806  BINARY_SUBSCR    
             1808  CALL_FUNCTION_1       1  '1 positional argument'
             1810  POP_TOP          

 L. 669      1812  LOAD_FAST                'output'
             1814  LOAD_STR                 'video_sync_events'
             1816  BINARY_SUBSCR    
             1818  LOAD_STR                 'VideoElapsedTime_ms'
             1820  BINARY_SUBSCR    
             1822  LOAD_ATTR                append
             1824  LOAD_GLOBAL              unpack
             1826  LOAD_STR                 '<I'
             1828  LOAD_FAST                'self'
             1830  LOAD_ATTR                datafile
             1832  LOAD_ATTR                read
             1834  LOAD_CONST               4
             1836  CALL_FUNCTION_1       1  '1 positional argument'
             1838  CALL_FUNCTION_2       2  '2 positional arguments'
             1840  LOAD_CONST               0
             1842  BINARY_SUBSCR    
             1844  CALL_FUNCTION_1       1  '1 positional argument'
             1846  POP_TOP          

 L. 670      1848  LOAD_FAST                'output'
             1850  LOAD_STR                 'video_sync_events'
             1852  BINARY_SUBSCR    
             1854  LOAD_STR                 'VideoSourceID'
             1856  BINARY_SUBSCR    
             1858  LOAD_ATTR                append
             1860  LOAD_GLOBAL              unpack
             1862  LOAD_STR                 '<I'
             1864  LOAD_FAST                'self'
             1866  LOAD_ATTR                datafile
             1868  LOAD_ATTR                read
             1870  LOAD_CONST               4
             1872  CALL_FUNCTION_1       1  '1 positional argument'
             1874  CALL_FUNCTION_2       2  '2 positional arguments'
             1876  LOAD_CONST               0
             1878  BINARY_SUBSCR    
             1880  CALL_FUNCTION_1       1  '1 positional argument'
             1882  POP_TOP          

 L. 671      1884  LOAD_FAST                'self'
             1886  LOAD_ATTR                datafile
             1888  LOAD_ATTR                seek
             1890  LOAD_FAST                'self'
             1892  LOAD_ATTR                basic_header
             1894  LOAD_STR                 'BytesInDataPackets'
             1896  BINARY_SUBSCR    
             1898  LOAD_CONST               20
             1900  BINARY_SUBTRACT  
             1902  LOAD_CONST               1
             1904  CALL_FUNCTION_2       2  '2 positional arguments'
             1906  POP_TOP          
             1908  JUMP_BACK            38  'to 38'
             1910  ELSE                     '2618'

 L. 674      1910  LOAD_DEREF               'packet_id'
             1912  LOAD_GLOBAL              TRACKING_PACKET_ID
             1914  COMPARE_OP               ==
             1916  POP_JUMP_IF_FALSE  2168  'to 2168'

 L. 677      1920  LOAD_STR                 'tracking_events'
             1922  LOAD_FAST                'output'
             1924  COMPARE_OP               not-in
             1926  POP_JUMP_IF_FALSE  1952  'to 1952'

 L. 678      1930  BUILD_LIST_0          0 
             1932  BUILD_LIST_0          0 
             1934  BUILD_LIST_0          0 
             1936  BUILD_LIST_0          0 

 L. 679      1938  BUILD_LIST_0          0 
             1940  BUILD_LIST_0          0 
             1942  LOAD_CONST               ('TimeStamps', 'ParentID', 'NodeID', 'NodeCount', 'PointCount', 'TrackingPoints')
             1944  BUILD_CONST_KEY_MAP_6     6 
             1946  LOAD_FAST                'output'
             1948  LOAD_STR                 'tracking_events'
             1950  STORE_SUBSCR     
           1952_0  COME_FROM          1926  '1926'

 L. 681      1952  LOAD_FAST                'output'
             1954  LOAD_STR                 'tracking_events'
             1956  BINARY_SUBSCR    
             1958  LOAD_STR                 'TimeStamps'
             1960  BINARY_SUBSCR    
             1962  LOAD_ATTR                append
             1964  LOAD_FAST                'time_stamp'
             1966  CALL_FUNCTION_1       1  '1 positional argument'
             1968  POP_TOP          

 L. 682      1970  LOAD_FAST                'output'
             1972  LOAD_STR                 'tracking_events'
             1974  BINARY_SUBSCR    
             1976  LOAD_STR                 'ParentID'
             1978  BINARY_SUBSCR    
             1980  LOAD_ATTR                append
             1982  LOAD_GLOBAL              unpack
             1984  LOAD_STR                 '<H'
             1986  LOAD_FAST                'self'
             1988  LOAD_ATTR                datafile
             1990  LOAD_ATTR                read
             1992  LOAD_CONST               2
             1994  CALL_FUNCTION_1       1  '1 positional argument'
             1996  CALL_FUNCTION_2       2  '2 positional arguments'
             1998  LOAD_CONST               0
             2000  BINARY_SUBSCR    
             2002  CALL_FUNCTION_1       1  '1 positional argument'
             2004  POP_TOP          

 L. 683      2006  LOAD_FAST                'output'
             2008  LOAD_STR                 'tracking_events'
             2010  BINARY_SUBSCR    
             2012  LOAD_STR                 'NodeID'
             2014  BINARY_SUBSCR    
             2016  LOAD_ATTR                append
             2018  LOAD_GLOBAL              unpack
             2020  LOAD_STR                 '<H'
             2022  LOAD_FAST                'self'
             2024  LOAD_ATTR                datafile
             2026  LOAD_ATTR                read
             2028  LOAD_CONST               2
             2030  CALL_FUNCTION_1       1  '1 positional argument'
             2032  CALL_FUNCTION_2       2  '2 positional arguments'
             2034  LOAD_CONST               0
             2036  BINARY_SUBSCR    
             2038  CALL_FUNCTION_1       1  '1 positional argument'
             2040  POP_TOP          

 L. 684      2042  LOAD_FAST                'output'
             2044  LOAD_STR                 'tracking_events'
             2046  BINARY_SUBSCR    
             2048  LOAD_STR                 'NodeCount'
             2050  BINARY_SUBSCR    
             2052  LOAD_ATTR                append
             2054  LOAD_GLOBAL              unpack
             2056  LOAD_STR                 '<H'
             2058  LOAD_FAST                'self'
             2060  LOAD_ATTR                datafile
             2062  LOAD_ATTR                read
             2064  LOAD_CONST               2
             2066  CALL_FUNCTION_1       1  '1 positional argument'
             2068  CALL_FUNCTION_2       2  '2 positional arguments'
             2070  LOAD_CONST               0
             2072  BINARY_SUBSCR    
             2074  CALL_FUNCTION_1       1  '1 positional argument'
             2076  POP_TOP          

 L. 685      2078  LOAD_FAST                'output'
             2080  LOAD_STR                 'tracking_events'
             2082  BINARY_SUBSCR    
             2084  LOAD_STR                 'PointCount'
             2086  BINARY_SUBSCR    
             2088  LOAD_ATTR                append
             2090  LOAD_GLOBAL              unpack
             2092  LOAD_STR                 '<H'
             2094  LOAD_FAST                'self'
             2096  LOAD_ATTR                datafile
             2098  LOAD_ATTR                read
             2100  LOAD_CONST               2
             2102  CALL_FUNCTION_1       1  '1 positional argument'
             2104  CALL_FUNCTION_2       2  '2 positional arguments'
             2106  LOAD_CONST               0
             2108  BINARY_SUBSCR    
             2110  CALL_FUNCTION_1       1  '1 positional argument'
             2112  POP_TOP          

 L. 686      2114  LOAD_FAST                'self'
             2116  LOAD_ATTR                basic_header
             2118  LOAD_STR                 'BytesInDataPackets'
             2120  BINARY_SUBSCR    
             2122  LOAD_CONST               14
             2124  BINARY_SUBTRACT  
             2126  LOAD_CONST               2
             2128  BINARY_FLOOR_DIVIDE
             2130  STORE_FAST               'samples'

 L. 687      2132  LOAD_FAST                'output'
             2134  LOAD_STR                 'tracking_events'
             2136  BINARY_SUBSCR    
             2138  LOAD_STR                 'TrackingPoints'
             2140  BINARY_SUBSCR    
             2142  LOAD_ATTR                append

 L. 688      2144  LOAD_GLOBAL              np
             2146  LOAD_ATTR                fromfile
             2148  LOAD_FAST                'self'
             2150  LOAD_ATTR                datafile
             2152  LOAD_GLOBAL              np
             2154  LOAD_ATTR                uint16
             2156  LOAD_FAST                'samples'
             2158  LOAD_CONST               ('file', 'dtype', 'count')
             2160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2162  CALL_FUNCTION_1       1  '1 positional argument'
             2164  POP_TOP          
             2166  JUMP_BACK            38  'to 38'
             2168  ELSE                     '2618'

 L. 691      2168  LOAD_DEREF               'packet_id'
             2170  LOAD_GLOBAL              BUTTON_PACKET_ID
             2172  COMPARE_OP               ==
             2174  POP_JUMP_IF_FALSE  2376  'to 2376'

 L. 694      2178  LOAD_STR                 'button_trigger_events'
             2180  LOAD_FAST                'output'
             2182  COMPARE_OP               not-in
             2184  POP_JUMP_IF_FALSE  2202  'to 2202'

 L. 695      2188  BUILD_LIST_0          0 
             2190  BUILD_LIST_0          0 
             2192  LOAD_CONST               ('TimeStamps', 'TriggerType')
             2194  BUILD_CONST_KEY_MAP_2     2 
             2196  LOAD_FAST                'output'
             2198  LOAD_STR                 'button_trigger_events'
             2200  STORE_SUBSCR     
           2202_0  COME_FROM          2184  '2184'

 L. 697      2202  LOAD_FAST                'output'
             2204  LOAD_STR                 'button_trigger_events'
             2206  BINARY_SUBSCR    
             2208  LOAD_STR                 'TimeStamps'
             2210  BINARY_SUBSCR    
             2212  LOAD_ATTR                append
             2214  LOAD_FAST                'time_stamp'
             2216  CALL_FUNCTION_1       1  '1 positional argument'
             2218  POP_TOP          

 L. 698      2220  LOAD_GLOBAL              unpack
             2222  LOAD_STR                 '<H'
             2224  LOAD_FAST                'self'
             2226  LOAD_ATTR                datafile
             2228  LOAD_ATTR                read
             2230  LOAD_CONST               2
             2232  CALL_FUNCTION_1       1  '1 positional argument'
             2234  CALL_FUNCTION_2       2  '2 positional arguments'
             2236  LOAD_CONST               0
             2238  BINARY_SUBSCR    
             2240  STORE_FAST               'trigger_type'

 L. 699      2242  LOAD_FAST                'trigger_type'
             2244  LOAD_GLOBAL              UNDEFINED
             2246  COMPARE_OP               ==
             2248  POP_JUMP_IF_FALSE  2272  'to 2272'

 L. 699      2252  LOAD_FAST                'output'
             2254  LOAD_STR                 'button_trigger_events'
             2256  BINARY_SUBSCR    
             2258  LOAD_STR                 'TriggerType'
             2260  BINARY_SUBSCR    
             2262  LOAD_ATTR                append
             2264  LOAD_STR                 'undefined'
             2266  CALL_FUNCTION_1       1  '1 positional argument'
             2268  POP_TOP          
             2270  JUMP_FORWARD       2350  'to 2350'
             2272  ELSE                     '2350'

 L. 700      2272  LOAD_FAST                'trigger_type'
             2274  LOAD_GLOBAL              BUTTON_PRESS
             2276  COMPARE_OP               ==
             2278  POP_JUMP_IF_FALSE  2302  'to 2302'

 L. 700      2282  LOAD_FAST                'output'
             2284  LOAD_STR                 'button_trigger_events'
             2286  BINARY_SUBSCR    
             2288  LOAD_STR                 'TriggerType'
             2290  BINARY_SUBSCR    
             2292  LOAD_ATTR                append
             2294  LOAD_STR                 'button press'
             2296  CALL_FUNCTION_1       1  '1 positional argument'
             2298  POP_TOP          
             2300  JUMP_FORWARD       2350  'to 2350'
             2302  ELSE                     '2350'

 L. 701      2302  LOAD_FAST                'trigger_type'
             2304  LOAD_GLOBAL              BUTTON_RESET
             2306  COMPARE_OP               ==
             2308  POP_JUMP_IF_FALSE  2332  'to 2332'

 L. 701      2312  LOAD_FAST                'output'
             2314  LOAD_STR                 'button_trigger_events'
             2316  BINARY_SUBSCR    
             2318  LOAD_STR                 'TriggerType'
             2320  BINARY_SUBSCR    
             2322  LOAD_ATTR                append
             2324  LOAD_STR                 'event reset'
             2326  CALL_FUNCTION_1       1  '1 positional argument'
             2328  POP_TOP          
             2330  JUMP_FORWARD       2350  'to 2350'
             2332  ELSE                     '2350'

 L. 702      2332  LOAD_FAST                'output'
             2334  LOAD_STR                 'button_trigger_events'
             2336  BINARY_SUBSCR    
             2338  LOAD_STR                 'TriggerType'
             2340  BINARY_SUBSCR    
             2342  LOAD_ATTR                append
             2344  LOAD_STR                 'error'
             2346  CALL_FUNCTION_1       1  '1 positional argument'
             2348  POP_TOP          
           2350_0  COME_FROM          2330  '2330'
           2350_1  COME_FROM          2300  '2300'
           2350_2  COME_FROM          2270  '2270'

 L. 703      2350  LOAD_FAST                'self'
             2352  LOAD_ATTR                datafile
             2354  LOAD_ATTR                seek
             2356  LOAD_FAST                'self'
             2358  LOAD_ATTR                basic_header
             2360  LOAD_STR                 'BytesInDataPackets'
             2362  BINARY_SUBSCR    
             2364  LOAD_CONST               8
             2366  BINARY_SUBTRACT  
             2368  LOAD_CONST               1
             2370  CALL_FUNCTION_2       2  '2 positional arguments'
             2372  POP_TOP          
             2374  JUMP_BACK            38  'to 38'
             2376  ELSE                     '2618'

 L. 706      2376  LOAD_DEREF               'packet_id'
             2378  LOAD_GLOBAL              CONFIGURATION_PACKET_ID
             2380  COMPARE_OP               ==
             2382  POP_JUMP_IF_FALSE  2594  'to 2594'

 L. 709      2386  LOAD_STR                 'configuration_events'
             2388  LOAD_FAST                'output'
             2390  COMPARE_OP               not-in
             2392  POP_JUMP_IF_FALSE  2412  'to 2412'

 L. 710      2396  BUILD_LIST_0          0 
             2398  BUILD_LIST_0          0 
             2400  BUILD_LIST_0          0 
             2402  LOAD_CONST               ('TimeStamps', 'ConfigChangeType', 'ConfigChanged')
             2404  BUILD_CONST_KEY_MAP_3     3 
             2406  LOAD_FAST                'output'
             2408  LOAD_STR                 'configuration_events'
             2410  STORE_SUBSCR     
           2412_0  COME_FROM          2392  '2392'

 L. 712      2412  LOAD_FAST                'output'
             2414  LOAD_STR                 'configuration_events'
             2416  BINARY_SUBSCR    
             2418  LOAD_STR                 'TimeStamps'
             2420  BINARY_SUBSCR    
             2422  LOAD_ATTR                append
             2424  LOAD_FAST                'time_stamp'
             2426  CALL_FUNCTION_1       1  '1 positional argument'
             2428  POP_TOP          

 L. 713      2430  LOAD_GLOBAL              unpack
             2432  LOAD_STR                 '<H'
             2434  LOAD_FAST                'self'
             2436  LOAD_ATTR                datafile
             2438  LOAD_ATTR                read
             2440  LOAD_CONST               2
             2442  CALL_FUNCTION_1       1  '1 positional argument'
             2444  CALL_FUNCTION_2       2  '2 positional arguments'
             2446  LOAD_CONST               0
             2448  BINARY_SUBSCR    
             2450  STORE_FAST               'change_type'

 L. 714      2452  LOAD_FAST                'change_type'
             2454  LOAD_GLOBAL              CHG_NORMAL
             2456  COMPARE_OP               ==
             2458  POP_JUMP_IF_FALSE  2482  'to 2482'

 L. 714      2462  LOAD_FAST                'output'
             2464  LOAD_STR                 'configuration_events'
             2466  BINARY_SUBSCR    
             2468  LOAD_STR                 'ConfigChangeType'
             2470  BINARY_SUBSCR    
             2472  LOAD_ATTR                append
             2474  LOAD_STR                 'normal'
             2476  CALL_FUNCTION_1       1  '1 positional argument'
             2478  POP_TOP          
             2480  JUMP_FORWARD       2530  'to 2530'
             2482  ELSE                     '2530'

 L. 715      2482  LOAD_FAST                'change_type'
             2484  LOAD_GLOBAL              CHG_CRITICAL
             2486  COMPARE_OP               ==
             2488  POP_JUMP_IF_FALSE  2512  'to 2512'

 L. 715      2492  LOAD_FAST                'output'
             2494  LOAD_STR                 'configuration_events'
             2496  BINARY_SUBSCR    
             2498  LOAD_STR                 'ConfigChangeType'
             2500  BINARY_SUBSCR    
             2502  LOAD_ATTR                append
             2504  LOAD_STR                 'critical'
             2506  CALL_FUNCTION_1       1  '1 positional argument'
             2508  POP_TOP          
             2510  JUMP_FORWARD       2530  'to 2530'
             2512  ELSE                     '2530'

 L. 716      2512  LOAD_FAST                'output'
             2514  LOAD_STR                 'configuration_events'
             2516  BINARY_SUBSCR    
             2518  LOAD_STR                 'ConfigChangeType'
             2520  BINARY_SUBSCR    
             2522  LOAD_ATTR                append
             2524  LOAD_STR                 'error'
             2526  CALL_FUNCTION_1       1  '1 positional argument'
             2528  POP_TOP          
           2530_0  COME_FROM          2510  '2510'
           2530_1  COME_FROM          2480  '2480'

 L. 718      2530  LOAD_FAST                'self'
             2532  LOAD_ATTR                basic_header
             2534  LOAD_STR                 'BytesInDataPackets'
             2536  BINARY_SUBSCR    
             2538  LOAD_CONST               8
             2540  BINARY_SUBTRACT  
             2542  STORE_FAST               'samples'

 L. 719      2544  LOAD_FAST                'output'
             2546  LOAD_STR                 'configuration_events'
             2548  BINARY_SUBSCR    
             2550  LOAD_STR                 'ConfigChanged'
             2552  BINARY_SUBSCR    
             2554  LOAD_ATTR                append
             2556  LOAD_GLOBAL              unpack
             2558  LOAD_STR                 '<'
             2560  LOAD_GLOBAL              str
             2562  LOAD_FAST                'samples'
             2564  CALL_FUNCTION_1       1  '1 positional argument'
             2566  BINARY_ADD       
             2568  LOAD_STR                 's'
             2570  BINARY_ADD       

 L. 720      2572  LOAD_FAST                'self'
             2574  LOAD_ATTR                datafile
             2576  LOAD_ATTR                read
             2578  LOAD_FAST                'samples'
             2580  CALL_FUNCTION_1       1  '1 positional argument'
             2582  CALL_FUNCTION_2       2  '2 positional arguments'
             2584  LOAD_CONST               0
             2586  BINARY_SUBSCR    
             2588  CALL_FUNCTION_1       1  '1 positional argument'
             2590  POP_TOP          
             2592  JUMP_BACK            38  'to 38'
             2594  ELSE                     '2618'

 L. 723      2594  LOAD_FAST                'self'
             2596  LOAD_ATTR                datafile
             2598  LOAD_ATTR                seek
             2600  LOAD_FAST                'self'
             2602  LOAD_ATTR                basic_header
             2604  LOAD_STR                 'BytesInDataPackets'
             2606  BINARY_SUBSCR    
             2608  LOAD_CONST               6
             2610  BINARY_SUBTRACT  
             2612  LOAD_CONST               1
             2614  CALL_FUNCTION_2       2  '2 positional arguments'
             2616  POP_TOP          
           2618_0  COME_FROM          1226  '1226'
             2618  JUMP_BACK            38  'to 38'
           2620_0  COME_FROM            60  '60'
             2620  POP_BLOCK        
           2622_0  COME_FROM_LOOP       34  '34'

 L. 725      2622  LOAD_FAST                'output'
             2624  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 170

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
                source_label = next(d['VideoSource'] for d in self.extended_headers if d['TrackableID'] == roi)
                if source_label in roi_events['Regions']:
                    idx = roi_events['Regions'].index(source_label)
                else:
                    idx = -1
                    roi_events['Regions'].append(source_label)
                    roi_events['EnterTimeStamps'].append([])
                    roi_events['ExitTimeStamps'].append([])
            if event == ENTER_EVENT:
                roi_events['EnterTimeStamps'][idx].append(comments['TimeStamp'][i])
            else:
                if event == EXIT_EVENT:
                    roi_events['ExitTimeStamps'][idx].append(comments['TimeStamp'][i])

        return roi_events

    def close(self):
        name = self.datafile.name
        self.datafile.close


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
        output = dict
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
            output['data_headers'][0]['NumDataPoints'] = (ospath.getsize(self.datafile.name) - self.datafile.tell) // (DATA_BYTE_SIZE * self.basic_header['ChannelCount'])
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
        else:
            num_elecs = len(output['elec_ids'])
            if self.basic_header['FileSpec'] != '2.1':
                for i in range(num_elecs):
                    idx = next(item for item, d in enumerate(self.extended_headers) if d['ElectrodeID'] == output['elec_ids'][i])
                    output['ExtendedHeaderIndices'].append(idx)
                    if self.extended_headers[idx]['PhysicalConnector'] < 5:
                        front_end_idxs.append(i)
                    else:
                        analog_input_idxs.append(i)

                if any(np.diff(np.array(front_end_idxs)) != 1):
                    front_end_idx_cont = False
                if any(np.diff(np.array(analog_input_idxs)) != 1):
                    analog_input_idx_cont = False
            if self.basic_header['FileSpec'] == '2.1':
                timestamp = TIMESTAMP_NULL_21
                num_data_pts = output['data_headers'][0]['NumDataPoints']
            else:
                while self.datafile.tell != ospath.getsize(self.datafile.name):
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
        else:
            try:
                output['data'] = np.zeros((total_samps, num_elecs), dtype=(np.float32))
            except MemoryError as err:
                err.args += (" Output data size requested is larger than available memory. Use the parameters\n              for getdata(), e.g., 'elec_ids', to request a subset of the data or use\n              NsxFile.savesubsetnsx() to create subsets of the main nsx file\n", )
                raise

            self.datafile.seek(self.basic_header['BytesInHeader'], 0)
            while not hit_stop:
                if self.basic_header['FileSpec'] != '2.1':
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
                    start_offset = hit_start or start_idx - timestamp_sample
                    if start_offset > output['data_headers'][(-1)]['NumDataPoints']:
                        self.datafile.seek(output['data_headers'][(-1)]['NumDataPoints'] * data_pt_size, 1)
                        if self.datafile.tell == ospath.getsize(self.datafile.name):
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
                    curr_file_pos = self.datafile.tell
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

            if not hit_stop:
                if start_idx > START_OFFSET_MIN:
                    raise Exception('Error: End of file found before start_time_s')
            if not hit_stop:
                if stop_idx:
                    print('\n*** WARNING: End of file found before stop_time_s, returning all data in file')
            output['data'] = output['data'].transpose
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
            subset_file.write(np.array(num_elecs).astype(np.uint32).tobytes)
            subset_file.write(np.array(elec_ids).astype(np.uint32).tobytes)
            self.datafile.seek(4 + 4 * self.basic_header['ChannelCount'], 1)
        else:
            subset_file.write(self.datafile.read(10))
            bytes_in_headers = NSX_BASIC_HEADER_BYTES_22 + NSX_EXT_HEADER_BYTES_22 * num_elecs
            num_pts_header_pos = bytes_in_headers + 5
            subset_file.write(np.array(bytes_in_headers).astype(np.uint32).tobytes)
            self.datafile.seek(4, 1)
            subset_file.write(self.datafile.read(296))
            subset_file.write(np.array(num_elecs).astype(np.uint32).tobytes)
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

        while self.datafile.tell != ospath.getsize(self.datafile.name):
            if self.basic_header['FileSpec'] == '2.1':
                packet_pts = (ospath.getsize(self.datafile.name) - self.datafile.tell) / (DATA_BYTE_SIZE * self.basic_header['ChannelCount'])
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
            datafile_pos = self.datafile.tell
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
                    shape = (int(num_pts), self.basic_header['ChannelCount'])
                    mm = np.memmap((self.datafile), dtype=(np.int16), mode='r', offset=file_offset, shape=shape)
                    if elec_id_indices:
                        mm = mm[:, elec_id_indices]
                    start_idx = 0
                    if file_size:
                        if file_size - subset_file.tell < DATA_PAGING_SIZE:
                            pts_can_add = int((file_size - subset_file.tell) // (num_elecs * DATA_BYTE_SIZE)) + 1
                            stop_idx = start_idx + pts_can_add
                            while pts_can_add < num_pts:
                                if elec_id_indices:
                                    subset_file.write(np.array(mm[start_idx:stop_idx]).tobytes)
                                else:
                                    subset_file.write(mm[start_idx:stop_idx])
                                prior_file_name = subset_file.name
                                prior_file_pkt_pts = subset_file_pkt_pts + pts_can_add
                                subset_file.close
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
                                        subset_file.write(np.array(timestamp_new).astype(np.uint32).tobytes)
                                        subset_file.write(np.array(num_pts - pts_can_add).astype(np.uint32).tobytes)
                                        prior_file.seek(num_pts_header_pos, 0)
                                        prior_file.write(np.array(prior_file_pkt_pts).astype(np.uint32).tobytes)
                                        num_pts_header_pos = bytes_in_headers + 5
                                prior_file.close
                                packet_read_pts += pts_can_add
                                start_idx += pts_can_add
                                num_pts -= pts_can_add
                                file_num += 1
                                subset_file_pkt_pts = 0
                                pausing = False
                                pts_can_add = int((file_size - subset_file.tell) // (num_elecs * DATA_BYTE_SIZE)) + 1
                                stop_idx = start_idx + pts_can_add

                    if elec_id_indices:
                        subset_file.write(np.array(mm[start_idx:]).tobytes)
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
            if file_time_s:
                if not pausing:
                    if self.datafile.tell != ospath.getsize(self.datafile.name):
                        pausing = True
                        print('\n*** Because of pausing in original datafile, this file may be slightly time shorter\n       than others, and will contain multiple data packets offset in time\n')
            if self.basic_header['FileSpec'] != '2.1':
                subset_file_pos = subset_file.tell
                subset_file.seek(curr_hdr_num_pts_pos, 0)
                subset_file.write(np.array(subset_file_pkt_pts).astype(np.uint32).tobytes)
                subset_file.seek(subset_file_pos, 0)

        subset_file.close
        print('\n *** All subset files written to disk and closed ***')
        return 'SUCCESS'

    def close(self):
        name = self.datafile.name
        self.datafile.close