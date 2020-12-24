# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/BdfFontFile.py
# Compiled at: 2007-09-25 20:00:35
import Image, FontFile, string
bdf_slant = {'R': 'Roman', 
   'I': 'Italic', 
   'O': 'Oblique', 
   'RI': 'Reverse Italic', 
   'RO': 'Reverse Oblique', 
   'OT': 'Other'}
bdf_spacing = {'P': 'Proportional', 
   'M': 'Monospaced', 
   'C': 'Cell'}

def bdf_char(f):
    while 1:
        s = f.readline()
        if not s:
            return
        elif s[:9] == 'STARTCHAR':
            break

    id = string.strip(s[9:])
    props = {}
    while 1:
        s = f.readline()
        if not s or s[:6] == 'BITMAP':
            break
        i = string.find(s, ' ')
        props[s[:i]] = s[i + 1:-1]

    bitmap = []
    while 1:
        s = f.readline()
        if not s or s[:7] == 'ENDCHAR':
            break
        bitmap.append(s[:-1])

    bitmap = string.join(bitmap, '')
    (x, y, l, d) = map(int, string.split(props['BBX']))
    (dx, dy) = map(int, string.split(props['DWIDTH']))
    bbox = (
     (
      dx, dy), (l, -d - y, x + l, -d), (0, 0, x, y))
    try:
        im = Image.fromstring('1', (x, y), bitmap, 'hex', '1')
    except ValueError:
        im = Image.new('1', (x, y))

    return (id, int(props['ENCODING']), bbox, im)


class BdfFontFile(FontFile.FontFile):

    def __init__(self, fp):
        FontFile.FontFile.__init__(self)
        s = fp.readline()
        if s[:13] != 'STARTFONT 2.1':
            raise SyntaxError, 'not a valid BDF file'
        props = {}
        comments = []
        while 1:
            s = fp.readline()
            if not s or s[:13] == 'ENDPROPERTIES':
                break
            i = string.find(s, ' ')
            props[s[:i]] = s[i + 1:-1]
            if s[:i] in ('COMMENT', 'COPYRIGHT'):
                if string.find(s, 'LogicalFontDescription') < 0:
                    comments.append(s[i + 1:-1])

        font = string.split(props['FONT'], '-')
        font[4] = bdf_slant[string.upper(font[4])]
        font[11] = bdf_spacing[string.upper(font[11])]
        ascent = int(props['FONT_ASCENT'])
        descent = int(props['FONT_DESCENT'])
        fontname = string.join(font[1:], ';')
        font = []
        while 1:
            c = bdf_char(fp)
            if not c:
                break
            (id, ch, (xy, dst, src), im) = c
            if ch >= 0 and ch < len(self.glyph):
                self.glyph[ch] = (
                 xy, dst, src, im)