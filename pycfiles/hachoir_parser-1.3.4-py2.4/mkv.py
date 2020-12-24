# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/container/mkv.py
# Compiled at: 2010-07-25 20:58:36
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, Link, MissingField, ParserError, Enum as _Enum, String as _String, Float32, Float64, NullBits, Bits, Bit, RawBytes, Bytes, Int16, GenericInteger
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.iso639 import ISO639_2
from hachoir_core.tools import humanDatetime
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_parser.container.ogg import XiphInt
from datetime import datetime, timedelta

class RawInt(GenericInteger):
    """
    Raw integer: have to be used in BIG_ENDIAN!
    """
    __module__ = __name__

    def __init__(self, parent, name, description=None):
        GenericInteger.__init__(self, parent, name, False, 8, description)
        i = GenericInteger.createValue(self)
        if i == 0:
            raise ParserError('Invalid integer length!')
        while i < 128:
            self._size += 8
            i <<= 1


class Unsigned(RawInt):
    __module__ = __name__

    def __init__(self, parent, name, description=None):
        RawInt.__init__(self, parent, name, description)

    def hasValue(self):
        return True

    def createValue(self):
        header = 1 << self._size / 8 * 7
        value = RawInt.createValue(self) - header
        if value + 1 == header:
            return
        return value


class Signed(Unsigned):
    __module__ = __name__

    def createValue(self):
        header = 1 << self._size / 8 * 7 - 1
        value = RawInt.createValue(self) - 3 * header + 1
        if value == header:
            return
        return value


def Enum(parent, enum):
    return _Enum(GenericInteger(parent, 'enum', False, parent['size'].value * 8), enum)


def Bool(parent):
    return textHandler(GenericInteger(parent, 'bool', False, parent['size'].value * 8), lambda chunk: str(chunk.value != 0))


def UInt(parent):
    return GenericInteger(parent, 'unsigned', False, parent['size'].value * 8)


def SInt(parent):
    return GenericInteger(parent, 'signed', True, parent['size'].value * 8)


def String(parent):
    return _String(parent, 'string', parent['size'].value, charset='ASCII')


def EnumString(parent, enum):
    return _Enum(String(parent), enum)


def Binary(parent):
    return RawBytes(parent, 'binary', parent['size'].value)


class AttachedFile(Bytes):
    __module__ = __name__

    def __init__(self, parent):
        Bytes.__init__(self, parent, 'file', parent['size'].value, None)
        return

    def _getFilename(self):
        if not hasattr(self, '_filename'):
            try:
                self._filename = self['../../FileName/unicode'].value
            except MissingField:
                self._filename = None

        return self._filename

    def createDescription(self):
        filename = self._getFilename()
        if filename:
            return 'File "%s"' % filename
        return "('Filename' entry not found)"

    def _createInputStream(self, **args):
        tags = args.setdefault('tags', [])
        try:
            tags.append(('mime', self['../../FileMimeType/string'].value))
        except MissingField:
            pass

        filename = self._getFilename()
        if filename:
            tags.append(('filename', filename))
        return Bytes._createInputStream(self, **args)


def UTF8(parent):
    return _String(parent, 'unicode', parent['size'].value, charset='UTF-8')


def Float(parent):
    size = parent['size'].value
    if size == 4:
        return Float32(parent, 'float')
    elif size == 8:
        return Float64(parent, 'double')
    else:
        return RawBytes(parent, 'INVALID_FLOAT', size)


TIMESTAMP_T0 = datetime(2001, 1, 1)

def dateToDatetime(value):
    return TIMESTAMP_T0 + timedelta(microseconds=value // 1000)


def dateToString(field):
    return humanDatetime(dateToDatetime(field.value))


def Date(parent):
    return textHandler(GenericInteger(parent, 'date', True, parent['size'].value * 8), dateToString)


def SeekID(parent):
    return textHandler(GenericInteger(parent, 'binary', False, parent['size'].value * 8), lambda chunk: segment.get(chunk.value, (hexadecimal(chunk),))[0])


def CueClusterPosition(parent):

    class Cluster(Link):
        __module__ = __name__

        def createValue(self):
            parent = self.parent
            segment = parent['.....']
            pos = parent['unsigned'].value * 8 + segment[2].address
            return segment.getFieldByAddress(pos, feed=False)

    return Cluster(parent, 'cluster')


def CueTrackPositions(parent):

    class Block(Link):
        __module__ = __name__

        def createValue(self):
            parent = self.parent
            time = parent['../CueTime/unsigned'].value
            track = parent['CueTrack/unsigned'].value
            cluster = parent['CueClusterPosition/cluster'].value
            time -= cluster['Timecode/unsigned'].value
            for field in cluster:
                if field.name.startswith('BlockGroup['):
                    for path in ('Block/block', 'SimpleBlock'):
                        try:
                            block = field[path]
                            if block['track'].value == track and block['timecode'].value == time:
                                return field
                        except MissingField:
                            pass

            parent.error('Cue point not found')
            return self

    return Block(parent, 'block')


class Lace(FieldSet):
    __module__ = __name__

    def __init__(self, parent, lacing, size):
        self.n_frames = parent['n_frames'].value
        self.createFields = (self.parseXiph, self.parseFixed, self.parseEBML)[lacing]
        FieldSet.__init__(self, parent, 'Lace', size=size * 8)

    def parseXiph(self):
        for i in xrange(self.n_frames):
            yield XiphInt(self, 'size[]')

        for i in xrange(self.n_frames):
            yield RawBytes(self, 'frame[]', self[('size[' + str(i) + ']')].value)

        yield RawBytes(self, 'frame[]', (self._size - self.current_size) / 8)

    def parseEBML(self):
        yield Unsigned(self, 'size')
        for i in xrange(1, self.n_frames):
            yield Signed(self, 'dsize[]')

        size = self['size'].value
        yield RawBytes(self, 'frame[]', size)
        for i in xrange(self.n_frames - 1):
            size += self[('dsize[' + str(i) + ']')].value
            yield RawBytes(self, 'frame[]', size)

        yield RawBytes(self, 'frame[]', (self._size - self.current_size) / 8)

    def parseFixed(self):
        n = self.n_frames + 1
        size = self._size / 8 / n
        for i in xrange(n):
            yield RawBytes(self, 'frame[]', size)


class Block(FieldSet):
    __module__ = __name__

    def __init__(self, parent):
        FieldSet.__init__(self, parent, 'block')
        self._size = 8 * parent['size'].value

    def lacing(self):
        return _Enum(Bits(self, 'lacing', 2), ['none', 'Xiph', 'fixed', 'EBML'])

    def createFields(self):
        yield Unsigned(self, 'track')
        yield Int16(self, 'timecode')
        if self.parent._name == 'Block':
            yield NullBits(self, 'reserved[]', 4)
            yield Bit(self, 'invisible')
            yield self.lacing()
            yield NullBits(self, 'reserved[]', 1)
        elif self.parent._name == 'SimpleBlock[]':
            yield Bit(self, 'keyframe')
            yield NullBits(self, 'reserved', 3)
            yield Bit(self, 'invisible')
            yield self.lacing()
            yield Bit(self, 'discardable')
        else:
            yield NullBits(self, 'reserved', 8)
            return
        size = (self._size - self.current_size) / 8
        lacing = self['lacing'].value
        if lacing:
            yield textHandler(GenericInteger(self, 'n_frames', False, 8), lambda chunk: str(chunk.value + 1))
            yield Lace(self, lacing - 1, size - 1)
        else:
            yield RawBytes(self, 'frame', size)


ebml = {440786851: ('EBML[]', {17030: ('EBMLVersion', UInt), 17143: ('EBMLReadVersion', UInt), 17138: ('EBMLMaxIDLength', UInt), 17139: ('EBMLMaxSizeLength', UInt), 17026: ('DocType', String), 17031: ('DocTypeVersion', UInt), 17029: ('DocTypeReadVersion', UInt)})}
signature = {32394: ('SignatureAlgo', UInt), 32410: ('SignatureHash', UInt), 32421: ('SignaturePublicKey', Binary), 32437: ('Signature', Binary), 32347: ('SignatureElements', {32379: ('SignatureElementList[]', {25906: ('SignedElement[]', Binary)})})}
chapter_atom = {29636: ('ChapterUID', UInt), 145: ('ChapterTimeStart', UInt), 146: ('ChapterTimeEnd', UInt), 152: ('ChapterFlagHidden', Bool), 17816: ('ChapterFlagEnabled', Bool), 28263: ('ChapterSegmentUID', Binary), 28348: ('ChapterSegmentEditionUID', Binary), 25539: ('ChapterPhysicalEquiv', UInt), 143: ('ChapterTrack', {137: ('ChapterTrackNumber[]', UInt)}), 128: ('ChapterDisplay[]', {133: ('ChapString', UTF8), 17276: ('ChapLanguage[]', String), 17278: ('ChapCountry[]', String)}), 26948: ('ChapProcess[]', {26965: ('ChapProcessCodecID', UInt), 17677: ('ChapProcessPrivate', Binary), 26897: ('ChapProcessCommand[]', {26914: ('ChapProcessTime', UInt), 26931: ('ChapProcessData', Binary)})})}
simple_tag = {17827: ('TagName', UTF8), 17530: ('TagLanguage', String), 17588: ('TagDefault', Bool), 17543: ('TagString', UTF8), 17541: ('TagBinary', Binary)}
segment_seek = {19899: ('Seek[]', {21419: ('SeekID', SeekID), 21420: ('SeekPosition', UInt)})}
segment_info = {29604: ('SegmentUID', Binary), 29572: ('SegmentFilename', UTF8), 3979555: ('PrevUID', Binary), 3965867: ('PrevFilename', UTF8), 4110627: ('NextUID', Binary), 4096955: ('NextFilename', UTF8), 17476: ('SegmentFamily[]', Binary), 26916: ('ChapterTranslate[]', {27132: ('ChapterTranslateEditionUID[]', UInt), 27071: ('ChapterTranslateCodec', UInt), 27045: ('ChapterTranslateID', Binary)}), 2807729: ('TimecodeScale', UInt), 17545: ('Duration', Float), 17505: ('DateUTC', Date), 31657: ('Title', UTF8), 19840: ('MuxingApp', UTF8), 22337: ('WritingApp', UTF8)}
segment_clusters = {231: ('Timecode', UInt), 22612: ('SilentTracks', {22743: ('SilentTrackNumber[]', UInt)}), 167: ('Position', UInt), 171: ('PrevSize', UInt), 160: ('BlockGroup[]', {161: ('Block', Block), 162: ('BlockVirtual[]', Block), 30113: ('BlockAdditions', {166: ('BlockMore[]', {238: ('BlockAddID', UInt), 165: ('BlockAdditional', Binary)})}), 155: ('BlockDuration', UInt), 250: ('ReferencePriority', UInt), 251: ('ReferenceBlock[]', SInt), 253: ('ReferenceVirtual', SInt), 164: ('CodecState', Binary), 142: ('Slices[]', {232: ('TimeSlice[]', {204: ('LaceNumber', UInt), 205: ('FrameNumber', UInt), 203: ('BlockAdditionID', UInt), 206: ('Delay', UInt), 207: ('Duration', UInt)})})}), 163: ('SimpleBlock[]', Block)}
tracks_video = {154: ('FlagInterlaced', Bool), 21432: ('StereoMode',
         lambda parent: Enum(parent, [
          'mono', 'right eye', 'left eye', 'both eyes'])), 
   176: ('PixelWidth', UInt), 186: ('PixelHeight', UInt), 21674: ('PixelCropBottom', UInt), 21691: ('PixelCropTop', UInt), 21708: ('PixelCropLeft', UInt), 21725: ('PixelCropRight', UInt), 21680: ('DisplayWidth', UInt), 21690: ('DisplayHeight', UInt), 21682: ('DisplayUnit',
         lambda parent: Enum(parent, [
          'pixels', 'centimeters', 'inches'])), 
   21683: ('AspectRatioType',
         lambda parent: Enum(parent, [
          'free resizing', 'keep aspect ratio', 'fixed'])), 
   3061028: ('ColourSpace', Binary), 3126563: ('GammaValue', Float)}
tracks_audio = {181: ('SamplingFrequency', Float), 30901: ('OutputSamplingFrequency', Float), 159: ('Channels', UInt), 32123: ('ChannelPositions', Binary), 25188: ('BitDepth', UInt)}
tracks_content_encodings = {25152: ('ContentEncoding[]', {20529: ('ContentEncodingOrder', UInt), 20530: ('ContentEncodingScope', UInt), 20531: ('ContentEncodingType', UInt), 20532: ('ContentCompression', {16980: ('ContentCompAlgo', UInt), 16981: ('ContentCompSettings', Binary)}), 20533: ('ContentEncryption', {18401: ('ContentEncAlgo', UInt), 18402: ('ContentEncKeyID', Binary), 18403: ('ContentSignature', Binary), 18404: ('ContentSigKeyID', Binary), 18405: ('ContentSigAlgo', UInt), 18406: ('ContentSigHashAlgo', UInt)})})}
segment_tracks = {174: ('TrackEntry[]',
       {215: ('TrackNumber', UInt), 29637: ('TrackUID', UInt), 131: ('TrackType',
              lambda parent: Enum(parent, {1: 'video', 2: 'audio', 3: 'complex', 16: 'logo', 17: 'subtitle', 18: 'buttons', 32: 'control'})), 
          185: ('FlagEnabled', Bool), 136: ('FlagDefault', Bool), 21930: ('FlagForced[]', Bool), 156: ('FlagLacing', Bool), 28135: ('MinCache', UInt), 28152: ('MaxCache', UInt), 2352003: ('DefaultDuration', UInt), 2306383: ('TrackTimecodeScale', Float), 21375: ('TrackOffset', SInt), 21998: ('MaxBlockAdditionID', UInt), 21358: ('Name', UTF8), 2274716: ('Language',
                  lambda parent: EnumString(parent, ISO639_2)), 
          134: ('CodecID', String), 25506: ('CodecPrivate', Binary), 2459272: ('CodecName', UTF8), 29766: ('AttachmentLink', UInt), 3839639: ('CodecSettings', UTF8), 3883072: ('CodecInfoURL[]', String), 2536000: ('CodecDownloadURL[]', String), 170: ('CodecDecodeAll', Bool), 28587: ('TrackOverlay[]', UInt), 26148: ('TrackTranslate[]', {26364: ('TrackTranslateEditionUID[]', UInt), 26303: ('TrackTranslateCodec', UInt), 26277: ('TrackTranslateTrackID', Binary)}), 224: ('Video', tracks_video), 225: ('Audio', tracks_audio), 28032: ('ContentEncodings', tracks_content_encodings)})}
segment_cues = {187: ('CuePoint[]', {179: ('CueTime', UInt), 183: ('CueTrackPositions[]', CueTrackPositions, {247: ('CueTrack', UInt), 241: ('CueClusterPosition', CueClusterPosition, UInt), 21368: ('CueBlockNumber', UInt), 234: ('CueCodecState', UInt), 219: ('CueReference[]', {150: ('CueRefTime', UInt), 151: ('CueRefCluster', UInt), 21343: ('CueRefNumber', UInt), 235: ('CueRefCodecState', UInt)})})})}
segment_attachments = {24999: ('AttachedFile[]', {18046: ('FileDescription', UTF8), 18030: ('FileName', UTF8), 18016: ('FileMimeType', String), 18012: ('FileData', AttachedFile), 18094: ('FileUID', UInt), 18037: ('FileReferral', Binary)})}
segment_chapters = {17849: ('EditionEntry[]', {17852: ('EditionUID', UInt), 17853: ('EditionFlagHidden', Bool), 17883: ('EditionFlagDefault', Bool), 17885: ('EditionFlagOrdered', Bool), 182: ('ChapterAtom[]', chapter_atom)})}
segment_tags = {29555: ('Tag[]', {25536: ('Targets', {26826: ('TargetTypeValue', UInt), 25546: ('TargetType', String), 25541: ('TrackUID[]', UInt), 25545: ('EditionUID[]', UInt), 25540: ('ChapterUID[]', UInt), 25542: ('AttachmentUID[]', UInt)}), 26568: ('SimpleTag[]', simple_tag)})}
segment = {290298740: ('SeekHead[]', segment_seek), 357149030: ('Info[]', segment_info), 524531317: ('Cluster[]', segment_clusters), 374648427: ('Tracks[]', segment_tracks), 475249515: ('Cues', segment_cues), 423732329: ('Attachments', segment_attachments), 272869232: ('Chapters', segment_chapters), 307544935: ('Tags[]', segment_tags)}

class EBML(FieldSet):
    __module__ = __name__

    def __init__(self, parent, ids):
        FieldSet.__init__(self, parent, '?[]')
        id = self['id'].value
        self.val = ids.get(id)
        if not self.val:
            if id == 191:
                self.val = (
                 'CRC-32[]', Binary)
            elif id == 236:
                self.val = (
                 'Void[]', Binary)
            elif id == 458458727:
                self.val = (
                 'SignatureSlot[]', signature)
            else:
                self.val = (
                 'Unknown[]', Binary)
        self._name = self.val[0]
        size = self['size']
        if size.value is not None:
            self._size = size.address + size.size + size.value * 8
        elif self._parent._parent:
            raise ParserError('Unknown length (only allowed for the last Level 0 element)')
        elif self._parent._size is not None:
            self._size = self._parent._size - self.address
        return

    def createFields(self):
        yield RawInt(self, 'id')
        yield Unsigned(self, 'size')
        for val in self.val[1:]:
            if callable(val):
                yield val(self)
            else:
                while not self.eof:
                    yield EBML(self, val)


class MkvFile(Parser):
    __module__ = __name__
    EBML_SIGNATURE = 440786851
    PARSER_TAGS = {'id': 'matroska', 'category': 'container', 'file_ext': ('mka', 'mkv', 'webm'), 'mime': ('video/x-matroska', 'audio/x-matroska', 'video/webm', 'audio/webm'), 'min_size': 5 * 8, 'magic': (('\x1aEߣ', 0), ), 'description': 'Matroska multimedia container'}
    endian = BIG_ENDIAN

    def _getDoctype(self):
        return self[0]['DocType/string'].value

    def validate(self):
        if self.stream.readBits(0, 32, self.endian) != self.EBML_SIGNATURE:
            return False
        try:
            first = self[0]
        except ParserError:
            return False

        if None < self._size < first._size:
            return 'First chunk size is invalid'
        if self._getDoctype() not in ('matroska', 'webm'):
            return "Stream isn't a matroska document."
        return True

    def createFields(self):
        hdr = EBML(self, ebml)
        yield hdr
        while not self.eof:
            yield EBML(self, {408125543: ('Segment[]', segment)})

    def createContentSize(self):
        field = self['Segment[0]/size']
        return field.absolute_address + field.value * 8 + field.size

    def createDescription(self):
        if self._getDoctype() == 'webm':
            return 'WebM video'
        else:
            return 'Matroska video'

    def createMimeType(self):
        if self._getDoctype() == 'webm':
            return 'video/webm'
        else:
            return 'video/x-matroska'