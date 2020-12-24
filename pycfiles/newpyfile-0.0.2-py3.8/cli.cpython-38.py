# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\newpyfile\cli.py
# Compiled at: 2020-01-03 12:50:25
# Size of source mod 2**32: 2742 bytes
"""
newpyfile

Usage:
    newpyfile [names] [--file=path] [--path=path] [--import=imports]
"""
import sys, os
from docopt import docopt
from . import VERSION

def main():
    args = sys.argv
    py_files = get_filenames(args)
    import_pkgs = get_imports(args)
    options = docopt(__doc__, version=VERSION)
    filepath = options.get('--path') or os.getcwd()
    create_files(py_files, filepath, imports=import_pkgs)


def get_filenames(args):
    file_index = [i for i, word in enumerate(args) if word.startswith('--file')]
    py_files = []
    if file_index:
        lines = []
        with open(args[file_index[0]].split('=')[1], 'r') as (file):
            lines = file.readlines()
        for line in lines:
            py_files.extend(line.strip().split(' '))

    else:
        path_index = [i for i, word in enumerate(args) if word.startswith('--path')]
        imports_index = [i for i, word in enumerate(args) if word.startswith('--imports')]
        py_files_index = path_index[0] if path_index else imports_index[0] if imports_index else len(args)
        py_files = args[1:py_files_index]
        args[1:py_files_index] = []
        sys.argv = args
    if not py_files:
        raise ValueError('At least one filename or path to a file with filenames must be given.')
    return py_files


def get_imports(args):
    imports_index = [i for i, word in enumerate(args) if word.startswith('--imports')]
    imports_index = imports_index[0] if imports_index else len(args)
    import_pkgs = args[imports_index:len(args)]
    if not import_pkgs:
        return
    args[imports_index:len(args)] = []
    sys.argv = args
    import_pkgs[0] = import_pkgs[0].split('=')[(-1)]
    if import_pkgs[0].count(','):
        import_pkgs = import_pkgs[0].split(',')
    for i, val in enumerate(import_pkgs):
        if val.count(':'):
            pkg, *subpkg = val.split(':')
            import_pkgs[i] = [pkg, ','.join(subpkg)]
        return import_pkgs


def create_files(filenames, path, imports=None):
    for file in filenames:
        full_path = os.path.join(path, f"{file}.py")
        with open(full_path, 'w') as (f):
            if imports:
                f.write('\n'.join([f"import {pkg}" if type(pkg) == str else f"from {pkg[0]} import {pkg[1]}" for pkg in imports]))