# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\formatting.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function
DEBUG = 0
import copy, re
from struct import unpack
from .timemachine import *
from .biffh import BaseObject, unpack_unicode, unpack_string, upkbits, upkbitsL, fprintf, FUN, FDT, FNU, FGE, FTX, XL_CELL_NUMBER, XL_CELL_DATE, XL_FORMAT, XL_FORMAT2, XLRDError
_cellty_from_fmtty = {FNU: XL_CELL_NUMBER, 
   FUN: XL_CELL_NUMBER, 
   FGE: XL_CELL_NUMBER, 
   FDT: XL_CELL_DATE, 
   FTX: XL_CELL_NUMBER}
excel_default_palette_b5 = (
 (
  0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
 (
  0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
 (
  128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
 (
  128, 0, 128), (0, 128, 128), (192, 192, 192), (128, 128, 128),
 (
  153, 153, 255), (153, 51, 102), (255, 255, 204), (204, 255, 255),
 (
  102, 0, 102), (255, 128, 128), (0, 102, 204), (204, 204, 255),
 (
  0, 0, 128), (255, 0, 255), (255, 255, 0), (0, 255, 255),
 (
  128, 0, 128), (128, 0, 0), (0, 128, 128), (0, 0, 255),
 (
  0, 204, 255), (204, 255, 255), (204, 255, 204), (255, 255, 153),
 (
  153, 204, 255), (255, 153, 204), (204, 153, 255), (227, 227, 227),
 (
  51, 102, 255), (51, 204, 204), (153, 204, 0), (255, 204, 0),
 (
  255, 153, 0), (255, 102, 0), (102, 102, 153), (150, 150, 150),
 (
  0, 51, 102), (51, 153, 102), (0, 51, 0), (51, 51, 0),
 (
  153, 51, 0), (153, 51, 102), (51, 51, 153), (51, 51, 51))
excel_default_palette_b2 = excel_default_palette_b5[:16]
excel_default_palette_b8 = (
 (
  0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
 (
  0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
 (
  128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
 (
  128, 0, 128), (0, 128, 128), (192, 192, 192), (128, 128, 128),
 (
  153, 153, 255), (153, 51, 102), (255, 255, 204), (204, 255, 255),
 (
  102, 0, 102), (255, 128, 128), (0, 102, 204), (204, 204, 255),
 (
  0, 0, 128), (255, 0, 255), (255, 255, 0), (0, 255, 255),
 (
  128, 0, 128), (128, 0, 0), (0, 128, 128), (0, 0, 255),
 (
  0, 204, 255), (204, 255, 255), (204, 255, 204), (255, 255, 153),
 (
  153, 204, 255), (255, 153, 204), (204, 153, 255), (255, 204, 153),
 (
  51, 102, 255), (51, 204, 204), (153, 204, 0), (255, 204, 0),
 (
  255, 153, 0), (255, 102, 0), (102, 102, 153), (150, 150, 150),
 (
  0, 51, 102), (51, 153, 102), (0, 51, 0), (51, 51, 0),
 (
  153, 51, 0), (153, 51, 102), (51, 51, 153), (51, 51, 51))
default_palette = {80: excel_default_palette_b8, 
   70: excel_default_palette_b5, 
   50: excel_default_palette_b5, 
   45: excel_default_palette_b2, 
   40: excel_default_palette_b2, 
   30: excel_default_palette_b2, 
   21: excel_default_palette_b2, 
   20: excel_default_palette_b2}
built_in_style_names = [
 'Normal',
 'RowLevel_',
 'ColLevel_',
 'Comma',
 'Currency',
 'Percent',
 'Comma [0]',
 'Currency [0]',
 'Hyperlink',
 'Followed Hyperlink']

def initialise_colour_map(book):
    book.colour_map = {}
    book.colour_indexes_used = {}
    if not book.formatting_info:
        return
    else:
        for i in xrange(8):
            book.colour_map[i] = excel_default_palette_b8[i]

        dpal = default_palette[book.biff_version]
        ndpal = len(dpal)
        for i in xrange(ndpal):
            book.colour_map[i + 8] = dpal[i]

        book.colour_map[ndpal + 8] = None
        book.colour_map[ndpal + 8 + 1] = None
        for ci in (81, 32767):
            book.colour_map[ci] = None

        return


def nearest_colour_index(colour_map, rgb, debug=0):
    best_metric = 196608
    best_colourx = 0
    for colourx, cand_rgb in colour_map.items():
        if cand_rgb is None:
            continue
        metric = 0
        for v1, v2 in zip(rgb, cand_rgb):
            metric += (v1 - v2) * (v1 - v2)

        if metric < best_metric:
            best_metric = metric
            best_colourx = colourx
            if metric == 0:
                break

    if 0 and debug:
        print('nearest_colour_index for %r is %r -> %r; best_metric is %d' % (
         rgb, best_colourx, colour_map[best_colourx], best_metric))
    return best_colourx


class EqNeAttrs(object):

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__


class Font(BaseObject, EqNeAttrs):
    bold = 0
    character_set = 0
    colour_index = 0
    escapement = 0
    family = 0
    font_index = 0
    height = 0
    italic = 0
    name = UNICODE_LITERAL('')
    struck_out = 0
    underline_type = 0
    underlined = 0
    weight = 400
    outline = 0
    shadow = 0


def handle_efont(book, data):
    if not book.formatting_info:
        return
    book.font_list[(-1)].colour_index = unpack('<H', data)[0]


def handle_font(book, data):
    if not book.formatting_info:
        return
    if not book.encoding:
        book.derive_encoding()
    blah = DEBUG or book.verbosity >= 2
    bv = book.biff_version
    k = len(book.font_list)
    if k == 4:
        f = Font()
        f.name = UNICODE_LITERAL('Dummy Font')
        f.font_index = k
        book.font_list.append(f)
        k += 1
    f = Font()
    f.font_index = k
    book.font_list.append(f)
    if bv >= 50:
        f.height, option_flags, f.colour_index, f.weight, f.escapement_type, f.underline_type, f.family, f.character_set = unpack('<HHHHHBBB', data[0:13])
        f.bold = option_flags & 1
        f.italic = (option_flags & 2) >> 1
        f.underlined = (option_flags & 4) >> 2
        f.struck_out = (option_flags & 8) >> 3
        f.outline = (option_flags & 16) >> 4
        f.shadow = (option_flags & 32) >> 5
        if bv >= 80:
            f.name = unpack_unicode(data, 14, lenlen=1)
        else:
            f.name = unpack_string(data, 14, book.encoding, lenlen=1)
    elif bv >= 30:
        f.height, option_flags, f.colour_index = unpack('<HHH', data[0:6])
        f.bold = option_flags & 1
        f.italic = (option_flags & 2) >> 1
        f.underlined = (option_flags & 4) >> 2
        f.struck_out = (option_flags & 8) >> 3
        f.outline = (option_flags & 16) >> 4
        f.shadow = (option_flags & 32) >> 5
        f.name = unpack_string(data, 6, book.encoding, lenlen=1)
        f.weight = [
         400, 700][f.bold]
        f.escapement_type = 0
        f.underline_type = f.underlined
        f.family = 0
        f.character_set = 1
    else:
        f.height, option_flags = unpack('<HH', data[0:4])
        f.colour_index = 32767
        f.bold = option_flags & 1
        f.italic = (option_flags & 2) >> 1
        f.underlined = (option_flags & 4) >> 2
        f.struck_out = (option_flags & 8) >> 3
        f.outline = 0
        f.shadow = 0
        f.name = unpack_string(data, 4, book.encoding, lenlen=1)
        f.weight = [
         400, 700][f.bold]
        f.escapement_type = 0
        f.underline_type = f.underlined
        f.family = 0
        f.character_set = 1
    if blah:
        f.dump(book.logfile, header='--- handle_font: font[%d] ---' % f.font_index, footer='-------------------')


class Format(BaseObject, EqNeAttrs):
    format_key = 0
    type = FUN
    format_str = UNICODE_LITERAL('')

    def __init__(self, format_key, ty, format_str):
        self.format_key = format_key
        self.type = ty
        self.format_str = format_str


std_format_strings = {0: 'General', 
   1: '0', 
   2: '0.00', 
   3: '#,##0', 
   4: '#,##0.00', 
   5: '$#,##0_);($#,##0)', 
   6: '$#,##0_);[Red]($#,##0)', 
   7: '$#,##0.00_);($#,##0.00)', 
   8: '$#,##0.00_);[Red]($#,##0.00)', 
   9: '0%', 
   10: '0.00%', 
   11: '0.00E+00', 
   12: '# ?/?', 
   13: '# ??/??', 
   14: 'm/d/yy', 
   15: 'd-mmm-yy', 
   16: 'd-mmm', 
   17: 'mmm-yy', 
   18: 'h:mm AM/PM', 
   19: 'h:mm:ss AM/PM', 
   20: 'h:mm', 
   21: 'h:mm:ss', 
   22: 'm/d/yy h:mm', 
   37: '#,##0_);(#,##0)', 
   38: '#,##0_);[Red](#,##0)', 
   39: '#,##0.00_);(#,##0.00)', 
   40: '#,##0.00_);[Red](#,##0.00)', 
   41: '_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)', 
   42: '_($* #,##0_);_($* (#,##0);_($* "-"_);_(@_)', 
   43: '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)', 
   44: '_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)', 
   45: 'mm:ss', 
   46: '[h]:mm:ss', 
   47: 'mm:ss.0', 
   48: '##0.0E+0', 
   49: '@'}
fmt_code_ranges = [
 (
  0, 0, FGE),
 (
  1, 13, FNU),
 (
  14, 22, FDT),
 (
  27, 36, FDT),
 (
  37, 44, FNU),
 (
  45, 47, FDT),
 (
  48, 48, FNU),
 (
  49, 49, FTX),
 (
  50, 58, FDT),
 (
  59, 62, FNU),
 (
  67, 70, FNU),
 (
  71, 81, FDT)]
std_format_code_types = {}
for lo, hi, ty in fmt_code_ranges:
    for x in xrange(lo, hi + 1):
        std_format_code_types[x] = ty

del lo
del hi
del ty
del x
date_chars = UNICODE_LITERAL('ymdhs')
date_char_dict = {}
for _c in date_chars + date_chars.upper():
    date_char_dict[_c] = 5

del _c
del date_chars
skip_char_dict = {}
for _c in UNICODE_LITERAL('$-+/(): '):
    skip_char_dict[_c] = 1

num_char_dict = {UNICODE_LITERAL('0'): 5, 
   UNICODE_LITERAL('#'): 5, 
   UNICODE_LITERAL('?'): 5}
non_date_formats = {UNICODE_LITERAL('0.00E+00'): 1, 
   UNICODE_LITERAL('##0.0E+0'): 1, 
   UNICODE_LITERAL('General'): 1, 
   UNICODE_LITERAL('GENERAL'): 1, 
   UNICODE_LITERAL('general'): 1, 
   UNICODE_LITERAL('@'): 1}
fmt_bracketed_sub = re.compile('\\[[^]]*\\]').sub

def is_date_format_string(book, fmt):
    state = 0
    s = ''
    for c in fmt:
        if state == 0:
            if c == UNICODE_LITERAL('"'):
                state = 1
            elif c in UNICODE_LITERAL('\\_*'):
                state = 2
            elif c in skip_char_dict:
                pass
            else:
                s += c
        elif state == 1:
            if c == UNICODE_LITERAL('"'):
                state = 0
        elif state == 2:
            state = 0
        assert 0 <= state <= 2

    if book.verbosity >= 4:
        print('is_date_format_string: reduced format is %s' % REPR(s), file=book.logfile)
    s = fmt_bracketed_sub('', s)
    if s in non_date_formats:
        return False
    state = 0
    separator = ';'
    got_sep = 0
    date_count = num_count = 0
    for c in s:
        if c in date_char_dict:
            date_count += date_char_dict[c]
        elif c in num_char_dict:
            num_count += num_char_dict[c]
        elif c == separator:
            got_sep = 1

    if date_count and not num_count:
        return True
    if num_count and not date_count:
        return False
    if date_count:
        if book.verbosity:
            fprintf(book.logfile, 'WARNING *** is_date_format: ambiguous d=%d n=%d fmt=%r\n', date_count, num_count, fmt)
    elif not got_sep:
        if book.verbosity:
            fprintf(book.logfile, 'WARNING *** format %r produces constant result\n', fmt)
    return date_count > num_count


def handle_format(self, data, rectype=XL_FORMAT):
    DEBUG = 0
    bv = self.biff_version
    if rectype == XL_FORMAT2:
        bv = min(bv, 30)
    if not self.encoding:
        self.derive_encoding()
    strpos = 2
    if bv >= 50:
        fmtkey = unpack('<H', data[0:2])[0]
    else:
        fmtkey = self.actualfmtcount
        if bv <= 30:
            strpos = 0
    self.actualfmtcount += 1
    if bv >= 80:
        unistrg = unpack_unicode(data, 2)
    else:
        unistrg = unpack_string(data, strpos, self.encoding, lenlen=1)
    blah = DEBUG or self.verbosity >= 3
    if blah:
        fprintf(self.logfile, 'FORMAT: count=%d fmtkey=0x%04x (%d) s=%r\n', self.actualfmtcount, fmtkey, fmtkey, unistrg)
    is_date_s = self.is_date_format_string(unistrg)
    ty = [FGE, FDT][is_date_s]
    if not (fmtkey > 163 or bv < 50):
        std_ty = std_format_code_types.get(fmtkey, FUN)
        is_date_c = std_ty == FDT
        if self.verbosity and 0 < fmtkey < 50 and is_date_c ^ is_date_s:
            DEBUG = 2
            fprintf(self.logfile, 'WARNING *** Conflict between std format key %d and its format string %r\n', fmtkey, unistrg)
    if DEBUG == 2:
        fprintf(self.logfile, 'ty: %d; is_date_c: %r; is_date_s: %r; fmt_strg: %r', ty, is_date_c, is_date_s, unistrg)
    fmtobj = Format(fmtkey, ty, unistrg)
    if blah:
        fmtobj.dump(self.logfile, header='--- handle_format [%d] ---' % (self.actualfmtcount - 1,))
    self.format_map[fmtkey] = fmtobj
    self.format_list.append(fmtobj)


def handle_palette(book, data):
    if not book.formatting_info:
        return
    blah = DEBUG or book.verbosity >= 2
    n_colours, = unpack('<H', data[:2])
    expected_n_colours = (16, 56)[(book.biff_version >= 50)]
    if (DEBUG or book.verbosity >= 1) and n_colours != expected_n_colours:
        fprintf(book.logfile, 'NOTE *** Expected %d colours in PALETTE record, found %d\n', expected_n_colours, n_colours)
    else:
        if blah:
            fprintf(book.logfile, 'PALETTE record with %d colours\n', n_colours)
        fmt = '<xx%di' % n_colours
        expected_size = 4 * n_colours + 2
        actual_size = len(data)
        tolerance = 4
        if not expected_size <= actual_size <= expected_size + tolerance:
            raise XLRDError('PALETTE record: expected size %d, actual size %d' % (expected_size, actual_size))
        colours = unpack(fmt, data[:expected_size])
        assert book.palette_record == []
        for i in xrange(n_colours):
            c = colours[i]
            red = c & 255
            green = c >> 8 & 255
            blue = c >> 16 & 255
            old_rgb = book.colour_map[(8 + i)]
            new_rgb = (red, green, blue)
            book.palette_record.append(new_rgb)
            book.colour_map[8 + i] = new_rgb
            if blah:
                if new_rgb != old_rgb:
                    print('%2d: %r -> %r' % (i, old_rgb, new_rgb), file=book.logfile)


def palette_epilogue(book):
    for font in book.font_list:
        if font.font_index == 4:
            continue
        cx = font.colour_index
        if cx == 32767:
            continue
        if cx in book.colour_map:
            book.colour_indexes_used[cx] = 1
        elif book.verbosity:
            print('Size of colour table:', len(book.colour_map), file=book.logfile)
            fprintf(self.logfile, '*** Font #%d (%r): colour index 0x%04x is unknown\n', font.font_index, font.name, cx)

    if book.verbosity >= 1:
        used = sorted(book.colour_indexes_used.keys())
        print('\nColour indexes used:\n%r\n' % used, file=book.logfile)


def handle_style(book, data):
    if not book.formatting_info:
        return
    blah = DEBUG or book.verbosity >= 2
    bv = book.biff_version
    flag_and_xfx, built_in_id, level = unpack('<HBB', data[:4])
    xf_index = flag_and_xfx & 4095
    if data == '\x00\x00\x00\x00' and 'Normal' not in book.style_name_map:
        built_in = 1
        built_in_id = 0
        xf_index = 0
        name = 'Normal'
        level = 255
    elif flag_and_xfx & 32768:
        built_in = 1
        name = built_in_style_names[built_in_id]
        if 1 <= built_in_id <= 2:
            name += str(level + 1)
    else:
        built_in = 0
        built_in_id = 0
        level = 0
        if bv >= 80:
            try:
                name = unpack_unicode(data, 2, lenlen=2)
            except UnicodeDecodeError:
                print('STYLE: built_in=%d xf_index=%d built_in_id=%d level=%d' % (
                 built_in, xf_index, built_in_id, level), file=book.logfile)
                print('raw bytes:', repr(data[2:]), file=book.logfile)
                raise

        else:
            name = unpack_string(data, 2, book.encoding, lenlen=1)
        if blah and not name:
            print('WARNING *** A user-defined style has a zero-length name', file=book.logfile)
    book.style_name_map[name] = (
     built_in, xf_index)
    if blah:
        fprintf(book.logfile, 'STYLE: built_in=%d xf_index=%d built_in_id=%d level=%d name=%r\n', built_in, xf_index, built_in_id, level, name)


def check_colour_indexes_in_obj(book, obj, orig_index):
    alist = sorted(obj.__dict__.items())
    for attr, nobj in alist:
        if hasattr(nobj, 'dump'):
            check_colour_indexes_in_obj(book, nobj, orig_index)
        elif attr.find('colour_index') >= 0:
            if nobj in book.colour_map:
                book.colour_indexes_used[nobj] = 1
                continue
            oname = obj.__class__.__name__
            print('*** xf #%d : %s.%s =  0x%04x (unknown)' % (
             orig_index, oname, attr, nobj), file=book.logfile)


def fill_in_standard_formats(book):
    for x in std_format_code_types.keys():
        if x not in book.format_map:
            ty = std_format_code_types[x]
            fmt_str = std_format_strings.get(x)
            fmtobj = Format(x, ty, fmt_str)
            book.format_map[x] = fmtobj


def handle_xf(self, data):
    blah = DEBUG or self.verbosity >= 3
    bv = self.biff_version
    xf = XF()
    xf.alignment = XFAlignment()
    xf.alignment.indent_level = 0
    xf.alignment.shrink_to_fit = 0
    xf.alignment.text_direction = 0
    xf.border = XFBorder()
    xf.border.diag_up = 0
    xf.border.diag_down = 0
    xf.border.diag_colour_index = 0
    xf.border.diag_line_style = 0
    xf.background = XFBackground()
    xf.protection = XFProtection()
    if bv >= 50 and not self.xfcount:
        fill_in_standard_formats(self)
    if bv >= 80:
        unpack_fmt = '<HHHBBBBIiH'
        xf.font_index, xf.format_key, pkd_type_par, pkd_align1, xf.alignment.rotation, pkd_align2, pkd_used, pkd_brdbkg1, pkd_brdbkg2, pkd_brdbkg3 = unpack(unpack_fmt, data[0:20])
        upkbits(xf.protection, pkd_type_par, (
         (0, 1, 'cell_locked'),
         (1, 2, 'formula_hidden')))
        upkbits(xf, pkd_type_par, (
         (2, 4, 'is_style'),
         (3, 8, 'lotus_123_prefix'),
         (4, 65520, 'parent_style_index')))
        upkbits(xf.alignment, pkd_align1, (
         (0, 7, 'hor_align'),
         (3, 8, 'text_wrapped'),
         (4, 112, 'vert_align')))
        upkbits(xf.alignment, pkd_align2, (
         (0, 15, 'indent_level'),
         (4, 16, 'shrink_to_fit'),
         (6, 192, 'text_direction')))
        reg = pkd_used >> 2
        for attr_stem in ('format font alignment border background protection').split():
            attr = '_' + attr_stem + '_flag'
            setattr(xf, attr, reg & 1)
            reg >>= 1

        upkbitsL(xf.border, pkd_brdbkg1, (
         (0, 15, 'left_line_style'),
         (4, 240, 'right_line_style'),
         (8, 3840, 'top_line_style'),
         (12, 61440, 'bottom_line_style'),
         (16, 8323072, 'left_colour_index'),
         (23, 1065353216, 'right_colour_index'),
         (30, 1073741824, 'diag_down'),
         (31, 2147483648, 'diag_up')))
        upkbits(xf.border, pkd_brdbkg2, (
         (0, 127, 'top_colour_index'),
         (7, 16256, 'bottom_colour_index'),
         (14, 2080768, 'diag_colour_index'),
         (21, 31457280, 'diag_line_style')))
        upkbitsL(xf.background, pkd_brdbkg2, ((26, 4227858432, 'fill_pattern'), ))
        upkbits(xf.background, pkd_brdbkg3, (
         (0, 127, 'pattern_colour_index'),
         (7, 16256, 'background_colour_index')))
    else:
        if bv >= 50:
            unpack_fmt = '<HHHBBIi'
            xf.font_index, xf.format_key, pkd_type_par, pkd_align1, pkd_orient_used, pkd_brdbkg1, pkd_brdbkg2 = unpack(unpack_fmt, data[0:16])
            upkbits(xf.protection, pkd_type_par, (
             (0, 1, 'cell_locked'),
             (1, 2, 'formula_hidden')))
            upkbits(xf, pkd_type_par, (
             (2, 4, 'is_style'),
             (3, 8, 'lotus_123_prefix'),
             (4, 65520, 'parent_style_index')))
            upkbits(xf.alignment, pkd_align1, (
             (0, 7, 'hor_align'),
             (3, 8, 'text_wrapped'),
             (4, 112, 'vert_align')))
            orientation = pkd_orient_used & 3
            xf.alignment.rotation = [0, 255, 90, 180][orientation]
            reg = pkd_orient_used >> 2
            for attr_stem in ('format font alignment border background protection').split():
                attr = '_' + attr_stem + '_flag'
                setattr(xf, attr, reg & 1)
                reg >>= 1

            upkbitsL(xf.background, pkd_brdbkg1, (
             (0, 127, 'pattern_colour_index'),
             (7, 16256, 'background_colour_index'),
             (16, 4128768, 'fill_pattern')))
            upkbitsL(xf.border, pkd_brdbkg1, (
             (22, 29360128, 'bottom_line_style'),
             (25, 4261412864, 'bottom_colour_index')))
            upkbits(xf.border, pkd_brdbkg2, (
             (0, 7, 'top_line_style'),
             (3, 56, 'left_line_style'),
             (6, 448, 'right_line_style'),
             (9, 65024, 'top_colour_index'),
             (16, 8323072, 'left_colour_index'),
             (23, 1065353216, 'right_colour_index')))
        elif bv >= 40:
            unpack_fmt = '<BBHBBHI'
            xf.font_index, xf.format_key, pkd_type_par, pkd_align_orient, pkd_used, pkd_bkg_34, pkd_brd_34 = unpack(unpack_fmt, data[0:12])
            upkbits(xf.protection, pkd_type_par, (
             (0, 1, 'cell_locked'),
             (1, 2, 'formula_hidden')))
            upkbits(xf, pkd_type_par, (
             (2, 4, 'is_style'),
             (3, 8, 'lotus_123_prefix'),
             (4, 65520, 'parent_style_index')))
            upkbits(xf.alignment, pkd_align_orient, (
             (0, 7, 'hor_align'),
             (3, 8, 'text_wrapped'),
             (4, 48, 'vert_align')))
            orientation = (pkd_align_orient & 192) >> 6
            xf.alignment.rotation = [0, 255, 90, 180][orientation]
            reg = pkd_used >> 2
            for attr_stem in ('format font alignment border background protection').split():
                attr = '_' + attr_stem + '_flag'
                setattr(xf, attr, reg & 1)
                reg >>= 1

            upkbits(xf.background, pkd_bkg_34, (
             (0, 63, 'fill_pattern'),
             (6, 1984, 'pattern_colour_index'),
             (11, 63488, 'background_colour_index')))
            upkbitsL(xf.border, pkd_brd_34, (
             (0, 7, 'top_line_style'),
             (3, 248, 'top_colour_index'),
             (8, 1792, 'left_line_style'),
             (11, 63488, 'left_colour_index'),
             (16, 458752, 'bottom_line_style'),
             (19, 16252928, 'bottom_colour_index'),
             (24, 117440512, 'right_line_style'),
             (27, 4160749568, 'right_colour_index')))
        elif bv == 30:
            unpack_fmt = '<BBBBHHI'
            xf.font_index, xf.format_key, pkd_type_prot, pkd_used, pkd_align_par, pkd_bkg_34, pkd_brd_34 = unpack(unpack_fmt, data[0:12])
            upkbits(xf.protection, pkd_type_prot, (
             (0, 1, 'cell_locked'),
             (1, 2, 'formula_hidden')))
            upkbits(xf, pkd_type_prot, (
             (2, 4, 'is_style'),
             (3, 8, 'lotus_123_prefix')))
            upkbits(xf.alignment, pkd_align_par, (
             (0, 7, 'hor_align'),
             (3, 8, 'text_wrapped')))
            upkbits(xf, pkd_align_par, ((4, 65520, 'parent_style_index'), ))
            reg = pkd_used >> 2
            for attr_stem in ('format font alignment border background protection').split():
                attr = '_' + attr_stem + '_flag'
                setattr(xf, attr, reg & 1)
                reg >>= 1

            upkbits(xf.background, pkd_bkg_34, (
             (0, 63, 'fill_pattern'),
             (6, 1984, 'pattern_colour_index'),
             (11, 63488, 'background_colour_index')))
            upkbitsL(xf.border, pkd_brd_34, (
             (0, 7, 'top_line_style'),
             (3, 248, 'top_colour_index'),
             (8, 1792, 'left_line_style'),
             (11, 63488, 'left_colour_index'),
             (16, 458752, 'bottom_line_style'),
             (19, 16252928, 'bottom_colour_index'),
             (24, 117440512, 'right_line_style'),
             (27, 4160749568, 'right_colour_index')))
            xf.alignment.vert_align = 2
            xf.alignment.rotation = 0
        elif bv == 21:
            xf.font_index, format_etc, halign_etc = unpack('<BxBB', data)
            xf.format_key = format_etc & 63
            upkbits(xf.protection, format_etc, (
             (6, 64, 'cell_locked'),
             (7, 128, 'formula_hidden')))
            upkbits(xf.alignment, halign_etc, ((0, 7, 'hor_align'), ))
            for mask, side in ((8, 'left'), (16, 'right'), (32, 'top'), (64, 'bottom')):
                if halign_etc & mask:
                    colour_index, line_style = (8, 1)
                else:
                    colour_index, line_style = (0, 0)
                setattr(xf.border, side + '_colour_index', colour_index)
                setattr(xf.border, side + '_line_style', line_style)

            bg = xf.background
            if halign_etc & 128:
                bg.fill_pattern = 17
            else:
                bg.fill_pattern = 0
            bg.background_colour_index = 9
            bg.pattern_colour_index = 8
            xf.parent_style_index = 0
            xf.alignment.vert_align = 2
            xf.alignment.rotation = 0
            for attr_stem in ('format font alignment border background protection').split():
                attr = '_' + attr_stem + '_flag'
                setattr(xf, attr, 1)

        else:
            raise XLRDError('programmer stuff-up: bv=%d' % bv)
        xf.xf_index = len(self.xf_list)
        self.xf_list.append(xf)
        self.xfcount += 1
        if blah:
            xf.dump(self.logfile, header='--- handle_xf: xf[%d] ---' % xf.xf_index, footer=' ')
        try:
            fmt = self.format_map[xf.format_key]
            cellty = _cellty_from_fmtty[fmt.type]
        except KeyError:
            cellty = XL_CELL_NUMBER

    self._xf_index_to_xl_type_map[xf.xf_index] = cellty
    if self.formatting_info:
        if self.verbosity and xf.is_style and xf.parent_style_index != 4095:
            msg = 'WARNING *** XF[%d] is a style XF but parent_style_index is 0x%04x, not 0x0fff\n'
            fprintf(self.logfile, msg, xf.xf_index, xf.parent_style_index)
        check_colour_indexes_in_obj(self, xf, xf.xf_index)
    if xf.format_key not in self.format_map:
        msg = 'WARNING *** XF[%d] unknown (raw) format key (%d, 0x%04x)\n'
        if self.verbosity:
            fprintf(self.logfile, msg, xf.xf_index, xf.format_key, xf.format_key)
        xf.format_key = 0


def xf_epilogue(self):
    self._xf_epilogue_done = 1
    num_xfs = len(self.xf_list)
    blah = DEBUG or self.verbosity >= 3
    blah1 = DEBUG or self.verbosity >= 1
    if blah:
        fprintf(self.logfile, 'xf_epilogue called ...\n')

    def check_same(book_arg, xf_arg, parent_arg, attr):
        if getattr(xf_arg, attr) != getattr(parent_arg, attr):
            fprintf(book_arg.logfile, 'NOTE !!! XF[%d] parent[%d] %s different\n', xf_arg.xf_index, parent_arg.xf_index, attr)

    for xfx in xrange(num_xfs):
        xf = self.xf_list[xfx]
        if xf.format_key not in self.format_map:
            msg = 'ERROR *** XF[%d] unknown format key (%d, 0x%04x)\n'
            fprintf(self.logfile, msg, xf.xf_index, xf.format_key, xf.format_key)
            xf.format_key = 0
        fmt = self.format_map[xf.format_key]
        cellty = _cellty_from_fmtty[fmt.type]
        self._xf_index_to_xl_type_map[xf.xf_index] = cellty
        if not self.formatting_info:
            continue
        if xf.is_style:
            continue
        if not 0 <= xf.parent_style_index < num_xfs:
            if blah1:
                fprintf(self.logfile, 'WARNING *** XF[%d]: is_style=%d but parent_style_index=%d\n', xf.xf_index, xf.is_style, xf.parent_style_index)
            xf.parent_style_index = 0
        if self.biff_version >= 30:
            if blah1:
                if xf.parent_style_index == xf.xf_index:
                    fprintf(self.logfile, 'NOTE !!! XF[%d]: parent_style_index is also %d\n', xf.xf_index, xf.parent_style_index)
                elif not self.xf_list[xf.parent_style_index].is_style:
                    fprintf(self.logfile, 'NOTE !!! XF[%d]: parent_style_index is %d; style flag not set\n', xf.xf_index, xf.parent_style_index)
            if blah1 and xf.parent_style_index > xf.xf_index:
                fprintf(self.logfile, 'NOTE !!! XF[%d]: parent_style_index is %d; out of order?\n', xf.xf_index, xf.parent_style_index)
            parent = self.xf_list[xf.parent_style_index]
            if not xf._alignment_flag and not parent._alignment_flag:
                if blah1:
                    check_same(self, xf, parent, 'alignment')
            if not xf._background_flag and not parent._background_flag:
                if blah1:
                    check_same(self, xf, parent, 'background')
            if not xf._border_flag and not parent._border_flag:
                if blah1:
                    check_same(self, xf, parent, 'border')
            if not xf._protection_flag and not parent._protection_flag:
                if blah1:
                    check_same(self, xf, parent, 'protection')
            if not xf._format_flag and not parent._format_flag:
                if blah1 and xf.format_key != parent.format_key:
                    fprintf(self.logfile, 'NOTE !!! XF[%d] fmtk=%d, parent[%d] fmtk=%r\n%r / %r\n', xf.xf_index, xf.format_key, parent.xf_index, parent.format_key, self.format_map[xf.format_key].format_str, self.format_map[parent.format_key].format_str)
            if not xf._font_flag and not parent._font_flag:
                if blah1 and xf.font_index != parent.font_index:
                    fprintf(self.logfile, 'NOTE !!! XF[%d] fontx=%d, parent[%d] fontx=%r\n', xf.xf_index, xf.font_index, parent.xf_index, parent.font_index)


def initialise_book(book):
    initialise_colour_map(book)
    book._xf_epilogue_done = 0
    methods = (
     handle_font,
     handle_efont,
     handle_format,
     is_date_format_string,
     handle_palette,
     palette_epilogue,
     handle_style,
     handle_xf,
     xf_epilogue)
    for method in methods:
        setattr(book.__class__, method.__name__, method)


class XFBorder(BaseObject, EqNeAttrs):
    top_colour_index = 0
    bottom_colour_index = 0
    left_colour_index = 0
    right_colour_index = 0
    diag_colour_index = 0
    top_line_style = 0
    bottom_line_style = 0
    left_line_style = 0
    right_line_style = 0
    diag_line_style = 0
    diag_down = 0
    diag_up = 0


class XFBackground(BaseObject, EqNeAttrs):
    fill_pattern = 0
    background_colour_index = 0
    pattern_colour_index = 0


class XFAlignment(BaseObject, EqNeAttrs):
    hor_align = 0
    vert_align = 0
    rotation = 0
    text_wrapped = 0
    indent_level = 0
    shrink_to_fit = 0
    text_direction = 0


class XFProtection(BaseObject, EqNeAttrs):
    cell_locked = 0
    formula_hidden = 0


class XF(BaseObject):
    is_style = 0
    parent_style_index = 0
    _format_flag = 0
    _font_flag = 0
    _alignment_flag = 0
    _border_flag = 0
    _background_flag = 0
    _protection_flag = 0
    xf_index = 0
    font_index = 0
    format_key = 0
    protection = None
    background = None
    alignment = None
    border = None