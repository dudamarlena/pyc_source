# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/utils.py
# Compiled at: 2015-10-31 16:12:15
"""
Miscellaneous Routines.
"""
import struct
INF = 2147483647
import six
if six.PY3:
    import chardet
    unicode = str

def make_compat_bytes(in_str):
    """In Py2, does nothing. In Py3, converts to bytes, encoding to unicode."""
    assert isinstance(in_str, str)
    if six.PY2:
        return in_str
    else:
        return in_str.encode()


def make_compat_str(in_str):
    """In Py2, does nothing. In Py3, converts to string, guessing encoding."""
    assert isinstance(in_str, (bytes, str, unicode))
    if six.PY3 and isinstance(in_str, bytes):
        enc = chardet.detect(in_str)
        in_str = in_str.decode(enc['encoding'])
    return in_str


def compatible_encode_method(bytesorstring, encoding='utf-8', erraction='ignore'):
    """When Py2 str.encode is called, it often means bytes.encode in Py3. This does either."""
    if six.PY2:
        assert isinstance(bytesorstring, (str, unicode)), ('Error: Assumed was calling encode() on a string in Py2: {}').format(type(bytesorstring))
        return bytesorstring.encode(encoding, erraction)
    if six.PY3:
        if isinstance(bytesorstring, str):
            return bytesorstring
        assert isinstance(bytesorstring, bytes), ('Error: Assumed was calling encode() on a bytes in Py3: {}').format(type(bytesorstring))
        return bytesorstring.decode(encoding, erraction)


def apply_png_predictor(pred, colors, columns, bitspercomponent, data):
    if bitspercomponent != 8:
        raise ValueError(bitspercomponent)
    nbytes = colors * columns * bitspercomponent // 8
    i = 0
    buf = ''
    line0 = '\x00' * columns
    for i in range(0, len(data), nbytes + 1):
        ft = data[i]
        if six.PY2:
            ft = six.byte2int(ft)
        i += 1
        line1 = data[i:i + nbytes]
        line2 = ''
        if ft == 0:
            line2 += line1
        elif ft == 1:
            c = 0
            for b in line1:
                if six.PY2:
                    b = six.byte2int(b)
                c = c + b & 255
                line2 += six.int2byte(c)

        elif ft == 2:
            for a, b in zip(line0, line1):
                if six.PY2:
                    a, b = six.byte2int(a), six.byte2int(b)
                c = a + b & 255
                line2 += six.int2byte(c)

        elif ft == 3:
            c = 0
            for a, b in zip(line0, line1):
                if six.PY2:
                    a, b = six.byte2int(a), six.byte2int(b)
                c = (c + a + b) // 2 & 255
                line2 += six.int2byte(c)

        else:
            raise ValueError(ft)
        buf += line2
        line0 = line2

    return buf


MATRIX_IDENTITY = (1, 0, 0, 1, 0, 0)

def mult_matrix(m1, m0):
    a1, b1, c1, d1, e1, f1 = m1
    a0, b0, c0, d0, e0, f0 = m0
    return (
     a0 * a1 + c0 * b1, b0 * a1 + d0 * b1,
     a0 * c1 + c0 * d1, b0 * c1 + d0 * d1,
     a0 * e1 + c0 * f1 + e0, b0 * e1 + d0 * f1 + f0)


def translate_matrix(m, v):
    """Translates a matrix by (x, y)."""
    a, b, c, d, e, f = m
    x, y = v
    return (a, b, c, d, x * a + y * c + e, x * b + y * d + f)


def apply_matrix_pt(m, v):
    a, b, c, d, e, f = m
    x, y = v
    return (
     a * x + c * y + e, b * x + d * y + f)


def apply_matrix_norm(m, v):
    """Equivalent to apply_matrix_pt(M, (p,q)) - apply_matrix_pt(M, (0,0))"""
    a, b, c, d, e, f = m
    p, q = v
    return (a * p + c * q, b * p + d * q)


def isnumber(x):
    return isinstance(x, (six.integer_types, float))


def uniq(objs):
    """Eliminates duplicated elements."""
    done = set()
    for obj in objs:
        if obj in done:
            continue
        done.add(obj)
        yield obj


def csort(objs, key):
    """Order-preserving sorting function."""
    idxs = dict((obj, i) for i, obj in enumerate(objs))
    return sorted(objs, key=lambda obj: (key(obj), idxs[obj]))


def fsplit(pred, objs):
    """Split a list into two classes according to the predicate."""
    t = []
    f = []
    for obj in objs:
        if pred(obj):
            t.append(obj)
        else:
            f.append(obj)

    return (
     t, f)


def drange(v0, v1, d):
    """Returns a discrete range."""
    assert v0 < v1
    return range(int(v0) // d, int(v1 + d) // d)


def get_bound(pts):
    """Compute a minimal rectangle that covers all the points."""
    x0, y0, x1, y1 = (
     INF, INF, -INF, -INF)
    for x, y in pts:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)

    return (
     x0, y0, x1, y1)


def pick(seq, func, maxobj=None):
    """Picks the object obj where func(obj) has the highest value."""
    maxscore = None
    for obj in seq:
        score = func(obj)
        if maxscore is None or maxscore < score:
            maxscore, maxobj = score, obj

    return maxobj


def choplist(n, seq):
    """Groups every n elements of the list."""
    r = []
    for x in seq:
        r.append(x)
        if len(r) == n:
            yield tuple(r)
            r = []


def nunpack(s, default=0):
    """Unpacks 1 to 4 byte integers (big endian)."""
    l = len(s)
    if not l:
        return default
    if l == 1:
        return ord(s)
    if l == 2:
        return struct.unpack('>H', s)[0]
    if l == 3:
        return struct.unpack('>L', '\x00' + s)[0]
    if l == 4:
        return struct.unpack('>L', s)[0]
    raise TypeError('invalid length: %d' % l)


PDFDocEncoding = ('').join(six.unichr(x) for x in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                   11, 12, 13, 14, 15, 16, 17, 18,
                                                   19, 20, 21, 23, 23, 728, 711,
                                                   710, 729, 733, 731, 730, 732,
                                                   32, 33, 34, 35, 36, 37, 38, 39,
                                                   40, 41, 42, 43, 44, 45, 46, 47,
                                                   48, 49, 50, 51, 52, 53, 54, 55,
                                                   56, 57, 58, 59, 60, 61, 62, 63,
                                                   64, 65, 66, 67, 68, 69, 70, 71,
                                                   72, 73, 74, 75, 76, 77, 78, 79,
                                                   80, 81, 82, 83, 84, 85, 86, 87,
                                                   88, 89, 90, 91, 92, 93, 94, 95,
                                                   96, 97, 98, 99, 100, 101, 102,
                                                   103, 104, 105, 106, 107, 108,
                                                   109, 110, 111, 112, 113, 114,
                                                   115, 116, 117, 118, 119, 120,
                                                   121, 122, 123, 124, 125, 126,
                                                   0, 8226, 8224, 8225, 8230, 8212,
                                                   8211, 402, 8260, 8249, 8250, 8722,
                                                   8240, 8222, 8220, 8221, 8216,
                                                   8217, 8218, 8482, 64257, 64258,
                                                   321, 338, 352, 376, 381, 305,
                                                   322, 339, 353, 382, 0, 8364, 161,
                                                   162, 163, 164, 165, 166, 167,
                                                   168, 169, 170, 171, 172, 0, 174,
                                                   175, 176, 177, 178, 179, 180,
                                                   181, 182, 183, 184, 185, 186,
                                                   187, 188, 189, 190, 191, 192,
                                                   193, 194, 195, 196, 197, 198,
                                                   199, 200, 201, 202, 203, 204,
                                                   205, 206, 207, 208, 209, 210,
                                                   211, 212, 213, 214, 215, 216,
                                                   217, 218, 219, 220, 221, 222,
                                                   223, 224, 225, 226, 227, 228,
                                                   229, 230, 231, 232, 233, 234,
                                                   235, 236, 237, 238, 239, 240,
                                                   241, 242, 243, 244, 245, 246,
                                                   247, 248, 249, 250, 251, 252,
                                                   253, 254, 255))

def decode_text(s):
    """Decodes a PDFDocEncoding string to Unicode."""
    if s.startswith(b'\xfe\xff'):
        return six.text_type(s[2:], 'utf-16be', 'ignore')
    else:
        return ('').join(PDFDocEncoding[ord(c)] for c in s)


def enc(x, codec='ascii'):
    """Encodes a string for SGML/XML/HTML"""
    x = x.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace('"', '&quot;')
    if codec:
        x = x.encode(codec, 'xmlcharrefreplace')
    return x


def bbox2str(bbox):
    x0, y0, x1, y1 = bbox
    return '%.3f,%.3f,%.3f,%.3f' % (x0, y0, x1, y1)


def matrix2str(m):
    a, b, c, d, e, f = m
    return '[%.2f,%.2f,%.2f,%.2f, (%.2f,%.2f)]' % (a, b, c, d, e, f)


class Plane(object):

    def __init__(self, bbox, gridsize=50):
        self._seq = []
        self._objs = set()
        self._grid = {}
        self.gridsize = gridsize
        self.x0, self.y0, self.x1, self.y1 = bbox

    def __repr__(self):
        return '<Plane objs=%r>' % list(self)

    def __iter__(self):
        return (obj for obj in self._seq if obj in self._objs)

    def __len__(self):
        return len(self._objs)

    def __contains__(self, obj):
        return obj in self._objs

    def _getrange(self, bbox):
        x0, y0, x1, y1 = bbox
        if x1 <= self.x0 or self.x1 <= x0 or y1 <= self.y0 or self.y1 <= y0:
            return
        x0 = max(self.x0, x0)
        y0 = max(self.y0, y0)
        x1 = min(self.x1, x1)
        y1 = min(self.y1, y1)
        for y in drange(y0, y1, self.gridsize):
            for x in drange(x0, x1, self.gridsize):
                yield (
                 x, y)

    def extend(self, objs):
        for obj in objs:
            self.add(obj)

    def add(self, obj):
        for k in self._getrange((obj.x0, obj.y0, obj.x1, obj.y1)):
            if k not in self._grid:
                r = []
                self._grid[k] = r
            else:
                r = self._grid[k]
            r.append(obj)

        self._seq.append(obj)
        self._objs.add(obj)

    def remove(self, obj):
        for k in self._getrange((obj.x0, obj.y0, obj.x1, obj.y1)):
            try:
                self._grid[k].remove(obj)
            except (KeyError, ValueError):
                pass

        self._objs.remove(obj)

    def find(self, bbox):
        x0, y0, x1, y1 = bbox
        done = set()
        for k in self._getrange(bbox):
            if k not in self._grid:
                continue
            for obj in self._grid[k]:
                if obj in done:
                    continue
                done.add(obj)
                if obj.x1 <= x0 or x1 <= obj.x0 or obj.y1 <= y0 or y1 <= obj.y0:
                    continue
                yield obj