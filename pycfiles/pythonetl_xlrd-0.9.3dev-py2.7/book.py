# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\book.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function
from .timemachine import *
from .biffh import *
import struct
unpack = struct.unpack
import sys, time
from . import sheet
from . import compdoc
from .formula import *
from . import formatting
if sys.version.startswith('IronPython'):
    import encodings
empty_cell = sheet.empty_cell
DEBUG = 0
USE_FANCY_CD = 1
TOGGLE_GC = 0
import gc
try:
    import mmap
    MMAP_AVAILABLE = 1
except ImportError:
    MMAP_AVAILABLE = 0

USE_MMAP = MMAP_AVAILABLE
MY_EOF = 251706026
SUPBOOK_UNK, SUPBOOK_INTERNAL, SUPBOOK_EXTERNAL, SUPBOOK_ADDIN, SUPBOOK_DDEOLE = range(5)
SUPPORTED_VERSIONS = (
 80, 70, 50, 45, 40, 30, 21, 20)
_code_from_builtin_name = {'Consolidate_Area': '\x00', 
   'Auto_Open': '\x01', 
   'Auto_Close': '\x02', 
   'Extract': '\x03', 
   'Database': '\x04', 
   'Criteria': '\x05', 
   'Print_Area': '\x06', 
   'Print_Titles': '\x07', 
   'Recorder': '\x08', 
   'Data_Form': '\t', 
   'Auto_Activate': '\n', 
   'Auto_Deactivate': '\x0b', 
   'Sheet_Title': '\x0c', 
   '_FilterDatabase': '\r'}
builtin_name_from_code = {}
code_from_builtin_name = {}
for _bin, _bic in _code_from_builtin_name.items():
    _bin = UNICODE_LITERAL(_bin)
    _bic = UNICODE_LITERAL(_bic)
    code_from_builtin_name[_bin] = _bic
    builtin_name_from_code[_bic] = _bin

del _bin
del _bic
del _code_from_builtin_name

def open_workbook_xls(filename=None, logfile=sys.stdout, verbosity=0, use_mmap=USE_MMAP, file_contents=None, encoding_override=None, formatting_info=False, on_demand=False, ragged_rows=False):
    t0 = time.clock()
    if TOGGLE_GC:
        orig_gc_enabled = gc.isenabled()
        if orig_gc_enabled:
            gc.disable()
    bk = Book()
    try:
        bk.biff2_8_load(filename=filename, file_contents=file_contents, logfile=logfile, verbosity=verbosity, use_mmap=use_mmap, encoding_override=encoding_override, formatting_info=formatting_info, on_demand=on_demand, ragged_rows=ragged_rows)
        t1 = time.clock()
        bk.load_time_stage_1 = t1 - t0
        biff_version = bk.getbof(XL_WORKBOOK_GLOBALS)
        if not biff_version:
            raise XLRDError("Can't determine file's BIFF version")
        if biff_version not in SUPPORTED_VERSIONS:
            raise XLRDError('BIFF version %s is not supported' % biff_text_from_num[biff_version])
        bk.biff_version = biff_version
        if biff_version <= 40:
            if on_demand:
                fprintf(bk.logfile, '*** WARNING: on_demand is not supported for this Excel version.\n*** Setting on_demand to False.\n')
                bk.on_demand = on_demand = False
            bk.fake_globals_get_sheet()
        elif biff_version == 45:
            bk.parse_globals()
            if on_demand:
                fprintf(bk.logfile, '*** WARNING: on_demand is not supported for this Excel version.\n*** Setting on_demand to False.\n')
                bk.on_demand = on_demand = False
        else:
            bk.parse_globals()
            bk._sheet_list = [ None for sh in bk._sheet_names ]
            if not on_demand:
                bk.get_sheets()
        bk.nsheets = len(bk._sheet_list)
        if biff_version == 45 and bk.nsheets > 1:
            fprintf(bk.logfile, '*** WARNING: Excel 4.0 workbook (.XLW) file contains %d worksheets.\n*** Book-level data will be that of the last worksheet.\n', bk.nsheets)
        if TOGGLE_GC:
            if orig_gc_enabled:
                gc.enable()
        t2 = time.clock()
        bk.load_time_stage_2 = t2 - t1
    except:
        bk.release_resources()
        raise

    if not on_demand:
        bk.release_resources()
    return bk


def dump(filename, outfile=sys.stdout, unnumbered=False):
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile)
    biff_dump(bk.mem, bk.base, bk.stream_len, 0, outfile, unnumbered)


def count_records(filename, outfile=sys.stdout):
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile)
    biff_count_records(bk.mem, bk.base, bk.stream_len, outfile)


class Name(BaseObject):
    _repr_these = [
     'stack']
    book = None
    hidden = 0
    func = 0
    vbasic = 0
    macro = 0
    complex = 0
    builtin = 0
    funcgroup = 0
    binary = 0
    name_index = 0
    name = UNICODE_LITERAL('')
    raw_formula = ''
    scope = -1
    result = None

    def cell(self):
        res = self.result
        if res:
            kind = res.kind
            value = res.value
            if kind == oREF and len(value) == 1:
                ref3d = value[0]
                if 0 <= ref3d.shtxlo == ref3d.shtxhi - 1 and ref3d.rowxlo == ref3d.rowxhi - 1 and ref3d.colxlo == ref3d.colxhi - 1:
                    sh = self.book.sheet_by_index(ref3d.shtxlo)
                    return sh.cell(ref3d.rowxlo, ref3d.colxlo)
        self.dump(self.book.logfile, header='=== Dump of Name object ===', footer='======= End of dump =======')
        raise XLRDError('Not a constant absolute reference to a single cell')

    def area2d(self, clipped=True):
        res = self.result
        if res:
            kind = res.kind
            value = res.value
            if kind == oREF and len(value) == 1:
                ref3d = value[0]
                if 0 <= ref3d.shtxlo == ref3d.shtxhi - 1:
                    sh = self.book.sheet_by_index(ref3d.shtxlo)
                    return clipped or (
                     sh, ref3d.rowxlo, ref3d.rowxhi, ref3d.colxlo, ref3d.colxhi)
                rowxlo = min(ref3d.rowxlo, sh.nrows)
                rowxhi = max(rowxlo, min(ref3d.rowxhi, sh.nrows))
                colxlo = min(ref3d.colxlo, sh.ncols)
                colxhi = max(colxlo, min(ref3d.colxhi, sh.ncols))
                assert 0 <= rowxlo <= rowxhi <= sh.nrows
                if not 0 <= colxlo <= colxhi <= sh.ncols:
                    raise AssertionError
                    return (
                     sh, rowxlo, rowxhi, colxlo, colxhi)
        self.dump(self.book.logfile, header='=== Dump of Name object ===', footer='======= End of dump =======')
        raise XLRDError('Not a constant absolute reference to a single area in a single sheet')


class Book(BaseObject):
    nsheets = 0
    datemode = 0
    biff_version = 0
    name_obj_list = []
    codepage = None
    encoding = None
    countries = (0, 0)
    user_name = UNICODE_LITERAL('')
    font_list = []
    xf_list = []
    format_list = []
    format_map = {}
    style_name_map = {}
    colour_map = {}
    palette_record = []
    load_time_stage_1 = -1.0
    load_time_stage_2 = -1.0

    def sheets(self):
        for sheetx in xrange(self.nsheets):
            if not self._sheet_list[sheetx]:
                self.get_sheet(sheetx)

        return self._sheet_list[:]

    def sheet_by_index(self, sheetx):
        return self._sheet_list[sheetx] or self.get_sheet(sheetx)

    def sheet_by_name(self, sheet_name):
        try:
            sheetx = self._sheet_names.index(sheet_name)
        except ValueError:
            raise XLRDError('No sheet named <%r>' % sheet_name)

        return self.sheet_by_index(sheetx)

    def sheet_names(self):
        return self._sheet_names[:]

    def sheet_loaded(self, sheet_name_or_index):
        if isinstance(sheet_name_or_index, type(1)):
            sheetx = sheet_name_or_index
        else:
            try:
                sheetx = self._sheet_names.index(sheet_name_or_index)
            except ValueError:
                raise XLRDError('No sheet named <%r>' % sheet_name_or_index)

        return self._sheet_list[sheetx] and True or False

    def unload_sheet(self, sheet_name_or_index):
        if isinstance(sheet_name_or_index, type(1)):
            sheetx = sheet_name_or_index
        else:
            try:
                sheetx = self._sheet_names.index(sheet_name_or_index)
            except ValueError:
                raise XLRDError('No sheet named <%r>' % sheet_name_or_index)

        self._sheet_list[sheetx] = None
        return

    def release_resources(self):
        self._resources_released = 1
        if hasattr(self.mem, 'close'):
            self.mem.close()
        self.mem = None
        if hasattr(self.filestr, 'close'):
            self.filestr.close()
        self.filestr = None
        self._sharedstrings = None
        self._rich_text_runlist_map = None
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.release_resources()

    name_and_scope_map = {}
    name_map = {}

    def __init__(self):
        self._sheet_list = []
        self._sheet_names = []
        self._sheet_visibility = []
        self.nsheets = 0
        self._sh_abs_posn = []
        self._sharedstrings = []
        self._rich_text_runlist_map = {}
        self.raw_user_name = False
        self._sheethdr_count = 0
        self.builtinfmtcount = -1
        self.initialise_format_info()
        self._all_sheets_count = 0
        self._supbook_count = 0
        self._supbook_locals_inx = None
        self._supbook_addins_inx = None
        self._all_sheets_map = []
        self._externsheet_info = []
        self._externsheet_type_b57 = []
        self._extnsht_name_from_num = {}
        self._sheet_num_from_name = {}
        self._extnsht_count = 0
        self._supbook_types = []
        self._resources_released = 0
        self.addin_func_names = []
        self.name_obj_list = []
        self.colour_map = {}
        self.palette_record = []
        self.xf_list = []
        self.style_name_map = {}
        self.mem = ''
        self.filestr = ''
        return

    def biff2_8_load(self, filename=None, file_contents=None, logfile=sys.stdout, verbosity=0, use_mmap=USE_MMAP, encoding_override=None, formatting_info=False, on_demand=False, ragged_rows=False):
        self.logfile = logfile
        self.verbosity = verbosity
        self.use_mmap = use_mmap and MMAP_AVAILABLE
        self.encoding_override = encoding_override
        self.formatting_info = formatting_info
        self.on_demand = on_demand
        self.ragged_rows = ragged_rows
        if not file_contents:
            if python_version < (2, 2) and self.use_mmap:
                open_mode = 'r+b'
            else:
                open_mode = 'rb'
            retry = False
            f = None
            try:
                try:
                    f = open(filename, open_mode)
                except IOError:
                    e, v = sys.exc_info()[:2]
                    if open_mode == 'r+b' and (v.errno == 13 or v.strerror == 'Permission denied'):
                        retry = True
                        self.use_mmap = False
                    else:
                        raise

                if retry:
                    f = open(filename, 'rb')
                f.seek(0, 2)
                size = f.tell()
                f.seek(0, 0)
                if size == 0:
                    raise XLRDError('File size is 0 bytes')
                if self.use_mmap:
                    if python_version < (2, 2):
                        self.filestr = mmap.mmap(f.fileno(), size)
                    else:
                        self.filestr = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)
                    self.stream_len = size
                else:
                    self.filestr = f.read()
                    self.stream_len = len(self.filestr)
            finally:
                if f:
                    f.close()

        else:
            self.filestr = file_contents
            self.stream_len = len(file_contents)
        self.base = 0
        if self.filestr[:8] != compdoc.SIGNATURE:
            self.mem = self.filestr
        else:
            cd = compdoc.CompDoc(self.filestr, logfile=self.logfile)
            if USE_FANCY_CD:
                for qname in ['Workbook', 'Book']:
                    self.mem, self.base, self.stream_len = cd.locate_named_stream(UNICODE_LITERAL(qname))
                    if self.mem:
                        break
                else:
                    raise XLRDError("Can't find workbook in OLE2 compound document")

            else:
                for qname in ['Workbook', 'Book']:
                    self.mem = cd.get_named_stream(UNICODE_LITERAL(qname))
                    if self.mem:
                        break
                else:
                    raise XLRDError("Can't find workbook in OLE2 compound document")

            self.stream_len = len(self.mem)
        del cd
        if self.mem is not self.filestr:
            if hasattr(self.filestr, 'close'):
                self.filestr.close()
            self.filestr = ''
        self._position = self.base
        if DEBUG:
            print('mem: %s, base: %d, len: %d' % (type(self.mem), self.base, self.stream_len), file=self.logfile)
        return

    def initialise_format_info(self):
        self.format_map = {}
        self.format_list = []
        self.xfcount = 0
        self.actualfmtcount = 0
        self._xf_index_to_xl_type_map = {0: XL_CELL_NUMBER}
        self._xf_epilogue_done = 0
        self.xf_list = []
        self.font_list = []

    def get2bytes(self):
        pos = self._position
        buff_two = self.mem[pos:pos + 2]
        lenbuff = len(buff_two)
        self._position += lenbuff
        if lenbuff < 2:
            return MY_EOF
        lo, hi = buff_two
        return BYTES_ORD(hi) << 8 | BYTES_ORD(lo)

    def get_record_parts(self):
        pos = self._position
        mem = self.mem
        code, length = unpack('<HH', mem[pos:pos + 4])
        pos += 4
        data = mem[pos:pos + length]
        self._position = pos + length
        return (code, length, data)

    def get_record_parts_conditional(self, reqd_record):
        pos = self._position
        mem = self.mem
        code, length = unpack('<HH', mem[pos:pos + 4])
        if code != reqd_record:
            return (None, 0, '')
        else:
            pos += 4
            data = mem[pos:pos + length]
            self._position = pos + length
            return (code, length, data)

    def get_sheet(self, sh_number, update_pos=True):
        if self._resources_released:
            raise XLRDError("Can't load sheets after releasing resources.")
        if update_pos:
            self._position = self._sh_abs_posn[sh_number]
        _unused_biff_version = self.getbof(XL_WORKSHEET)
        sh = sheet.Sheet(self, self._position, self._sheet_names[sh_number], sh_number)
        sh.read(self)
        self._sheet_list[sh_number] = sh
        return sh

    def get_sheets(self):
        if DEBUG:
            print('GET_SHEETS:', self._sheet_names, self._sh_abs_posn, file=self.logfile)
        for sheetno in xrange(len(self._sheet_names)):
            if DEBUG:
                print('GET_SHEETS: sheetno =', sheetno, self._sheet_names, self._sh_abs_posn, file=self.logfile)
            self.get_sheet(sheetno)

    def fake_globals_get_sheet(self):
        formatting.initialise_book(self)
        fake_sheet_name = UNICODE_LITERAL('Sheet 1')
        self._sheet_names = [fake_sheet_name]
        self._sh_abs_posn = [0]
        self._sheet_visibility = [0]
        self._sheet_list.append(None)
        self.get_sheets()
        return

    def handle_boundsheet(self, data):
        bv = self.biff_version
        self.derive_encoding()
        if DEBUG:
            fprintf(self.logfile, 'BOUNDSHEET: bv=%d data %r\n', bv, data)
        if bv == 45:
            sheet_name = unpack_string(data, 0, self.encoding, lenlen=1)
            visibility = 0
            sheet_type = XL_BOUNDSHEET_WORKSHEET
            if len(self._sh_abs_posn) == 0:
                abs_posn = self._sheetsoffset + self.base
            else:
                abs_posn = -1
        else:
            offset, visibility, sheet_type = unpack('<iBB', data[0:6])
            abs_posn = offset + self.base
            if bv < BIFF_FIRST_UNICODE:
                sheet_name = unpack_string(data, 6, self.encoding, lenlen=1)
            else:
                sheet_name = unpack_unicode(data, 6, lenlen=1)
        if DEBUG or self.verbosity >= 2:
            fprintf(self.logfile, 'BOUNDSHEET: inx=%d vis=%r sheet_name=%r abs_posn=%d sheet_type=0x%02x\n', self._all_sheets_count, visibility, sheet_name, abs_posn, sheet_type)
        self._all_sheets_count += 1
        if sheet_type != XL_BOUNDSHEET_WORKSHEET:
            self._all_sheets_map.append(-1)
            descr = {1: 'Macro sheet', 
               2: 'Chart', 
               6: 'Visual Basic module'}.get(sheet_type, 'UNKNOWN')
            if DEBUG or self.verbosity >= 1:
                fprintf(self.logfile, 'NOTE *** Ignoring non-worksheet data named %r (type 0x%02x = %s)\n', sheet_name, sheet_type, descr)
        else:
            snum = len(self._sheet_names)
            self._all_sheets_map.append(snum)
            self._sheet_names.append(sheet_name)
            self._sh_abs_posn.append(abs_posn)
            self._sheet_visibility.append(visibility)
            self._sheet_num_from_name[sheet_name] = snum

    def handle_builtinfmtcount(self, data):
        builtinfmtcount = unpack('<H', data[0:2])[0]
        if DEBUG:
            fprintf(self.logfile, 'BUILTINFMTCOUNT: %r\n', builtinfmtcount)
        self.builtinfmtcount = builtinfmtcount

    def derive_encoding(self):
        if self.encoding_override:
            self.encoding = self.encoding_override
        elif self.codepage is None:
            if self.biff_version < 80:
                fprintf(self.logfile, "*** No CODEPAGE record, no encoding_override: will use 'ascii'\n")
                self.encoding = 'ascii'
            else:
                self.codepage = 1200
                if self.verbosity >= 2:
                    fprintf(self.logfile, '*** No CODEPAGE record; assuming 1200 (utf_16_le)\n')
        else:
            codepage = self.codepage
            if codepage in encoding_from_codepage:
                encoding = encoding_from_codepage[codepage]
            elif 300 <= codepage <= 1999:
                encoding = 'cp' + str(codepage)
            else:
                encoding = 'unknown_codepage_' + str(codepage)
            if DEBUG or self.verbosity and encoding != self.encoding:
                fprintf(self.logfile, 'CODEPAGE: codepage %r -> encoding %r\n', codepage, encoding)
            self.encoding = encoding
        if self.codepage != 1200:
            try:
                _unused = unicode('trial', self.encoding)
            except:
                ei = sys.exc_info()[:2]
                fprintf(self.logfile, 'ERROR *** codepage %r -> encoding %r -> %s: %s\n', self.codepage, self.encoding, ei[0].__name__.split('.')[(-1)], ei[1])
                raise

        if self.raw_user_name:
            strg = unpack_string(self.user_name, 0, self.encoding, lenlen=1)
            strg = strg.rstrip()
            self.user_name = strg
            self.raw_user_name = False
        return self.encoding

    def handle_codepage(self, data):
        codepage = unpack('<H', data[0:2])[0]
        self.codepage = codepage
        self.derive_encoding()

    def handle_country(self, data):
        countries = unpack('<HH', data[0:4])
        if self.verbosity:
            print('Countries:', countries, file=self.logfile)
        assert self.countries == (0, 0) or self.countries == countries
        self.countries = countries

    def handle_datemode(self, data):
        datemode = unpack('<H', data[0:2])[0]
        if DEBUG or self.verbosity:
            fprintf(self.logfile, 'DATEMODE: datemode %r\n', datemode)
        assert datemode in (0, 1)
        self.datemode = datemode

    def handle_externname(self, data):
        blah = DEBUG or self.verbosity >= 2
        if self.biff_version >= 80:
            option_flags, other_info = unpack('<HI', data[:6])
            pos = 6
            name, pos = unpack_unicode_update_pos(data, pos, lenlen=1)
            extra = data[pos:]
            if self._supbook_types[(-1)] == SUPBOOK_ADDIN:
                self.addin_func_names.append(name)
            if blah:
                fprintf(self.logfile, 'EXTERNNAME: sbktype=%d oflags=0x%04x oinfo=0x%08x name=%r extra=%r\n', self._supbook_types[(-1)], option_flags, other_info, name, extra)

    def handle_externsheet(self, data):
        self.derive_encoding()
        self._extnsht_count += 1
        blah1 = DEBUG or self.verbosity >= 1
        blah2 = DEBUG or self.verbosity >= 2
        if self.biff_version >= 80:
            num_refs = unpack('<H', data[0:2])[0]
            bytes_reqd = num_refs * 6 + 2
            while len(data) < bytes_reqd:
                if blah1:
                    fprintf(self.logfile, 'INFO: EXTERNSHEET needs %d bytes, have %d\n', bytes_reqd, len(data))
                code2, length2, data2 = self.get_record_parts()
                if code2 != XL_CONTINUE:
                    raise XLRDError('Missing CONTINUE after EXTERNSHEET record')
                data += data2

            pos = 2
            for k in xrange(num_refs):
                info = unpack('<HHH', data[pos:pos + 6])
                ref_recordx, ref_first_sheetx, ref_last_sheetx = info
                self._externsheet_info.append(info)
                pos += 6
                if blah2:
                    fprintf(self.logfile, 'EXTERNSHEET(b8): k = %2d, record = %2d, first_sheet = %5d, last sheet = %5d\n', k, ref_recordx, ref_first_sheetx, ref_last_sheetx)

        else:
            nc, ty = unpack('<BB', data[:2])
            if blah2:
                print('EXTERNSHEET(b7-):', file=self.logfile)
                hex_char_dump(data, 0, len(data), fout=self.logfile)
                msg = {1: 'Encoded URL', 
                   2: 'Current sheet!!', 
                   3: "Specific sheet in own doc't", 
                   4: "Nonspecific sheet in own doc't!!"}.get(ty, 'Not encoded')
                print('   %3d chars, type is %d (%s)' % (nc, ty, msg), file=self.logfile)
            if ty == 3:
                sheet_name = unicode(data[2:nc + 2], self.encoding)
                self._extnsht_name_from_num[self._extnsht_count] = sheet_name
                if blah2:
                    print(self._extnsht_name_from_num, file=self.logfile)
            if not 1 <= ty <= 4:
                ty = 0
            self._externsheet_type_b57.append(ty)

    def handle_filepass(self, data):
        if self.verbosity >= 2:
            logf = self.logfile
            fprintf(logf, 'FILEPASS:\n')
            hex_char_dump(data, 0, len(data), base=0, fout=logf)
            if self.biff_version >= 80:
                kind1, = unpack('<H', data[:2])
                if kind1 == 0:
                    key, hash_value = unpack('<HH', data[2:])
                    fprintf(logf, 'weak XOR: key=0x%04x hash=0x%04x\n', key, hash_value)
                elif kind1 == 1:
                    kind2, = unpack('<H', data[4:6])
                    if kind2 == 1:
                        caption = 'BIFF8 std'
                    elif kind2 == 2:
                        caption = 'BIFF8 strong'
                    else:
                        caption = '** UNKNOWN ENCRYPTION METHOD **'
                    fprintf(logf, '%s\n', caption)
        raise XLRDError('Workbook is encrypted')

    def handle_name(self, data):
        blah = DEBUG or self.verbosity >= 2
        bv = self.biff_version
        if bv < 50:
            return
        else:
            self.derive_encoding()
            option_flags, kb_shortcut, name_len, fmla_len, extsht_index, sheet_index, menu_text_len, description_text_len, help_topic_text_len, status_bar_text_len = unpack('<HBBHHH4B', data[0:14])
            nobj = Name()
            nobj.book = self
            name_index = len(self.name_obj_list)
            nobj.name_index = name_index
            self.name_obj_list.append(nobj)
            nobj.option_flags = option_flags
            for attr, mask, nshift in (
             ('hidden', 1, 0),
             ('func', 2, 1),
             ('vbasic', 4, 2),
             ('macro', 8, 3),
             ('complex', 16, 4),
             ('builtin', 32, 5),
             ('funcgroup', 4032, 6),
             ('binary', 4096, 12)):
                setattr(nobj, attr, (option_flags & mask) >> nshift)

            macro_flag = ' M'[nobj.macro]
            if bv < 80:
                internal_name, pos = unpack_string_update_pos(data, 14, self.encoding, known_len=name_len)
            else:
                internal_name, pos = unpack_unicode_update_pos(data, 14, known_len=name_len)
            nobj.extn_sheet_num = extsht_index
            nobj.excel_sheet_index = sheet_index
            nobj.scope = None
            if blah:
                fprintf(self.logfile, 'NAME[%d]:%s oflags=%d, name_len=%d, fmla_len=%d, extsht_index=%d, sheet_index=%d, name=%r\n', name_index, macro_flag, option_flags, name_len, fmla_len, extsht_index, sheet_index, internal_name)
            name = internal_name
            if nobj.builtin:
                name = builtin_name_from_code.get(name, '??Unknown??')
                if blah:
                    print('    builtin: %s' % name, file=self.logfile)
            nobj.name = name
            nobj.raw_formula = data[pos:]
            nobj.basic_formula_len = fmla_len
            nobj.evaluated = 0
            if blah:
                nobj.dump(self.logfile, header='--- handle_name: name[%d] ---' % name_index, footer='-------------------')
            return

    def names_epilogue(self):
        blah = self.verbosity >= 2
        f = self.logfile
        if blah:
            print('+++++ names_epilogue +++++', file=f)
            print('_all_sheets_map', REPR(self._all_sheets_map), file=f)
            print('_extnsht_name_from_num', REPR(self._extnsht_name_from_num), file=f)
            print('_sheet_num_from_name', REPR(self._sheet_num_from_name), file=f)
        num_names = len(self.name_obj_list)
        for namex in range(num_names):
            nobj = self.name_obj_list[namex]
            if self.biff_version >= 80:
                sheet_index = nobj.excel_sheet_index
                if sheet_index == 0:
                    intl_sheet_index = -1
                elif 1 <= sheet_index <= len(self._all_sheets_map):
                    intl_sheet_index = self._all_sheets_map[(sheet_index - 1)]
                    if intl_sheet_index == -1:
                        intl_sheet_index = -2
                else:
                    intl_sheet_index = -3
            elif 50 <= self.biff_version <= 70:
                sheet_index = nobj.extn_sheet_num
                if sheet_index == 0:
                    intl_sheet_index = -1
                else:
                    sheet_name = self._extnsht_name_from_num[sheet_index]
                    intl_sheet_index = self._sheet_num_from_name.get(sheet_name, -2)
            nobj.scope = intl_sheet_index

        for namex in range(num_names):
            nobj = self.name_obj_list[namex]
            if nobj.macro or nobj.binary:
                continue
            if nobj.evaluated:
                continue
            evaluate_name_formula(self, nobj, namex, blah=blah)

        if self.verbosity >= 2:
            print('---------- name object dump ----------', file=f)
            for namex in range(num_names):
                nobj = self.name_obj_list[namex]
                nobj.dump(f, header='--- name[%d] ---' % namex)

            print('--------------------------------------', file=f)
        name_and_scope_map = {}
        name_map = {}
        for namex in range(num_names):
            nobj = self.name_obj_list[namex]
            name_lcase = nobj.name.lower()
            key = (name_lcase, nobj.scope)
            if key in name_and_scope_map and self.verbosity:
                fprintf(f, 'Duplicate entry %r in name_and_scope_map\n', key)
            name_and_scope_map[key] = nobj
            sort_data = (nobj.scope, namex, nobj)
            if name_lcase in name_map:
                name_map[name_lcase].append(sort_data)
            else:
                name_map[name_lcase] = [
                 sort_data]

        for key in name_map.keys():
            alist = name_map[key]
            alist.sort()
            name_map[key] = [ x[2] for x in alist ]

        self.name_and_scope_map = name_and_scope_map
        self.name_map = name_map

    def handle_obj(self, data):
        obj_type, obj_id = unpack('<HI', data[4:10])

    def handle_supbook(self, data):
        self._supbook_types.append(None)
        blah = DEBUG or self.verbosity >= 2
        if blah:
            print('SUPBOOK:', file=self.logfile)
            hex_char_dump(data, 0, len(data), fout=self.logfile)
        num_sheets = unpack('<H', data[0:2])[0]
        if blah:
            print('num_sheets = %d' % num_sheets, file=self.logfile)
        sbn = self._supbook_count
        self._supbook_count += 1
        if data[2:4] == '\x01\x04':
            self._supbook_types[-1] = SUPBOOK_INTERNAL
            self._supbook_locals_inx = self._supbook_count - 1
            if blah:
                print('SUPBOOK[%d]: internal 3D refs; %d sheets' % (sbn, num_sheets), file=self.logfile)
                print('    _all_sheets_map', self._all_sheets_map, file=self.logfile)
            return
        if data[0:4] == '\x01\x00\x01:':
            self._supbook_types[-1] = SUPBOOK_ADDIN
            self._supbook_addins_inx = self._supbook_count - 1
            if blah:
                print('SUPBOOK[%d]: add-in functions' % sbn, file=self.logfile)
            return
        url, pos = unpack_unicode_update_pos(data, 2, lenlen=2)
        if num_sheets == 0:
            self._supbook_types[-1] = SUPBOOK_DDEOLE
            if blah:
                fprintf(self.logfile, 'SUPBOOK[%d]: DDE/OLE document = %r\n', sbn, url)
            return
        self._supbook_types[-1] = SUPBOOK_EXTERNAL
        if blah:
            fprintf(self.logfile, 'SUPBOOK[%d]: url = %r\n', sbn, url)
        sheet_names = []
        for x in range(num_sheets):
            try:
                shname, pos = unpack_unicode_update_pos(data, pos, lenlen=2)
            except struct.error:
                if self.verbosity:
                    print('*** WARNING: unpack failure in sheet %d of %d in SUPBOOK record for file %r' % (
                     x, num_sheets, url), file=self.logfile)
                break

            sheet_names.append(shname)
            if blah:
                fprintf(self.logfile, '  sheetx=%d namelen=%d name=%r (next pos=%d)\n', x, len(shname), shname, pos)

        return

    def handle_sheethdr(self, data):
        self.derive_encoding()
        sheet_len = unpack('<i', data[:4])[0]
        sheet_name = unpack_string(data, 4, self.encoding, lenlen=1)
        sheetno = self._sheethdr_count
        assert sheet_name == self._sheet_names[sheetno]
        self._sheethdr_count += 1
        BOF_posn = self._position
        posn = BOF_posn - 4 - len(data)
        if DEBUG:
            fprintf(self.logfile, 'SHEETHDR %d at posn %d: len=%d name=%r\n', sheetno, posn, sheet_len, sheet_name)
        self.initialise_format_info()
        if DEBUG:
            print('SHEETHDR: xf epilogue flag is %d' % self._xf_epilogue_done, file=self.logfile)
        self._sheet_list.append(None)
        self.get_sheet(sheetno, update_pos=False)
        if DEBUG:
            print('SHEETHDR: posn after get_sheet() =', self._position, file=self.logfile)
        self._position = BOF_posn + sheet_len
        return

    def handle_sheetsoffset(self, data):
        posn = unpack('<i', data)[0]
        if DEBUG:
            print('SHEETSOFFSET:', posn, file=self.logfile)
        self._sheetsoffset = posn

    def handle_sst(self, data):
        if DEBUG:
            print('SST Processing', file=self.logfile)
            t0 = time.time()
        nbt = len(data)
        strlist = [data]
        uniquestrings = unpack('<i', data[4:8])[0]
        if DEBUG or self.verbosity >= 2:
            fprintf(self.logfile, 'SST: unique strings: %d\n', uniquestrings)
        while 1:
            code, nb, data = self.get_record_parts_conditional(XL_CONTINUE)
            if code is None:
                break
            nbt += nb
            if DEBUG >= 2:
                fprintf(self.logfile, 'CONTINUE: adding %d bytes to SST -> %d\n', nb, nbt)
            strlist.append(data)

        self._sharedstrings, rt_runlist = unpack_SST_table(strlist, uniquestrings)
        if self.formatting_info:
            self._rich_text_runlist_map = rt_runlist
        if DEBUG:
            t1 = time.time()
            print('SST processing took %.2f seconds' % (t1 - t0,), file=self.logfile)
        return

    def handle_writeaccess(self, data):
        DEBUG = 0
        if self.biff_version < 80:
            if not self.encoding:
                self.raw_user_name = True
                self.user_name = data
                return
            strg = unpack_string(data, 0, self.encoding, lenlen=1)
        else:
            strg = unpack_unicode(data, 0, lenlen=2)
        if DEBUG:
            fprintf(self.logfile, 'WRITEACCESS: %d bytes; raw=%s %r\n', len(data), self.raw_user_name, strg)
        strg = strg.rstrip()
        self.user_name = strg

    def parse_globals(self):
        formatting.initialise_book(self)
        while 1:
            rc, length, data = self.get_record_parts()
            if DEBUG:
                print('parse_globals: record code is 0x%04x' % rc, file=self.logfile)
            if rc == XL_SST:
                self.handle_sst(data)
            elif rc == XL_FONT or rc == XL_FONT_B3B4:
                self.handle_font(data)
            elif rc == XL_FORMAT:
                self.handle_format(data)
            elif rc == XL_XF:
                self.handle_xf(data)
            elif rc == XL_BOUNDSHEET:
                self.handle_boundsheet(data)
            elif rc == XL_DATEMODE:
                self.handle_datemode(data)
            elif rc == XL_CODEPAGE:
                self.handle_codepage(data)
            elif rc == XL_COUNTRY:
                self.handle_country(data)
            elif rc == XL_EXTERNNAME:
                self.handle_externname(data)
            elif rc == XL_EXTERNSHEET:
                self.handle_externsheet(data)
            elif rc == XL_FILEPASS:
                self.handle_filepass(data)
            elif rc == XL_WRITEACCESS:
                self.handle_writeaccess(data)
            elif rc == XL_SHEETSOFFSET:
                self.handle_sheetsoffset(data)
            elif rc == XL_SHEETHDR:
                self.handle_sheethdr(data)
            elif rc == XL_SUPBOOK:
                self.handle_supbook(data)
            elif rc == XL_NAME:
                self.handle_name(data)
            elif rc == XL_PALETTE:
                self.handle_palette(data)
            elif rc == XL_STYLE:
                self.handle_style(data)
            elif rc & 255 == 9 and self.verbosity:
                fprintf(self.logfile, '*** Unexpected BOF at posn %d: 0x%04x len=%d data=%r\n', self._position - length - 4, rc, length, data)
            elif rc == XL_EOF:
                self.xf_epilogue()
                self.names_epilogue()
                self.palette_epilogue()
                if not self.encoding:
                    self.derive_encoding()
                if self.biff_version == 45:
                    if DEBUG:
                        print('global EOF: position', self._position, file=self.logfile)
                return

    def read(self, pos, length):
        data = self.mem[pos:pos + length]
        self._position = pos + len(data)
        return data

    def getbof(self, rqd_stream):
        if DEBUG:
            print('reqd: 0x%04x' % rqd_stream, file=self.logfile)

        def bof_error(msg):
            raise XLRDError('Unsupported format, or corrupt file: ' + msg)

        savpos = self._position
        opcode = self.get2bytes()
        if opcode == MY_EOF:
            bof_error('Expected BOF record; met end of file')
        if opcode not in bofcodes:
            bof_error('Expected BOF record; found %r' % self.mem[savpos:savpos + 8])
        length = self.get2bytes()
        if length == MY_EOF:
            bof_error('Incomplete BOF record[1]; met end of file')
        if not 4 <= length <= 20:
            bof_error('Invalid length (%d) for BOF record type 0x%04x' % (
             length, opcode))
        padding = '\x00' * max(0, boflen[opcode] - length)
        data = self.read(self._position, length)
        if DEBUG:
            fprintf(self.logfile, '\ngetbof(): data=%r\n', data)
        if len(data) < length:
            bof_error('Incomplete BOF record[2]; met end of file')
        data += padding
        version1 = opcode >> 8
        version2, streamtype = unpack('<HH', data[0:4])
        if DEBUG:
            print('getbof(): op=0x%04x version2=0x%04x streamtype=0x%04x' % (
             opcode, version2, streamtype), file=self.logfile)
        bof_offset = self._position - 4 - length
        if DEBUG:
            print('getbof(): BOF found at offset %d; savpos=%d' % (
             bof_offset, savpos), file=self.logfile)
        version = build = year = 0
        if version1 == 8:
            build, year = unpack('<HH', data[4:8])
            if version2 == 1536:
                version = 80
            elif version2 == 1280:
                if year < 1994 or build in (2412, 3218, 3321):
                    version = 50
                else:
                    version = 70
            else:
                version = {0: 21, 
                   7: 21, 
                   512: 21, 
                   768: 30, 
                   1024: 40}.get(version2, 0)
        else:
            if version1 in (4, 2, 0):
                version = {4: 40, 2: 30, 0: 21}[version1]
            if version == 40 and streamtype == XL_WORKBOOK_GLOBALS_4W:
                version = 45
            if DEBUG or self.verbosity >= 2:
                print('BOF: op=0x%04x vers=0x%04x stream=0x%04x buildid=%d buildyr=%d -> BIFF%d' % (
                 opcode, version2, streamtype, build, year, version), file=self.logfile)
            got_globals = streamtype == XL_WORKBOOK_GLOBALS or version == 45 and streamtype == XL_WORKBOOK_GLOBALS_4W
            if rqd_stream == XL_WORKBOOK_GLOBALS and got_globals or streamtype == rqd_stream:
                return version
            if version < 50 and streamtype == XL_WORKSHEET:
                return version
        if version >= 50 and streamtype == 256:
            bof_error('Workspace file -- no spreadsheet data')
        bof_error('BOF not workbook/worksheet: op=0x%04x vers=0x%04x strm=0x%04x build=%d year=%d -> BIFF%d' % (
         opcode, version2, streamtype, build, year, version))


def expand_cell_address(inrow, incol):
    outrow = inrow
    if incol & 32768:
        if outrow >= 32768:
            outrow -= 65536
        relrow = 1
    else:
        relrow = 0
    outcol = incol & 255
    if incol & 16384:
        if outcol >= 128:
            outcol -= 256
        relcol = 1
    else:
        relcol = 0
    return (
     outrow, outcol, relrow, relcol)


def colname(colx, _A2Z='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    assert colx >= 0
    name = UNICODE_LITERAL('')
    while 1:
        quot, rem = divmod(colx, 26)
        name = _A2Z[rem] + name
        if not quot:
            return name
        colx = quot - 1


def display_cell_address(rowx, colx, relrow, relcol):
    if relrow:
        rowpart = '(*%s%d)' % ('+-'[(rowx < 0)], abs(rowx))
    else:
        rowpart = '$%d' % (rowx + 1,)
    if relcol:
        colpart = '(*%s%d)' % ('+-'[(colx < 0)], abs(colx))
    else:
        colpart = '$' + colname(colx)
    return colpart + rowpart


def unpack_SST_table(datatab, nstrings):
    """Return list of strings"""
    datainx = 0
    ndatas = len(datatab)
    data = datatab[0]
    datalen = len(data)
    pos = 8
    strings = []
    strappend = strings.append
    richtext_runs = {}
    local_unpack = unpack
    local_min = min
    local_BYTES_ORD = BYTES_ORD
    latin_1 = 'latin_1'
    for _unused_i in xrange(nstrings):
        nchars = local_unpack('<H', data[pos:pos + 2])[0]
        pos += 2
        options = local_BYTES_ORD(data[pos])
        pos += 1
        rtcount = 0
        phosz = 0
        if options & 8:
            rtcount = local_unpack('<H', data[pos:pos + 2])[0]
            pos += 2
        if options & 4:
            phosz = local_unpack('<i', data[pos:pos + 4])[0]
            pos += 4
        accstrg = UNICODE_LITERAL('')
        charsgot = 0
        while 1:
            charsneed = nchars - charsgot
            if options & 1:
                charsavail = local_min(datalen - pos >> 1, charsneed)
                rawstrg = data[pos:pos + 2 * charsavail]
                try:
                    accstrg += unicode(rawstrg, 'utf_16_le')
                except:
                    raise

                pos += 2 * charsavail
            else:
                charsavail = local_min(datalen - pos, charsneed)
                rawstrg = data[pos:pos + charsavail]
                accstrg += unicode(rawstrg, latin_1)
                pos += charsavail
            charsgot += charsavail
            if charsgot == nchars:
                break
            datainx += 1
            data = datatab[datainx]
            datalen = len(data)
            options = local_BYTES_ORD(data[0])
            pos = 1

        if rtcount:
            runs = []
            for runindex in xrange(rtcount):
                if pos == datalen:
                    pos = 0
                    datainx += 1
                    data = datatab[datainx]
                    datalen = len(data)
                runs.append(local_unpack('<HH', data[pos:pos + 4]))
                pos += 4

            richtext_runs[len(strings)] = runs
        pos += phosz
        if pos >= datalen:
            pos = pos - datalen
            datainx += 1
            if datainx < ndatas:
                data = datatab[datainx]
                datalen = len(data)
            else:
                assert _unused_i == nstrings - 1
        strappend(accstrg)

    return (
     strings, richtext_runs)