# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glyphviewer/blocks.py
# Compiled at: 2018-03-17 21:18:23
import re
PRIV_USE_BLOCK = 144

def block(ch):
    """
    Return the Unicode block name for ch, or None if ch has no block.

    >>> block(u'a')
    'Basic Latin'
    >>> block(unichr(0x0b80))
    'Tamil'
    >>> block(unichr(0xe0080))
    """
    assert isinstance(ch, unicode) and len(ch) == 1, repr(ch)
    cp = ord(ch)
    for start, end, name in _blocks:
        if start <= cp <= end:
            return name


def blockbyint(intval):
    for start, end, name in _blocks:
        if start <= intval <= end:
            return name


def namefromindex(ith):
    """ Returns the name of the ith block. """
    return _blocks[ith][2]


def indexfromname(name):
    """ Returns the index of a block name. """
    if name:
        return _blockmap[name]
    else:
        return PRIV_USE_BLOCK


def numblocks():
    """ Gets the number of blocks. """
    return _blocksize


def _initBlocks(text):
    global _blockmap
    global _blocks
    global _blocksize
    _blocks = []
    _blockmap = {}
    iter = 0
    pattern = re.compile('([0-9A-F]+)\\.\\.([0-9A-F]+);\\ (\\S.*\\S)')
    for line in text.splitlines():
        m = pattern.match(line)
        if m:
            start, end, name = m.groups()
            _blocks.append((int(start, 16), int(end, 16), name))
            _blockmap[name] = iter
            iter += 1

    _blocksize = len(_blocks)


_initBlocks('\n# Blocks-8.0.0.txt\n# Date: 2014-11-10, 23:04:00 GMT [KW]\n#\n# Unicode Character Database\n# Copyright (c) 1991-2014 Unicode, Inc.\n# For terms of use, see http://www.unicode.org/terms_of_use.html\n# For documentation, see http://www.unicode.org/reports/tr44/\n#\n# Format:\n# Start Code..End Code; Block Name\n\n# ================================================\n\n# Note:   When comparing block names, casing, whitespace, hyphens,\n#         and underbars are ignored.\n#         For example, "Latin Extended-A" and "latin extended a" are equivalent.\n#         For more information on the comparison of property values,\n#            see UAX #44: http://www.unicode.org/reports/tr44/\n#\n#  All block ranges start with a value where (cp MOD 16) = 0,\n#  and end with a value where (cp MOD 16) = 15. In other words,\n#  the last hexadecimal digit of the start of range is ...0\n#  and the last hexadecimal digit of the end of range is ...F.\n#  This constraint on block ranges guarantees that allocations\n#  are done in terms of whole columns, and that code chart display\n#  never involves splitting columns in the charts.\n#\n#  All code points not explicitly listed for Block\n#  have the value No_Block.\n\n# Property:\tBlock\n#\n# @missing: 0000..10FFFF; No_Block\n\n0000..007F; Basic Latin\n0080..00FF; Latin-1 Supplement\n0100..017F; Latin Extended-A\n0180..024F; Latin Extended-B\n0250..02AF; IPA Extensions\n02B0..02FF; Spacing Modifier Letters\n0300..036F; Combining Diacritical Marks\n0370..03FF; Greek and Coptic\n0400..04FF; Cyrillic\n0500..052F; Cyrillic Supplement\n0530..058F; Armenian\n0590..05FF; Hebrew\n0600..06FF; Arabic\n0700..074F; Syriac\n0750..077F; Arabic Supplement\n0780..07BF; Thaana\n07C0..07FF; NKo\n0800..083F; Samaritan\n0840..085F; Mandaic\n08A0..08FF; Arabic Extended-A\n0900..097F; Devanagari\n0980..09FF; Bengali\n0A00..0A7F; Gurmukhi\n0A80..0AFF; Gujarati\n0B00..0B7F; Oriya\n0B80..0BFF; Tamil\n0C00..0C7F; Telugu\n0C80..0CFF; Kannada\n0D00..0D7F; Malayalam\n0D80..0DFF; Sinhala\n0E00..0E7F; Thai\n0E80..0EFF; Lao\n0F00..0FFF; Tibetan\n1000..109F; Myanmar\n10A0..10FF; Georgian\n1100..11FF; Hangul Jamo\n1200..137F; Ethiopic\n1380..139F; Ethiopic Supplement\n13A0..13FF; Cherokee\n1400..167F; Unified Canadian Aboriginal Syllabics\n1680..169F; Ogham\n16A0..16FF; Runic\n1700..171F; Tagalog\n1720..173F; Hanunoo\n1740..175F; Buhid\n1760..177F; Tagbanwa\n1780..17FF; Khmer\n1800..18AF; Mongolian\n18B0..18FF; Unified Canadian Aboriginal Syllabics Extended\n1900..194F; Limbu\n1950..197F; Tai Le\n1980..19DF; New Tai Lue\n19E0..19FF; Khmer Symbols\n1A00..1A1F; Buginese\n1A20..1AAF; Tai Tham\n1AB0..1AFF; Combining Diacritical Marks Extended\n1B00..1B7F; Balinese\n1B80..1BBF; Sundanese\n1BC0..1BFF; Batak\n1C00..1C4F; Lepcha\n1C50..1C7F; Ol Chiki\n1CC0..1CCF; Sundanese Supplement\n1CD0..1CFF; Vedic Extensions\n1D00..1D7F; Phonetic Extensions\n1D80..1DBF; Phonetic Extensions Supplement\n1DC0..1DFF; Combining Diacritical Marks Supplement\n1E00..1EFF; Latin Extended Additional\n1F00..1FFF; Greek Extended\n2000..206F; General Punctuation\n2070..209F; Superscripts and Subscripts\n20A0..20CF; Currency Symbols\n20D0..20FF; Combining Diacritical Marks for Symbols\n2100..214F; Letterlike Symbols\n2150..218F; Number Forms\n2190..21FF; Arrows\n2200..22FF; Mathematical Operators\n2300..23FF; Miscellaneous Technical\n2400..243F; Control Pictures\n2440..245F; Optical Character Recognition\n2460..24FF; Enclosed Alphanumerics\n2500..257F; Box Drawing\n2580..259F; Block Elements\n25A0..25FF; Geometric Shapes\n2600..26FF; Miscellaneous Symbols\n2700..27BF; Dingbats\n27C0..27EF; Miscellaneous Mathematical Symbols-A\n27F0..27FF; Supplemental Arrows-A\n2800..28FF; Braille Patterns\n2900..297F; Supplemental Arrows-B\n2980..29FF; Miscellaneous Mathematical Symbols-B\n2A00..2AFF; Supplemental Mathematical Operators\n2B00..2BFF; Miscellaneous Symbols and Arrows\n2C00..2C5F; Glagolitic\n2C60..2C7F; Latin Extended-C\n2C80..2CFF; Coptic\n2D00..2D2F; Georgian Supplement\n2D30..2D7F; Tifinagh\n2D80..2DDF; Ethiopic Extended\n2DE0..2DFF; Cyrillic Extended-A\n2E00..2E7F; Supplemental Punctuation\n2E80..2EFF; CJK Radicals Supplement\n2F00..2FDF; Kangxi Radicals\n2FF0..2FFF; Ideographic Description Characters\n3000..303F; CJK Symbols and Punctuation\n3040..309F; Hiragana\n30A0..30FF; Katakana\n3100..312F; Bopomofo\n3130..318F; Hangul Compatibility Jamo\n3190..319F; Kanbun\n31A0..31BF; Bopomofo Extended\n31C0..31EF; CJK Strokes\n31F0..31FF; Katakana Phonetic Extensions\n3200..32FF; Enclosed CJK Letters and Months\n3300..33FF; CJK Compatibility\n3400..4DBF; CJK Unified Ideographs Extension A\n4DC0..4DFF; Yijing Hexagram Symbols\n4E00..9FFF; CJK Unified Ideographs\nA000..A48F; Yi Syllables\nA490..A4CF; Yi Radicals\nA4D0..A4FF; Lisu\nA500..A63F; Vai\nA640..A69F; Cyrillic Extended-B\nA6A0..A6FF; Bamum\nA700..A71F; Modifier Tone Letters\nA720..A7FF; Latin Extended-D\nA800..A82F; Syloti Nagri\nA830..A83F; Common Indic Number Forms\nA840..A87F; Phags-pa\nA880..A8DF; Saurashtra\nA8E0..A8FF; Devanagari Extended\nA900..A92F; Kayah Li\nA930..A95F; Rejang\nA960..A97F; Hangul Jamo Extended-A\nA980..A9DF; Javanese\nA9E0..A9FF; Myanmar Extended-B\nAA00..AA5F; Cham\nAA60..AA7F; Myanmar Extended-A\nAA80..AADF; Tai Viet\nAAE0..AAFF; Meetei Mayek Extensions\nAB00..AB2F; Ethiopic Extended-A\nAB30..AB6F; Latin Extended-E\nAB70..ABBF; Cherokee Supplement\nABC0..ABFF; Meetei Mayek\nAC00..D7AF; Hangul Syllables\nD7B0..D7FF; Hangul Jamo Extended-B\nD800..DB7F; High Surrogates\nDB80..DBFF; High Private Use Surrogates\nDC00..DFFF; Low Surrogates\nE000..F8FF; Private Use Area\nF900..FAFF; CJK Compatibility Ideographs\nFB00..FB4F; Alphabetic Presentation Forms\nFB50..FDFF; Arabic Presentation Forms-A\nFE00..FE0F; Variation Selectors\nFE10..FE1F; Vertical Forms\nFE20..FE2F; Combining Half Marks\nFE30..FE4F; CJK Compatibility Forms\nFE50..FE6F; Small Form Variants\nFE70..FEFF; Arabic Presentation Forms-B\nFF00..FFEF; Halfwidth and Fullwidth Forms\nFFF0..FFFF; Specials\n10000..1007F; Linear B Syllabary\n10080..100FF; Linear B Ideograms\n10100..1013F; Aegean Numbers\n10140..1018F; Ancient Greek Numbers\n10190..101CF; Ancient Symbols\n101D0..101FF; Phaistos Disc\n10280..1029F; Lycian\n102A0..102DF; Carian\n102E0..102FF; Coptic Epact Numbers\n10300..1032F; Old Italic\n10330..1034F; Gothic\n10350..1037F; Old Permic\n10380..1039F; Ugaritic\n103A0..103DF; Old Persian\n10400..1044F; Deseret\n10450..1047F; Shavian\n10480..104AF; Osmanya\n10500..1052F; Elbasan\n10530..1056F; Caucasian Albanian\n10600..1077F; Linear A\n10800..1083F; Cypriot Syllabary\n10840..1085F; Imperial Aramaic\n10860..1087F; Palmyrene\n10880..108AF; Nabataean\n108E0..108FF; Hatran\n10900..1091F; Phoenician\n10920..1093F; Lydian\n10980..1099F; Meroitic Hieroglyphs\n109A0..109FF; Meroitic Cursive\n10A00..10A5F; Kharoshthi\n10A60..10A7F; Old South Arabian\n10A80..10A9F; Old North Arabian\n10AC0..10AFF; Manichaean\n10B00..10B3F; Avestan\n10B40..10B5F; Inscriptional Parthian\n10B60..10B7F; Inscriptional Pahlavi\n10B80..10BAF; Psalter Pahlavi\n10C00..10C4F; Old Turkic\n10C80..10CFF; Old Hungarian\n10E60..10E7F; Rumi Numeral Symbols\n11000..1107F; Brahmi\n11080..110CF; Kaithi\n110D0..110FF; Sora Sompeng\n11100..1114F; Chakma\n11150..1117F; Mahajani\n11180..111DF; Sharada\n111E0..111FF; Sinhala Archaic Numbers\n11200..1124F; Khojki\n11280..112AF; Multani\n112B0..112FF; Khudawadi\n11300..1137F; Grantha\n11480..114DF; Tirhuta\n11580..115FF; Siddham\n11600..1165F; Modi\n11680..116CF; Takri\n11700..1173F; Ahom\n118A0..118FF; Warang Citi\n11AC0..11AFF; Pau Cin Hau\n12000..123FF; Cuneiform\n12400..1247F; Cuneiform Numbers and Punctuation\n12480..1254F; Early Dynastic Cuneiform\n13000..1342F; Egyptian Hieroglyphs\n14400..1467F; Anatolian Hieroglyphs\n16800..16A3F; Bamum Supplement\n16A40..16A6F; Mro\n16AD0..16AFF; Bassa Vah\n16B00..16B8F; Pahawh Hmong\n16F00..16F9F; Miao\n1B000..1B0FF; Kana Supplement\n1BC00..1BC9F; Duployan\n1BCA0..1BCAF; Shorthand Format Controls\n1D000..1D0FF; Byzantine Musical Symbols\n1D100..1D1FF; Musical Symbols\n1D200..1D24F; Ancient Greek Musical Notation\n1D300..1D35F; Tai Xuan Jing Symbols\n1D360..1D37F; Counting Rod Numerals\n1D400..1D7FF; Mathematical Alphanumeric Symbols\n1D800..1DAAF; Sutton SignWriting\n1E800..1E8DF; Mende Kikakui\n1EE00..1EEFF; Arabic Mathematical Alphabetic Symbols\n1F000..1F02F; Mahjong Tiles\n1F030..1F09F; Domino Tiles\n1F0A0..1F0FF; Playing Cards\n1F100..1F1FF; Enclosed Alphanumeric Supplement\n1F200..1F2FF; Enclosed Ideographic Supplement\n1F300..1F5FF; Miscellaneous Symbols and Pictographs\n1F600..1F64F; Emoticons\n1F650..1F67F; Ornamental Dingbats\n1F680..1F6FF; Transport and Map Symbols\n1F700..1F77F; Alchemical Symbols\n1F780..1F7FF; Geometric Shapes Extended\n1F800..1F8FF; Supplemental Arrows-C\n1F900..1F9FF; Supplemental Symbols and Pictographs\n20000..2A6DF; CJK Unified Ideographs Extension B\n2A700..2B73F; CJK Unified Ideographs Extension C\n2B740..2B81F; CJK Unified Ideographs Extension D\n2B820..2CEAF; CJK Unified Ideographs Extension E\n2F800..2FA1F; CJK Compatibility Ideographs Supplement\nE0000..E007F; Tags\nE0100..E01EF; Variation Selectors Supplement\nF0000..FFFFF; Supplementary Private Use Area-A\n100000..10FFFF; Supplementary Private Use Area-B\n\n# EOF')
if __name__ == '__main__':
    print indexfromname('Private Use Area')
    print block('a')
    print block(unichr(57344))
    print block(unichr(63743))
    print block(unichr(65536))
    print block(unichr(1114111))