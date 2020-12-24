# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Formatting.py
# Compiled at: 2008-03-17 12:58:02
"""
The  XF  record is able to store explicit cell formatting attributes or the
attributes  of  a cell style. Explicit formatting includes the reference to
a  cell  style  XF  record. This allows to extend a defined cell style with
some  explicit  attributes.  The  formatting  attributes  are  divided into
6 groups:

Group           Attributes
-------------------------------------
Number format   Number format index (index to FORMAT record)
Font            Font index (index to FONT record)
Alignment       Horizontal and vertical alignment, text wrap, indentation, 
                orientation/rotation, text direction
Border          Border line styles and colours
Background      Background area style and colours
Protection      Cell locked, formula hidden

For  each  group  a flag in the cell XF record specifies whether to use the
attributes  contained  in  that  XF  record  or  in  the  referenced  style
XF  record. In style XF records, these flags specify whether the attributes
will  overwrite  explicit  cell  formatting  when  the  style is applied to
a  cell. Changing a cell style (without applying this style to a cell) will
change  all  cells which already use that style and do not contain explicit
cell  attributes for the changed style attributes. If a cell XF record does
not  contain  explicit  attributes  in a group (if the attribute group flag
is not set), it repeats the attributes of its style XF record.

"""
__rev_id__ = '$Id: Formatting.py,v 1.4 2005/07/20 07:24:11 rvk Exp $'
import BIFFRecords

class Font(object):
    ESCAPEMENT_NONE = 0
    ESCAPEMENT_SUPERSCRIPT = 1
    ESCAPEMENT_SUBSCRIPT = 2
    UNDERLINE_NONE = 0
    UNDERLINE_SINGLE = 1
    UNDERLINE_SINGLE_ACC = 33
    UNDERLINE_DOUBLE = 2
    UNDERLINE_DOUBLE_ACC = 34
    FAMILY_NONE = 0
    FAMILY_ROMAN = 1
    FAMILY_SWISS = 2
    FAMILY_MODERN = 3
    FAMILY_SCRIPT = 4
    FAMILY_DECORARTIVE = 5
    CHARSET_ANSI_LATIN = 0
    CHARSET_SYS_DEFAULT = 1
    CHARSET_SYMBOL = 2
    CHARSET_APPLE_ROMAN = 77
    CHARSET_ANSI_JAP_SHIFT_JIS = 128
    CHARSET_ANSI_KOR_HANGUL = 129
    CHARSET_ANSI_KOR_JOHAB = 130
    CHARSET_ANSI_CHINESE_GBK = 134
    CHARSET_ANSI_CHINESE_BIG5 = 136
    CHARSET_ANSI_GREEK = 161
    CHARSET_ANSI_TURKISH = 162
    CHARSET_ANSI_VIETNAMESE = 163
    CHARSET_ANSI_HEBREW = 177
    CHARSET_ANSI_ARABIC = 178
    CHARSET_ANSI_BALTIC = 186
    CHARSET_ANSI_CYRILLIC = 204
    CHARSET_ANSI_THAI = 222
    CHARSET_ANSI_LATIN_II = 238
    CHARSET_OEM_LATIN_I = 255

    def __init__(self):
        self.height = 200
        self.italic = False
        self.struck_out = False
        self.outline = False
        self.shadow = False
        self.colour_index = 32767
        self.bold = False
        self._weight = 400
        self.escapement = self.ESCAPEMENT_NONE
        self.underline = self.UNDERLINE_NONE
        self.family = self.FAMILY_NONE
        self.charset = self.CHARSET_ANSI_CYRILLIC
        self.name = 'Arial'

    def get_biff_record(self):
        height = self.height
        options = 0
        if self.bold:
            options |= 1
            self._weight = 700
        if self.italic:
            options |= 2
        if self.underline != self.UNDERLINE_NONE:
            options |= 4
        if self.struck_out:
            options |= 8
        if self.outline:
            options |= 16
        if self.shadow:
            options |= 32
        colour_index = self.colour_index
        weight = self._weight
        escapement = self.escapement
        underline = self.underline
        family = self.family
        charset = self.charset
        name = self.name
        return BIFFRecords.FontRecord(height, options, colour_index, weight, escapement, underline, family, charset, name)


class Alignment(object):
    HORZ_GENERAL = 0
    HORZ_LEFT = 1
    HORZ_CENTER = 2
    HORZ_RIGHT = 3
    HORZ_FILLED = 4
    HORZ_JUSTIFIED = 5
    HORZ_CENTER_ACROSS_SEL = 6
    HORZ_DISTRIBUTED = 7
    VERT_TOP = 0
    VERT_CENTER = 1
    VERT_BOTTOM = 2
    VERT_JUSTIFIED = 3
    VERT_DISIRIBUTED = 4
    DIRECTION_GENERAL = 0
    DIRECTION_LR = 1
    DIRECTION_RL = 2
    ORIENTATION_NOT_ROTATED = 0
    ORIENTATION_STACKED = 1
    ORIENTATION_90_CC = 2
    ORIENTATION_90_CW = 3
    ROTATION_0_ANGLE = 0
    ROTATION_STACKED = 255
    WRAP_AT_RIGHT = 1
    NOT_WRAP_AT_RIGHT = 0
    SHRINK_TO_FIT = 1
    NOT_SHRINK_TO_FIT = 0

    def __init__(self):
        self.horz = self.HORZ_GENERAL
        self.vert = self.VERT_BOTTOM
        self.dire = self.DIRECTION_GENERAL
        self.orie = self.ORIENTATION_NOT_ROTATED
        self.rota = self.ROTATION_0_ANGLE
        self.wrap = self.NOT_WRAP_AT_RIGHT
        self.shri = self.NOT_SHRINK_TO_FIT
        self.inde = 0
        self.merg = 0


class Borders(object):
    NO_LINE = 0
    THIN = 1
    MEDIUM = 2
    DASHED = 3
    DOTTED = 4
    THICK = 5
    DOUBLE = 6
    HAIR = 7
    MEDIUM_DASHED = 8
    THIN_DASH_DOTTED = 9
    MEDIUM_DASH_DOTTED = 10
    THIN_DASH_DOT_DOTTED = 11
    MEDIUM_DASH_DOT_DOTTED = 12
    SLANTED_MEDIUM_DASH_DOTTED = 13
    NEED_DIAG1 = 1
    NEED_DIAG2 = 1
    NO_NEED_DIAG1 = 0
    NO_NEED_DIAG2 = 0

    def __init__(self):
        self.left = self.NO_LINE
        self.right = self.NO_LINE
        self.top = self.NO_LINE
        self.bottom = self.NO_LINE
        self.diag = self.NO_LINE
        self.left_colour = 64
        self.right_colour = 64
        self.top_colour = 64
        self.bottom_colour = 64
        self.diag_colour = 64
        self.need_diag1 = self.NO_NEED_DIAG1
        self.need_diag2 = self.NO_NEED_DIAG2


class Pattern(object):
    NO_PATTERN = 0
    SOLID_PATTERN = 1

    def __init__(self):
        self.pattern = self.NO_PATTERN
        self.pattern_fore_colour = 64
        self.pattern_back_colour = 65


class Protection(object):

    def __init__(self):
        self.cell_locked = 1
        self.formula_hidden = 0


if __name__ == '__main__':
    font0 = Font()
    font0.name = 'Arial'
    font1 = Font()
    font1.name = 'Arial Cyr'
    font2 = Font()
    font2.name = 'Times New Roman'
    font3 = Font()
    font3.name = 'Courier New Cyr'
    for (font, filename) in [(font0, 'font0.bin'), (font1, 'font1.bin'), (font2, 'font2.bin'), (font3, 'font3.bin')]:
        f = file(filename, 'wb')
        f.write(font.get_biff_record().get_data())
        f.close