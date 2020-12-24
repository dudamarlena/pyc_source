# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/__main__.py
# Compiled at: 2020-04-09 19:08:42
# Size of source mod 2**32: 3040 bytes
import argparse, pathlib, sys
from unimport import __version__
from unimport.session import Session
parser = argparse.ArgumentParser(description='Detect or remove unused Python imports.')
exclusive_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('sources',
  default='.',
  nargs='*',
  help='files and folders to find the unused imports.',
  type=(pathlib.Path))
parser.add_argument('-c',
  '--config',
  default='.',
  help='read configuration from PATH.',
  metavar='PATH',
  type=(pathlib.Path))
parser.add_argument('-d',
  '--diff',
  action='store_true',
  help='Prints a diff of all the changes unimport would make to a file.')
exclusive_group.add_argument('-r',
  '--remove',
  action='store_true',
  help='remove unused imports automatically.')
exclusive_group.add_argument('-p',
  '--permission',
  action='store_true',
  help='Refactor permission after see diff.')
parser.add_argument('--check',
  action='store_true',
  help='Prints which file the unused imports are in.')
parser.add_argument('-v',
  '--version',
  action='version',
  version=f"Unimport {__version__}",
  help='Prints version of unimport')

def print_if_exists(sequence):
    if sequence:
        print(*sequence, **{'sep': '\n'})
        return True


def main(argv=None):
    namespace = parser.parse_args(argv)
    any_namespace = any([value for key, value in vars(namespace).items()][2:])
    if namespace.permission:
        if not namespace.diff:
            namespace.diff = True
    session = Session(config_file=(namespace.config))
    for source_path in namespace.sources:
        for py_path in session._list_paths(source_path, '**/*.py'):
            if any_namespace:
                if namespace.check:
                    session.scanner.run_visit(source=(session._read(py_path)[0]))
                    for imp in session.scanner.get_unused_imports():
                        if imp['star']:
                            modules = f"Used object; {imp['modules']}, "
                        else:
                            modules = ''
                        print(f"\x1b[93m{imp['name']}\x1b[00m at \x1b[92m{str(py_path)}:{imp['lineno']}\x1b[00m {modules}")

                    session.scanner.clear()
                if namespace.diff:
                    exists_diff = print_if_exists(tuple(session.diff_file(py_path)))
                    if namespace.permission and exists_diff:
                        action = input(f"Apply suggested changes to \x1b[92m'{py_path}'\x1b[00m [y/n/q] ? >")
                        if action == 'q':
                            break
                        else:
                            if action == 'y':
                                namespace.remove = True
                if namespace.remove:
                    session.refactor_file(py_path, apply=True)


if __name__ == '__main__':
    main(sys.argv[1:])