# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pymaoyanfont\parsefont.py
# Compiled at: 2019-05-14 11:37:13
# Size of source mod 2**32: 4335 bytes
import io
from fontTools.ttLib import TTFont
import os
data_dir = os.path.abspath(os.path.join(os.path.pardir, './data/base.woff'))

class MaoyanFont(object):

    def __init__(self):
        self._glyphs_map = None
        self._baseValue = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self._baseCode = ('uniECF6', 'uniF619', 'uniF624', 'uniF67D', 'uniF6A8', 'uniF807',
                          'uniE701', 'uniE9D7', 'uniF836', 'uniE25B')

    @property
    def glyphs(self):
        return self._glyphs_map

    @property
    def basecode(self):
        return self._baseCode

    @property
    def basevalue(self):
        return self._baseValue

    @basecode.setter
    def basecode(self, *args):
        self._baseCode = args

    @basevalue.setter
    def basevalue(self, *args):
        self._baseValue = args

    def _parseFont(self, parse_font, base_font):
        """

        :param parse_font:
        :param base_font:
        :return:
        """
        glynames = parse_font.getGlyphNames()[1:-1]
        glyph = {}
        for code in glynames:
            tmp_glyph = parse_font['glyf'][code]
            for i in range(len(self._baseCode)):
                if tmp_glyph == base_font['glyf'][self._baseCode[i]]:
                    glyph[code] = self._baseValue[i]
                    break

        return glyph

    def load(self, file, base_file=None, base_font=None):
        """

        :param file:
        :param base_file:
        :return:
        """
        parse_font = TTFont(file)
        if base_font is None:
            if base_file is None:
                base_file = data_dir
            base_font = TTFont(base_file)
        self._glyphs_map = self._parseFont(parse_font, base_font)
        return self._glyphs_map

    def loads(self, s, base_file=None, base_font=None):
        """

        :param s:
        :param base_file:
        :return:
        """
        parse_font = TTFont(io.BytesIO(s))
        if base_font is None:
            if base_file is None:
                base_file = data_dir
            base_font = TTFont(base_file)
        self._glyphs_map = self._parseFont(parse_font, base_font)
        return self._glyphs_map

    def uni_to_raw(self):
        if self._glyphs_map is None:
            return
        else:
            tmp = {}
            for _ in self._glyphs_map:
                tmp['&#%s;' % _[3:].lower()] = self._glyphs_map[_]

            return tmp

    def uni_to_int(self):
        if self._glyphs_map is None:
            return
        else:
            tmp = {}
            for _ in self._glyphs_map:
                tmp[eval('0x' + _[3:])] = self._glyphs_map[_]

            return tmp

    def __del__(self):
        del self