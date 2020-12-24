# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\examples\xlrdnameAPIdemo.py
# Compiled at: 2013-10-17 14:03:42
from __future__ import print_function
import xlrd
from xlrd.timemachine import REPR
import sys, glob

def scope_as_string(book, scope):
    if 0 <= scope < book.nsheets:
        return 'sheet #%d (%r)' % (scope, REPR(book.sheet_names()[scope]))
    if scope == -1:
        return 'Global'
    if scope == -2:
        return 'Macro/VBA'
    return 'Unknown scope value (%r)' % REPR(scope)


def do_scope_query(book, scope_strg, show_contents=0, f=sys.stdout):
    try:
        qscope = int(scope_strg)
    except ValueError:
        if scope_strg == '*':
            qscope = None
        else:
            qscope = book.sheet_names().index(scope_strg)
            print('%r => %d' % (scope_strg, qscope), file=f)

    for nobj in book.name_obj_list:
        if qscope is None or nobj.scope == qscope:
            show_name_object(book, nobj, show_contents, f)

    return


def show_name_details(book, name, show_contents=0, f=sys.stdout):
    """
    book -- Book object obtained from xlrd.open_workbook().
    name -- The name that's being investigated.
    show_contents -- 0: Don't; 1: Non-empty cells only; 2: All cells
    f -- Open output file handle.
    """
    name_lcase = name.lower()
    nobj_list = book.name_map.get(name_lcase)
    if not nobj_list:
        print('%r: unknown name' % name, file=f)
        return
    for nobj in nobj_list:
        show_name_object(book, nobj, show_contents, f)


def show_name_details_in_scope(book, name, scope_strg, show_contents=0, f=sys.stdout):
    try:
        scope = int(scope_strg)
    except ValueError:
        scope = book.sheet_names().index(scope_strg)
        print('%r => %d' % (scope_strg, scope), file=f)

    name_lcase = name.lower()
    while 1:
        nobj = book.name_and_scope_map.get((name_lcase, scope))
        if nobj:
            break
        print('Name %s not found in scope %d' % (REPR(name), scope), file=f)
        if scope == -1:
            return
        scope = -1

    print('Name %s found in scope %d' % (REPR(name), scope), file=f)
    show_name_object(book, nobj, show_contents, f)


def showable_cell_value(celltype, cellvalue, datemode):
    if celltype == xlrd.XL_CELL_DATE:
        try:
            showval = xlrd.xldate_as_tuple(cellvalue, datemode)
        except xlrd.XLDateError:
            e1, e2 = sys.exc_info()[:2]
            showval = '%s:%s' % (e1.__name__, e2)

    elif celltype == xlrd.XL_CELL_ERROR:
        showval = xlrd.error_text_from_code.get(cellvalue, '<Unknown error code 0x%02x>' % cellvalue)
    else:
        showval = cellvalue
    return showval


def show_name_object(book, nobj, show_contents=0, f=sys.stdout):
    print('\nName: %s, scope: %s (%s)' % (
     REPR(nobj.name), REPR(nobj.scope), scope_as_string(book, nobj.scope)), file=f)
    res = nobj.result
    print('Formula eval result: %s' % REPR(res), file=f)
    if res is None:
        return
    else:
        kind = res.kind
        value = res.value
        if kind >= 0:
            pass
        elif kind == xlrd.oREL:
            for i in range(len(value)):
                ref3d = value[i]
                print('Range %d: %s ==> %s' % (i, REPR(ref3d.coords), REPR(xlrd.rangename3drel(book, ref3d))), file=f)

        elif kind == xlrd.oREF:
            for i in range(len(value)):
                ref3d = value[i]
                print('Range %d: %s ==> %s' % (i, REPR(ref3d.coords), REPR(xlrd.rangename3d(book, ref3d))), file=f)
                if not show_contents:
                    continue
                datemode = book.datemode
                for shx in range(ref3d.shtxlo, ref3d.shtxhi):
                    sh = book.sheet_by_index(shx)
                    print('   Sheet #%d (%s)' % (shx, sh.name), file=f)
                    rowlim = min(ref3d.rowxhi, sh.nrows)
                    collim = min(ref3d.colxhi, sh.ncols)
                    for rowx in range(ref3d.rowxlo, rowlim):
                        for colx in range(ref3d.colxlo, collim):
                            cty = sh.cell_type(rowx, colx)
                            if cty == xlrd.XL_CELL_EMPTY and show_contents == 1:
                                continue
                            cval = sh.cell_value(rowx, colx)
                            sval = showable_cell_value(cty, cval, datemode)
                            print('      (%3d,%3d) %-5s: %s' % (
                             rowx, colx, xlrd.cellname(rowx, colx), REPR(sval)), file=f)

        return


if __name__ == '__main__':

    def usage():
        text = '\nusage: xlrdnameAIPdemo.py glob_pattern name scope show_contents\n\nwhere:\n    "glob_pattern" designates a set of files\n    "name" is a name or \'*\' (all names)\n    "scope" is -1 (global) or a sheet number\n        or a sheet name or * (all scopes)\n    "show_contents" is one of 0 (no show),\n       1 (only non-empty cells), or 2 (all cells)\n\nExamples (script name and glob_pattern arg omitted for brevity)\n    [Searching through book.name_obj_list]\n    * * 0 lists all names\n    * * 1 lists all names, showing referenced non-empty cells\n    * 1 0 lists all names local to the 2nd sheet\n    * Northern 0 lists all names local to the \'Northern\' sheet\n    * -1 0 lists all names with global scope\n    [Initial direct access through book.name_map]\n    Sales * 0 lists all occurrences of "Sales" in any scope\n    [Direct access through book.name_and_scope_map]\n    Revenue -1 0 checks if "Revenue" exists in global scope\n\n'
        sys.stdout.write(text)


    if len(sys.argv) != 5:
        usage()
        sys.exit(0)
    arg_pattern = sys.argv[1]
    arg_name = sys.argv[2]
    arg_scope = sys.argv[3]
    arg_show_contents = int(sys.argv[4])
    for fname in glob.glob(arg_pattern):
        book = xlrd.open_workbook(fname)
        if arg_name == '*':
            do_scope_query(book, arg_scope, arg_show_contents)
        elif arg_scope == '*':
            show_name_details(book, arg_name, arg_show_contents)
        else:
            show_name_details_in_scope(book, arg_name, arg_scope, arg_show_contents)