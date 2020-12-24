# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/audio/midi.py
# Compiled at: 2009-09-07 17:44:28
"""
Musical Instrument Digital Interface (MIDI) audio file parser.

Documentation:
 - Standard MIDI File Format, Dustin Caldwell (downloaded on wotsit.org)

Author: Victor Stinner
Creation: 27 december 2006
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Bits, ParserError, String, UInt32, UInt24, UInt16, UInt8, Enum, RawBytes
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import createDict, humanDurationNanosec
from hachoir_parser.common.tracker import NOTE_NAME
MAX_FILESIZE = 10 * 1024 * 1024

class Integer(Bits):
    __module__ = __name__

    def __init__(self, parent, name, description=None):
        Bits.__init__(self, parent, name, 8, description)
        stream = parent.stream
        addr = self.absolute_address
        value = 0
        while True:
            bits = stream.readBits(addr, 8, parent.endian)
            value = (value << 7) + (bits & 127)
            if not bits & 128:
                break
            addr += 8
            self._size += 8
            if 32 < self._size:
                raise ParserError('Integer size is bigger than 32-bit')

        self.createValue = lambda : value


def parseNote(parser):
    yield Enum(UInt8(parser, 'note', 'Note number'), NOTE_NAME)
    yield UInt8(parser, 'velocity')


def parseControl(parser):
    yield UInt8(parser, 'control', 'Controller number')
    yield UInt8(parser, 'value', 'New value')


def parsePatch(parser):
    yield UInt8(parser, 'program', 'New program number')


def parseChannel(parser):
    yield UInt8(parser, 'channel', 'Channel number')


def parsePitch(parser):
    yield UInt8(parser, 'bottom', '(least sig) 7 bits of value')
    yield UInt8(parser, 'top', '(most sig) 7 bits of value')


def parseText(parser, size):
    yield String(parser, 'text', size)


def formatTempo(field):
    return humanDurationNanosec(field.value * 1000)


def parseTempo(parser, size):
    yield textHandler(UInt24(parser, 'microsec_quarter', 'Microseconds per quarter note'), formatTempo)


def parseTimeSignature(parser, size):
    yield UInt8(parser, 'numerator', 'Numerator of time signature')
    yield UInt8(parser, 'denominator', 'denominator of time signature 2=quarter 3=eighth, etc.')
    yield UInt8(parser, 'nb_tick', 'Number of ticks in metronome click')
    yield UInt8(parser, 'nb_32nd_note', 'Number of 32nd notes to the quarter note')


class Command(FieldSet):
    __module__ = __name__
    COMMAND = {}
    for channel in xrange(16):
        COMMAND[128 + channel] = (
         'Note off (channel %u)' % channel, parseNote)
        COMMAND[144 + channel] = ('Note on (channel %u)' % channel, parseNote)
        COMMAND[160 + channel] = ('Key after-touch (channel %u)' % channel, parseNote)
        COMMAND[176 + channel] = ('Control change (channel %u)' % channel, parseControl)
        COMMAND[192 + channel] = ('Program (patch) change (channel %u)' % channel, parsePatch)
        COMMAND[208 + channel] = ('Channel after-touch (channel %u)' % channel, parseChannel)
        COMMAND[224 + channel] = ('Pitch wheel change (channel %u)' % channel, parsePitch)

    COMMAND_DESC = createDict(COMMAND, 0)
    COMMAND_PARSER = createDict(COMMAND, 1)
    META_COMMAND_TEXT = 1
    META_COMMAND_NAME = 3
    META_COMMAND = {0: ("Sets the track's sequence number", None), 1: ('Text event', parseText), 2: ('Copyright info', parseText), 3: ('Sequence or Track name', parseText), 4: ('Track instrument name', parseText), 5: ('Lyric', parseText), 6: ('Marker', parseText), 7: ('Cue point', parseText), 47: ('End of the track', None), 81: ('Set tempo', parseTempo), 88: ('Time Signature', parseTimeSignature), 89: ('Key signature', None), 127: ('Sequencer specific information', None)}
    META_COMMAND_DESC = createDict(META_COMMAND, 0)
    META_COMMAND_PARSER = createDict(META_COMMAND, 1)

    def createFields--- This code section failed: ---

 L. 105         0  LOAD_GLOBAL           0  'Integer'
                3  LOAD_FAST             0  'self'
                6  LOAD_CONST               'time'
                9  LOAD_CONST               'Delta time in ticks'
               12  CALL_FUNCTION_3       3  None
               15  YIELD_VALUE      

 L. 106        16  LOAD_GLOBAL           2  'Enum'
               19  LOAD_GLOBAL           3  'textHandler'
               22  LOAD_GLOBAL           4  'UInt8'
               25  LOAD_FAST             0  'self'
               28  LOAD_CONST               'command'
               31  CALL_FUNCTION_2       2  None
               34  LOAD_GLOBAL           5  'hexadecimal'
               37  CALL_FUNCTION_2       2  None
               40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             6  'COMMAND_DESC'
               46  CALL_FUNCTION_2       2  None
               49  YIELD_VALUE      

 L. 107        50  LOAD_FAST             0  'self'
               53  LOAD_CONST               'command'
               56  BINARY_SUBSCR    
               57  LOAD_ATTR             7  'value'
               60  STORE_FAST            3  'command'

 L. 108        63  LOAD_FAST             3  'command'
               66  LOAD_CONST               255
               69  COMPARE_OP            2  ==
               72  JUMP_IF_FALSE       184  'to 259'
               75  POP_TOP          

 L. 109        76  LOAD_GLOBAL           2  'Enum'
               79  LOAD_GLOBAL           3  'textHandler'
               82  LOAD_GLOBAL           4  'UInt8'
               85  LOAD_FAST             0  'self'
               88  LOAD_CONST               'meta_command'
               91  CALL_FUNCTION_2       2  None
               94  LOAD_GLOBAL           5  'hexadecimal'
               97  CALL_FUNCTION_2       2  None
              100  LOAD_FAST             0  'self'
              103  LOAD_ATTR             9  'META_COMMAND_DESC'
              106  CALL_FUNCTION_2       2  None
              109  YIELD_VALUE      

 L. 110       110  LOAD_GLOBAL           4  'UInt8'
              113  LOAD_FAST             0  'self'
              116  LOAD_CONST               'data_len'
              119  CALL_FUNCTION_2       2  None
              122  YIELD_VALUE      

 L. 111       123  LOAD_FAST             0  'self'
              126  LOAD_CONST               'data_len'
              129  BINARY_SUBSCR    
              130  LOAD_ATTR             7  'value'
              133  STORE_FAST            4  'size'

 L. 112       136  LOAD_FAST             4  'size'
              139  JUMP_IF_FALSE       113  'to 255'
              142  POP_TOP          

 L. 113       143  LOAD_FAST             0  'self'
              146  LOAD_CONST               'meta_command'
              149  BINARY_SUBSCR    
              150  LOAD_ATTR             7  'value'
              153  STORE_FAST            3  'command'

 L. 114       156  LOAD_FAST             3  'command'
              159  LOAD_FAST             0  'self'
              162  LOAD_ATTR            11  'META_COMMAND_PARSER'
              165  COMPARE_OP            6  in
              168  JUMP_IF_FALSE        17  'to 188'
              171  POP_TOP          

 L. 115       172  LOAD_FAST             0  'self'
              175  LOAD_ATTR            11  'META_COMMAND_PARSER'
              178  LOAD_FAST             3  'command'
              181  BINARY_SUBSCR    
              182  STORE_FAST            1  'parser'
              185  JUMP_FORWARD          7  'to 195'
            188_0  COME_FROM           168  '168'
              188  POP_TOP          

 L. 117       189  LOAD_CONST               None
              192  STORE_FAST            1  'parser'
            195_0  COME_FROM           185  '185'

 L. 118       195  LOAD_FAST             1  'parser'
              198  JUMP_IF_FALSE        34  'to 235'
              201  POP_TOP          

 L. 119       202  SETUP_LOOP           47  'to 252'
              205  LOAD_FAST             1  'parser'
              208  LOAD_FAST             0  'self'
              211  LOAD_FAST             4  'size'
              214  CALL_FUNCTION_2       2  None
              217  GET_ITER         
              218  FOR_ITER             10  'to 231'
              221  STORE_FAST            2  'field'

 L. 120       224  LOAD_FAST             2  'field'
              227  YIELD_VALUE      
              228  JUMP_BACK           218  'to 218'
              231  POP_BLOCK        
              232  JUMP_ABSOLUTE       256  'to 256'
            235_0  COME_FROM           198  '198'
              235  POP_TOP          

 L. 122       236  LOAD_GLOBAL          15  'RawBytes'
              239  LOAD_FAST             0  'self'
              242  LOAD_CONST               'data'
              245  LOAD_FAST             4  'size'
              248  CALL_FUNCTION_3       3  None
              251  YIELD_VALUE      
            252_0  COME_FROM           202  '202'
              252  JUMP_ABSOLUTE       343  'to 343'
            255_0  COME_FROM           139  '139'
              255  POP_TOP          
              256  JUMP_FORWARD         84  'to 343'
            259_0  COME_FROM            72  '72'
              259  POP_TOP          

 L. 124       260  LOAD_FAST             3  'command'
              263  LOAD_FAST             0  'self'
              266  LOAD_ATTR            16  'COMMAND_PARSER'
              269  COMPARE_OP            7  not-in
              272  JUMP_IF_FALSE        27  'to 302'
            275_0  THEN                     303
              275  POP_TOP          

 L. 125       276  LOAD_GLOBAL          17  'ParserError'
              279  LOAD_CONST               'Unknown command: %s'
              282  LOAD_FAST             0  'self'
              285  LOAD_CONST               'command'
              288  BINARY_SUBSCR    
              289  LOAD_ATTR            18  'display'
              292  BINARY_MODULO    
              293  CALL_FUNCTION_1       1  None
              296  RAISE_VARARGS_1       1  None
              299  JUMP_FORWARD          1  'to 303'
            302_0  COME_FROM           272  '272'
              302  POP_TOP          
            303_0  COME_FROM           299  '299'

 L. 126       303  LOAD_FAST             0  'self'
              306  LOAD_ATTR            16  'COMMAND_PARSER'
              309  LOAD_FAST             3  'command'
              312  BINARY_SUBSCR    
              313  STORE_FAST            1  'parser'

 L. 127       316  SETUP_LOOP           24  'to 343'
              319  LOAD_FAST             1  'parser'
              322  LOAD_FAST             0  'self'
              325  CALL_FUNCTION_1       1  None
              328  GET_ITER         
              329  FOR_ITER             10  'to 342'
              332  STORE_FAST            2  'field'

 L. 128       335  LOAD_FAST             2  'field'
              338  YIELD_VALUE      
              339  JUMP_BACK           329  'to 329'
              342  POP_BLOCK        
            343_0  COME_FROM           316  '316'
            343_1  COME_FROM           256  '256'
              343  LOAD_CONST               None
              346  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 252

    def createDescription(self):
        if 'meta_command' in self:
            return self['meta_command'].display
        else:
            return self['command'].display


class Track(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = (8 + self['size'].value) * 8

    def createFields(self):
        yield String(self, 'marker', 4, 'Track marker (MTrk)', charset='ASCII')
        yield UInt32(self, 'size')
        if True:
            while not self.eof:
                yield Command(self, 'command[]')

        size = self['size'].value
        if size:
            yield RawBytes(self, 'raw', size)

    def createDescription(self):
        command = self['command[0]']
        if 'meta_command' in command and command['meta_command'].value in (Command.META_COMMAND_TEXT, Command.META_COMMAND_NAME) and 'text' in command:
            return command['text'].value.strip('\r\n')
        else:
            return ''


class Header(FieldSet):
    __module__ = __name__
    static_size = 10 * 8
    FILE_FORMAT = {0: 'Single track', 1: 'Multiple tracks, synchronous', 2: 'Multiple tracks, asynchronous'}

    def createFields(self):
        yield UInt32(self, 'size')
        yield Enum(UInt16(self, 'file_format'), self.FILE_FORMAT)
        yield UInt16(self, 'nb_track')
        yield UInt16(self, 'delta_time', 'Delta-time ticks per quarter note')

    def createDescription(self):
        return '%s; %s tracks' % (self['file_format'].display, self['nb_track'].value)


class MidiFile(Parser):
    __module__ = __name__
    MAGIC = 'MThd'
    PARSER_TAGS = {'id': 'midi', 'category': 'audio', 'file_ext': ['mid', 'midi'], 'mime': ('audio/mime', ), 'magic': ((MAGIC, 0),), 'min_size': 64, 'description': 'MIDI audio'}
    endian = BIG_ENDIAN

    def validate(self):
        if self.stream.readBytes(0, 4) != self.MAGIC:
            return 'Invalid signature'
        if self['header/size'].value != 6:
            return 'Invalid header size'
        return True

    def createFields(self):
        yield String(self, 'signature', 4, 'MIDI signature (MThd)', charset='ASCII')
        yield Header(self, 'header')
        while not self.eof:
            yield Track(self, 'track[]')

    def createDescription(self):
        return 'MIDI audio: %s' % self['header'].description

    def createContentSize(self):
        count = self['/header/nb_track'].value - 1
        start = self[('track[%u]' % count)].absolute_address
        end = self.stream.searchBytes(b'\xff/\x00', start, MAX_FILESIZE * 8)
        if end is not None:
            return end + 3 * 8
        return