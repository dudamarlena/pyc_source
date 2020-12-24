# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: //bigfoot/grimmhelga/Production/scripts/libraries/nuke\pysideuic\__init__.py
# Compiled at: 2014-04-26 08:59:26
__all__ = ('compileUi', 'compileUiDir', 'widgetPluginPath')
__version__ = '0.2.15'
from pysideuic.Compiler import indenter, compiler
_header = "# -*- coding: utf-8 -*-\n\n# Form implementation generated from reading ui file '%s'\n#\n# Created: %s\n#      by: pyside-uic %s running on PySide %s\n#\n# WARNING! All changes made in this file will be lost!\n\n"
_display_code = '\nif __name__ == "__main__":\n\timport sys\n\tapp = QtGui.QApplication(sys.argv)\n\t%(widgetname)s = QtGui.%(baseclass)s()\n\tui = %(uiclass)s()\n\tui.setupUi(%(widgetname)s)\n\t%(widgetname)s.show()\n\tsys.exit(app.exec_())\n'

def compileUiDir(dir, recurse=False, map=None, **compileUi_args):
    """compileUiDir(dir, recurse=False, map=None, **compileUi_args)

    Creates Python modules from Qt Designer .ui files in a directory or
    directory tree.

    dir is the name of the directory to scan for files whose name ends with
    '.ui'.  By default the generated Python module is created in the same
    directory ending with '.py'.
    recurse is set if any sub-directories should be scanned.  The default is
    False.
    map is an optional callable that is passed the name of the directory
    containing the '.ui' file and the name of the Python module that will be
    created.  The callable should return a tuple of the name of the directory
    in which the Python module will be created and the (possibly modified)
    name of the module.  The default is None.
    compileUi_args are any additional keyword arguments that are passed to
    the compileUi() function that is called to create each Python module.
    """
    import os

    def compile_ui(ui_dir, ui_file):
        if ui_file.endswith('.ui'):
            py_dir = ui_dir
            py_file = ui_file[:-3] + '.py'
            if map is not None:
                py_dir, py_file = map(py_dir, py_file)
            try:
                os.makedirs(py_dir)
            except:
                pass

            ui_path = os.path.join(ui_dir, ui_file)
            py_path = os.path.join(py_dir, py_file)
            ui_file = open(ui_path, 'r')
            py_file = open(py_path, 'w')
            try:
                compileUi(ui_file, py_file, **compileUi_args)
            finally:
                ui_file.close()
                py_file.close()

        return

    if recurse:
        for root, _, files in os.walk(dir):
            for ui in files:
                compile_ui(root, ui)

    else:
        for ui in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, ui)):
                compile_ui(dir, ui)


def compileUi(uifile, pyfile, execute=False, indent=4, from_imports=False):
    """compileUi(uifile, pyfile, execute=False, indent=4, from_imports=False)

    Creates a Python module from a Qt Designer .ui file.

    uifile is a file name or file-like object containing the .ui file.
    pyfile is the file-like object to which the Python code will be written to.
    execute is optionally set to generate extra Python code that allows the
    code to be run as a standalone application.  The default is False.
    indent is the optional indentation width using spaces.  If it is 0 then a
    tab is used.  The default is 4.
    from_imports is optionally set to generate import statements that are
    relative to '.'.
    """
    from time import ctime
    import PySide
    try:
        uifname = uifile.name
    except AttributeError:
        uifname = uifile

    indenter.indentwidth = indent
    pyfile.write(_header % (uifname, ctime(), __version__, PySide.__version__))
    winfo = compiler.UICompiler().compileUi(uifile, pyfile, from_imports)
    if execute:
        indenter.write_code(_display_code % winfo)


from pysideuic.objcreator import widgetPluginPath