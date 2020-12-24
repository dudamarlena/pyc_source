# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sixel/converter.py
# Compiled at: 2015-03-24 11:11:16
import sys
if sys.version_info[0] == 3:
    xrange = range
del sys

class SixelConverter:

    def __init__(self, file, f8bit=False, w=None, h=None, ncolor=256, alphathreshold=0, chromakey=False, fast=True):
        self.__alphathreshold = alphathreshold
        self.__chromakey = chromakey
        self._slots = [0] * 257
        self._fast = fast
        if ncolor >= 256:
            ncolor = 256
        self._ncolor = ncolor
        if f8bit:
            self.DCS = b'\x90'
            self.ST = b'\x9c'
        else:
            self.DCS = '\x1bP'
            self.ST = '\x1b\\'
        try:
            from PIL import Image
        except ImportError:
            import imageloader as Image

        image = Image.open(file)
        image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=ncolor)
        if w or h:
            (width, height) = image.size
            if not w:
                w = width
            if not h:
                h = height
            image = image.resize((w, h))
        self.palette = image.getpalette()
        self.data = image.getdata()
        (self.width, self.height) = image.size
        if alphathreshold > 0:
            self.rawdata = Image.open(file).convert('RGBA').getdata()

    def __write_header(self, output):
        output.write(self.DCS)
        aspect_ratio = 7
        if self.__chromakey:
            background_option = 2
        else:
            background_option = 1
        dpi = 75
        template = '%d;%d;%dq"1;1;%d;%d'
        args = (aspect_ratio, background_option, dpi, self.width, self.height)
        output.write(template % args)

    def __write_palette_section(self, output):
        palette = self.palette
        for i in xrange(0, self._ncolor * 3, 3):
            no = i / 3
            r = palette[(i + 0)] * 100 / 256
            g = palette[(i + 1)] * 100 / 256
            b = palette[(i + 2)] * 100 / 256
            output.write('#%d;2;%d;%d;%d' % (no, r, g, b))

    def __write_body_without_alphathreshold(self, output, data, keycolor):
        for n in xrange(0, self._ncolor):
            palette = self.palette
            r = palette[(n * 3 + 0)] * 100 / 256
            g = palette[(n * 3 + 1)] * 100 / 256
            b = palette[(n * 3 + 2)] * 100 / 256
            output.write('#%d;2;%d;%d;%d\n' % (n, r, g, b))

        height = self.height
        width = self.width
        for y in xrange(0, height, 6):
            if height - y <= 5:
                band = height - y
            else:
                band = 6
            buf = []
            set_ = set()

            def add_node(n, s):
                node = []
                cache = 0
                count = 0
                if s:
                    node.append((0, s))
                for x in xrange(s, width):
                    count += 1
                    p = y * width + x
                    six = 0
                    for i in xrange(0, band):
                        d = data[(p + width * i)]
                        if d == n:
                            six |= 1 << i
                        elif d not in set_:
                            set_.add(d)
                            add_node(d, x)

                    if six != cache:
                        node.append([cache, count])
                        count = 0
                        cache = six

                if cache != 0:
                    node.append([cache, count])
                buf.append((n, node))

            add_node(data[(y * width)], 0)
            for (n, node) in buf:
                output.write('#%d\n' % n)
                for (six, count) in node:
                    if count < 4:
                        output.write(chr(63 + six) * count)
                    else:
                        output.write('!%d%c' % (count, 63 + six))

                output.write('$\n')

            output.write('-\n')

    def __write_body_without_alphathreshold_fast(self, output, data, keycolor):
        height = self.height
        width = self.width
        n = 1
        for y in xrange(0, height):
            p = y * width
            cached_no = data[p]
            count = 1
            c = -1
            for x in xrange(0, width):
                color_no = data[(p + x)]
                if color_no == cached_no:
                    count += 1
                else:
                    if cached_no == keycolor:
                        c = 63
                    else:
                        c = 63 + n
                        if self._slots[cached_no] == 0:
                            palette = self.palette
                            r = palette[(cached_no * 3 + 0)] * 100 / 256
                            g = palette[(cached_no * 3 + 1)] * 100 / 256
                            b = palette[(cached_no * 3 + 2)] * 100 / 256
                            self._slots[cached_no] = 1
                            output.write('#%d;2;%d;%d;%d' % (cached_no, r, g, b))
                        output.write('#%d' % cached_no)
                    if count < 3:
                        output.write(chr(c) * count)
                    else:
                        output.write('!%d%c' % (count, c))
                    count = 1
                    cached_no = color_no

            if c != -1 and count > 1:
                if cached_no == keycolor:
                    c = 63
                else:
                    if self._slots[cached_no] == 0:
                        palette = self.palette
                        r = palette[(cached_no * 3 + 0)] * 100 / 256
                        g = palette[(cached_no * 3 + 1)] * 100 / 256
                        b = palette[(cached_no * 3 + 2)] * 100 / 256
                        self._slots[cached_no] = 1
                        output.write('#%d;2;%d;%d;%d' % (cached_no, r, g, b))
                    output.write('#%d' % cached_no)
                if count < 3:
                    output.write(chr(c) * count)
                else:
                    output.write('!%d%c' % (count, c))
            if n == 32:
                n = 1
                output.write('-')
            else:
                n <<= 1
                output.write('$')

    def __write_body_with_alphathreshold(self, output, data, keycolor):
        rawdata = self.rawdata
        height = self.height
        width = self.width
        max_runlength = 255
        n = 1
        for y in xrange(0, height):
            p = y * width
            cached_no = data[p]
            cached_alpha = rawdata[p][3]
            count = 1
            c = -1
            for x in xrange(0, width):
                color_no = data[(p + x)]
                alpha = rawdata[(p + x)][3]
                if color_no == cached_no:
                    if alpha == cached_alpha:
                        if count < max_runlength:
                            count += 1
                            continue
                if cached_no == keycolor:
                    c = 63
                elif cached_alpha < self.__alphathreshold:
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
                cached_alpha = alpha

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

    def __write_body_section(self, output):
        data = self.data
        if self.__chromakey:
            keycolor = data[0]
        else:
            keycolor = -1
        if self.__alphathreshold == 0:
            if self._fast:
                self.__write_body_without_alphathreshold_fast(output, data, keycolor)
            else:
                self.__write_body_without_alphathreshold(output, data, keycolor)
        else:
            self.__write_body_with_alphathreshold(output, data, keycolor)

    def __write_terminator(self, output):
        output.write(self.ST)

    def getvalue(self):
        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO

        output = StringIO()
        try:
            self.write(output)
            value = output.getvalue()
        finally:
            output.close()

        return value

    def write(self, output, bodyonly=False):
        if not bodyonly:
            self.__write_header(output)
        self.__write_body_section(output)
        if not bodyonly:
            self.__write_terminator(output)