# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\biffh.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function
DEBUG = 0
from struct import unpack
import sys
from .timemachine import *

class XLRDError(Exception):
    pass


class BaseObject(object):
    _repr_these = []

    def dump(self, f=None, header=None, footer=None, indent=0):
        if f is None:
            f = sys.stderr
        if hasattr(self, '__slots__'):
            alist = []
            for attr in self.__slots__:
                alist.append((attr, getattr(self, attr)))

        else:
            alist = self.__dict__.items()
        alist = sorted(alist)
        pad = ' ' * indent
        if header is not None:
            print(header, file=f)
        list_type = type([])
        dict_type = type({})
        for attr, value in alist:
            if getattr(value, 'dump', None) and attr != 'book':
                value.dump(f, header='%s%s (%s object):' % (pad, attr, value.__class__.__name__), indent=indent + 4)
            elif attr not in self._repr_these and (isinstance(value, list_type) or isinstance(value, dict_type)):
                print('%s%s: %s, len = %d' % (pad, attr, type(value), len(value)), file=f)
            else:
                fprintf(f, '%s%s: %r\n', pad, attr, value)

        if footer is not None:
            print(footer, file=f)
        return


FUN, FDT, FNU, FGE, FTX = range(5)
DATEFORMAT = FDT
NUMBERFORMAT = FNU
XL_CELL_EMPTY, XL_CELL_TEXT, XL_CELL_NUMBER, XL_CELL_DATE, XL_CELL_BOOLEAN, XL_CELL_ERROR, XL_CELL_BLANK = range(7)
biff_text_from_num = {0: '(not BIFF)', 
   20: '2.0', 
   21: '2.1', 
   30: '3', 
   40: '4S', 
   45: '4W', 
   50: '5', 
   70: '7', 
   80: '8', 
   85: '8X'}
error_text_from_code = {0: '#NULL!', 
   7: '#DIV/0!', 
   15: '#VALUE!', 
   23: '#REF!', 
   29: '#NAME?', 
   36: '#NUM!', 
   42: '#N/A'}
BIFF_FIRST_UNICODE = 80
XL_WORKBOOK_GLOBALS = WBKBLOBAL = 5
XL_WORKBOOK_GLOBALS_4W = 256
XL_WORKSHEET = WRKSHEET = 16
XL_BOUNDSHEET_WORKSHEET = 0
XL_BOUNDSHEET_CHART = 2
XL_BOUNDSHEET_VB_MODULE = 6
XL_ARRAY = 545
XL_ARRAY2 = 33
XL_BLANK = 513
XL_BLANK_B2 = 1
XL_BOF = 2057
XL_BOOLERR = 517
XL_BOOLERR_B2 = 5
XL_BOUNDSHEET = 133
XL_BUILTINFMTCOUNT = 86
XL_CF = 433
XL_CODEPAGE = 66
XL_COLINFO = 125
XL_COLUMNDEFAULT = 32
XL_COLWIDTH = 36
XL_CONDFMT = 432
XL_CONTINUE = 60
XL_COUNTRY = 140
XL_DATEMODE = 34
XL_DEFAULTROWHEIGHT = 549
XL_DEFCOLWIDTH = 85
XL_DIMENSION = 512
XL_DIMENSION2 = 0
XL_EFONT = 69
XL_EOF = 10
XL_EXTERNNAME = 35
XL_EXTERNSHEET = 23
XL_EXTSST = 255
XL_FEAT11 = 2162
XL_FILEPASS = 47
XL_FONT = 49
XL_FONT_B3B4 = 561
XL_FORMAT = 1054
XL_FORMAT2 = 30
XL_FORMULA = 6
XL_FORMULA3 = 518
XL_FORMULA4 = 1030
XL_GCW = 171
XL_HLINK = 440
XL_QUICKTIP = 2048
XL_HORIZONTALPAGEBREAKS = 27
XL_INDEX = 523
XL_INTEGER = 2
XL_IXFE = 68
XL_LABEL = 516
XL_LABEL_B2 = 4
XL_LABELRANGES = 351
XL_LABELSST = 253
XL_LEFTMARGIN = 38
XL_TOPMARGIN = 40
XL_RIGHTMARGIN = 39
XL_BOTTOMMARGIN = 41
XL_HEADER = 20
XL_FOOTER = 21
XL_HCENTER = 131
XL_VCENTER = 132
XL_MERGEDCELLS = 229
XL_MSO_DRAWING = 236
XL_MSO_DRAWING_GROUP = 235
XL_MSO_DRAWING_SELECTION = 237
XL_MULRK = 189
XL_MULBLANK = 190
XL_NAME = 24
XL_NOTE = 28
XL_NUMBER = 515
XL_NUMBER_B2 = 3
XL_OBJ = 93
XL_PAGESETUP = 161
XL_PALETTE = 146
XL_PANE = 65
XL_PRINTGRIDLINES = 43
XL_PRINTHEADERS = 42
XL_RK = 638
XL_ROW = 520
XL_ROW_B2 = 8
XL_RSTRING = 214
XL_SCL = 160
XL_SHEETHDR = 143
XL_SHEETPR = 129
XL_SHEETSOFFSET = 142
XL_SHRFMLA = 1212
XL_SST = 252
XL_STANDARDWIDTH = 153
XL_STRING = 519
XL_STRING_B2 = 7
XL_STYLE = 659
XL_SUPBOOK = 430
XL_TABLEOP = 566
XL_TABLEOP2 = 55
XL_TABLEOP_B2 = 54
XL_TXO = 438
XL_UNCALCED = 94
XL_UNKNOWN = 65535
XL_VERTICALPAGEBREAKS = 26
XL_WINDOW2 = 574
XL_WINDOW2_B2 = 62
XL_WRITEACCESS = 92
XL_WSBOOL = XL_SHEETPR
XL_XF = 224
XL_XF2 = 67
XL_XF3 = 579
XL_XF4 = 1091
boflen = {2057: 8, 1033: 6, 521: 6, 9: 4}
bofcodes = (2057, 1033, 521, 9)
XL_FORMULA_OPCODES = (6, 1030, 518)
_cell_opcode_list = [
 XL_BOOLERR,
 XL_FORMULA,
 XL_FORMULA3,
 XL_FORMULA4,
 XL_LABEL,
 XL_LABELSST,
 XL_MULRK,
 XL_NUMBER,
 XL_RK,
 XL_RSTRING]
_cell_opcode_dict = {}
for _cell_opcode in _cell_opcode_list:
    _cell_opcode_dict[_cell_opcode] = 1

def is_cell_opcode(c):
    return c in _cell_opcode_dict


def upkbits(tgt_obj, src, manifest, local_setattr=setattr):
    for n, mask, attr in manifest:
        local_setattr(tgt_obj, attr, (src & mask) >> n)


def upkbitsL(tgt_obj, src, manifest, local_setattr=setattr, local_int=int):
    for n, mask, attr in manifest:
        local_setattr(tgt_obj, attr, local_int((src & mask) >> n))


def unpack_string(data, pos, encoding, lenlen=1):
    nchars = unpack('<' + 'BH'[(lenlen - 1)], data[pos:pos + lenlen])[0]
    pos += lenlen
    return unicode(data[pos:pos + nchars], encoding)


def unpack_string_update_pos(data, pos, encoding, lenlen=1, known_len=None):
    if known_len is not None:
        nchars = known_len
    else:
        nchars = unpack('<' + 'BH'[(lenlen - 1)], data[pos:pos + lenlen])[0]
        pos += lenlen
    newpos = pos + nchars
    return (unicode(data[pos:newpos], encoding), newpos)


def unpack_unicode(data, pos, lenlen=2):
    """Return unicode_strg"""
    nchars = unpack('<' + 'BH'[(lenlen - 1)], data[pos:pos + lenlen])[0]
    if not nchars:
        return UNICODE_LITERAL('')
    pos += lenlen
    options = BYTES_ORD(data[pos])
    pos += 1
    if options & 8:
        pos += 2
    if options & 4:
        pos += 4
    if options & 1:
        rawstrg = data[pos:pos + 2 * nchars]
        strg = unicode(rawstrg, 'utf_16_le')
    else:
        strg = unicode(data[pos:pos + nchars], 'latin_1')
    return strg


def unpack_unicode_update_pos(data, pos, lenlen=2, known_len=None):
    """Return (unicode_strg, updated value of pos)"""
    if known_len is not None:
        nchars = known_len
    else:
        nchars = unpack('<' + 'BH'[(lenlen - 1)], data[pos:pos + lenlen])[0]
        pos += lenlen
    if not nchars and not data[pos:]:
        return (
         UNICODE_LITERAL(''), pos)
    else:
        options = BYTES_ORD(data[pos])
        pos += 1
        phonetic = options & 4
        richtext = options & 8
        if richtext:
            rt = unpack('<H', data[pos:pos + 2])[0]
            pos += 2
        if phonetic:
            sz = unpack('<i', data[pos:pos + 4])[0]
            pos += 4
        if options & 1:
            strg = unicode(data[pos:pos + 2 * nchars], 'utf_16_le')
            pos += 2 * nchars
        else:
            strg = unicode(data[pos:pos + nchars], 'latin_1')
            pos += nchars
        if richtext:
            pos += 4 * rt
        if phonetic:
            pos += sz
        return (
         strg, pos)


def unpack_cell_range_address_list_update_pos(output_list, data, pos, biff_version, addr_size=6):
    assert addr_size in (6, 8)
    n, = unpack('<H', data[pos:pos + 2])
    pos += 2
    if n:
        if addr_size == 6:
            fmt = '<HHBB'
        else:
            fmt = '<HHHH'
        for _unused in xrange(n):
            ra, rb, ca, cb = unpack(fmt, data[pos:pos + addr_size])
            output_list.append((ra, rb + 1, ca, cb + 1))
            pos += addr_size

    return pos


_brecstrg = '0000 DIMENSIONS_B2\n0001 BLANK_B2\n0002 INTEGER_B2_ONLY\n0003 NUMBER_B2\n0004 LABEL_B2\n0005 BOOLERR_B2\n0006 FORMULA\n0007 STRING_B2\n0008 ROW_B2\n0009 BOF_B2\n000A EOF\n000B INDEX_B2_ONLY\n000C CALCCOUNT\n000D CALCMODE\n000E PRECISION\n000F REFMODE\n0010 DELTA\n0011 ITERATION\n0012 PROTECT\n0013 PASSWORD\n0014 HEADER\n0015 FOOTER\n0016 EXTERNCOUNT\n0017 EXTERNSHEET\n0018 NAME_B2,5+\n0019 WINDOWPROTECT\n001A VERTICALPAGEBREAKS\n001B HORIZONTALPAGEBREAKS\n001C NOTE\n001D SELECTION\n001E FORMAT_B2-3\n001F BUILTINFMTCOUNT_B2\n0020 COLUMNDEFAULT_B2_ONLY\n0021 ARRAY_B2_ONLY\n0022 DATEMODE\n0023 EXTERNNAME\n0024 COLWIDTH_B2_ONLY\n0025 DEFAULTROWHEIGHT_B2_ONLY\n0026 LEFTMARGIN\n0027 RIGHTMARGIN\n0028 TOPMARGIN\n0029 BOTTOMMARGIN\n002A PRINTHEADERS\n002B PRINTGRIDLINES\n002F FILEPASS\n0031 FONT\n0032 FONT2_B2_ONLY\n0036 TABLEOP_B2\n0037 TABLEOP2_B2\n003C CONTINUE\n003D WINDOW1\n003E WINDOW2_B2\n0040 BACKUP\n0041 PANE\n0042 CODEPAGE\n0043 XF_B2\n0044 IXFE_B2_ONLY\n0045 EFONT_B2_ONLY\n004D PLS\n0051 DCONREF\n0055 DEFCOLWIDTH\n0056 BUILTINFMTCOUNT_B3-4\n0059 XCT\n005A CRN\n005B FILESHARING\n005C WRITEACCESS\n005D OBJECT\n005E UNCALCED\n005F SAVERECALC\n0063 OBJECTPROTECT\n007D COLINFO\n007E RK2_mythical_?\n0080 GUTS\n0081 WSBOOL\n0082 GRIDSET\n0083 HCENTER\n0084 VCENTER\n0085 BOUNDSHEET\n0086 WRITEPROT\n008C COUNTRY\n008D HIDEOBJ\n008E SHEETSOFFSET\n008F SHEETHDR\n0090 SORT\n0092 PALETTE\n0099 STANDARDWIDTH\n009B FILTERMODE\n009C FNGROUPCOUNT\n009D AUTOFILTERINFO\n009E AUTOFILTER\n00A0 SCL\n00A1 SETUP\n00AB GCW\n00BD MULRK\n00BE MULBLANK\n00C1 MMS\n00D6 RSTRING\n00D7 DBCELL\n00DA BOOKBOOL\n00DD SCENPROTECT\n00E0 XF\n00E1 INTERFACEHDR\n00E2 INTERFACEEND\n00E5 MERGEDCELLS\n00E9 BITMAP\n00EB MSO_DRAWING_GROUP\n00EC MSO_DRAWING\n00ED MSO_DRAWING_SELECTION\n00EF PHONETIC\n00FC SST\n00FD LABELSST\n00FF EXTSST\n013D TABID\n015F LABELRANGES\n0160 USESELFS\n0161 DSF\n01AE SUPBOOK\n01AF PROTECTIONREV4\n01B0 CONDFMT\n01B1 CF\n01B2 DVAL\n01B6 TXO\n01B7 REFRESHALL\n01B8 HLINK\n01BC PASSWORDREV4\n01BE DV\n01C0 XL9FILE\n01C1 RECALCID\n0200 DIMENSIONS\n0201 BLANK\n0203 NUMBER\n0204 LABEL\n0205 BOOLERR\n0206 FORMULA_B3\n0207 STRING\n0208 ROW\n0209 BOF\n020B INDEX_B3+\n0218 NAME\n0221 ARRAY\n0223 EXTERNNAME_B3-4\n0225 DEFAULTROWHEIGHT\n0231 FONT_B3B4\n0236 TABLEOP\n023E WINDOW2\n0243 XF_B3\n027E RK\n0293 STYLE\n0406 FORMULA_B4\n0409 BOF\n041E FORMAT\n0443 XF_B4\n04BC SHRFMLA\n0800 QUICKTIP\n0809 BOF\n0862 SHEETLAYOUT\n0867 SHEETPROTECTION\n0868 RANGEPROTECTION\n'
biff_rec_name_dict = {}
for _buff in _brecstrg.splitlines():
    _numh, _name = _buff.split()
    biff_rec_name_dict[int(_numh, 16)] = _name

del _buff
del _name
del _brecstrg

def hex_char_dump(strg, ofs, dlen, base=0, fout=sys.stdout, unnumbered=False):
    endpos = min(ofs + dlen, len(strg))
    pos = ofs
    numbered = not unnumbered
    num_prefix = ''
    while pos < endpos:
        endsub = min(pos + 16, endpos)
        substrg = strg[pos:endsub]
        lensub = endsub - pos
        if lensub <= 0 or lensub != len(substrg):
            fprintf(sys.stdout, '??? hex_char_dump: ofs=%d dlen=%d base=%d -> endpos=%d pos=%d endsub=%d substrg=%r\n', ofs, dlen, base, endpos, pos, endsub, substrg)
            break
        hexd = ('').join([ '%02x ' % BYTES_ORD(c) for c in substrg ])
        chard = ''
        for c in substrg:
            c = chr(BYTES_ORD(c))
            if c == '\x00':
                c = '~'
            elif not ' ' <= c <= '~':
                c = '?'
            chard += c

        if numbered:
            num_prefix = '%5d: ' % (base + pos - ofs)
        fprintf(fout, '%s     %-48s %s\n', num_prefix, hexd, chard)
        pos = endsub


def biff_dump(mem, stream_offset, stream_len, base=0, fout=sys.stdout, unnumbered=False):
    pos = stream_offset
    stream_end = stream_offset + stream_len
    adj = base - stream_offset
    dummies = 0
    numbered = not unnumbered
    num_prefix = ''
    while stream_end - pos >= 4:
        rc, length = unpack('<HH', mem[pos:pos + 4])
        if rc == 0 and length == 0:
            if mem[pos:] == '\x00' * (stream_end - pos):
                dummies = stream_end - pos
                savpos = pos
                pos = stream_end
                break
            if dummies:
                dummies += 4
            else:
                savpos = pos
                dummies = 4
            pos += 4
        else:
            if dummies:
                if numbered:
                    num_prefix = '%5d: ' % (adj + savpos)
                fprintf(fout, '%s---- %d zero bytes skipped ----\n', num_prefix, dummies)
                dummies = 0
            recname = biff_rec_name_dict.get(rc, '<UNKNOWN>')
            if numbered:
                num_prefix = '%5d: ' % (adj + pos)
            fprintf(fout, '%s%04x %s len = %04x (%d)\n', num_prefix, rc, recname, length, length)
            pos += 4
            hex_char_dump(mem, pos, length, adj + pos, fout, unnumbered)
            pos += length

    if dummies:
        if numbered:
            num_prefix = '%5d: ' % (adj + savpos)
        fprintf(fout, '%s---- %d zero bytes skipped ----\n', num_prefix, dummies)
    if pos < stream_end:
        if numbered:
            num_prefix = '%5d: ' % (adj + pos)
        fprintf(fout, '%s---- Misc bytes at end ----\n', num_prefix)
        hex_char_dump(mem, pos, stream_end - pos, adj + pos, fout, unnumbered)
    elif pos > stream_end:
        fprintf(fout, 'Last dumped record has length (%d) that is too large\n', length)


def biff_count_records(mem, stream_offset, stream_len, fout=sys.stdout):
    pos = stream_offset
    stream_end = stream_offset + stream_len
    tally = {}
    while stream_end - pos >= 4:
        rc, length = unpack('<HH', mem[pos:pos + 4])
        if rc == 0 and length == 0:
            if mem[pos:] == '\x00' * (stream_end - pos):
                break
            recname = '<Dummy (zero)>'
        else:
            recname = biff_rec_name_dict.get(rc, None)
            if recname is None:
                recname = 'Unknown_0x%04X' % rc
        if recname in tally:
            tally[recname] += 1
        else:
            tally[recname] = 1
        pos += length + 4

    slist = sorted(tally.items())
    for recname, count in slist:
        print('%8d %s' % (count, recname), file=fout)

    return


encoding_from_codepage = {1200: 'utf_16_le', 
   10000: 'mac_roman', 
   10006: 'mac_greek', 
   10007: 'mac_cyrillic', 
   10029: 'mac_latin2', 
   10079: 'mac_iceland', 
   10081: 'mac_turkish', 
   32768: 'mac_roman', 
   32769: 'cp1252'}