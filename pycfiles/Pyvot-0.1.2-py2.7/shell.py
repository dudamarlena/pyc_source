# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\shell.py
# Compiled at: 2011-11-21 15:27:19
"""Interactive shell for the `xl` package. It can be invoked as:

    python -m xl.shell

The shell mimics the normal Python REPL, but performs additional set-up for convenient usage of `xl`.
    - `xl` is imported
    - An empty Excel workbook is opened, if no others are present
    - Open Excel workbooks are assigned variables (workbook, workbook_1, etc.).
      Each such variable and its workbook's name are printed in a table"""
import code, xl, itertools, sys, textwrap

def workbook_table_str(workbook_map):
    col_format = '{0:<20}{1:>20}\n'
    s = col_format.format('Workbook', 'Name')
    s += col_format.format('========', '====')
    for wb_var, wb in workbook_map.iteritems():
        s += col_format.format(wb_var, wb.name)

    return s


def make_banner(workbook_map):
    banner_format = '\n    Entering Pyvot Shell\n\n    %s\n\n    Imported the `xl` module. Run `help(xl)` for a usage summary.\n\n    Python %s\n    Type "help", "copyright", "credits" or "license" for more information.'
    banner_format = textwrap.dedent(banner_format)
    banner = banner_format % (workbook_table_str(workbook_map), sys.version)
    return banner


def ensure_open_workbook():
    if not xl.workbooks():
        xl.Workbook()
    assert xl.workbooks()


def make_workbook_map():

    def _names():
        yield 'workbook'
        for c in itertools.count(1):
            yield 'workbook_%d' % c

    return dict(zip(_names(), xl.workbooks()))


def shell_input(*args, **kwargs):
    return raw_input(*args, **kwargs)


def run_shell():
    ensure_open_workbook()
    workbook_vars = make_workbook_map()
    banner = make_banner(workbook_vars)
    locals = {'__name__': '__console__', '__doc__': None, 
       'license': license, 
       'copyright': copyright, 
       'xl': xl}
    locals.update(workbook_vars)
    code.interact(banner, shell_input, locals)
    return


if __name__ == '__main__':
    run_shell()