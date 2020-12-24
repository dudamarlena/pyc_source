# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\sheet.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function
from array import array
from struct import unpack, calcsize
from .biffh import *
from .timemachine import *
from .formula import dump_formula, decompile_formula, rangename2d, FMLA_TYPE_CELL, FMLA_TYPE_SHARED
from .formatting import nearest_colour_index, Format
DEBUG = 0
OBJ_MSO_DEBUG = 0
_WINDOW2_options = (
 (
  'show_formulas', 0),
 (
  'show_grid_lines', 1),
 (
  'show_sheet_headers', 1),
 (
  'panes_are_frozen', 0),
 (
  'show_zero_values', 1),
 (
  'automatic_grid_line_colour', 1),
 (
  'columns_from_right_to_left', 0),
 (
  'show_outline_symbols', 1),
 (
  'remove_splits_if_pane_freeze_is_removed', 0),
 (
  'sheet_selected', 0),
 (
  'sheet_visible', 0),
 (
  'show_in_page_break_preview', 0))

class Sheet(BaseObject):
    name = ''
    book = None
    nrows = 0
    ncols = 0
    colinfo_map = {}
    rowinfo_map = {}
    col_label_ranges = []
    row_label_ranges = []
    merged_cells = []
    rich_text_runlist_map = {}
    defcolwidth = None
    standardwidth = None
    default_row_height = None
    default_row_height_mismatch = None
    default_row_hidden = None
    default_additional_space_above = None
    default_additional_space_below = None
    visibility = 0
    gcw = (
     0,) * 256
    hyperlink_list = []
    hyperlink_map = {}
    cell_note_map = {}
    vert_split_pos = 0
    horz_split_pos = 0
    horz_split_first_visible = 0
    vert_split_first_visible = 0
    split_active_pane = 0
    has_pane_record = 0
    horizontal_page_breaks = []
    vertical_page_breaks = []

    def __init__(self, book, position, name, number):
        self.book = book
        self.biff_version = book.biff_version
        self._position = position
        self.logfile = book.logfile
        self.bt = array('B', [XL_CELL_EMPTY])
        self.bf = array('h', [-1])
        self.name = name
        self.number = number
        self.verbosity = book.verbosity
        self.formatting_info = book.formatting_info
        self.ragged_rows = book.ragged_rows
        if self.ragged_rows:
            self.put_cell = self.put_cell_ragged
        else:
            self.put_cell = self.put_cell_unragged
        self._xf_index_to_xl_type_map = book._xf_index_to_xl_type_map
        self.nrows = 0
        self.ncols = 0
        self._maxdatarowx = -1
        self._maxdatacolx = -1
        self._dimnrows = 0
        self._dimncols = 0
        self._cell_values = []
        self._cell_types = []
        self._cell_xf_indexes = []
        self.defcolwidth = None
        self.standardwidth = None
        self.default_row_height = None
        self.default_row_height_mismatch = 0
        self.default_row_hidden = 0
        self.default_additional_space_above = 0
        self.default_additional_space_below = 0
        self.colinfo_map = {}
        self.rowinfo_map = {}
        self.col_label_ranges = []
        self.row_label_ranges = []
        self.merged_cells = []
        self.rich_text_runlist_map = {}
        self.horizontal_page_breaks = []
        self.vertical_page_breaks = []
        self._xf_index_stats = [0, 0, 0, 0]
        self.visibility = book._sheet_visibility[number]
        for attr, defval in _WINDOW2_options:
            setattr(self, attr, defval)

        self.first_visible_rowx = 0
        self.first_visible_colx = 0
        self.gridline_colour_index = 64
        self.gridline_colour_rgb = None
        self.hyperlink_list = []
        self.hyperlink_map = {}
        self.cell_note_map = {}
        self.cooked_page_break_preview_mag_factor = 60
        self.cooked_normal_view_mag_factor = 100
        self.cached_page_break_preview_mag_factor = None
        self.cached_normal_view_mag_factor = None
        self.scl_mag_factor = None
        self._ixfe = None
        self._cell_attr_to_xfx = {}
        if self.biff_version >= 80:
            self.utter_max_rows = 65536
        else:
            self.utter_max_rows = 16384
        self.utter_max_cols = 256
        self._first_full_rowx = -1
        return

    def cell(self, rowx, colx):
        if self.formatting_info:
            xfx = self.cell_xf_index(rowx, colx)
        else:
            xfx = None
        return Cell(self._cell_types[rowx][colx], self._cell_values[rowx][colx], xfx)

    def cell_value(self, rowx, colx):
        return self._cell_values[rowx][colx]

    def cell_type(self, rowx, colx):
        return self._cell_types[rowx][colx]

    def cell_xf_index(self, rowx, colx):
        self.req_fmt_info()
        xfx = self._cell_xf_indexes[rowx][colx]
        if xfx > -1:
            self._xf_index_stats[0] += 1
            return xfx
        try:
            xfx = self.rowinfo_map[rowx].xf_index
            if xfx > -1:
                self._xf_index_stats[1] += 1
                return xfx
        except KeyError:
            pass

        try:
            xfx = self.colinfo_map[colx].xf_index
            if xfx == -1:
                xfx = 15
            self._xf_index_stats[2] += 1
            return xfx
        except KeyError:
            self._xf_index_stats[3] += 1
            return 15

    def row_len(self, rowx):
        return len(self._cell_values[rowx])

    def row(self, rowx):
        return [ self.cell(rowx, colx) for colx in xrange(len(self._cell_values[rowx]))
               ]

    def row_types(self, rowx, start_colx=0, end_colx=None):
        if end_colx is None:
            return self._cell_types[rowx][start_colx:]
        else:
            return self._cell_types[rowx][start_colx:end_colx]

    def row_values(self, rowx, start_colx=0, end_colx=None):
        if end_colx is None:
            return self._cell_values[rowx][start_colx:]
        else:
            return self._cell_values[rowx][start_colx:end_colx]

    def row_slice(self, rowx, start_colx=0, end_colx=None):
        nc = len(self._cell_values[rowx])
        if start_colx < 0:
            start_colx += nc
            if start_colx < 0:
                start_colx = 0
        if end_colx is None or end_colx > nc:
            end_colx = nc
        elif end_colx < 0:
            end_colx += nc
        return [ self.cell(rowx, colx) for colx in xrange(start_colx, end_colx)
               ]

    def col_slice(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [ self.cell(rowx, colx) for rowx in xrange(start_rowx, end_rowx)
               ]

    def col_values(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [ self._cell_values[rowx][colx] for rowx in xrange(start_rowx, end_rowx)
               ]

    def col_types(self, colx, start_rowx=0, end_rowx=None):
        nr = self.nrows
        if start_rowx < 0:
            start_rowx += nr
            if start_rowx < 0:
                start_rowx = 0
        if end_rowx is None or end_rowx > nr:
            end_rowx = nr
        elif end_rowx < 0:
            end_rowx += nr
        return [ self._cell_types[rowx][colx] for rowx in xrange(start_rowx, end_rowx)
               ]

    def col(self, colx):
        return self.col_slice(colx)

    col = col_slice

    def tidy_dimensions(self):
        if self.verbosity >= 3:
            fprintf(self.logfile, 'tidy_dimensions: nrows=%d ncols=%d \n', self.nrows, self.ncols)
        if 1 and self.merged_cells:
            nr = nc = 0
            umaxrows = self.utter_max_rows
            umaxcols = self.utter_max_cols
            for crange in self.merged_cells:
                rlo, rhi, clo, chi = crange
                if not 0 <= rlo < rhi <= umaxrows or not 0 <= clo < chi <= umaxcols:
                    fprintf(self.logfile, '*** WARNING: sheet #%d (%r), MERGEDCELLS bad range %r\n', self.number, self.name, crange)
                if rhi > nr:
                    nr = rhi
                if chi > nc:
                    nc = chi

            if nc > self.ncols:
                self.ncols = nc
            if nr > self.nrows:
                self.put_cell(nr - 1, 0, XL_CELL_EMPTY, '', -1)
        if self.verbosity >= 1 and (self.nrows != self._dimnrows or self.ncols != self._dimncols):
            fprintf(self.logfile, 'NOTE *** sheet %d (%r): DIMENSIONS R,C = %d,%d should be %d,%d\n', self.number, self.name, self._dimnrows, self._dimncols, self.nrows, self.ncols)
        if not self.ragged_rows:
            ncols = self.ncols
            s_cell_types = self._cell_types
            s_cell_values = self._cell_values
            s_cell_xf_indexes = self._cell_xf_indexes
            s_fmt_info = self.formatting_info
            if self._first_full_rowx == -2:
                ubound = self.nrows
            else:
                ubound = self._first_full_rowx
            for rowx in xrange(ubound):
                trow = s_cell_types[rowx]
                rlen = len(trow)
                nextra = ncols - rlen
                if nextra > 0:
                    s_cell_values[rowx][rlen:] = [
                     ''] * nextra
                    trow[rlen:] = self.bt * nextra
                    if s_fmt_info:
                        s_cell_xf_indexes[rowx][rlen:] = self.bf * nextra

    def put_cell_ragged(self, rowx, colx, ctype, value, xf_index):
        if ctype is None:
            ctype = self._xf_index_to_xl_type_map[xf_index]
        assert 0 <= colx < self.utter_max_cols
        assert 0 <= rowx < self.utter_max_rows
        fmt_info = self.formatting_info
        try:
            nr = rowx + 1
            if self.nrows < nr:
                scta = self._cell_types.append
                scva = self._cell_values.append
                scxa = self._cell_xf_indexes.append
                bt = self.bt
                bf = self.bf
                for _unused in xrange(self.nrows, nr):
                    scta(bt * 0)
                    scva([])
                    if fmt_info:
                        scxa(bf * 0)

                self.nrows = nr
            types_row = self._cell_types[rowx]
            values_row = self._cell_values[rowx]
            if fmt_info:
                fmt_row = self._cell_xf_indexes[rowx]
            ltr = len(types_row)
            if colx >= self.ncols:
                self.ncols = colx + 1
            num_empty = colx - ltr
            if not num_empty:
                types_row.append(ctype)
                values_row.append(value)
                if fmt_info:
                    fmt_row.append(xf_index)
                return
            if num_empty > 0:
                num_empty += 1
                types_row[ltr:] = self.bt * num_empty
                values_row[ltr:] = [''] * num_empty
                if fmt_info:
                    fmt_row[ltr:] = self.bf * num_empty
            types_row[colx] = ctype
            values_row[colx] = value
            if fmt_info:
                fmt_row[colx] = xf_index
        except:
            print('put_cell', rowx, colx, file=self.logfile)
            raise

        return

    def put_cell_unragged(self, rowx, colx, ctype, value, xf_index):
        if ctype is None:
            ctype = self._xf_index_to_xl_type_map[xf_index]
        try:
            self._cell_types[rowx][colx] = ctype
            self._cell_values[rowx][colx] = value
            if self.formatting_info:
                self._cell_xf_indexes[rowx][colx] = xf_index
        except IndexError:
            nr = rowx + 1
            nc = colx + 1
            assert 1 <= nc <= self.utter_max_cols
            assert 1 <= nr <= self.utter_max_rows
            if nc > self.ncols:
                self.ncols = nc
                if nr < self.nrows:
                    self._first_full_rowx = -2
                elif rowx > self._first_full_rowx > -2:
                    self._first_full_rowx = rowx
            if nr <= self.nrows:
                trow = self._cell_types[rowx]
                nextra = self.ncols - len(trow)
                if nextra > 0:
                    trow.extend(self.bt * nextra)
                    if self.formatting_info:
                        self._cell_xf_indexes[rowx].extend(self.bf * nextra)
                    self._cell_values[rowx].extend([''] * nextra)
            else:
                scta = self._cell_types.append
                scva = self._cell_values.append
                scxa = self._cell_xf_indexes.append
                fmt_info = self.formatting_info
                nc = self.ncols
                bt = self.bt
                bf = self.bf
                for _unused in xrange(self.nrows, nr):
                    scta(bt * nc)
                    scva([''] * nc)
                    if fmt_info:
                        scxa(bf * nc)

                self.nrows = nr
            try:
                self._cell_types[rowx][colx] = ctype
                self._cell_values[rowx][colx] = value
                if self.formatting_info:
                    self._cell_xf_indexes[rowx][colx] = xf_index
            except:
                print('put_cell', rowx, colx, file=self.logfile)
                raise

        except:
            print('put_cell', rowx, colx, file=self.logfile)
            raise

        return

    def read(self, bk):
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        blah_rows = DEBUG or self.verbosity >= 4
        blah_formulas = 0 and blah
        r1c1 = 0
        oldpos = bk._position
        bk._position = self._position
        XL_SHRFMLA_ETC_ETC = (
         XL_SHRFMLA, XL_ARRAY, XL_TABLEOP, XL_TABLEOP2,
         XL_ARRAY2, XL_TABLEOP_B2)
        self_put_cell = self.put_cell
        local_unpack = unpack
        bk_get_record_parts = bk.get_record_parts
        bv = self.biff_version
        fmt_info = self.formatting_info
        do_sst_rich_text = fmt_info and bk._rich_text_runlist_map
        rowinfo_sharing_dict = {}
        txos = {}
        eof_found = 0
        while 1:
            rc, data_len, data = bk_get_record_parts()
            if rc == XL_NUMBER:
                rowx, colx, xf_index, d = local_unpack('<HHHd', data[:14])
                self_put_cell(rowx, colx, None, d, xf_index)
        else:
            if rc == XL_LABELSST:
                rowx, colx, xf_index, sstindex = local_unpack('<HHHi', data)
                self_put_cell(rowx, colx, XL_CELL_TEXT, bk._sharedstrings[sstindex], xf_index)
                if do_sst_rich_text:
                    runlist = bk._rich_text_runlist_map.get(sstindex)
                    if runlist:
                        self.rich_text_runlist_map[(rowx, colx)] = runlist
            elif rc == XL_LABEL:
                rowx, colx, xf_index = local_unpack('<HHH', data[0:6])
                if bv < BIFF_FIRST_UNICODE:
                    strg = unpack_string(data, 6, bk.encoding or bk.derive_encoding(), lenlen=2)
                else:
                    strg = unpack_unicode(data, 6, lenlen=2)
                self_put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
            elif rc == XL_RSTRING:
                rowx, colx, xf_index = local_unpack('<HHH', data[0:6])
                if bv < BIFF_FIRST_UNICODE:
                    strg, pos = unpack_string_update_pos(data, 6, bk.encoding or bk.derive_encoding(), lenlen=2)
                    nrt = BYTES_ORD(data[pos])
                    pos += 1
                    runlist = []
                    for _unused in xrange(nrt):
                        runlist.append(unpack('<BB', data[pos:pos + 2]))
                        pos += 2

                    assert pos == len(data)
                else:
                    strg, pos = unpack_unicode_update_pos(data, 6, lenlen=2)
                    nrt = unpack('<H', data[pos:pos + 2])[0]
                    pos += 2
                    runlist = []
                    for _unused in xrange(nrt):
                        runlist.append(unpack('<HH', data[pos:pos + 4]))
                        pos += 4

                    assert pos == len(data)
                self_put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
                self.rich_text_runlist_map[(rowx, colx)] = runlist
            elif rc == XL_RK:
                rowx, colx, xf_index = local_unpack('<HHH', data[:6])
                d = unpack_RK(data[6:10])
                self_put_cell(rowx, colx, None, d, xf_index)
            elif rc == XL_MULRK:
                mulrk_row, mulrk_first = local_unpack('<HH', data[0:4])
                mulrk_last, = local_unpack('<H', data[-2:])
                pos = 4
                for colx in xrange(mulrk_first, mulrk_last + 1):
                    xf_index, = local_unpack('<H', data[pos:pos + 2])
                    d = unpack_RK(data[pos + 2:pos + 6])
                    pos += 6
                    self_put_cell(mulrk_row, colx, None, d, xf_index)

            elif rc == XL_ROW:
                if not fmt_info:
                    continue
                rowx, bits1, bits2 = local_unpack('<H4xH4xi', data[0:16])
                if not 0 <= rowx < self.utter_max_rows:
                    print('*** NOTE: ROW record has row index %d; should have 0 <= rowx < %d -- record ignored!' % (
                     rowx, self.utter_max_rows), file=self.logfile)
                    continue
                key = (
                 bits1, bits2)
                r = rowinfo_sharing_dict.get(key)
                if r is None:
                    rowinfo_sharing_dict[key] = r = Rowinfo()
                    r.height = bits1 & 32767
                    r.has_default_height = bits1 >> 15 & 1
                    r.outline_level = bits2 & 7
                    r.outline_group_starts_ends = bits2 >> 4 & 1
                    r.hidden = bits2 >> 5 & 1
                    r.height_mismatch = bits2 >> 6 & 1
                    r.has_default_xf_index = bits2 >> 7 & 1
                    r.xf_index = bits2 >> 16 & 4095
                    r.additional_space_above = bits2 >> 28 & 1
                    r.additional_space_below = bits2 >> 29 & 1
                    if not r.has_default_xf_index:
                        r.xf_index = -1
                self.rowinfo_map[rowx] = r
                if 0 and r.xf_index > -1:
                    fprintf(self.logfile, '**ROW %d %d %d\n', self.number, rowx, r.xf_index)
                if blah_rows:
                    print('ROW', rowx, bits1, bits2, file=self.logfile)
                    r.dump(self.logfile, header='--- sh #%d, rowx=%d ---' % (self.number, rowx))
            elif rc in XL_FORMULA_OPCODES:
                if bv >= 50:
                    rowx, colx, xf_index, result_str, flags = local_unpack('<HHH8sH', data[0:16])
                    lenlen = 2
                    tkarr_offset = 20
                elif bv >= 30:
                    rowx, colx, xf_index, result_str, flags = local_unpack('<HHH8sH', data[0:16])
                    lenlen = 2
                    tkarr_offset = 16
                else:
                    rowx, colx, cell_attr, result_str, flags = local_unpack('<HH3s8sB', data[0:16])
                    xf_index = self.fixed_BIFF2_xfindex(cell_attr, rowx, colx)
                    lenlen = 1
                    tkarr_offset = 16
                if blah_formulas:
                    fprintf(self.logfile, 'FORMULA: rowx=%d colx=%d\n', rowx, colx)
                    fmlalen = local_unpack('<H', data[20:22])[0]
                    decompile_formula(bk, data[22:], fmlalen, FMLA_TYPE_CELL, browx=rowx, bcolx=colx, blah=1, r1c1=r1c1)
                if result_str[6:8] == b'\xff\xff':
                    first_byte = BYTES_ORD(result_str[0])
                    if first_byte == 0:
                        gotstring = 0
                        rc2, data2_len, data2 = bk.get_record_parts()
                        if rc2 == XL_STRING or rc2 == XL_STRING_B2:
                            gotstring = 1
                        elif rc2 == XL_ARRAY:
                            row1x, rownx, col1x, colnx, array_flags, tokslen = local_unpack('<HHBBBxxxxxH', data2[:14])
                            if blah_formulas:
                                fprintf(self.logfile, 'ARRAY: %d %d %d %d %d\n', row1x, rownx, col1x, colnx, array_flags)
                        elif rc2 == XL_SHRFMLA:
                            row1x, rownx, col1x, colnx, nfmlas, tokslen = local_unpack('<HHBBxBH', data2[:10])
                            if blah_formulas:
                                fprintf(self.logfile, 'SHRFMLA (sub): %d %d %d %d %d\n', row1x, rownx, col1x, colnx, nfmlas)
                                decompile_formula(bk, data2[10:], tokslen, FMLA_TYPE_SHARED, blah=1, browx=rowx, bcolx=colx, r1c1=r1c1)
                        elif rc2 not in XL_SHRFMLA_ETC_ETC:
                            raise XLRDError('Expected SHRFMLA, ARRAY, TABLEOP* or STRING record; found 0x%04x' % rc2)
                        if not gotstring:
                            rc2, _unused_len, data2 = bk.get_record_parts()
                            if rc2 not in (XL_STRING, XL_STRING_B2):
                                raise XLRDError('Expected STRING record; found 0x%04x' % rc2)
                        strg = self.string_record_contents(data2)
                        self.put_cell(rowx, colx, XL_CELL_TEXT, strg, xf_index)
                    elif first_byte == 1:
                        value = BYTES_ORD(result_str[2])
                        self_put_cell(rowx, colx, XL_CELL_BOOLEAN, value, xf_index)
                    elif first_byte == 2:
                        value = BYTES_ORD(result_str[2])
                        self_put_cell(rowx, colx, XL_CELL_ERROR, value, xf_index)
                    elif first_byte == 3:
                        self_put_cell(rowx, colx, XL_CELL_TEXT, '', xf_index)
                    else:
                        raise XLRDError('unexpected special case (0x%02x) in FORMULA' % first_byte)
                else:
                    d = local_unpack('<d', result_str)[0]
                    self_put_cell(rowx, colx, None, d, xf_index)
            elif rc == XL_BOOLERR:
                rowx, colx, xf_index, value, is_err = local_unpack('<HHHBB', data[:8])
                cellty = (
                 XL_CELL_BOOLEAN, XL_CELL_ERROR)[is_err]
                self_put_cell(rowx, colx, cellty, value, xf_index)
            elif rc == XL_COLINFO:
                if not fmt_info:
                    continue
                c = Colinfo()
                first_colx, last_colx, c.width, c.xf_index, flags = local_unpack('<HHHHH', data[:10])
                if not 0 <= first_colx <= last_colx <= 256:
                    print('*** NOTE: COLINFO record has first col index %d, last %d; should have 0 <= first <= last <= 255 -- record ignored!' % (
                     first_colx, last_colx), file=self.logfile)
                    del c
                    continue
                upkbits(c, flags, (
                 (0, 1, 'hidden'),
                 (1, 2, 'bit1_flag'),
                 (8, 1792, 'outline_level'),
                 (12, 4096, 'collapsed')))
                for colx in xrange(first_colx, last_colx + 1):
                    if colx > 255:
                        break
                    self.colinfo_map[colx] = c

                if blah:
                    fprintf(self.logfile, 'COLINFO sheet #%d cols %d-%d: wid=%d xf_index=%d flags=0x%04x\n', self.number, first_colx, last_colx, c.width, c.xf_index, flags)
                    c.dump(self.logfile, header='===')
            elif rc == XL_DEFCOLWIDTH:
                self.defcolwidth, = local_unpack('<H', data[:2])
            elif rc == XL_STANDARDWIDTH:
                if data_len != 2:
                    print('*** ERROR *** STANDARDWIDTH', data_len, repr(data), file=self.logfile)
                self.standardwidth, = local_unpack('<H', data[:2])
            elif rc == XL_GCW:
                if not fmt_info:
                    continue
                assert data_len == 34
                assert data[0:2] == ' \x00'
                iguff = unpack('<8i', data[2:34])
                gcw = []
                for bits in iguff:
                    for j in xrange(32):
                        gcw.append(bits & 1)
                        bits >>= 1

                self.gcw = tuple(gcw)
            elif rc == XL_BLANK:
                if not fmt_info:
                    continue
                rowx, colx, xf_index = local_unpack('<HHH', data[:6])
                self_put_cell(rowx, colx, XL_CELL_BLANK, '', xf_index)
            elif rc == XL_MULBLANK:
                if not fmt_info:
                    continue
                nitems = data_len >> 1
                result = local_unpack('<%dH' % nitems, data)
                rowx, mul_first = result[:2]
                mul_last = result[(-1)]
                assert nitems == mul_last + 4 - mul_first
                pos = 2
                for colx in xrange(mul_first, mul_last + 1):
                    self_put_cell(rowx, colx, XL_CELL_BLANK, '', result[pos])
                    pos += 1

            elif rc == XL_DIMENSION or rc == XL_DIMENSION2:
                if bv < 80:
                    dim_tuple = local_unpack('<HxxH', data[2:8])
                else:
                    dim_tuple = local_unpack('<ixxH', data[4:12])
                self.nrows, self.ncols = (0, 0)
                self._dimnrows, self._dimncols = dim_tuple
                if bv in (21, 30, 40) and self.book.xf_list and not self.book._xf_epilogue_done:
                    self.book.xf_epilogue()
                if blah:
                    fprintf(self.logfile, 'sheet %d(%r) DIMENSIONS: ncols=%d nrows=%d\n', self.number, self.name, self._dimncols, self._dimnrows)
            elif rc == XL_HLINK:
                self.handle_hlink(data)
            elif rc == XL_QUICKTIP:
                self.handle_quicktip(data)
            elif rc == XL_EOF:
                DEBUG = 0
                if DEBUG:
                    print('SHEET.READ: EOF', file=self.logfile)
                eof_found = 1
                break
            elif rc == XL_OBJ:
                saved_obj = self.handle_obj(data)
                if saved_obj:
                    saved_obj_id = saved_obj.id
                else:
                    saved_obj_id = None
            elif rc == XL_MSO_DRAWING:
                self.handle_msodrawingetc(rc, data_len, data)
            elif rc == XL_TXO:
                txo = self.handle_txo(data)
                if txo and saved_obj_id:
                    txos[saved_obj_id] = txo
                    saved_obj_id = None
            elif rc == XL_NOTE:
                self.handle_note(data, txos)
            elif rc == XL_FEAT11:
                self.handle_feat11(data)
            elif rc in bofcodes:
                version, boftype = local_unpack('<HH', data[0:4])
                if boftype != 32:
                    print('*** Unexpected embedded BOF (0x%04x) at offset %d: version=0x%04x type=0x%04x' % (
                     rc, bk._position - data_len - 4, version, boftype), file=self.logfile)
                while 1:
                    code, data_len, data = bk.get_record_parts()
                    if code == XL_EOF:
                        break

                if DEBUG:
                    print('---> found EOF', file=self.logfile)
            elif rc == XL_COUNTRY:
                bk.handle_country(data)
            elif rc == XL_LABELRANGES:
                pos = 0
                pos = unpack_cell_range_address_list_update_pos(self.row_label_ranges, data, pos, bv, addr_size=8)
                pos = unpack_cell_range_address_list_update_pos(self.col_label_ranges, data, pos, bv, addr_size=8)
                assert pos == data_len
            elif rc == XL_ARRAY:
                row1x, rownx, col1x, colnx, array_flags, tokslen = local_unpack('<HHBBBxxxxxH', data[:14])
                if blah_formulas:
                    print('ARRAY:', row1x, rownx, col1x, colnx, array_flags, file=self.logfile)
            elif rc == XL_SHRFMLA:
                row1x, rownx, col1x, colnx, nfmlas, tokslen = local_unpack('<HHBBxBH', data[:10])
                if blah_formulas:
                    print('SHRFMLA (main):', row1x, rownx, col1x, colnx, nfmlas, file=self.logfile)
                    decompile_formula(bk, data[10:], tokslen, FMLA_TYPE_SHARED, blah=1, browx=rowx, bcolx=colx, r1c1=r1c1)
            elif rc == XL_CONDFMT:
                if not fmt_info:
                    continue
                assert bv >= 80
                num_CFs, needs_recalc, browx1, browx2, bcolx1, bcolx2 = unpack('<6H', data[0:12])
                if self.verbosity >= 1:
                    fprintf(self.logfile, '\n*** WARNING: Ignoring CONDFMT (conditional formatting) record\n*** in Sheet %d (%r).\n*** %d CF record(s); needs_recalc_or_redraw = %d\n*** Bounding box is %s\n', self.number, self.name, num_CFs, needs_recalc, rangename2d(browx1, browx2 + 1, bcolx1, bcolx2 + 1))
                olist = []
                pos = unpack_cell_range_address_list_update_pos(olist, data, 12, bv, addr_size=8)
                if self.verbosity >= 1:
                    fprintf(self.logfile, '*** %d individual range(s):\n*** %s\n', len(olist), (', ').join([ rangename2d(*coords) for coords in olist ]))
            elif rc == XL_CF:
                if not fmt_info:
                    continue
                cf_type, cmp_op, sz1, sz2, flags = unpack('<BBHHi', data[0:10])
                font_block = flags >> 26 & 1
                bord_block = flags >> 28 & 1
                patt_block = flags >> 29 & 1
                if self.verbosity >= 1:
                    fprintf(self.logfile, '\n*** WARNING: Ignoring CF (conditional formatting) sub-record.\n*** cf_type=%d, cmp_op=%d, sz1=%d, sz2=%d, flags=0x%08x\n*** optional data blocks: font=%d, border=%d, pattern=%d\n', cf_type, cmp_op, sz1, sz2, flags, font_block, bord_block, patt_block)
                pos = 12
                if font_block:
                    font_height, font_options, weight, escapement, underline, font_colour_index, two_bits, font_esc, font_underl = unpack('<64x i i H H B 3x i 4x i i i 18x', data[pos:pos + 118])
                    font_style = (two_bits > 1) & 1
                    posture = (font_options > 1) & 1
                    font_canc = (two_bits > 7) & 1
                    cancellation = (font_options > 7) & 1
                    if self.verbosity >= 1:
                        fprintf(self.logfile, '*** Font info: height=%d, weight=%d, escapement=%d,\n*** underline=%d, colour_index=%d, esc=%d, underl=%d,\n*** style=%d, posture=%d, canc=%d, cancellation=%d\n', font_height, weight, escapement, underline, font_colour_index, font_esc, font_underl, font_style, posture, font_canc, cancellation)
                    pos += 118
                if bord_block:
                    pos += 8
                if patt_block:
                    pos += 4
                fmla1 = data[pos:pos + sz1]
                pos += sz1
                if blah and sz1:
                    fprintf(self.logfile, '*** formula 1:\n')
                    dump_formula(bk, fmla1, sz1, bv, reldelta=0, blah=1)
                fmla2 = data[pos:pos + sz2]
                pos += sz2
                assert pos == data_len
                if blah and sz2:
                    fprintf(self.logfile, '*** formula 2:\n')
                    dump_formula(bk, fmla2, sz2, bv, reldelta=0, blah=1)
            elif rc == XL_DEFAULTROWHEIGHT:
                if data_len == 4:
                    bits, self.default_row_height = unpack('<HH', data[:4])
                elif data_len == 2:
                    self.default_row_height, = unpack('<H', data)
                    bits = 0
                    fprintf(self.logfile, '*** WARNING: DEFAULTROWHEIGHT record len is 2, should be 4; assuming BIFF2 format\n')
                else:
                    bits = 0
                    fprintf(self.logfile, '*** WARNING: DEFAULTROWHEIGHT record len is %d, should be 4; ignoring this record\n', data_len)
                self.default_row_height_mismatch = bits & 1
                self.default_row_hidden = bits >> 1 & 1
                self.default_additional_space_above = bits >> 2 & 1
                self.default_additional_space_below = bits >> 3 & 1
            elif rc == XL_MERGEDCELLS:
                if not fmt_info:
                    continue
                pos = unpack_cell_range_address_list_update_pos(self.merged_cells, data, 0, bv, addr_size=8)
                if blah:
                    fprintf(self.logfile, 'MERGEDCELLS: %d ranges\n', (pos - 2) // 8)
                assert pos == data_len, 'MERGEDCELLS: pos=%d data_len=%d' % (pos, data_len)
            elif rc == XL_WINDOW2:
                if bv >= 80 and data_len >= 14:
                    options, self.first_visible_rowx, self.first_visible_colx, self.gridline_colour_index, self.cached_page_break_preview_mag_factor, self.cached_normal_view_mag_factor = unpack('<HHHHxxHH', data[:14])
                else:
                    assert bv >= 30
                    options, self.first_visible_rowx, self.first_visible_colx = unpack('<HHH', data[:6])
                    self.gridline_colour_rgb = unpack('<BBB', data[6:9])
                    self.gridline_colour_index = nearest_colour_index(self.book.colour_map, self.gridline_colour_rgb, debug=0)
                    self.cached_page_break_preview_mag_factor = 0
                    self.cached_normal_view_mag_factor = 0
                for attr, _unused_defval in _WINDOW2_options:
                    setattr(self, attr, options & 1)
                    options >>= 1

            elif rc == XL_SCL:
                num, den = unpack('<HH', data)
                result = 0
                if den:
                    result = num * 100 // den
                if not 10 <= result <= 400:
                    if DEBUG or self.verbosity >= 0:
                        print('WARNING *** SCL rcd sheet %d: should have 0.1 <= num/den <= 4; got %d/%d' % (
                         self.number, num, den), file=self.logfile)
                    result = 100
                self.scl_mag_factor = result
            elif rc == XL_PANE:
                self.vert_split_pos, self.horz_split_pos, self.horz_split_first_visible, self.vert_split_first_visible, self.split_active_pane = unpack('<HHHHB', data[:9])
                self.has_pane_record = 1
            elif rc == XL_HORIZONTALPAGEBREAKS:
                if not fmt_info:
                    continue
                num_breaks, = local_unpack('<H', data[:2])
                assert num_breaks * (2 + 4 * (bv >= 80)) + 2 == data_len
                pos = 2
                if bv < 80:
                    while pos < data_len:
                        self.horizontal_page_breaks.append((local_unpack('<H', data[pos:pos + 2])[0], 0, 255))
                        pos += 2

                else:
                    while pos < data_len:
                        self.horizontal_page_breaks.append(local_unpack('<HHH', data[pos:pos + 6]))
                        pos += 6

            elif rc == XL_VERTICALPAGEBREAKS:
                if not fmt_info:
                    continue
                num_breaks, = local_unpack('<H', data[:2])
                assert num_breaks * (2 + 4 * (bv >= 80)) + 2 == data_len
                pos = 2
                if bv < 80:
                    while pos < data_len:
                        self.vertical_page_breaks.append((local_unpack('<H', data[pos:pos + 2])[0], 0, 65535))
                        pos += 2

                else:
                    while pos < data_len:
                        self.vertical_page_breaks.append(local_unpack('<HHH', data[pos:pos + 6]))
                        pos += 6

            elif bv <= 45:
                if rc == XL_FORMAT or rc == XL_FORMAT2:
                    bk.handle_format(data, rc)
                elif rc == XL_FONT or rc == XL_FONT_B3B4:
                    bk.handle_font(data)
                elif rc == XL_STYLE:
                    if not self.book._xf_epilogue_done:
                        self.book.xf_epilogue()
                    bk.handle_style(data)
                elif rc == XL_PALETTE:
                    bk.handle_palette(data)
                elif rc == XL_BUILTINFMTCOUNT:
                    bk.handle_builtinfmtcount(data)
                elif rc == XL_XF4 or rc == XL_XF3 or rc == XL_XF2:
                    bk.handle_xf(data)
                elif rc == XL_DATEMODE:
                    bk.handle_datemode(data)
                elif rc == XL_CODEPAGE:
                    bk.handle_codepage(data)
                elif rc == XL_FILEPASS:
                    bk.handle_filepass(data)
                elif rc == XL_WRITEACCESS:
                    bk.handle_writeaccess(data)
                elif rc == XL_IXFE:
                    self._ixfe = local_unpack('<H', data)[0]
                elif rc == XL_NUMBER_B2:
                    rowx, colx, cell_attr, d = local_unpack('<HH3sd', data)
                    self_put_cell(rowx, colx, None, d, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_INTEGER:
                    rowx, colx, cell_attr, d = local_unpack('<HH3sH', data)
                    self_put_cell(rowx, colx, None, float(d), self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_LABEL_B2:
                    rowx, colx, cell_attr = local_unpack('<HH3s', data[0:7])
                    strg = unpack_string(data, 7, bk.encoding or bk.derive_encoding(), lenlen=1)
                    self_put_cell(rowx, colx, XL_CELL_TEXT, strg, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_BOOLERR_B2:
                    rowx, colx, cell_attr, value, is_err = local_unpack('<HH3sBB', data)
                    cellty = (XL_CELL_BOOLEAN, XL_CELL_ERROR)[is_err]
                    self_put_cell(rowx, colx, cellty, value, self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_BLANK_B2:
                    if not fmt_info:
                        continue
                    rowx, colx, cell_attr = local_unpack('<HH3s', data[:7])
                    self_put_cell(rowx, colx, XL_CELL_BLANK, '', self.fixed_BIFF2_xfindex(cell_attr, rowx, colx))
                elif rc == XL_EFONT:
                    bk.handle_efont(data)
                elif rc == XL_ROW_B2:
                    if not fmt_info:
                        continue
                    rowx, bits1, bits2 = local_unpack('<H4xH2xB', data[0:11])
                    if not 0 <= rowx < self.utter_max_rows:
                        print('*** NOTE: ROW_B2 record has row index %d; should have 0 <= rowx < %d -- record ignored!' % (
                         rowx, self.utter_max_rows), file=self.logfile)
                        continue
                    if not bits2 & 1:
                        xf_index = -1
                    elif data_len == 18:
                        xfx = local_unpack('<H', data[16:18])[0]
                        xf_index = self.fixed_BIFF2_xfindex(cell_attr=None, rowx=rowx, colx=-1, true_xfx=xfx)
                    else:
                        cell_attr = data[13:16]
                        xf_index = self.fixed_BIFF2_xfindex(cell_attr, rowx, colx=-1)
                    key = (
                     bits1, bits2, xf_index)
                    r = rowinfo_sharing_dict.get(key)
                    if r is None:
                        rowinfo_sharing_dict[key] = r = Rowinfo()
                        r.height = bits1 & 32767
                        r.has_default_height = bits1 >> 15 & 1
                        r.has_default_xf_index = bits2 & 1
                        r.xf_index = xf_index
                    self.rowinfo_map[rowx] = r
                    if 0 and r.xf_index > -1:
                        fprintf(self.logfile, '**ROW %d %d %d\n', self.number, rowx, r.xf_index)
                    if blah_rows:
                        print('ROW_B2', rowx, bits1, has_defaults, file=self.logfile)
                        r.dump(self.logfile, header='--- sh #%d, rowx=%d ---' % (self.number, rowx))
                elif rc == XL_COLWIDTH:
                    if not fmt_info:
                        continue
                    first_colx, last_colx, width = local_unpack('<BBH', data[:4])
                    if not first_colx <= last_colx:
                        print('*** NOTE: COLWIDTH record has first col index %d, last %d; should have first <= last -- record ignored!' % (
                         first_colx, last_colx), file=self.logfile)
                        continue
                    for colx in xrange(first_colx, last_colx + 1):
                        if colx in self.colinfo_map:
                            c = self.colinfo_map[colx]
                        else:
                            c = Colinfo()
                            self.colinfo_map[colx] = c
                        c.width = width

                    if blah:
                        fprintf(self.logfile, 'COLWIDTH sheet #%d cols %d-%d: wid=%d\n', self.number, first_colx, last_colx, width)
                elif rc == XL_COLUMNDEFAULT:
                    if not fmt_info:
                        continue
                    first_colx, last_colx = local_unpack('<HH', data[:4])
                    if blah:
                        fprintf(self.logfile, 'COLUMNDEFAULT sheet #%d cols in range(%d, %d)\n', self.number, first_colx, last_colx)
                    if not 0 <= first_colx < last_colx <= 256:
                        print('*** NOTE: COLUMNDEFAULT record has first col index %d, last %d; should have 0 <= first < last <= 256' % (
                         first_colx, last_colx), file=self.logfile)
                        last_colx = min(last_colx, 256)
                    for colx in xrange(first_colx, last_colx):
                        offset = 4 + 3 * (colx - first_colx)
                        cell_attr = data[offset:offset + 3]
                        xf_index = self.fixed_BIFF2_xfindex(cell_attr, rowx=-1, colx=colx)
                        if colx in self.colinfo_map:
                            c = self.colinfo_map[colx]
                        else:
                            c = Colinfo()
                            self.colinfo_map[colx] = c
                        c.xf_index = xf_index

                elif rc == XL_WINDOW2_B2:
                    attr_names = ('show_formulas', 'show_grid_lines', 'show_sheet_headers',
                                  'panes_are_frozen', 'show_zero_values')
                    for attr, char in zip(attr_names, data[0:5]):
                        setattr(self, attr, int(char != '\x00'))

                    self.first_visible_rowx, self.first_visible_colx, self.automatic_grid_line_colour = unpack('<HHB', data[5:10])
                    self.gridline_colour_rgb = unpack('<BBB', data[10:13])
                    self.gridline_colour_index = nearest_colour_index(self.book.colour_map, self.gridline_colour_rgb, debug=0)
                    self.cached_page_break_preview_mag_factor = 0
                    self.cached_normal_view_mag_factor = 0
            else:
                continue

        if not eof_found:
            raise XLRDError('Sheet %d (%r) missing EOF record' % (
             self.number, self.name))
        self.tidy_dimensions()
        self.update_cooked_mag_factors()
        bk._position = oldpos
        return 1

    def string_record_contents(self, data):
        bv = self.biff_version
        bk = self.book
        lenlen = (bv >= 30) + 1
        nchars_expected = unpack('<' + 'BH'[(lenlen - 1)], data[:lenlen])[0]
        offset = lenlen
        if bv < 80:
            enc = bk.encoding or bk.derive_encoding()
        nchars_found = 0
        result = UNICODE_LITERAL('')
        while 1:
            if bv >= 80:
                flag = BYTES_ORD(data[offset]) & 1
                enc = ('latin_1', 'utf_16_le')[flag]
                offset += 1
            chunk = unicode(data[offset:], enc)
            result += chunk
            nchars_found += len(chunk)
            if nchars_found == nchars_expected:
                return result
            if nchars_found > nchars_expected:
                msg = 'STRING/CONTINUE: expected %d chars, found %d' % (
                 nchars_expected, nchars_found)
                raise XLRDError(msg)
            rc, _unused_len, data = bk.get_record_parts()
            if rc != XL_CONTINUE:
                raise XLRDError('Expected CONTINUE record; found record-type 0x%04X' % rc)
            offset = 0

    def update_cooked_mag_factors(self):
        blah = DEBUG or self.verbosity > 0
        if self.show_in_page_break_preview:
            if self.scl_mag_factor is None:
                self.cooked_page_break_preview_mag_factor = 100
            else:
                self.cooked_page_break_preview_mag_factor = self.scl_mag_factor
            zoom = self.cached_normal_view_mag_factor
            if not 10 <= zoom <= 400:
                if blah:
                    print('WARNING *** WINDOW2 rcd sheet %d: Bad cached_normal_view_mag_factor: %d' % (
                     self.number, self.cached_normal_view_mag_factor), file=self.logfile)
                zoom = self.cooked_page_break_preview_mag_factor
            self.cooked_normal_view_mag_factor = zoom
        else:
            if self.scl_mag_factor is None:
                self.cooked_normal_view_mag_factor = 100
            else:
                self.cooked_normal_view_mag_factor = self.scl_mag_factor
            zoom = self.cached_page_break_preview_mag_factor
            if zoom == 0:
                zoom = 60
            elif not 10 <= zoom <= 400:
                if blah:
                    print('WARNING *** WINDOW2 rcd sheet %r: Bad cached_page_break_preview_mag_factor: %r' % (
                     self.number, self.cached_page_break_preview_mag_factor), file=self.logfile)
                zoom = self.cooked_normal_view_mag_factor
            self.cooked_page_break_preview_mag_factor = zoom
        return

    def fixed_BIFF2_xfindex(self, cell_attr, rowx, colx, true_xfx=None):
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        if self.biff_version == 21:
            if self.book.xf_list:
                if true_xfx is not None:
                    xfx = true_xfx
                else:
                    xfx = BYTES_ORD(cell_attr[0]) & 63
                if xfx == 63:
                    if self._ixfe is None:
                        raise XLRDError('BIFF2 cell record has XF index 63 but no preceding IXFE record.')
                    xfx = self._ixfe
                return xfx
            self.biff_version = self.book.biff_version = 20
        xfx_slot = BYTES_ORD(cell_attr[0]) & 63
        assert xfx_slot == 0
        xfx = self._cell_attr_to_xfx.get(cell_attr)
        if xfx is not None:
            return xfx
        else:
            if blah:
                fprintf(self.logfile, 'New cell_attr %r at (%r, %r)\n', cell_attr, rowx, colx)
            if not self.book.xf_list:
                for xfx in xrange(16):
                    self.insert_new_BIFF20_xf(cell_attr='@\x00\x00', style=xfx < 15)

            xfx = self.insert_new_BIFF20_xf(cell_attr=cell_attr)
            return xfx

    def insert_new_BIFF20_xf(self, cell_attr, style=0):
        DEBUG = 0
        blah = DEBUG or self.verbosity >= 2
        book = self.book
        xfx = len(book.xf_list)
        xf = self.fake_XF_from_BIFF20_cell_attr(cell_attr, style)
        xf.xf_index = xfx
        book.xf_list.append(xf)
        if blah:
            xf.dump(self.logfile, header='=== Faked XF %d ===' % xfx, footer='======')
        if xf.format_key not in book.format_map:
            if xf.format_key:
                msg = 'ERROR *** XF[%d] unknown format key (%d, 0x%04x)\n'
                fprintf(self.logfile, msg, xf.xf_index, xf.format_key, xf.format_key)
            fmt = Format(xf.format_key, FUN, UNICODE_LITERAL('General'))
            book.format_map[xf.format_key] = fmt
            book.format_list.append(fmt)
        cellty_from_fmtty = {FNU: XL_CELL_NUMBER, FUN: XL_CELL_NUMBER, 
           FGE: XL_CELL_NUMBER, 
           FDT: XL_CELL_DATE, 
           FTX: XL_CELL_NUMBER}
        fmt = book.format_map[xf.format_key]
        cellty = cellty_from_fmtty[fmt.type]
        self._xf_index_to_xl_type_map[xf.xf_index] = cellty
        self._cell_attr_to_xfx[cell_attr] = xfx
        return xfx

    def fake_XF_from_BIFF20_cell_attr(self, cell_attr, style=0):
        from .formatting import XF, XFAlignment, XFBorder, XFBackground, XFProtection
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
        prot_bits, font_and_format, halign_etc = unpack('<BBB', cell_attr)
        xf.format_key = font_and_format & 63
        xf.font_index = (font_and_format & 192) >> 6
        upkbits(xf.protection, prot_bits, (
         (6, 64, 'cell_locked'),
         (7, 128, 'formula_hidden')))
        xf.alignment.hor_align = halign_etc & 7
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
        xf.parent_style_index = (4095, 0)[style]
        xf.alignment.vert_align = 2
        xf.alignment.rotation = 0
        for attr_stem in ('format font alignment border background protection').split():
            attr = '_' + attr_stem + '_flag'
            setattr(xf, attr, 1)

        return xf

    def req_fmt_info(self):
        if not self.formatting_info:
            raise XLRDError('Feature requires open_workbook(..., formatting_info=True)')

    def computed_column_width(self, colx):
        self.req_fmt_info()
        if self.biff_version >= 80:
            colinfo = self.colinfo_map.get(colx, None)
            if colinfo is not None:
                return colinfo.width
            if self.standardwidth is not None:
                return self.standardwidth
        elif self.biff_version >= 40:
            if self.gcw[colx]:
                if self.standardwidth is not None:
                    return self.standardwidth
            else:
                colinfo = self.colinfo_map.get(colx, None)
                if colinfo is not None:
                    return colinfo.width
        elif self.biff_version == 30:
            colinfo = self.colinfo_map.get(colx, None)
            if colinfo is not None:
                return colinfo.width
        if self.defcolwidth is not None:
            return self.defcolwidth * 256
        else:
            return 2048

    def handle_hlink(self, data):
        if DEBUG:
            print('\n=== hyperlink ===', file=self.logfile)
        record_size = len(data)
        h = Hyperlink()
        h.frowx, h.lrowx, h.fcolx, h.lcolx, guid0, dummy, options = unpack('<HHHH16s4si', data[:32])
        assert guid0 == b'\xd0\xc9\xeay\xf9\xba\xce\x11\x8c\x82\x00\xaa\x00K\xa9\x0b'
        assert dummy == '\x02\x00\x00\x00'
        if DEBUG:
            print('options: %08X' % options, file=self.logfile)
        offset = 32

        def get_nul_terminated_unicode(buf, ofs):
            nb = unpack('<L', buf[ofs:ofs + 4])[0] * 2
            ofs += 4
            uc = unicode(buf[ofs:ofs + nb], 'UTF-16le')[:-1]
            ofs += nb
            return (uc, ofs)

        if options & 20:
            h.desc, offset = get_nul_terminated_unicode(data, offset)
        if options & 128:
            h.target, offset = get_nul_terminated_unicode(data, offset)
        if options & 1 and not options & 256:
            clsid, = unpack('<16s', data[offset:offset + 16])
            if DEBUG:
                fprintf(self.logfile, 'clsid=%r\n', clsid)
            offset += 16
            if clsid == b'\xe0\xc9\xeay\xf9\xba\xce\x11\x8c\x82\x00\xaa\x00K\xa9\x0b':
                h.type = UNICODE_LITERAL('url')
                nbytes = unpack('<L', data[offset:offset + 4])[0]
                offset += 4
                h.url_or_path = unicode(data[offset:offset + nbytes], 'UTF-16le')
                if DEBUG:
                    fprintf(self.logfile, 'initial url=%r len=%d\n', h.url_or_path, len(h.url_or_path))
                endpos = h.url_or_path.find('\x00')
                if DEBUG:
                    print('endpos=%d' % endpos, file=self.logfile)
                h.url_or_path = h.url_or_path[:endpos]
                true_nbytes = 2 * (endpos + 1)
                offset += true_nbytes
                extra_nbytes = nbytes - true_nbytes
                extra_data = data[offset:offset + extra_nbytes]
                offset += extra_nbytes
                if DEBUG:
                    fprintf(self.logfile, 'url=%r\nextra=%r\nnbytes=%d true_nbytes=%d extra_nbytes=%d\n', h.url_or_path, extra_data, nbytes, true_nbytes, extra_nbytes)
                assert extra_nbytes in (24, 0)
            elif clsid == b'\x03\x03\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00F':
                h.type = UNICODE_LITERAL('local file')
                uplevels, nbytes = unpack('<Hi', data[offset:offset + 6])
                offset += 6
                shortpath = '..\\' * uplevels + data[offset:offset + nbytes - 1]
                if DEBUG:
                    fprintf(self.logfile, 'uplevels=%d shortpath=%r\n', uplevels, shortpath)
                offset += nbytes
                offset += 24
                sz = unpack('<i', data[offset:offset + 4])[0]
                if DEBUG:
                    print('sz=%d' % sz, file=self.logfile)
                offset += 4
                if sz:
                    xl = unpack('<i', data[offset:offset + 4])[0]
                    offset += 4
                    offset += 2
                    extended_path = unicode(data[offset:offset + xl], 'UTF-16le')
                    offset += xl
                    h.url_or_path = extended_path
                else:
                    h.url_or_path = shortpath
            else:
                fprintf(self.logfile, '*** unknown clsid %r\n', clsid)
        elif options & 355 == 259:
            h.type = UNICODE_LITERAL('unc')
            h.url_or_path, offset = get_nul_terminated_unicode(data, offset)
        elif options & 363 == 8:
            h.type = UNICODE_LITERAL('workbook')
        else:
            h.type = UNICODE_LITERAL('unknown')
        if options & 8:
            h.textmark, offset = get_nul_terminated_unicode(data, offset)
        if DEBUG:
            h.dump(header='... object dump ...')
            print('offset=%d record_size=%d' % (offset, record_size))
        extra_nbytes = record_size - offset
        if extra_nbytes > 0:
            fprintf(self.logfile, '*** WARNING: hyperlink at r=%d c=%d has %d extra data bytes: %s\n', h.frowx, h.fcolx, extra_nbytes, REPR(data[-extra_nbytes:]))
        else:
            if extra_nbytes < 0:
                raise XLRDError('Bug or corrupt file, send copy of input file for debugging')
            self.hyperlink_list.append(h)
            for rowx in xrange(h.frowx, h.lrowx + 1):
                for colx in xrange(h.fcolx, h.lcolx + 1):
                    self.hyperlink_map[(rowx, colx)] = h

    def handle_quicktip(self, data):
        rcx, frowx, lrowx, fcolx, lcolx = unpack('<5H', data[:10])
        assert rcx == XL_QUICKTIP
        assert self.hyperlink_list
        h = self.hyperlink_list[(-1)]
        assert (frowx, lrowx, fcolx, lcolx) == (h.frowx, h.lrowx, h.fcolx, h.lcolx)
        assert data[-2:] == '\x00\x00'
        h.quicktip = unicode(data[10:-2], 'utf_16_le')

    def handle_msodrawingetc(self, recid, data_len, data):
        if not OBJ_MSO_DEBUG:
            return
        DEBUG = 1
        if self.biff_version < 80:
            return
        o = MSODrawing()
        pos = 0
        while 1:
            if pos < data_len:
                tmp, fbt, cb = unpack('<HHI', data[pos:pos + 8])
                ver = tmp & 15
                inst = tmp >> 4 & 4095
                if ver == 15:
                    ndb = 0
                else:
                    ndb = cb
                if DEBUG:
                    hex_char_dump(data, pos, ndb + 8, base=0, fout=self.logfile)
                    fprintf(self.logfile, 'fbt:0x%04X  inst:%d  ver:0x%X  cb:%d (0x%04X)\n', fbt, inst, ver, cb, cb)
                if fbt == 61456:
                    assert ndb == 18
                    o.anchor_unk, o.anchor_colx_lo, o.anchor_rowx_lo, o.anchor_colx_hi, o.anchor_rowx_hi = unpack('<Hiiii', data[pos + 8:pos + 8 + ndb])
                elif fbt == 61457:
                    assert cb == 0
                    assert pos + 8 == data_len
                pos += ndb + 8
        else:
            assert pos == data_len

        if DEBUG:
            o.dump(self.logfile, header='=== MSODrawing ===', footer=' ')

    def handle_obj(self, data):
        if self.biff_version < 80:
            return None
        else:
            o = MSObj()
            data_len = len(data)
            pos = 0
            if OBJ_MSO_DEBUG:
                fprintf(self.logfile, '... OBJ record len=%d...\n', data_len)
            while pos < data_len:
                ft, cb = unpack('<HH', data[pos:pos + 4])
                if OBJ_MSO_DEBUG:
                    fprintf(self.logfile, 'pos=%d ft=0x%04X cb=%d\n', pos, ft, cb)
                    hex_char_dump(data, pos, cb + 4, base=0, fout=self.logfile)
                if pos == 0 and not (ft == 21 and cb == 18):
                    if self.verbosity:
                        fprintf(self.logfile, '*** WARNING Ignoring antique or corrupt OBJECT record\n')
                    return None
                if ft == 21:
                    assert pos == 0
                    o.type, o.id, option_flags = unpack('<HHH', data[pos + 4:pos + 10])
                    upkbits(o, option_flags, (
                     (0, 1, 'locked'),
                     (4, 16, 'printable'),
                     (8, 256, 'autofilter'),
                     (9, 512, 'scrollbar_flag'),
                     (13, 8192, 'autofill'),
                     (14, 16384, 'autoline')))
                elif ft == 0:
                    if data[pos:data_len] == '\x00' * (data_len - pos):
                        break
                    msg = 'Unexpected data at end of OBJECT record'
                    fprintf(self.logfile, '*** ERROR %s\n' % msg)
                    hex_char_dump(data, pos, data_len - pos, base=0, fout=self.logfile)
                    raise XLRDError(msg)
                elif ft == 12:
                    values = unpack('<5H', data[pos + 8:pos + 18])
                    for value, tag in zip(values, ('value', 'min', 'max', 'inc', 'page')):
                        setattr(o, 'scrollbar_' + tag, value)

                elif ft == 13:
                    if OBJ_MSO_DEBUG:
                        fprintf(self.logfile, "*** OBJ record has ft==0x0D 'notes' structure\n")
                elif ft == 19:
                    if o.autofilter:
                        break
                pos += cb + 4

            if OBJ_MSO_DEBUG:
                o.dump(self.logfile, header='=== MSOBj ===', footer=' ')
            return o

    def handle_note(self, data, txos):
        if OBJ_MSO_DEBUG:
            fprintf(self.logfile, '... NOTE record ...\n')
            hex_char_dump(data, 0, len(data), base=0, fout=self.logfile)
        o = Note()
        data_len = len(data)
        if self.biff_version < 80:
            o.rowx, o.colx, expected_bytes = unpack('<HHH', data[:6])
            nb = len(data) - 6
            assert nb <= expected_bytes
            pieces = [data[6:]]
            expected_bytes -= nb
            while expected_bytes > 0:
                rc2, data2_len, data2 = self.book.get_record_parts()
                assert rc2 == XL_NOTE
                dummy_rowx, nb = unpack('<H2xH', data2[:6])
                assert dummy_rowx == 65535
                assert nb == data2_len - 6
                pieces.append(data2[6:])
                expected_bytes -= nb

            assert expected_bytes == 0
            enc = self.book.encoding or self.book.derive_encoding()
            o.text = unicode(('').join(pieces), enc)
            o.rich_text_runlist = [(0, 0)]
            o.show = 0
            o.row_hidden = 0
            o.col_hidden = 0
            o.author = UNICODE_LITERAL('')
            o._object_id = None
            self.cell_note_map[(o.rowx, o.colx)] = o
            return
        else:
            o.rowx, o.colx, option_flags, o._object_id = unpack('<4H', data[:8])
            o.show = option_flags >> 1 & 1
            o.row_hidden = option_flags >> 7 & 1
            o.col_hidden = option_flags >> 8 & 1
            o.author, endpos = unpack_unicode_update_pos(data, 8, lenlen=2)
            assert data_len - endpos in (0, 1)
            if OBJ_MSO_DEBUG:
                o.dump(self.logfile, header='=== Note ===', footer=' ')
            txo = txos.get(o._object_id)
            if txo:
                o.text = txo.text
                o.rich_text_runlist = txo.rich_text_runlist
                self.cell_note_map[(o.rowx, o.colx)] = o
            return

    def handle_txo(self, data):
        if self.biff_version < 80:
            return
        o = MSTxo()
        data_len = len(data)
        fmt = '<HH6sHHH'
        fmtsize = calcsize(fmt)
        option_flags, o.rot, controlInfo, cchText, cbRuns, o.ifntEmpty = unpack(fmt, data[:fmtsize])
        o.fmla = data[fmtsize:]
        upkbits(o, option_flags, (
         (3, 14, 'horz_align'),
         (6, 112, 'vert_align'),
         (9, 512, 'lock_text'),
         (14, 16384, 'just_last'),
         (15, 32768, 'secret_edit')))
        totchars = 0
        o.text = UNICODE_LITERAL('')
        while totchars < cchText:
            rc2, data2_len, data2 = self.book.get_record_parts()
            assert rc2 == XL_CONTINUE
            if OBJ_MSO_DEBUG:
                hex_char_dump(data2, 0, data2_len, base=0, fout=self.logfile)
            nb = BYTES_ORD(data2[0])
            nchars = data2_len - 1
            if nb:
                assert nchars % 2 == 0
                nchars //= 2
            utext, endpos = unpack_unicode_update_pos(data2, 0, known_len=nchars)
            assert endpos == data2_len
            o.text += utext
            totchars += nchars

        o.rich_text_runlist = []
        totruns = 0
        while totruns < cbRuns:
            rc3, data3_len, data3 = self.book.get_record_parts()
            assert rc3 == XL_CONTINUE
            assert data3_len % 8 == 0
            for pos in xrange(0, data3_len, 8):
                run = unpack('<HH4x', data3[pos:pos + 8])
                o.rich_text_runlist.append(run)
                totruns += 8

        while o.rich_text_runlist and o.rich_text_runlist[(-1)][0] == cchText:
            del o.rich_text_runlist[-1]

        if OBJ_MSO_DEBUG:
            o.dump(self.logfile, header='=== MSTxo ===', footer=' ')
            print(o.rich_text_runlist, file=self.logfile)
        return o

    def handle_feat11(self, data):
        if not OBJ_MSO_DEBUG:
            return
        rt, grbitFrt, Ref0, isf, fHdr, reserved0, cref, cbFeatData, reserved1, Ref1 = unpack('<HH8sHBiHiH8s', data[0:35])
        assert reserved0 == 0
        assert reserved1 == 0
        assert isf == 5
        assert rt == 2162
        assert fHdr == 0
        assert Ref1 == Ref0
        print(self.logfile, 'FEAT11: grbitFrt=%d  Ref0=%r cref=%d cbFeatData=%d\n', grbitFrt, Ref0, cref, cbFeatData)
        lt, idList, crwHeader, crwTotals, idFieldNext, cbFSData, rupBuild, unusedShort, listFlags, lPosStmCache, cbStmCache, cchStmCache, lem, rgbHashParam, cchName = unpack('<iiiiiiHHiiiii16sH', data[35:101])
        print('lt=%d  idList=%d crwHeader=%d  crwTotals=%d  idFieldNext=%d cbFSData=%d\nrupBuild=%d  unusedShort=%d listFlags=%04X  lPosStmCache=%d  cbStmCache=%d\ncchStmCache=%d  lem=%d  rgbHashParam=%r  cchName=%d' % (
         lt, idList, crwHeader, crwTotals, idFieldNext, cbFSData,
         rupBuild, unusedShort, listFlags, lPosStmCache, cbStmCache,
         cchStmCache, lem, rgbHashParam, cchName), file=self.logfile)


class MSODrawing(BaseObject):
    pass


class MSObj(BaseObject):
    pass


class MSTxo(BaseObject):
    pass


class Note(BaseObject):
    author = UNICODE_LITERAL('')
    col_hidden = 0
    colx = 0
    rich_text_runlist = None
    row_hidden = 0
    rowx = 0
    show = 0
    text = UNICODE_LITERAL('')


class Hyperlink(BaseObject):
    frowx = None
    lrowx = None
    fcolx = None
    lcolx = None
    type = None
    url_or_path = None
    desc = None
    target = None
    textmark = None
    quicktip = None


def unpack_RK(rk_str):
    flags = BYTES_ORD(rk_str[0])
    if flags & 2:
        i, = unpack('<i', rk_str)
        i >>= 2
        if flags & 1:
            return i / 100.0
        return float(i)
    else:
        d, = unpack('<d', '\x00\x00\x00\x00' + BYTES_LITERAL(chr(flags & 252)) + rk_str[1:4])
        if flags & 1:
            return d / 100.0
        return d


cellty_from_fmtty = {FNU: XL_CELL_NUMBER, 
   FUN: XL_CELL_NUMBER, 
   FGE: XL_CELL_NUMBER, 
   FDT: XL_CELL_DATE, 
   FTX: XL_CELL_NUMBER}
ctype_text = {XL_CELL_EMPTY: 'empty', 
   XL_CELL_TEXT: 'text', 
   XL_CELL_NUMBER: 'number', 
   XL_CELL_DATE: 'xldate', 
   XL_CELL_BOOLEAN: 'bool', 
   XL_CELL_ERROR: 'error', 
   XL_CELL_BLANK: 'blank'}

class Cell(BaseObject):
    __slots__ = [
     'ctype', 'value', 'xf_index']

    def __init__(self, ctype, value, xf_index=None):
        self.ctype = ctype
        self.value = value
        self.xf_index = xf_index

    def __repr__(self):
        if self.xf_index is None:
            return '%s:%r' % (ctype_text[self.ctype], self.value)
        else:
            return '%s:%r (XF:%r)' % (ctype_text[self.ctype], self.value, self.xf_index)
            return


empty_cell = Cell(XL_CELL_EMPTY, '')

class Colinfo(BaseObject):
    width = 0
    xf_index = -1
    hidden = 0
    bit1_flag = 0
    outline_level = 0
    collapsed = 0


_USE_SLOTS = 1

class Rowinfo(BaseObject):
    if _USE_SLOTS:
        __slots__ = ('height', 'has_default_height', 'outline_level', 'outline_group_starts_ends',
                     'hidden', 'height_mismatch', 'has_default_xf_index', 'xf_index',
                     'additional_space_above', 'additional_space_below')

    def __init__(self):
        self.height = None
        self.has_default_height = None
        self.outline_level = None
        self.outline_group_starts_ends = None
        self.hidden = None
        self.height_mismatch = None
        self.has_default_xf_index = None
        self.xf_index = None
        self.additional_space_above = None
        self.additional_space_below = None
        return

    def __getstate__(self):
        return (
         self.height,
         self.has_default_height,
         self.outline_level,
         self.outline_group_starts_ends,
         self.hidden,
         self.height_mismatch,
         self.has_default_xf_index,
         self.xf_index,
         self.additional_space_above,
         self.additional_space_below)

    def __setstate__(self, state):
        self.height, self.has_default_height, self.outline_level, self.outline_group_starts_ends, self.hidden, self.height_mismatch, self.has_default_xf_index, self.xf_index, self.additional_space_above, self.additional_space_below = state