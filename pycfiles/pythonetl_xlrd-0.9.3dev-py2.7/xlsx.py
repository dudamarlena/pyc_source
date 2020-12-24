# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\xlsx.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function, unicode_literals
DEBUG = 0
import sys, re
from .timemachine import *
from .book import Book, Name
from .biffh import error_text_from_code, XLRDError, XL_CELL_BLANK, XL_CELL_TEXT, XL_CELL_BOOLEAN, XL_CELL_ERROR
from .formatting import is_date_format_string, Format, XF
from .sheet import Sheet
DLF = sys.stdout
ET = None
ET_has_iterparse = False

def ensure_elementtree_imported(verbosity, logfile):
    global ET
    global ET_has_iterparse
    if ET is not None:
        return
    else:
        if b'IronPython' in sys.version:
            import xml.etree.ElementTree as ET
        else:
            try:
                import xml.etree.cElementTree as ET
            except ImportError:
                try:
                    import cElementTree as ET
                except ImportError:
                    try:
                        import lxml.etree as ET
                    except ImportError:
                        try:
                            import xml.etree.ElementTree as ET
                        except ImportError:
                            try:
                                import elementtree.ElementTree as ET
                            except ImportError:
                                raise Exception(b'Failed to import an ElementTree implementation')

        if hasattr(ET, b'iterparse'):
            _dummy_stream = BYTES_IO(b'')
            try:
                ET.iterparse(_dummy_stream)
                ET_has_iterparse = True
            except NotImplementedError:
                pass

        if verbosity:
            etree_version = repr([ (item, getattr(ET, item)) for item in ET.__dict__.keys() if item.lower().replace(b'_', b'') == b'version'
                                 ])
            print(ET.__file__, ET.__name__, etree_version, ET_has_iterparse, file=logfile)
        return


def split_tag(tag):
    pos = tag.rfind(b'}') + 1
    if pos >= 2:
        return (tag[:pos], tag[pos:])
    return (
     b'', tag)


def augment_keys(adict, uri):
    for x in list(adict.keys()):
        adict[uri + x] = adict[x]


_UPPERCASE_1_REL_INDEX = {}
for _x in xrange(26):
    _UPPERCASE_1_REL_INDEX[b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[_x]] = _x + 1

for _x in b'123456789':
    _UPPERCASE_1_REL_INDEX[_x] = 0

del _x

def cell_name_to_rowx_colx(cell_name, letter_value=_UPPERCASE_1_REL_INDEX):
    colx = 0
    charx = -1
    try:
        for c in cell_name:
            charx += 1
            lv = letter_value[c]
            if lv:
                colx = colx * 26 + lv
            else:
                colx = colx - 1
                assert 0 <= colx < X12_MAX_COLS
                break

    except KeyError:
        raise Exception(b'Unexpected character %r in cell name %r' % (c, cell_name))

    rowx = int(cell_name[charx:]) - 1
    return (rowx, colx)


error_code_from_text = {}
for _code, _text in error_text_from_code.items():
    error_code_from_text[_text] = _code

U_SSML12 = b'{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
U_ODREL = b'{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
U_PKGREL = b'{http://schemas.openxmlformats.org/package/2006/relationships}'
U_CP = b'{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}'
U_DC = b'{http://purl.org/dc/elements/1.1/}'
U_DCTERMS = b'{http://purl.org/dc/terms/}'
XML_SPACE_ATTR = b'{http://www.w3.org/XML/1998/namespace}space'
XML_WHITESPACE = b'\t\n \r'
X12_MAX_ROWS = 1048576
X12_MAX_COLS = 16384
V_TAG = U_SSML12 + b'v'
F_TAG = U_SSML12 + b'f'
IS_TAG = U_SSML12 + b'is'

def unescape(s, subber=re.compile(b'_x[0-9A-Fa-f]{4,4}_', re.UNICODE).sub, repl=lambda mobj: unichr(int(mobj.group(0)[2:6], 16))):
    if b'_' in s:
        return subber(repl, s)
    return s


def cooked_text(self, elem):
    t = elem.text
    if t is None:
        return b''
    else:
        if elem.get(XML_SPACE_ATTR) != b'preserve':
            t = t.strip(XML_WHITESPACE)
        return ensure_unicode(unescape(t))


def get_text_from_si_or_is(self, elem, r_tag=U_SSML12 + b'r', t_tag=U_SSML12 + b't'):
    """Returns unescaped unicode"""
    accum = []
    for child in elem:
        tag = child.tag
        if tag == t_tag:
            t = cooked_text(self, child)
            if t:
                accum.append(t)
        elif tag == r_tag:
            for tnode in child:
                if tnode.tag == t_tag:
                    t = cooked_text(self, tnode)
                    if t:
                        accum.append(t)

    return (b'').join(accum)


def map_attributes(amap, elem, obj):
    for xml_attr, obj_attr, cnv_func_or_const in amap:
        if not xml_attr:
            setattr(obj, obj_attr, cnv_func_or_const)
            continue
        if not obj_attr:
            continue
        raw_value = elem.get(xml_attr)
        cooked_value = cnv_func_or_const(raw_value)
        setattr(obj, obj_attr, cooked_value)


def cnv_ST_Xstring(s):
    if s is None:
        return b''
    else:
        return ensure_unicode(s)


def cnv_xsd_unsignedInt(s):
    if not s:
        return None
    else:
        value = int(s)
        assert value >= 0
        return value


def cnv_xsd_boolean(s):
    if not s:
        return 0
    if s in ('1', 'true', 'on'):
        return 1
    if s in ('0', 'false', 'off'):
        return 0
    raise ValueError(b'unexpected xsd:boolean value: %r' % s)


_defined_name_attribute_map = (
 (
  b'name', b'name', cnv_ST_Xstring),
 (
  b'comment', b'', cnv_ST_Xstring),
 (
  b'customMenu', b'', cnv_ST_Xstring),
 (
  b'description', b'', cnv_ST_Xstring),
 (
  b'help', b'', cnv_ST_Xstring),
 (
  b'statusBar', b'', cnv_ST_Xstring),
 (
  b'localSheetId', b'scope', cnv_xsd_unsignedInt),
 (
  b'hidden', b'hidden', cnv_xsd_boolean),
 (
  b'function', b'func', cnv_xsd_boolean),
 (
  b'vbProcedure', b'vbasic', cnv_xsd_boolean),
 (
  b'xlm', b'macro', cnv_xsd_boolean),
 (
  b'functionGroupId', b'funcgroup', cnv_xsd_unsignedInt),
 (
  b'shortcutKey', b'', cnv_ST_Xstring),
 (
  b'publishToServer', b'', cnv_xsd_boolean),
 (
  b'workbookParameter', b'', cnv_xsd_boolean),
 ('', 'any_err', 0),
 ('', 'any_external', 0),
 ('', 'any_rel', 0),
 ('', 'basic_formula_len', 0),
 ('', 'binary', 0),
 ('', 'builtin', 0),
 ('', 'complex', 0),
 ('', 'evaluated', 0),
 ('', 'excel_sheet_index', 0),
 ('', 'excel_sheet_num', 0),
 ('', 'option_flags', 0),
 ('', 'result', None),
 ('', 'stack', None))

def make_name_access_maps(bk):
    name_and_scope_map = {}
    name_map = {}
    num_names = len(bk.name_obj_list)
    for namex in xrange(num_names):
        nobj = bk.name_obj_list[namex]
        name_lcase = nobj.name.lower()
        key = (name_lcase, nobj.scope)
        if key in name_and_scope_map:
            msg = b'Duplicate entry %r in name_and_scope_map' % (key,)
            if bk.verbosity:
                print(msg, file=bk.logfile)
        name_and_scope_map[key] = nobj
        if name_lcase in name_map:
            name_map[name_lcase].append((nobj.scope, nobj))
        else:
            name_map[name_lcase] = [
             (
              nobj.scope, nobj)]

    for key in name_map.keys():
        alist = name_map[key]
        alist.sort()
        name_map[key] = [ x[1] for x in alist ]

    bk.name_and_scope_map = name_and_scope_map
    bk.name_map = name_map


class X12General(object):

    def process_stream(self, stream, heading=None):
        if self.verbosity >= 2 and heading is not None:
            fprintf(self.logfile, b'\n=== %s ===\n', heading)
        self.tree = ET.parse(stream)
        getmethod = self.tag2meth.get
        for elem in self.tree.getiterator():
            if self.verbosity >= 3:
                self.dump_elem(elem)
            meth = getmethod(elem.tag)
            if meth:
                meth(self, elem)

        self.finish_off()
        return

    def finish_off(self):
        pass

    def dump_elem(self, elem):
        fprintf(self.logfile, b'===\ntag=%r len=%d attrib=%r text=%r tail=%r\n', split_tag(elem.tag)[1], len(elem), elem.attrib, elem.text, elem.tail)

    def dumpout(self, fmt, *vargs):
        text = (b'            ' + fmt + b'\n') % vargs
        self.logfile.write(text)


class X12Book(X12General):

    def __init__(self, bk, logfile=DLF, verbosity=False):
        self.bk = bk
        self.logfile = logfile
        self.verbosity = verbosity
        self.bk.nsheets = 0
        self.bk.props = {}
        self.relid2path = {}
        self.relid2reltype = {}
        self.sheet_targets = []
        self.sheetIds = []

    core_props_menu = {U_CP + b'lastModifiedBy': (
                                b'last_modified_by', cnv_ST_Xstring), 
       U_DC + b'creator': (
                         b'creator', cnv_ST_Xstring), 
       U_DCTERMS + b'modified': (
                               b'modified', cnv_ST_Xstring), 
       U_DCTERMS + b'created': (
                              b'created', cnv_ST_Xstring)}

    def process_coreprops(self, stream):
        if self.verbosity >= 2:
            fprintf(self.logfile, b'\n=== coreProps ===\n')
        self.tree = ET.parse(stream)
        getmenu = self.core_props_menu.get
        props = {}
        for elem in self.tree.getiterator():
            if self.verbosity >= 3:
                self.dump_elem(elem)
            menu = getmenu(elem.tag)
            if menu:
                attr, func = menu
                value = func(elem.text)
                props[attr] = value

        self.bk.user_name = props.get(b'last_modified_by') or props.get(b'creator')
        self.bk.props = props
        if self.verbosity >= 2:
            fprintf(self.logfile, b'props: %r\n', props)
        self.finish_off()

    def process_rels(self, stream):
        if self.verbosity >= 2:
            fprintf(self.logfile, b'\n=== Relationships ===\n')
        tree = ET.parse(stream)
        r_tag = U_PKGREL + b'Relationship'
        for elem in tree.findall(r_tag):
            rid = elem.get(b'Id')
            target = elem.get(b'Target')
            reltype = elem.get(b'Type').split(b'/')[(-1)]
            if self.verbosity >= 2:
                self.dumpout(b'Id=%r Type=%r Target=%r', rid, reltype, target)
            self.relid2reltype[rid] = reltype
            if target.startswith(b'/'):
                self.relid2path[rid] = target[1:]
            else:
                self.relid2path[rid] = b'xl/' + target

    def do_defined_name(self, elem):
        if 0 and self.verbosity >= 3:
            self.dump_elem(elem)
        nobj = Name()
        bk = self.bk
        nobj.bk = bk
        nobj.name_index = len(bk.name_obj_list)
        bk.name_obj_list.append(nobj)
        nobj.name = elem.get(b'name')
        nobj.raw_formula = None
        nobj.formula_text = cooked_text(self, elem)
        map_attributes(_defined_name_attribute_map, elem, nobj)
        if nobj.scope is None:
            nobj.scope = -1
        if nobj.name.startswith(b'_xlnm.'):
            nobj.builtin = 1
        if self.verbosity >= 2:
            nobj.dump(header=b'=== Name object ===')
        return

    def do_defined_names(self, elem):
        for child in elem:
            self.do_defined_name(child)

        make_name_access_maps(self.bk)

    def do_sheet(self, elem):
        bk = self.bk
        sheetx = bk.nsheets
        rid = elem.get(U_ODREL + b'id')
        sheetId = int(elem.get(b'sheetId'))
        name = unescape(ensure_unicode(elem.get(b'name')))
        reltype = self.relid2reltype[rid]
        target = self.relid2path[rid]
        if self.verbosity >= 2:
            self.dumpout(b'sheetx=%d sheetId=%r rid=%r type=%r name=%r', sheetx, sheetId, rid, reltype, name)
        if reltype != b'worksheet':
            if self.verbosity >= 2:
                self.dumpout(b'Ignoring sheet of type %r (name=%r)', reltype, name)
            return
        state = elem.get(b'state')
        visibility_map = {None: 0, 
           b'visible': 0, 
           b'hidden': 1, 
           b'veryHidden': 2}
        bk._sheet_visibility.append(visibility_map[state])
        sheet = Sheet(bk, position=None, name=name, number=sheetx)
        sheet.utter_max_rows = X12_MAX_ROWS
        sheet.utter_max_cols = X12_MAX_COLS
        bk._sheet_list.append(sheet)
        bk._sheet_names.append(name)
        bk.nsheets += 1
        self.sheet_targets.append(target)
        self.sheetIds.append(sheetId)
        return

    def do_workbookpr(self, elem):
        datemode = cnv_xsd_boolean(elem.get(b'date1904'))
        if self.verbosity >= 2:
            self.dumpout(b'datemode=%r', datemode)
        self.bk.datemode = datemode

    tag2meth = {b'definedNames': do_defined_names, 
       b'workbookPr': do_workbookpr, 
       b'sheet': do_sheet}
    augment_keys(tag2meth, U_SSML12)


class X12SST(X12General):

    def __init__(self, bk, logfile=DLF, verbosity=0):
        self.bk = bk
        self.logfile = logfile
        self.verbosity = verbosity
        if ET_has_iterparse:
            self.process_stream = self.process_stream_iterparse
        else:
            self.process_stream = self.process_stream_findall

    def process_stream_iterparse(self, stream, heading=None):
        if self.verbosity >= 2 and heading is not None:
            fprintf(self.logfile, b'\n=== %s ===\n', heading)
        si_tag = U_SSML12 + b'si'
        elemno = -1
        sst = self.bk._sharedstrings
        for event, elem in ET.iterparse(stream):
            if elem.tag != si_tag:
                continue
            elemno = elemno + 1
            if self.verbosity >= 3:
                fprintf(self.logfile, b'element #%d\n', elemno)
                self.dump_elem(elem)
            result = get_text_from_si_or_is(self, elem)
            sst.append(result)
            elem.clear()

        if self.verbosity >= 2:
            self.dumpout(b'Entries in SST: %d', len(sst))
        if self.verbosity >= 3:
            for x, s in enumerate(sst):
                fprintf(self.logfile, b'SST x=%d s=%r\n', x, s)

        return

    def process_stream_findall(self, stream, heading=None):
        if self.verbosity >= 2 and heading is not None:
            fprintf(self.logfile, b'\n=== %s ===\n', heading)
        self.tree = ET.parse(stream)
        si_tag = U_SSML12 + b'si'
        elemno = -1
        sst = self.bk._sharedstrings
        for elem in self.tree.findall(si_tag):
            elemno = elemno + 1
            if self.verbosity >= 3:
                fprintf(self.logfile, b'element #%d\n', elemno)
                self.dump_elem(elem)
            result = get_text_from_si_or_is(self, elem)
            sst.append(result)

        if self.verbosity >= 2:
            self.dumpout(b'Entries in SST: %d', len(sst))
        return


class X12Styles(X12General):

    def __init__(self, bk, logfile=DLF, verbosity=0):
        self.bk = bk
        self.logfile = logfile
        self.verbosity = verbosity
        self.xf_counts = [0, 0]
        self.xf_type = None
        self.fmt_is_date = {}
        for x in list(range(14, 23)) + list(range(45, 48)):
            self.fmt_is_date[x] = 1

        self.bk._xf_index_to_xl_type_map[0] = 2
        return

    def do_cellstylexfs(self, elem):
        self.xf_type = 0

    def do_cellxfs(self, elem):
        self.xf_type = 1

    def do_numfmt(self, elem):
        formatCode = ensure_unicode(elem.get(b'formatCode'))
        numFmtId = int(elem.get(b'numFmtId'))
        is_date = is_date_format_string(self.bk, formatCode)
        self.fmt_is_date[numFmtId] = is_date
        fmt_obj = Format(numFmtId, is_date + 2, formatCode)
        self.bk.format_map[numFmtId] = fmt_obj
        if self.verbosity >= 3:
            self.dumpout(b'numFmtId=%d formatCode=%r is_date=%d', numFmtId, formatCode, is_date)

    def do_xf(self, elem):
        if self.xf_type != 1:
            return
        xfx = self.xf_counts[self.xf_type]
        self.xf_counts[self.xf_type] = xfx + 1
        xf = XF()
        self.bk.xf_list.append(xf)
        self.bk.xfcount += 1
        numFmtId = int(elem.get(b'numFmtId', b'0'))
        xf.format_key = numFmtId
        is_date = self.fmt_is_date.get(numFmtId, 0)
        self.bk._xf_index_to_xl_type_map[xfx] = is_date + 2
        if self.verbosity >= 3:
            self.dumpout(b'xfx=%d numFmtId=%d', xfx, numFmtId)
            self.dumpout(repr(self.bk._xf_index_to_xl_type_map))

    tag2meth = {b'cellStyleXfs': do_cellstylexfs, 
       b'cellXfs': do_cellxfs, 
       b'numFmt': do_numfmt, 
       b'xf': do_xf}
    augment_keys(tag2meth, U_SSML12)


class X12Sheet(X12General):

    def __init__(self, sheet, logfile=DLF, verbosity=0):
        self.sheet = sheet
        self.logfile = logfile
        self.verbosity = verbosity
        self.rowx = -1
        self.bk = sheet.book
        self.sst = self.bk._sharedstrings
        self.warned_no_cell_name = 0
        self.warned_no_row_num = 0
        if ET_has_iterparse:
            self.process_stream = self.own_process_stream

    def own_process_stream(self, stream, heading=None):
        if self.verbosity >= 2 and heading is not None:
            fprintf(self.logfile, b'\n=== %s ===\n', heading)
        getmethod = self.tag2meth.get
        row_tag = U_SSML12 + b'row'
        self_do_row = self.do_row
        for event, elem in ET.iterparse(stream):
            if elem.tag == row_tag:
                self_do_row(elem)
                elem.clear()
            elif elem.tag == U_SSML12 + b'dimension':
                self.do_dimension(elem)

        self.finish_off()
        return

    def do_dimension(self, elem):
        ref = elem.get(b'ref')
        if ref:
            last_cell_ref = ref.split(b':')[(-1)]
            rowx, colx = cell_name_to_rowx_colx(last_cell_ref)
            self.sheet._dimnrows = rowx + 1
            self.sheet._dimncols = colx + 1

    def do_row(self, row_elem):

        def bad_child_tag(child_tag):
            raise Exception(b'cell type %s has unexpected child <%s> at rowx=%r colx=%r' % (cell_type, child_tag, rowx, colx))

        row_number = row_elem.get(b'r')
        if row_number is None:
            self.rowx += 1
            explicit_row_number = 0
            if self.verbosity and not self.warned_no_row_num:
                self.dumpout(b'no row number; assuming rowx=%d', self.rowx)
                self.warned_no_row_num = 1
        else:
            self.rowx = int(row_number) - 1
            explicit_row_number = 1
        assert 0 <= self.rowx < X12_MAX_ROWS
        rowx = self.rowx
        colx = -1
        if self.verbosity >= 3:
            self.dumpout(b'<row> row_number=%r rowx=%d explicit=%d', row_number, self.rowx, explicit_row_number)
        letter_value = _UPPERCASE_1_REL_INDEX
        for cell_elem in row_elem:
            cell_name = cell_elem.get(b'r')
            if cell_name is None:
                colx += 1
                if self.verbosity and not self.warned_no_cell_name:
                    self.dumpout(b'no cellname; assuming rowx=%d colx=%d', rowx, colx)
                    self.warned_no_cell_name = 1
            else:
                colx = 0
                charx = -1
                try:
                    for c in cell_name:
                        charx += 1
                        lv = letter_value[c]
                        if lv:
                            colx = colx * 26 + lv
                        else:
                            colx = colx - 1
                            assert 0 <= colx < X12_MAX_COLS
                            break

                except KeyError:
                    raise Exception(b'Unexpected character %r in cell name %r' % (c, cell_name))

            if explicit_row_number and cell_name[charx:] != row_number:
                raise Exception(b'cell name %r but row number is %r' % (cell_name, row_number))
            xf_index = int(cell_elem.get(b's', b'0'))
            cell_type = cell_elem.get(b't', b'n')
            tvalue = None
            formula = None
            if cell_type == b'n':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == V_TAG:
                        tvalue = child.text
                    elif child_tag == F_TAG:
                        formula = cooked_text(self, child)
                    else:
                        raise Exception(b'unexpected tag %r' % child_tag)

                if not tvalue:
                    if self.bk.formatting_info:
                        self.sheet.put_cell(rowx, colx, XL_CELL_BLANK, b'', xf_index)
                else:
                    self.sheet.put_cell(rowx, colx, None, float(tvalue), xf_index)
            elif cell_type == b's':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == V_TAG:
                        tvalue = child.text
                    elif child_tag == F_TAG:
                        formula = child.text
                    else:
                        bad_child_tag(child_tag)

                if not tvalue:
                    if self.bk.formatting_info:
                        self.sheet.put_cell(rowx, colx, XL_CELL_BLANK, b'', xf_index)
                else:
                    value = self.sst[int(tvalue)]
                    self.sheet.put_cell(rowx, colx, XL_CELL_TEXT, value, xf_index)
            elif cell_type == b'str':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == V_TAG:
                        tvalue = cooked_text(self, child)
                    elif child_tag == F_TAG:
                        formula = cooked_text(self, child)
                    else:
                        bad_child_tag(child_tag)

                self.sheet.put_cell(rowx, colx, XL_CELL_TEXT, tvalue, xf_index)
            elif cell_type == b'b':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == V_TAG:
                        tvalue = child.text
                    elif child_tag == F_TAG:
                        formula = cooked_text(self, child)
                    else:
                        bad_child_tag(child_tag)

                self.sheet.put_cell(rowx, colx, XL_CELL_BOOLEAN, int(tvalue), xf_index)
            elif cell_type == b'e':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == V_TAG:
                        tvalue = child.text
                    elif child_tag == F_TAG:
                        formula = cooked_text(self, child)
                    else:
                        bad_child_tag(child_tag)

                value = error_code_from_text[tvalue]
                self.sheet.put_cell(rowx, colx, XL_CELL_ERROR, value, xf_index)
            elif cell_type == b'inlineStr':
                for child in cell_elem:
                    child_tag = child.tag
                    if child_tag == IS_TAG:
                        tvalue = get_text_from_si_or_is(self, child)
                    else:
                        bad_child_tag(child_tag)

                assert tvalue is not None
                self.sheet.put_cell(rowx, colx, XL_CELL_TEXT, tvalue, xf_index)
            else:
                raise Exception(b'Unknown cell type %r in rowx=%d colx=%d' % (cell_type, rowx, colx))

        return

    tag2meth = {b'row': do_row}
    augment_keys(tag2meth, U_SSML12)


def getzflo(zipfile, member_path):
    try:
        return zipfile.open(member_path)
    except AttributeError:
        return BYTES_IO(zipfile.read(member_path))


def open_workbook_2007_xml(zf, component_names, logfile=sys.stdout, verbosity=0, use_mmap=0, formatting_info=0, on_demand=0, ragged_rows=0):
    ensure_elementtree_imported(verbosity, logfile)
    bk = Book()
    bk.logfile = logfile
    bk.verbosity = verbosity
    bk.formatting_info = formatting_info
    if formatting_info:
        raise NotImplementedError(b'formatting_info=True not yet implemented')
    bk.use_mmap = False
    bk.on_demand = on_demand
    if on_demand:
        if verbosity:
            print(b'WARNING *** on_demand=True not yet implemented; falling back to False', file=bk.logfile)
        bk.on_demand = False
    bk.ragged_rows = ragged_rows
    x12book = X12Book(bk, logfile, verbosity)
    zflo = getzflo(zf, b'xl/_rels/workbook.xml.rels')
    x12book.process_rels(zflo)
    del zflo
    zflo = getzflo(zf, b'xl/workbook.xml')
    x12book.process_stream(zflo, b'Workbook')
    del zflo
    props_name = b'docProps/core.xml'
    if props_name in component_names:
        zflo = getzflo(zf, props_name)
        x12book.process_coreprops(zflo)
    x12sty = X12Styles(bk, logfile, verbosity)
    if b'xl/styles.xml' in component_names:
        zflo = getzflo(zf, b'xl/styles.xml')
        x12sty.process_stream(zflo, b'styles')
        del zflo
    sst_fname = b'xl/sharedStrings.xml'
    x12sst = X12SST(bk, logfile, verbosity)
    if sst_fname in component_names:
        zflo = getzflo(zf, sst_fname)
        x12sst.process_stream(zflo, b'SST')
        del zflo
    for sheetx in range(bk.nsheets):
        fname = x12book.sheet_targets[sheetx]
        zflo = getzflo(zf, fname)
        sheet = bk._sheet_list[sheetx]
        x12sheet = X12Sheet(sheet, logfile, verbosity)
        heading = b'Sheet %r (sheetx=%d) from %r' % (sheet.name, sheetx, fname)
        x12sheet.process_stream(zflo, heading)
        del zflo
        sheet.tidy_dimensions()

    return bk