# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PdfImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.4'
import Image, ImageFile, StringIO

def _obj(fp, obj, **dict):
    fp.write('%d 0 obj\n' % obj)
    if dict:
        fp.write('<<\n')
        for (k, v) in dict.items():
            if v is not None:
                fp.write('/%s %s\n' % (k, v))

        fp.write('>>\n')
    return


def _endobj(fp):
    fp.write('endobj\n')


def _save(im, fp, filename):
    im.load()
    xref = [
     0] * 6
    fp.write('%PDF-1.2\n')
    fp.write('% created by PIL PDF driver ' + __version__ + '\n')
    (width, height) = im.size
    bits = 8
    params = None
    if im.mode == '1':
        filter = '/ASCIIHexDecode'
        colorspace = '/DeviceGray'
        procset = '/ImageB'
        bits = 1
    elif im.mode == 'L':
        filter = '/DCTDecode'
        colorspace = '/DeviceGray'
        procset = '/ImageB'
    elif im.mode == 'P':
        filter = '/ASCIIHexDecode'
        colorspace = '[ /Indexed /DeviceRGB 255 <'
        palette = im.im.getpalette('RGB')
        for i in range(256):
            r = ord(palette[(i * 3)])
            g = ord(palette[(i * 3 + 1)])
            b = ord(palette[(i * 3 + 2)])
            colorspace = colorspace + '%02x%02x%02x ' % (r, g, b)

        colorspace = colorspace + '> ]'
        procset = '/ImageI'
    elif im.mode == 'RGB':
        filter = '/DCTDecode'
        colorspace = '/DeviceRGB'
        procset = '/ImageC'
    elif im.mode == 'CMYK':
        filter = '/DCTDecode'
        colorspace = '/DeviceCMYK'
        procset = '/ImageC'
    else:
        raise ValueError('cannot save mode %s' % im.mode)
    xref[1] = fp.tell()
    _obj(fp, 1, Type='/Catalog', Pages='2 0 R')
    _endobj(fp)
    xref[2] = fp.tell()
    _obj(fp, 2, Type='/Pages', Count=1, Kids='[4 0 R]')
    _endobj(fp)
    op = StringIO.StringIO()
    if filter == '/ASCIIHexDecode':
        if bits == 1:
            data = im.tostring('raw', '1')
            im = Image.new('L', (len(data), 1), None)
            im.putdata(data)
        ImageFile._save(im, op, [('hex', (0, 0) + im.size, 0, im.mode)])
    elif filter == '/DCTDecode':
        ImageFile._save(im, op, [('jpeg', (0, 0) + im.size, 0, im.mode)])
    elif filter == '/FlateDecode':
        ImageFile._save(im, op, [('zip', (0, 0) + im.size, 0, im.mode)])
    elif filter == '/RunLengthDecode':
        ImageFile._save(im, op, [('packbits', (0, 0) + im.size, 0, im.mode)])
    else:
        raise ValueError('unsupported PDF filter (%s)' % filter)
    xref[3] = fp.tell()
    _obj(fp, 3, Type='/XObject', Subtype='/Image', Width=width, Height=height, Length=len(op.getvalue()), Filter=filter, BitsPerComponent=bits, DecodeParams=params, ColorSpace=colorspace)
    fp.write('stream\n')
    fp.write(op.getvalue())
    fp.write('\nendstream\n')
    _endobj(fp)
    xref[4] = fp.tell()
    _obj(fp, 4)
    fp.write('<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/ProcSet [ /PDF %s ]\n/XObject << /image 3 0 R >>\n>>\n/MediaBox [ 0 0 %d %d ]\n/Contents 5 0 R\n>>\n' % (
     procset, width, height))
    _endobj(fp)
    op = StringIO.StringIO()
    op.write('q %d 0 0 %d 0 0 cm /image Do Q\n' % (width, height))
    xref[5] = fp.tell()
    _obj(fp, 5, Length=len(op.getvalue()))
    fp.write('stream\n')
    fp.write(op.getvalue())
    fp.write('\nendstream\n')
    _endobj(fp)
    startxref = fp.tell()
    fp.write('xref\n0 %d\n0000000000 65535 f \n' % len(xref))
    for x in xref[1:]:
        fp.write('%010d 00000 n \n' % x)

    fp.write('trailer\n<<\n/Size %d\n/Root 1 0 R\n>>\n' % len(xref))
    fp.write('startxref\n%d\n%%%%EOF\n' % startxref)
    fp.flush()
    return


Image.register_save('PDF', _save)
Image.register_extension('PDF', '.pdf')
Image.register_mime('PDF', 'application/pdf')