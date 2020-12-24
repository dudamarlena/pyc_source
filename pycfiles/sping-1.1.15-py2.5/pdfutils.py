# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sping\PDF\pdfutils.py
# Compiled at: 2002-01-21 21:51:42
import os, string, cStringIO
LINEEND = '\r\n'

def cacheImageFile(filename):
    """Processes the image as if for encoding, saves to a file ending in AHX"""
    from PIL import Image
    import zlib
    img1 = Image.open(filename)
    img = img1.convert('RGB')
    (imgwidth, imgheight) = img.size
    code = []
    code.append('BI')
    code.append('/W %s /H %s /BPC 8 /CS /RGB /F [/A85 /Fl]' % (imgwidth, imgheight))
    code.append('ID')
    raw = img.tostring()
    assert (len(raw) == imgwidth * imgheight, 'Wrong amount of data for image')
    compressed = zlib.compress(raw)
    encoded = _AsciiBase85Encode(compressed)
    outstream = cStringIO.StringIO(encoded)
    dataline = outstream.read(60)
    while dataline != '':
        code.append(dataline)
        dataline = outstream.read(60)

    code.append('EI')
    cachedname = os.path.splitext(filename)[0] + '.a85'
    f = open(cachedname, 'wb')
    f.write(string.join(code, LINEEND) + LINEEND)
    f.close()
    print 'cached image as %s' % cachedname


def preProcessImages(spec):
    r"""accepts either a filespec ('C:\mydir\*.jpg') or a list
    of image filenames, crunches them all to save time.  Run this
    to save huge amounts of time when repeatedly building image
    documents."""
    import types
    if type(spec) is types.StringType:
        filelist = glob.glob(spec)
    else:
        filelist = spec
    for filename in filelist:
        if cachedImageExists(filename):
            print 'cached version of %s already exists' % filename
        else:
            cacheImageFile(filename)


def cachedImageExists(filename):
    """Determines if a cached image exists which has
    the same name and equal or newer date to the given
    file."""
    cachedname = os.path.splitext(filename)[0] + '.a85'
    if os.path.isfile(cachedname):
        original_date = os.stat(filename)[8]
        cached_date = os.stat(cachedname)[8]
        if original_date > cached_date:
            return 0
        else:
            return 1
    else:
        return 0


def _escape(s):
    """PDF escapes are almost like Python ones, but brackets
    need slashes before them too. Use Python's repr function
    and chop off the quotes first"""
    s = repr(s)[1:-1]
    s = string.replace(s, '(', '\\(')
    s = string.replace(s, ')', '\\)')
    return s


def _normalizeLineEnds(text, desired=LINEEND):
    """ensures all instances of CR, LF and CRLF end up as the specified one"""
    unlikely = '\x00\x01\x02\x03'
    text = string.replace(text, '\r\n', unlikely)
    text = string.replace(text, '\r', unlikely)
    text = string.replace(text, '\n', unlikely)
    text = string.replace(text, unlikely, desired)
    return text


def _AsciiHexEncode(input):
    """This is a verbose encoding used for binary data within
    a PDF file.  One byte binary becomes two bytes of ASCII."""
    output = cStringIO.StringIO()
    for char in input:
        output.write('%02x' % ord(char))

    output.write('>')
    output.reset()
    return output.read()


def _AsciiHexDecode(input):
    """Not used except to provide a test of the preceding"""
    stripped = string.join(string.split(input), '')
    assert stripped[(-1)] == '>', 'Invalid terminator for Ascii Hex Stream'
    stripped = stripped[:-1]
    assert len(stripped) % 2 == 0, 'Ascii Hex stream has odd number of bytes'
    i = 0
    output = cStringIO.StringIO()
    while i < len(stripped):
        twobytes = stripped[i:i + 2]
        output.write(chr(eval('0x' + twobytes)))
        i = i + 2

    output.reset()
    return output.read()


def _AsciiHexTest(text='What is the average velocity of a sparrow?'):
    """Do the obvious test for whether Ascii Hex encoding works"""
    print 'Plain text:', text
    encoded = _AsciiHexEncode(text)
    print 'Encoded:', encoded
    decoded = _AsciiHexDecode(encoded)
    print 'Decoded:', decoded
    if decoded == text:
        print 'Passed'
    else:
        print 'Failed!'


def _AsciiBase85Encode(input):
    """This is a compact encoding used for binary data within
    a PDF file.  Four bytes of binary data become five bytes of
    ASCII.  This is the default method used for encoding images."""
    outstream = cStringIO.StringIO()
    (whole_word_count, remainder_size) = divmod(len(input), 4)
    cut = 4 * whole_word_count
    body, lastbit = input[0:cut], input[cut:]
    for i in range(whole_word_count):
        offset = i * 4
        b1 = ord(body[offset])
        b2 = ord(body[(offset + 1)])
        b3 = ord(body[(offset + 2)])
        b4 = ord(body[(offset + 3)])
        num = 16777216 * b1 + 65536 * b2 + 256 * b3 + b4
        if num == 0:
            outstream.write('z')
        else:
            (temp, c5) = divmod(num, 85)
            (temp, c4) = divmod(temp, 85)
            (temp, c3) = divmod(temp, 85)
            (c1, c2) = divmod(temp, 85)
            assert 52200625 * c1 + 614125 * c2 + 7225 * c3 + 85 * c4 + c5 == num, 'dodgy code!'
            outstream.write(chr(c1 + 33))
            outstream.write(chr(c2 + 33))
            outstream.write(chr(c3 + 33))
            outstream.write(chr(c4 + 33))
            outstream.write(chr(c5 + 33))

    if remainder_size > 0:
        while len(lastbit) < 4:
            lastbit = lastbit + '\x00'

        b1 = ord(lastbit[0])
        b2 = ord(lastbit[1])
        b3 = ord(lastbit[2])
        b4 = ord(lastbit[3])
        num = 16777216 * b1 + 65536 * b2 + 256 * b3 + b4
        (temp, c5) = divmod(num, 85)
        (temp, c4) = divmod(temp, 85)
        (temp, c3) = divmod(temp, 85)
        (c1, c2) = divmod(temp, 85)
        lastword = chr(c1 + 33) + chr(c2 + 33) + chr(c3 + 33) + chr(c4 + 33) + chr(c5 + 33)
        outstream.write(lastword[0:remainder_size + 1])
    outstream.write('~>')
    outstream.reset()
    return outstream.read()


def _AsciiBase85Decode(input):
    """This is not used - Acrobat Reader decodes for you - but a round
    trip is essential for testing."""
    outstream = cStringIO.StringIO()
    stripped = string.join(string.split(input), '')
    assert stripped[-2:] == '~>', 'Invalid terminator for Ascii Base 85 Stream'
    stripped = stripped[:-2]
    stripped = string.replace(stripped, 'z', '!!!!!')
    (whole_word_count, remainder_size) = divmod(len(stripped), 5)
    assert remainder_size != 1, 'invalid Ascii 85 stream!'
    cut = 5 * whole_word_count
    body, lastbit = stripped[0:cut], stripped[cut:]
    for i in range(whole_word_count):
        offset = i * 5
        c1 = ord(body[offset]) - 33
        c2 = ord(body[(offset + 1)]) - 33
        c3 = ord(body[(offset + 2)]) - 33
        c4 = ord(body[(offset + 3)]) - 33
        c5 = ord(body[(offset + 4)]) - 33
        num = 52200625 * c1 + 614125 * c2 + 7225 * c3 + 85 * c4 + c5
        (temp, b4) = divmod(num, 256)
        (temp, b3) = divmod(temp, 256)
        (b1, b2) = divmod(temp, 256)
        assert num == 16777216 * b1 + 65536 * b2 + 256 * b3 + b4, 'dodgy code!'
        outstream.write(chr(b1))
        outstream.write(chr(b2))
        outstream.write(chr(b3))
        outstream.write(chr(b4))

    if remainder_size > 0:
        while len(lastbit) < 5:
            lastbit = lastbit + '!'

        c1 = ord(lastbit[0]) - 33
        c2 = ord(lastbit[1]) - 33
        c3 = ord(lastbit[2]) - 33
        c4 = ord(lastbit[3]) - 33
        c5 = ord(lastbit[4]) - 33
        num = 52200625 * c1 + 614125 * c2 + 7225 * c3 + 85 * c4 + c5
        (temp, b4) = divmod(num, 256)
        (temp, b3) = divmod(temp, 256)
        (b1, b2) = divmod(temp, 256)
        assert num == 16777216 * b1 + 65536 * b2 + 256 * b3 + b4, 'dodgy code!'
        if remainder_size == 2:
            lastword = chr(b1 + 1)
        elif remainder_size == 3:
            lastword = chr(b1) + chr(b2 + 1)
        elif remainder_size == 4:
            lastword = chr(b1) + chr(b2) + chr(b3 + 1)
        outstream.write(lastword)
    outstream.reset()
    return outstream.read()


def _wrap(input, columns=60):
    output = []
    length = len(input)
    i = 0
    pos = columns * i
    while pos < length:
        output.append(input[pos:pos + columns])
        i = i + 1
        pos = columns * i

    return string.join(output, LINEEND)


def _AsciiBase85Test(text='What is the average velocity of a sparrow?'):
    """Do the obvious test for whether Base 85 encoding works"""
    print 'Plain text:', text
    encoded = _AsciiBase85Encode(text)
    print 'Encoded:', encoded
    decoded = _AsciiBase85Decode(encoded)
    print 'Decoded:', decoded
    if decoded == text:
        print 'Passed'
    else:
        print 'Failed!'