# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/textgrids/__init__.py
# Compiled at: 2020-03-23 11:33:13
# Size of source mod 2**32: 17132 bytes
"""textgrids -- Read and handle Praat’s textgrid files

  © Legisign.org, Tommi Nieminen <software@legisign.org>, 2012-20
  Published under GNU General Public License version 3 or newer.

  2020-03-23  1.3.1   BUG FIX: Tier.concat() fixed.

"""
import codecs, io, struct
from collections import OrderedDict, namedtuple
from .transcript import *
from .templates import *
version = '1.3.1'

class BinaryError(Exception):
    __doc__ = 'Read error for binary files.'


class ParseError(Exception):
    __doc__ = 'Read error for text files.'

    def __str__(self):
        return 'Parse error on line {}'.format(self.args[0])


Point = namedtuple('Point', ['text', 'xpos'])

class Interval(object):
    __doc__ = 'Interval is a timeframe xmin..xmax labelled "text".\n\n    xmin, xmax are floats, text a string that is converted into a Transcript\n    object.\n    '

    def __init__(self, text=None, xmin=0.0, xmax=0.0):
        self.text = Transcript(text)
        self.xmin = xmin
        self.xmax = xmax
        if self.xmin > self.xmax:
            return ValueError

    def __repr__(self):
        """Return (semi-)readable representation of self."""
        return '<Interval text="{}" xmin={} xmax={}>'.format(self.text, self.xmin, self.xmax)

    def containsvowel(self):
        """Boolean: Does the label contain a vowel?"""
        return any([vow in self.text for vow in vowels])

    @property
    def dur(self):
        """Return duration of the Interval."""
        return self.xmax - self.xmin

    def endswithvowel(self):
        """Boolean: does the label end with a vowel?

        Discards diacritics before testing."""
        text = self.text.transcode(retain_diacritics=False)
        return any([text.endswith(vow) for vow in vowels])

    @property
    def mid(self):
        """Return temporal midpoint for the Interval."""
        return self.xmin + self.dur / 2

    def startswithvowel(self):
        """Boolean: does the label start with a vowel?"""
        return any([self.text.startswith(vow) for vow in vowels])

    def timegrid(self, num=3):
        """Create an even-spaced time grid.

        Takes one optional integer argument "num", the number of timepoints.
        Returns a list of timepoints (floats) where the first element is
        Interval. xmin and the last Interval.xmax.
        """
        if num <= 1 or num != int(num):
            raise ValueError
        step = self.dur / num
        return [self.xmin + step * i for i in range(num + 1)]


class Tier(list):
    __doc__ = 'Tier is a list of either Interval or Point objects.'

    def __init__(self, data=None, point_tier=False):
        self.is_point_tier = point_tier
        if not data:
            data = []
        super().__init__(data)

    def __add__(self, elem):
        if self.is_point_tier:
            if not isinstance(elem, Point):
                raise TypeError
        if not isinstance(elem, Interval):
            raise TypeError
        super().__add__(elem)

    def concat(self, first=0, last=-1):
        """Return tier with intervals Tier[first]...Tier[last] concatenated.

        Parameters follow the usual Python index semantics: starting from 0,
        negative number count from the end. Note that the tier is not changed
        in place, you have to assign it to a variable.

        The method raises a TypeError if the Tier is a point tier,
        and ValueError if Tier[first:last] is not a slice.
        """
        if self.is_point_tier:
            raise TypeError
        area = self[first:last + 1]
        if not area:
            raise ValueError
        xmin = self[first].xmin
        xmax = self[last].xmax
        text = ''.join([segm.text for segm in area])
        new = Interval(text, xmin, xmax)
        self = self[:first] + [new] + self[last + 1:]
        return self

    def to_csv(self):
        """Format tier data as CSV, each row a separate string."""
        if self.is_point_tier:
            return ['"{}";{}'.format(t, xp) for t, xp in self]
        else:
            return ['"{}";{};{}'.format(t, xb, xe) for t, xb, xe in self]

    @property
    def tier_type(self):
        """Return tier type as string (for convenience)."""
        if self.is_point_tier:
            return 'PointTier'
        else:
            return 'IntervalTier'


class TextGrid(OrderedDict):
    __doc__ = 'TextGrid is a dict of tier names (keys) and Tiers (values).'

    def __init__(self, filename=None):
        self.filename = filename
        if self.filename:
            self.read(self.filename)

    def __repr__(self):
        """Return Praat (long) text format representation"""
        return self.format()

    def format(self, fmt=TEXT_LONG):
        """Format data as long text, short text, or binary.

        The optional argument can be TEXT_LONG (or 0) for long text,
        TEXT_SHORT (or 1) for short text, or BINARY (or 2) for binary.
        """
        if fmt == TEXT_LONG:
            return self._format_long()
        else:
            if fmt == TEXT_SHORT:
                return self._format_short()
            if fmt == BINARY:
                return self._format_binary()
        raise ValueError

    def _format_binary(self):
        """Format self as binary. Not intended to be used directly."""
        out = b'ooBinaryFile\x08TextGrid'
        out += struct.pack('>2d?i', self.xmin, self.xmax, True, len(self))
        for name, tier in self.items():
            typ = b'PointTier' if tier.is_point_tier else b'IntervalTier'
            out += struct.pack('B', len(typ))
            out += typ
            try:
                encoded_name = bytes(name, encoding='ascii')
                out += struct.pack('>h', len(encoded_name))
            except UnicodeEncodeError:
                encoded_name = bytes(name, encoding='utf-16-be')
                out += struct.pack('>2h', -1, len(encoded_name))

            out += encoded_name
            out += struct.pack('>2di', self.xmin, self.xmax, len(tier))
            for elem in tier:
                if tier.is_point_tier:
                    out += struct.pack('>d', elem.xpos)
                else:
                    out += struct.pack('>2d', elem.xmin, elem.xmax)
                try:
                    encoded_text = bytes((elem.text), encoding='ascii')
                    out += struct.pack('>h', len(encoded_text))
                except UnicodeEncodeError:
                    encoded_text = bytes((elem.text), encoding='utf-16-be')
                    out += struct.pack('>2h', -1, len(encoded_text))

                out += encoded_text

        return out

    def _format_long(self):
        """Format self as long text. Not intended to be used directly."""
        out = long_header.format(self.xmin, self.xmax, len(self))
        tier_count = 1
        for name, tier in self.items():
            if tier.is_point_tier:
                tier_type = 'PointTier'
                elem_type = 'points'
            else:
                tier_type = 'IntervalTier'
                elem_type = 'intervals'
            out += long_tier.format(tier_count, tier_type, name, self.xmin, self.xmax, elem_type, len(tier))
            for elem_count, elem in enumerate(tier, 1):
                if tier.is_point_tier:
                    out += long_point.format(elem_count, elem.xpos, elem.text)
                else:
                    out += long_interval.format(elem_count, elem.xmin, elem.xmax, elem.text)

        return out

    def _format_short(self):
        """Format self as short text. Not intended to be used directly."""
        out = short_header.format(xmin=(self.xmin), xmax=(self.xmax),
          length=(len(self)))
        for name, tier in self.items():
            out += short_tier.format(tier_type=(tier.tier_type), name=name,
              xmin=(self.xmin),
              xmax=(self.xmax),
              length=(len(tier)))
            for elem in tier:
                if tier.is_point_tier:
                    out += short_point.format(xpos=(elem.xpos), text=(elem.text))
                else:
                    out += short_interval.format(xmin=(elem.xmin), xmax=(elem.xmax),
                      text=(elem.text))

        return out

    def parse(self, data):
        """Parse textgrid data.

        Obligatory argument "data" is bytes.
        """
        if not isinstance(data, bytes):
            raise TypeError
        else:
            binary = b'ooBinaryFile\x08TextGrid'
            text = ['File type = "ooTextFile"', 'Object class = "TextGrid"', '']
            if data[:len(binary)] == binary:
                buff = io.BytesIO(data[len(binary):])
                try:
                    self._parse_binary(buff)
                except (IndexError, ValueError):
                    raise BinaryError

            else:
                coding = 'utf-8'
                if data[:2] == b'\xfe\xff':
                    coding = 'utf-16-be'
                    data = data[2:]
                buff = [s.strip() for s in data.decode(coding).split('\n')]
                if buff[:len(text)] != text:
                    raise TypeError
                buff = buff[len(text):]
                if buff[0][0] in '-0123456789':
                    self._parse_short(buff)
                else:
                    self._parse_long(buff)

    def _parse_binary(self, data):
        """Parse BINARY textgrid files. Not intended to be used directly."""
        sBool, sByte, sShort, sInt, sDouble = [struct.calcsize(c) for c in '?Bhid']
        self.xmin, self.xmax = struct.unpack('>2d', data.read(2 * sDouble))
        if not struct.unpack('?', data.read(sBool))[0]:
            return
        tiers = struct.unpack('>i', data.read(sInt))[0]
        for i in range(tiers):
            size = struct.unpack('B', data.read(sByte))[0]
            desc = data.read(size)
            if desc in (b'PointTier', b'TextTier'):
                point_tier = True
            else:
                if desc == b'IntervalTier':
                    point_tier = False
                else:
                    raise BinaryError
            tier = Tier(point_tier=point_tier)
            size = struct.unpack('>h', data.read(sShort))[0]
            tier_name = data.read(size).decode()
            data.read(2 * sDouble)
            elems = struct.unpack('>i', data.read(sInt))[0]
            for j in range(elems):
                if point_tier:
                    xpos = struct.unpack('>d', data.read(sDouble))[0]
                else:
                    xmin, xmax = struct.unpack('>2d', data.read(2 * sDouble))
                size = struct.unpack('>h', data.read(sShort))[0]
                if size == -1:
                    size = struct.unpack('>h', data.read(sShort))[0] * 2
                    coding = 'utf-16-be'
                else:
                    coding = 'ascii'
                text = Transcript(data.read(size).decode(coding))
                if point_tier:
                    tier.append(Point(text, xpos))
                else:
                    tier.append(Interval(text, xmin, xmax))

            self[tier_name] = tier

    def _parse_long(self, data):
        """Parse LONG textgrid files. Not intended to be used directly."""
        grab = lambda s: s.split(' = ')[1]
        self.xmin, self.xmax = [float(grab(s)) for s in data[:2]]
        if data[2] != 'tiers? <exists>':
            return
        tiers = int(grab(data[3]))
        p = 6
        for i in range(tiers):
            tier_type, tier_name = [grab(s).strip('"') for s in data[p:p + 2]]
            tier = Tier(point_tier=(tier_type != 'IntervalTier'))
            p += 2
            tier_xmin, tier_xmax = [float(grab(s)) for s in data[p:p + 2]]
            tier_len = int(grab(data[(p + 2)]))
            p += 4
            for j in range(tier_len):
                if tier.is_point_tier:
                    x1 = float(grab(data[p]))
                    text = Transcript(grab(data[(p + 1)]).strip('"'))
                    tier.append(Point(text, x1))
                    p += 3
                else:
                    x0, x1 = [float(grab(s)) for s in data[p:p + 2]]
                    text = Transcript(grab(data[(p + 2)]).strip('"'))
                    tier.append(Interval(text, x0, x1))
                    p += 4

            self[tier_name] = tier

    def _parse_short(self, data):
        """Parse SHORT textgrid files. Not intended to be used directly."""
        self.xmin, self.xmax = [float(s) for s in data[:2]]
        if data[2] != '<exists>':
            return
        tiers = int(data[3])
        p = 4
        for i in range(tiers):
            tier_type, tier_name = [s.strip('"') for s in data[p:p + 2]]
            tier = Tier(point_tier=(tier_type == 'PointTier'))
            p += 4
            elems = int(data[p])
            p += 1
            for j in range(elems):
                if tier.is_point_tier:
                    x1, text = data[p:p + 2]
                    x1 = float(x1)
                    text = Transcript(text.strip('"'))
                    tier.append(Point(text, x1))
                    p += 2
                else:
                    x0, x1, text = data[p:p + 3]
                    x0 = float(x0)
                    x1 = float(x1)
                    text = Transcript(text.strip('"'))
                    tier.append(Interval(text, x0, x1))
                    p += 3

            self[tier_name] = tier

    def read(self, filename):
        """Read given file as a TextGrid.

        "filename" is the name of the file.
        """
        self.filename = filename
        with open(self.filename, 'rb') as (infile):
            data = infile.read()
        self.parse(data)

    def tier_from_csv(self, tier_name, filename):
        """Import CSV file to an interval or point tier.

        "tier_name" (string) is the name for the new tier.
        "filename" (string) is the name of the input file.
        """
        import csv
        tier = None
        with open(filename, 'r') as (csvfile):
            reader = csv.reader(csvfile, delimiter=';')
            for line in reader:
                if len(line) == 2:
                    text, xpos = line
                    elem = Point(text, xpos)
                else:
                    if len(line) == 3:
                        text, xmin, xmax = line
                        elem = Interval(text, xmin, xmax)
                    else:
                        raise ValueError
                    if not tier:
                        if isinstance(elem, Point):
                            tier = Tier(point_tier=True)
                        else:
                            tier = Tier()
                tier.append(elem)

        self[tier_name] = tier

    def tier_to_csv(self, tier_name, filename):
        """Export given tier into a CSV file.

        "tier_name" is the name of the (existing) tier to be exported.
        "filename" is the name of the file.
        """
        with open(filename, 'w') as (csvfile):
            csvfile.write('\n'.join(self[tier_name].to_csv()))

    def write(self, filename, fmt=TEXT_LONG):
        """Write the text grid into a Praat TextGrid file.

        Obligatory argument "filename" gives the file name.
        Optional argument "formatting" can be TEXT_LONG, TEXT_SHORT, or
        BINARY (see "TextGrid.format()"). Default is TEXT_LONG.
        """
        with open(filename, 'w' if fmt != BINARY else 'wb') as (outfile):
            outfile.write(self.format(fmt))