# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/audio/s3m.py
# Compiled at: 2009-09-07 17:44:28
"""
The ScreamTracker 3.0x module format description for .s3m files.

Documents:
- Search s3m on Wotsit
  http://www.wotsit.org/

Author: Christophe GISQUET <christophe.gisquet@free.fr>
Creation: 11th February 2007
"""
from hachoir_parser import Parser
from hachoir_core.field import StaticFieldSet, FieldSet, Field, Bit, Bits, UInt32, UInt16, UInt8, Enum, PaddingBytes, RawBytes, NullBytes, String, GenericVector, ParserError
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_core.tools import alignValue

class Chunk:
    __module__ = __name__

    def __init__(self, cls, name, offset, size, *args):
        assert size != None and size >= 0
        self.cls = cls
        self.name = name
        self.offset = offset
        self.size = size
        self.args = args
        return


class ChunkIndexer:
    __module__ = __name__

    def __init__(self):
        self.chunks = []

    def canHouse(self, chunk, index):
        if index > 1:
            if chunk.offset + chunk.size > self.chunks[(index - 1)].offset:
                return False
        return True

    def addChunk(self, new_chunk):
        index = 0
        while index < len(self.chunks):
            offset = self.chunks[index].offset
            if offset < new_chunk.offset:
                if not self.canHouse(new_chunk, index):
                    raise ParserError("Chunk '%s' doesn't fit!" % new_chunk.name)
                self.chunks.insert(index, new_chunk)
                return
            index += 1

        self.chunks.append(new_chunk)

    def yieldChunks(self, obj):
        while len(self.chunks) > 0:
            chunk = self.chunks.pop()
            current_pos = obj.current_size // 8
            size = chunk.offset - current_pos
            if size > 0:
                obj.info('Padding of %u bytes needed: curr=%u offset=%u' % (size, current_pos, chunk.offset))
                yield PaddingBytes(obj, 'padding[]', size)
                current_pos = obj.current_size // 8
            count = 0
            old_off = chunk.offset
            while chunk.offset < current_pos:
                count += 1
                chunk = self.chunks.pop()
                if chunk == None:
                    obj.info("Couldn't resynch: %u object skipped to reach %u" % (count, current_pos))
                    return

            size = chunk.offset - current_pos
            if size > 0:
                obj.info('Skipped %u objects to resynch to %u; chunk offset: %u->%u' % (count, current_pos, old_off, chunk.offset))
                yield RawBytes(obj, 'resynch[]', size)
            obj.info('Yielding element of size %u at offset %u' % (chunk.size, chunk.offset))
            field = chunk.cls(obj, chunk.name, chunk.size, *chunk.args)
            yield field
            if hasattr(field, 'getSubChunks'):
                for sub_chunk in field.getSubChunks():
                    obj.info("Adding sub chunk: position=%u size=%u name='%s'" % (sub_chunk.offset, sub_chunk.size, sub_chunk.name))
                    self.addChunk(sub_chunk)

        return


class S3MFlags(StaticFieldSet):
    __module__ = __name__
    format = ((Bit, 'st2_vibrato', 'Vibrato (File version 1/ScreamTrack 2)'), (Bit, 'st2_tempo', 'Tempo (File version 1/ScreamTrack 2)'), (Bit, 'amiga_slides', 'Amiga slides (File version 1/ScreamTrack 2)'), (Bit, 'zero_vol_opt', 'Automatically turn off looping notes whose volume is zero for >2 note rows'), (Bit, 'amiga_limits', 'Disallow notes beyond Amiga hardware specs'), (Bit, 'sb_processing', 'Enable filter/SFX with SoundBlaster'), (Bit, 'vol_slide', 'Volume slide also performed on first row'), (Bit, 'extended', 'Special custom data in file'), (Bits, 'unused[]', 8))


def parseChannelType(val):
    val = val.value
    if val < 8:
        return 'Left Sample Channel %u' % val
    if val < 16:
        return 'Right Sample Channel %u' % (val - 8)
    if val < 32:
        return 'Adlib channel %u' % (val - 16)
    return 'Value %u unknown' % val


class ChannelSettings(FieldSet):
    __module__ = __name__
    static_size = 8

    def createFields(self):
        yield textHandler(Bits(self, 'type', 7), parseChannelType)
        yield Bit(self, 'enabled')


class ChannelPanning(FieldSet):
    __module__ = __name__
    static_size = 8

    def createFields(self):
        yield Bits(self, 'default_position', 4, 'Default pan position')
        yield Bit(self, 'reserved[]')
        yield Bit(self, 'use_default', 'Bits 0:3 specify default position')
        yield Bits(self, 'reserved[]', 2)


class SizeFieldSet(FieldSet):
    """
    Provide an automatic constructor for a sized field that can be aligned
    on byte positions according to ALIGN.

    Size is ignored if static_size is set. Real size is stored
    for convenience, but beware, it is not in bits, but in bytes.

    Field can be automatically padded, unless:
    - size is 0 (unknown, so padding doesn't make sense)
    - it shouldn't be aligned

    If it shouldn't be aligned, two solutions:
    - change _size to another value than the one found through aligment.
    - derive a class with ALIGN = 0.
    """
    __module__ = __name__
    ALIGN = 16

    def __init__(self, parent, name, size, desc=None):
        FieldSet.__init__(self, parent, name, desc)
        if size:
            self.real_size = size
            if self.static_size == None:
                self.setCheckedSizes(size)
        return

    def setCheckedSizes(self, size):
        self.real_size = size
        size *= 8
        if self.ALIGN:
            size = alignValue(self.absolute_address + size, 8 * self.ALIGN) - self.absolute_address
        if self._parent._size:
            if self._parent.current_size + size > self._parent._size:
                size = self._parent._size - self._parent.current_size
        self._size = size

    def createFields(self):
        for field in self.createUnpaddedFields():
            yield field

        size = (self._size - self.current_size) // 8
        if size > 0:
            yield PaddingBytes(self, 'padding', size)


class Header(SizeFieldSet):
    __module__ = __name__

    def createDescription(self):
        return '%s (%u patterns, %u instruments)' % (self['title'].value, self['num_patterns'].value, self['num_instruments'].value)

    def createValue(self):
        return self['title'].value

    def createUnpaddedFields(self):
        yield String(self, 'title', 28, strip='\x00')
        yield textHandler(UInt8(self, 'marker[]'), hexadecimal)
        for field in self.getFileVersionField():
            yield field

        yield UInt16(self, 'num_orders')
        yield UInt16(self, 'num_instruments')
        yield UInt16(self, 'num_patterns')
        for field in self.getFirstProperties():
            yield field

        yield String(self, 'marker[]', 4)
        for field in self.getLastProperties():
            yield field

        yield GenericVector(self, 'channel_settings', 32, ChannelSettings, 'channel')
        yield GenericVector(self, 'orders', self.getNumOrders(), UInt8, 'order')
        for field in self.getHeaderEndFields():
            yield field


class S3MHeader(Header):
    """
          0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0000: | Song name, max 28 chars (end with NUL (0))                    |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0010: |                                               |1Ah|Typ| x | x |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0020: |OrdNum |InsNum |PatNum | Flags | Cwt/v | Ffi   |'S'|'C'|'R'|'M'|
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0030: |g.v|i.s|i.t|m.v|u.c|d.p| x | x | x | x | x | x | x | x |Special|
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0040: |Channel settings for 32 channels, 255=unused,+128=disabled     |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0050: |                                                               |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0060: |Orders; length=OrdNum (should be even)                         |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  xxx1: |Parapointers to instruments; length=InsNum*2                   |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  xxx2: |Parapointers to patterns; length=PatNum*2                      |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  xxx3: |Channel default pan positions                                  |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        xxx1=70h+orders
        xxx2=70h+orders+instruments*2
        xxx3=70h+orders+instruments*2+patterns*2
    """
    __module__ = __name__

    def __init__(self, parent, name, size, desc=None):
        Header.__init__(self, parent, name, size, desc)
        size = 96 + self['num_orders'].value + 2 * (self['num_instruments'].value + self['num_patterns'].value)
        if self['panning_info'].value == 252:
            size += 32
        self.setCheckedSizes(size)

    def getFileVersionField(self):
        yield UInt8(self, 'type')
        yield RawBytes(self, 'reserved[]', 2)

    def getFirstProperties(self):
        yield S3MFlags(self, 'flags')
        yield UInt8(self, 'creation_version_minor')
        yield Bits(self, 'creation_version_major', 4)
        yield Bits(self, 'creation_version_unknown', 4, '(=1)')
        yield UInt16(self, 'format_version')

    def getLastProperties(self):
        yield UInt8(self, 'glob_vol', 'Global volume')
        yield UInt8(self, 'init_speed', 'Initial speed (command A)')
        yield UInt8(self, 'init_tempo', 'Initial tempo (command T)')
        yield Bits(self, 'volume', 7)
        yield Bit(self, 'stereo')
        yield UInt8(self, 'click_removal', 'Number of GUS channels to run to prevent clicks')
        yield UInt8(self, 'panning_info')
        yield RawBytes(self, 'reserved[]', 8)
        yield UInt16(self, 'custom_data_parapointer', 'Parapointer to special custom data (not used by ST3.01)')

    def getNumOrders(self):
        return self['num_orders'].value

    def getHeaderEndFields(self):
        instr = self['num_instruments'].value
        patterns = self['num_patterns'].value
        if instr > 0:
            yield GenericVector(self, 'instr_pptr', instr, UInt16, 'offset')
        if patterns > 0:
            yield GenericVector(self, 'pattern_pptr', patterns, UInt16, 'offset')
        if self['creation_version_major'].value >= 3 and self['creation_version_minor'].value >= 32 and self['panning_info'].value == 252:
            yield GenericVector(self, 'channel_panning', 32, ChannelPanning, 'channel')
        size = self._size - self.current_size
        if size > 0:
            yield PaddingBytes(self, 'padding', size // 8)

    def getSubChunks(self):
        for index in xrange(self['num_instruments'].value):
            yield Chunk(S3MInstrument, 'instrument[]', 16 * self[('instr_pptr/offset[%u]' % index)].value, S3MInstrument.static_size // 8)

        for index in xrange(self['num_patterns'].value):
            yield Chunk(S3MPattern, 'pattern[]', 16 * self[('pattern_pptr/offset[%u]' % index)].value, 0)


class PTMHeader(Header):
    __module__ = __name__
    static_size = 8 * 608

    def getTrackerVersion(val):
        val = val.value
        return 'ProTracker x%04X' % val

    def getFileVersionField(self):
        yield UInt16(self, 'type')
        yield RawBytes(self, 'reserved[]', 1)

    def getFirstProperties(self):
        yield UInt16(self, 'channels')
        yield UInt16(self, 'flags')
        yield UInt16(self, 'reserved[]')

    def getLastProperties(self):
        yield RawBytes(self, 'reserved[]', 16)

    def getNumOrders(self):
        return 256

    def getHeaderEndFields(self):
        yield GenericVector(self, 'pattern_pptr', 128, UInt16, 'offset')

    def getSubChunks(self):
        if self._parent._size:
            min_off = self.absolute_address + self._parent._size
        else:
            min_off = 99999999999
        count = self['num_instruments'].value
        addr = self.absolute_address
        for index in xrange(count):
            offset = (self.static_size + index * PTMInstrument.static_size) // 8
            yield Chunk(PTMInstrument, 'instrument[]', offset, PTMInstrument.static_size // 8)
            offset = self.stream.readBits(addr + 8 * (offset + 18), 32, LITTLE_ENDIAN)
            min_off = min(min_off, offset)

        count = self['num_patterns'].value
        prev_off = 16 * self['pattern_pptr/offset[0]'].value
        for index in range(1, count):
            offset = 16 * self[('pattern_pptr/offset[%u]' % index)].value
            yield Chunk(PTMPattern, 'pattern[]', prev_off, offset - prev_off)
            prev_off = offset

        yield Chunk(PTMPattern, 'pattern[]', prev_off, min_off - prev_off)


class SampleFlags(StaticFieldSet):
    __module__ = __name__
    format = ((Bit, 'loop_on'), (Bit, 'stereo', 'Sample size will be 2*length'), (Bit, '16bits', '16b sample, Intel LO-HI byteorder'), (Bits, 'unused', 5))


class S3MUInt24(Field):
    __module__ = __name__
    static_size = 24

    def __init__(self, parent, name, desc=None):
        Field.__init__(self, parent, name, size=24, description=desc)
        addr = self.absolute_address
        val = parent.stream.readBits(addr, 8, LITTLE_ENDIAN) << 20
        val += parent.stream.readBits(addr + 8, 16, LITTLE_ENDIAN) << 4
        self.createValue = lambda : val


class SampleData(SizeFieldSet):
    __module__ = __name__

    def createUnpaddedFields(self):
        yield RawBytes(self, 'data', self.real_size)


class PTMSampleData(SampleData):
    __module__ = __name__
    ALIGN = 0


class Instrument(SizeFieldSet):
    __module__ = __name__
    static_size = 8 * 80

    def createDescription(self):
        info = [
         self['c4_speed'].display]
        if 'flags/stereo' in self:
            if self['flags/stereo'].value:
                info.append('stereo')
            else:
                info.append('mono')
        info.append('%u bits' % self.getSampleBits())
        return (', ').join(info)

    def createFields(self):
        yield self.getType()
        yield String(self, 'filename', 12, strip='\x00')
        for field in self.getInstrumentFields():
            yield field

        yield String(self, 'name', 28, strip='\x00')
        yield String(self, 'marker', 4, "Either 'SCRS' or '(empty)'", strip='\x00')

    def createValue(self):
        return self['name'].value


class S3MInstrument(Instrument):
    """
    In fact a sample. Description follows:

          0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0000: |[T]| Dos filename (12345678.ABC)                   |    MemSeg |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0010: |Length |HI:leng|LoopBeg|HI:LBeg|LoopEnd|HI:Lend|Vol| x |[P]|[F]|
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0020: |C2Spd  |HI:C2sp| x | x | x | x |Int:Gp |Int:512|Int:lastused   |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0030: | Sample name, 28 characters max... (incl. NUL)                 |
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  0040: | ...sample name...                             |'S'|'C'|'R'|'S'|
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  xxxx: sampledata
    """
    __module__ = __name__
    MAGIC = 'SCRS'
    PACKING = {0: 'Unpacked', 1: 'DP30ADPCM'}
    TYPE = {0: 'Unknown', 1: 'Sample', 2: 'adlib melody', 3: 'adlib drum2'}

    def getType(self):
        return Enum(UInt8(self, 'type'), self.TYPE)

    def getSampleBits(self):
        return 8 * (1 + self['flags/16bits'].value)

    def getInstrumentFields(self):
        yield S3MUInt24(self, 'sample_offset')
        yield UInt32(self, 'sample_size')
        yield UInt32(self, 'loop_begin')
        yield UInt32(self, 'loop_end')
        yield UInt8(self, 'volume')
        yield UInt8(self, 'reserved[]')
        yield Enum(UInt8(self, 'packing'), self.PACKING)
        yield SampleFlags(self, 'flags')
        yield UInt32(self, 'c4_speed', 'Frequency for middle C note')
        yield UInt32(self, 'reserved[]', 4)
        yield UInt16(self, 'internal[]', 'Sample address in GUS memory')
        yield UInt16(self, 'internal[]', 'Flags for SoundBlaster loop expansion')
        yield UInt32(self, 'internal[]', 'Last used position (SB)')

    def getSubChunks(self):
        size = self['sample_size'].value
        if self['flags/stereo'].value:
            size *= 2
        if self['flags/16bits'].value:
            size *= 2
        yield Chunk(SampleData, 'sample_data[]', self['sample_offset'].value, size)


class PTMType(FieldSet):
    __module__ = __name__
    TYPES = {0: 'No sample', 1: 'Regular', 2: 'OPL2/OPL2 instrument', 3: 'MIDI instrument'}
    static_size = 8

    def createFields(self):
        yield Bits(self, 'unused', 2)
        yield Bit(self, 'is_tonable')
        yield Bit(self, '16bits')
        yield Bit(self, 'loop_bidir')
        yield Bit(self, 'loop')
        yield Enum(Bits(self, 'origin', 2), self.TYPES)


class PTMInstrument(Instrument):
    __module__ = __name__
    MAGIC = 'PTMI'
    ALIGN = 0

    def getType(self):
        return PTMType(self, 'flags')

    def getSampleBits(self):
        return 8

    def getInstrumentFields(self):
        yield UInt8(self, 'volume')
        yield UInt16(self, 'c4_speed')
        yield UInt16(self, 'sample_segment')
        yield UInt32(self, 'sample_offset')
        yield UInt32(self, 'sample_size')
        yield UInt32(self, 'loop_begin')
        yield UInt32(self, 'loop_end')
        yield UInt32(self, 'gus_begin')
        yield UInt32(self, 'gus_loop_start')
        yield UInt32(self, 'gus_loop_end')
        yield textHandler(UInt8(self, 'gus_loop_flags'), hexadecimal)
        yield UInt8(self, 'reserved[]')

    def getSubChunks(self):
        size = self['sample_size'].value
        if size:
            yield Chunk(PTMSampleData, 'sample_data[]', self['sample_offset'].value, size)


class S3MNoteInfo(StaticFieldSet):
    """
0=end of row
&31=channel
&32=follows;  BYTE:note, BYTE:instrument
&64=follows;  BYTE:volume
&128=follows; BYTE:command, BYTE:info
    """
    __module__ = __name__
    format = (
     (
      Bits, 'channel', 5), (Bit, 'has_note'), (Bit, 'has_volume'), (Bit, 'has_effect'))


class PTMNoteInfo(StaticFieldSet):
    __module__ = __name__
    format = ((Bits, 'channel', 5), (Bit, 'has_note'), (Bit, 'has_effect'), (Bit, 'has_volume'))


class Note(FieldSet):
    __module__ = __name__

    def createFields(self):
        info = self.NOTE_INFO(self, 'info')
        yield info
        if info['has_note'].value:
            yield UInt8(self, 'note')
            yield UInt8(self, 'instrument')
        if info['has_volume'].value:
            yield UInt8(self, 'volume')
        if info['has_effect'].value:
            yield UInt8(self, 'effect')
            yield UInt8(self, 'param')


class S3MNote(Note):
    __module__ = __name__
    NOTE_INFO = S3MNoteInfo


class PTMNote(Note):
    __module__ = __name__
    NOTE_INFO = PTMNoteInfo


class Row(FieldSet):
    __module__ = __name__

    def createFields(self):
        addr = self.absolute_address
        while True:
            byte = self.stream.readBits(addr, 8, self.endian)
            if not byte:
                yield NullBytes(self, 'terminator', 1)
                return
            note = self.NOTE(self, 'note[]')
            yield note
            addr += note.size


class S3MRow(Row):
    __module__ = __name__
    NOTE = S3MNote


class PTMRow(Row):
    __module__ = __name__
    NOTE = PTMNote


class Pattern(SizeFieldSet):
    __module__ = __name__

    def createUnpaddedFields(self):
        count = 0
        while count < 64 and not self.eof:
            yield self.ROW(self, 'row[]')
            count += 1


class S3MPattern(Pattern):
    __module__ = __name__
    ROW = S3MRow

    def __init__(self, parent, name, size, desc=None):
        Pattern.__init__(self, parent, name, size, desc)
        addr = self.absolute_address
        size = self.stream.readBits(addr, 16, LITTLE_ENDIAN)
        self.setCheckedSizes(size)


class PTMPattern(Pattern):
    __module__ = __name__
    ROW = PTMRow


class Module(Parser):
    __module__ = __name__
    endian = LITTLE_ENDIAN

    def validate(self):
        marker = self.stream.readBits(28 * 8, 8, LITTLE_ENDIAN)
        if marker != 26:
            return 'Invalid start marker %u' % marker
        marker = self.stream.readBytes(44 * 8, 4)
        if marker != self.MARKER:
            return 'Invalid marker %s!=%s' % (marker, self.MARKER)
        return True

    def createFields(self):
        indexer = ChunkIndexer()
        indexer.addChunk(Chunk(self.HEADER, 'header', 0, 80))
        for field in indexer.yieldChunks(self):
            yield field


class S3MModule(Module):
    __module__ = __name__
    PARSER_TAGS = {'id': 's3m', 'category': 'audio', 'file_ext': ('s3m', ), 'mime': ('audio/s3m', 'audio/x-s3m'), 'min_size': 64 * 8, 'description': 'ScreamTracker3 module'}
    MARKER = 'SCRM'
    HEADER = S3MHeader


class PTMModule(Module):
    __module__ = __name__
    PARSER_TAGS = {'id': 'ptm', 'category': 'audio', 'file_ext': ('ptm', ), 'min_size': 64 * 8, 'description': 'PolyTracker module (v1.17)'}
    MARKER = 'PTMF'
    HEADER = PTMHeader