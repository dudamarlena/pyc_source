# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/pdfdevice.py
# Compiled at: 2015-10-31 16:12:15
from .pdffont import PDFUnicodeNotDefined
from . import utils

class PDFDevice(object):

    def __init__(self, rsrcmgr):
        self.rsrcmgr = rsrcmgr
        self.ctm = None
        return

    def __repr__(self):
        return '<PDFDevice>'

    def close(self):
        pass

    def set_ctm(self, ctm):
        self.ctm = ctm

    def begin_tag(self, tag, props=None):
        pass

    def end_tag(self):
        pass

    def do_tag(self, tag, props=None):
        pass

    def begin_page(self, page, ctm):
        pass

    def end_page(self, page):
        pass

    def begin_figure(self, name, bbox, matrix):
        pass

    def end_figure(self, name):
        pass

    def paint_path(self, graphicstate, stroke, fill, evenodd, path):
        pass

    def render_image(self, name, stream):
        pass

    def render_string(self, textstate, seq):
        pass


class PDFTextDevice(PDFDevice):

    def render_string(self, textstate, seq):
        matrix = utils.mult_matrix(textstate.matrix, self.ctm)
        font = textstate.font
        fontsize = textstate.fontsize
        scaling = textstate.scaling * 0.01
        charspace = textstate.charspace * scaling
        wordspace = textstate.wordspace * scaling
        rise = textstate.rise
        if font.is_multibyte():
            wordspace = 0
        dxscale = 0.001 * fontsize * scaling
        if font.is_vertical():
            textstate.linematrix = self.render_string_vertical(seq, matrix, textstate.linematrix, font, fontsize, scaling, charspace, wordspace, rise, dxscale)
        else:
            textstate.linematrix = self.render_string_horizontal(seq, matrix, textstate.linematrix, font, fontsize, scaling, charspace, wordspace, rise, dxscale)

    def render_string_horizontal(self, seq, matrix, pos, font, fontsize, scaling, charspace, wordspace, rise, dxscale):
        x, y = pos
        needcharspace = False
        for obj in seq:
            if utils.isnumber(obj):
                x -= obj * dxscale
                needcharspace = True
            else:
                for cid in font.decode(obj):
                    if needcharspace:
                        x += charspace
                    x += self.render_char(utils.translate_matrix(matrix, (x, y)), font, fontsize, scaling, rise, cid)
                    if cid == 32 and wordspace:
                        x += wordspace
                    needcharspace = True

        return (
         x, y)

    def render_string_vertical(self, seq, matrix, pos, font, fontsize, scaling, charspace, wordspace, rise, dxscale):
        x, y = pos
        needcharspace = False
        for obj in seq:
            if utils.isnumber(obj):
                y -= obj * dxscale
                needcharspace = True
            else:
                for cid in font.decode(obj):
                    if needcharspace:
                        y += charspace
                    y += self.render_char(utils.translate_matrix(matrix, (x, y)), font, fontsize, scaling, rise, cid)
                    if cid == 32 and wordspace:
                        y += wordspace
                    needcharspace = True

        return (
         x, y)

    def render_char(self, matrix, font, fontsize, scaling, rise, cid):
        return 0


class TagExtractor(PDFDevice):

    def __init__(self, rsrcmgr, outfp, codec='utf-8'):
        PDFDevice.__init__(self, rsrcmgr)
        self.outfp = outfp
        self.codec = codec
        self.pageno = 0
        self._stack = []

    def render_string(self, textstate, seq):
        font = textstate.font
        text = ''
        for obj in seq:
            obj = utils.make_compat_str(obj)
            if not isinstance(obj, str):
                continue
            chars = font.decode(obj)
            for cid in chars:
                try:
                    char = font.to_unichr(cid)
                    text += char
                except PDFUnicodeNotDefined:
                    print chars

        self.outfp.write(utils.enc(text, self.codec))

    def begin_page(self, page, ctm):
        output = '<page id="%s" bbox="%s" rotate="%d">' % (self.pageno, utils.bbox2str(page.mediabox), page.rotate)
        self.outfp.write(utils.make_compat_bytes(output))

    def end_page(self, page):
        self.outfp.write(utils.make_compat_bytes('</page>\n'))
        self.pageno += 1

    def begin_tag(self, tag, props=None):
        s = ''
        if isinstance(props, dict):
            s = ('').join(' %s="%s"' % (utils.enc(k), utils.enc(str(v))) for k, v in sorted(props.iteritems()))
        out_s = '<%s%s>' % (utils.enc(tag.name), s)
        self.outfp.write(utils.make_compat_bytes(out_s))
        self._stack.append(tag)

    def end_tag(self):
        assert self._stack
        tag = self._stack.pop(-1)
        out_s = '</%s>' % utils.enc(tag.name)
        self.outfp.write(utils.make_compat_bytes(out_s))

    def do_tag(self, tag, props=None):
        self.begin_tag(tag, props)
        self._stack.pop(-1)