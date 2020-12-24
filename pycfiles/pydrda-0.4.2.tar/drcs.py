# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/drcs/drcs.py
# Compiled at: 2014-02-04 06:56:05
import sys, os

class DrcsConverter:

    def __init__(self, image, f8bit, columns, rows=None, negate=False, use_unicode=False, ncolor=1):
        if f8bit:
            self.DCS = b'\x90'
            self.ST = b'\x9c'
        else:
            self.DCS = '\x1bP'
            self.ST = '\x1b\\'
        self.cellwidth = 15
        self.cellheight = 24
        self.columns = columns
        (width, height) = image.size
        if rows is None:
            display_width = columns * self.cellwidth
            display_height = 1.0 * display_width * height / width
            rows = int(display_height / self.cellheight)
        self.rows = rows
        self.negate = negate
        self._use_unicode = use_unicode
        width = self.cellwidth * self.columns
        height = self.cellheight * rows
        image = image.resize((width, height))
        if ncolor > 256:
            ncolor = 256
        self._ncolor = ncolor
        if ncolor == 1:
            image = image.convert('L')
            image = image.convert('1')
            self.palette = None
        else:
            from PIL import Image
            image = image.convert('P', palette=Image.ADAPTIVE, colors=ncolor)
            self.palette = image.getpalette()
        self.data = image.getdata()
        return

    def __write_header(self, output, fbyte):
        output.write(self.DCS)
        cellwidth = self.cellwidth
        cellheight = self.cellheight
        if self._ncolor > 1:
            pt = 3
        else:
            pt = 1
        output.write('1;0;0;%d;1;%d;%d;0{ %c' % (cellwidth, pt, cellheight, fbyte))

    def _write_sixel_palette(self, output):
        palette = self.palette
        for i in xrange(0, self._ncolor * 3, 3):
            no = i / 3
            r = palette[(i + 0)] * 100 / 256
            g = palette[(i + 1)] * 100 / 256
            b = palette[(i + 2)] * 100 / 256
            output.write('#%d;2;%d;%d;%d' % (no, r, g, b))

    def _write_colored_sixel(self, output, data, width, top, keycolor):
        n = 1
        for y in xrange(top, top + 6):
            p = y * width
            cached_no = data[p]
            count = 1
            c = -1
            for x in xrange(0, width):
                color_no = data[(p + x)]
                if color_no == cached_no and count < 255:
                    count += 1
                else:
                    if cached_no == keycolor:
                        c = 63
                    else:
                        c = n + 63
                    if count == 1:
                        output.write('#%d%c' % (cached_no, c))
                    elif count == 2:
                        output.write('#%d%c%c' % (cached_no, c, c))
                        count = 1
                    else:
                        output.write('#%d!%d%c' % (cached_no, count, c))
                        count = 1
                    cached_no = color_no

            if c != -1:
                if cached_no == keycolor:
                    c = 63
                if count == 1:
                    output.write('#%d%c' % (cached_no, c))
                elif count == 2:
                    output.write('#%d%c%c' % (cached_no, c, c))
                else:
                    output.write('#%d!%d%c' % (cached_no, count, c))
            output.write('$')
            if n == 32:
                n = 1
                output.write('-')
            else:
                n <<= 1

    def __write_body_section(self, output, n):
        data = self.data
        cellheight = self.cellheight
        cellwidth = self.cellwidth
        width = self.cellwidth * self.columns
        if self.palette:
            for y in xrange(cellheight * n, cellheight * (n + 1), 6):
                self._write_colored_sixel(output, data, width, y, -1)

        else:
            startpos = width * cellheight * n
            positive = 255 if self.negate else 0
            for c in xrange(0, self.columns):
                startx = cellwidth * c
                for y in xrange(0, cellheight, 6):
                    if y != 0:
                        output.write('/')
                    for x in range(0, cellwidth):
                        acc = 0
                        for i in xrange(0, 6):
                            acc = acc * 2
                            index = (y + 5 - i) * width + startx + x
                            if data[(startpos + index)] == positive:
                                acc += 1

                        output.write(chr(acc + 63))

                output.write(';')

    def __write_terminator(self, output):
        output.write(self.ST)

    def write(self, output, defonly, startoffset):
        if self._use_unicode:
            import codecs
            output = codecs.getwriter('utf-8')(output)
        for n in xrange(0, self.rows):
            self.__write_header(output, 64 + n + startoffset)
            if self._ncolor > 1:
                self._write_sixel_palette(output)
            self.__write_body_section(output, n)
            self.__write_terminator(output)

        if not defonly:
            if self._use_unicode:
                for dscs in xrange(startoffset, self.rows + startoffset):
                    for c in xrange(0, self.columns):
                        code = 1048576 | 64 + dscs << 8 | 33 + c
                        code -= 65536
                        c1 = (code >> 10) + 55296
                        c2 = (code & 1023) + 56320
                        output.write(unichr(c1) + unichr(c2))

                    output.write('\n')

            else:
                for dscs in xrange(0, self.rows):
                    output.write('\x1b( %c' % (64 + dscs + startoffset))
                    for c in xrange(0, self.columns):
                        output.write(chr(33 + c))

                    output.write('\x1b(B\n')


class DrcsWriter:

    def __init__(self, f8bit=False):
        self.f8bit = f8bit

    def draw(self, image, columns=62, rows=None, negate=False, use_unicode=False, output=sys.stdout, ncolor=1, defonly=False, startoffset=0):
        drcs_converter = DrcsConverter(image, self.f8bit, columns, rows, negate, use_unicode, ncolor=ncolor)
        drcs_converter.write(output, defonly=defonly, startoffset=startoffset)